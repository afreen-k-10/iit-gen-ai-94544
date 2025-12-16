import streamlit as st
import pandas as pd
from pandasql import sqldf

st.title("CSV Explorer")

data_file = st.file_uploader("Upload a CSV file", type=["csv"])

if data_file is not None:
    df = pd.read_csv(data_file)
    st.dataframe(df)

    query = st.text_area(
        "Enter SQL query (table name: df)",
        "SELECT category, AVG(price) AS avg_price FROM df GROUP BY category"
    )

    if st.button("RUN"):
        try:
            result = sqldf(query, {"df": df})
            st.dataframe(result)
        except Exception as e:
            st.error(e)
