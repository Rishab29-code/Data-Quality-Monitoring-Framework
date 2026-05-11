from snowflake.snowpark import Session
import pandas as pd
from config import connection_parameters

session = Session.builder.configs(connection_parameters).create()

files = {
    "RAW_PRODUCTS": "../datasets/products.csv",
    "RAW_USERS": "../datasets/users.csv",
    "RAW_CARTS": "../datasets/carts.csv"
}

for table_name, file_path in files.items():
    df = pd.read_csv(file_path)

    session.write_pandas(
        df,
        table_name,
        auto_create_table=True,
        overwrite=False
    )

    print(f"Loaded {table_name}")

session.close()

