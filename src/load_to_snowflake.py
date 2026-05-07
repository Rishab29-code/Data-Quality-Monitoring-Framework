from snowflake.snowpark import Session
from config import connection_parameters
import pandas as pd

# Create session
session = Session.builder.configs(connection_parameters).create()

# Load local API data
df = pd.read_csv("../datasets/raw_products.csv")

# Upload to Snowflake
session.write_pandas(
    df,
    table_name="RAW_PRODUCTS",
    auto_create_table=True,
    overwrite=True
)

print("Data loaded successfully!")

count = session.table("RAW_PRODUCTS").count()
print(f"Loaded {count} rows")

session.close()
