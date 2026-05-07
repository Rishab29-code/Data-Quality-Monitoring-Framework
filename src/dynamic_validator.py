from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
from config import connection_parameters
import json
import uuid
from datetime import datetime

session = Session.builder.configs(connection_parameters).create()

run_id = str(uuid.uuid4())
execution_time = datetime.now()

table = session.table("RAW_PRODUCTS")

with open("../config/validation_rules.json") as f:
    rules = json.load(f)["rules"]

for rule in rules:

    rule_name = rule["name"]
    column_name = rule["column"]
    rule_type = rule["type"]

    if rule_type == "null":
        failures = table.filter(col(f'"{column_name}"').is_null())

    elif rule_type == "negative":
        failures = table.filter(col(f'"{column_name}"') < 0)

    else:
        continue

    fail_count = failures.count()

    session.sql(f"""
    INSERT INTO DQ_FRAMEWORK.VALIDATION.VALIDATION_RESULTS
    VALUES (
    '{run_id}',
    '{rule_name}',
    {fail_count},
    '{"FAIL" if fail_count > 0 else "PASS"}',
    CURRENT_TIMESTAMP()
    )
    """).collect()

    if fail_count > 0:
        failed_rows = [
            (
                run_id,
                rule_name,
                str(row.as_dict()),
                execution_time
            )
            for row in failures.collect()
        ]

        session.create_dataframe(
            failed_rows,
            schema=["RUN_ID", "RULE_NAME", "RECORD_DATA", "EXECUTION_TIME"]
        ).write.mode("append").save_as_table(
            "DQ_FRAMEWORK.VALIDATION.FAILED_RECORDS"
        )

print("Dynamic validation completed")

session.close()