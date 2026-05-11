import streamlit as st
import snowflake.connector
import pandas as pd
from src.config import connection_parameters

st.set_page_config(page_title="Data Quality Dashboard")

st.title("Data Quality Monitoring Dashboard")

conn = snowflake.connector.connect(
    **connection_parameters
)

query = """
SELECT *
FROM DQ_FRAMEWORK.ANALYTICS.VALIDATION_SUMMARY
"""

df = pd.read_sql(query, conn)

st.subheader("Validation Summary")
st.dataframe(df)

if not df.empty:
    st.subheader("Failed Records")
    st.bar_chart(df.set_index("RULE_NAME")["TOTAL_FAILED_RECORDS"])

    st.subheader("Success Rate")
    st.bar_chart(df.set_index("RULE_NAME")["SUCCESS_RATE"])