from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
from config import connection_parameters
from datetime import datetime
import uuid
import json

# Create session
session = Session.builder.configs(connection_parameters).create()

run_id = str(uuid.uuid4())
execution_time = datetime.now()

table = session.table("RAW_PRODUCTS")

print(f"Validation Run Started: {run_id}")


# ------------------------
# NULL CHECK
# ------------------------
null_failures = table.filter(
    (col('"price"').is_null()) |
    (col('"title"').is_null())
)

null_count = null_failures.count()

session.sql(f"""
INSERT INTO DQ_FRAMEWORK.VALIDATION.VALIDATION_RESULTS
VALUES (
'{run_id}',
'NULL_CHECK',
{null_count},
'{"FAIL" if null_count > 0 else "PASS"}',
'{execution_time}'
)
""").collect()

if null_count > 0:
    failed_rows = [
        (
            run_id,
            "NULL_CHECK",
            str(row.as_dict()),
            execution_time
        )
        for row in null_failures.collect()
    ]

    session.create_dataframe(
        failed_rows,
        schema=["RUN_ID", "RULE_NAME", "RECORD_DATA", "EXECUTION_TIME"]
    ).write.mode("append").save_as_table(
        "DQ_FRAMEWORK.VALIDATION.FAILED_RECORDS"
    )


# ------------------------
# DUPLICATE CHECK
# ------------------------
duplicate_failures = session.sql("""
SELECT "id"
FROM RAW_PRODUCTS
GROUP BY "id"
HAVING COUNT(*) > 1
""")

dup_count = duplicate_failures.count()

session.sql(f"""
INSERT INTO DQ_FRAMEWORK.VALIDATION.VALIDATION_RESULTS
VALUES (
'{run_id}',
'DUPLICATE_CHECK',
{dup_count},
'{"FAIL" if dup_count > 0 else "PASS"}',
'{execution_time}'
)
""").collect()


# ------------------------
# NEGATIVE PRICE CHECK
# ------------------------
negative_failures = table.filter(col('"price"') < 0)

neg_count = negative_failures.count()

session.sql(f"""
INSERT INTO DQ_FRAMEWORK.VALIDATION.VALIDATION_RESULTS
VALUES (
'{run_id}',
'NEGATIVE_PRICE_CHECK',
{neg_count},
'{"FAIL" if neg_count > 0 else "PASS"}',
'{execution_time}'
)
""").collect()

if neg_count > 0:
    failed_rows = [
        (
            run_id,
            "NEGATIVE_PRICE_CHECK",
            str(row.as_dict()),
            execution_time
        )
        for row in negative_failures.collect()
    ]

    session.create_dataframe(
        failed_rows,
        schema=["RUN_ID", "RULE_NAME", "RECORD_DATA", "EXECUTION_TIME"]
    ).write.mode("append").save_as_table(
        "DQ_FRAMEWORK.VALIDATION.FAILED_RECORDS"
    )


print("Validation completed")
print(f"Null failures: {null_count}")
print(f"Duplicate failures: {dup_count}")
print(f"Negative price failures: {neg_count}")

cart_user_check = session.sql("""
SELECT COUNT(*) AS FAILED_COUNT
FROM RAW_CARTS c
LEFT JOIN RAW_USERS u
ON c."userId" = u."id"
WHERE u."id" IS NULL
""").collect()[0]["FAILED_COUNT"]

status = "PASS" if cart_user_check == 0 else "FAIL"

session.sql(f"""
INSERT INTO DQ_FRAMEWORK.VALIDATION.VALIDATION_RESULTS
VALUES (
    '{run_id}',
    'CART_USER_INTEGRITY',
    {cart_user_check},
    '{status}',
    '{execution_time}'
)
""").collect()

print("CART_USER_INTEGRITY complete")

cart_product_check = session.sql("""
SELECT COUNT(*) AS FAILED_COUNT
FROM RAW_CARTS c
JOIN LATERAL FLATTEN(input => PARSE_JSON(c."products"::STRING)) p
LEFT JOIN RAW_PRODUCTS rp
ON p.value:"id"::INT = rp."id"
WHERE rp."id" IS NULL
""").collect()[0]["FAILED_COUNT"]

status = "PASS" if cart_product_check == 0 else "FAIL"

session.sql(f"""
INSERT INTO DQ_FRAMEWORK.VALIDATION.VALIDATION_RESULTS
VALUES (
    '{run_id}',
    'CART_PRODUCT_INTEGRITY',
    {cart_product_check},
    '{status}',
    '{execution_time}'
)
""").collect()

print("CART_PRODUCT_INTEGRITY complete")    

session.close()