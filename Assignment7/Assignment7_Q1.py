import streamlit as st
import pandas as pd
from pandasql import sqldf
from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model
load_dotenv()
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("groq_api")
)
st.set_page_config(page_title="CSV SQL Explorer", layout="wide")
st.title("CSV SQL Explorer with LLM")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("CSV Preview")
    st.dataframe(df.head())
    st.subheader("CSV Schema")
    schema_df = pd.DataFrame({"Column": df.columns, "Data Type": df.dtypes.astype(str)})
    st.table(schema_df)
    st.subheader("Ask a Question about the CSV")
    user_question = st.text_input("Example: What is the average price per category?")
    if st.button("Generate & Run SQL"):
        if user_question.strip() == "":
            st.warning("Please enter a question.")
        else:
            sql_prompt = f"""
Table name: df
Table schema:
{df.dtypes}
Question:
{user_question}
Instruction:
Generate ONLY a valid SQL query.
Use table name df.
Do not explain anything.
Output only SQL.
If not possible output Error.
"""
            raw_sql = llm.invoke(sql_prompt).content.strip()
            sql_query = raw_sql.replace("```sql", "").replace("```", "").strip()
            if sql_query.lower().startswith("sql"):
                sql_query = sql_query[3:].strip()
            st.subheader("Generated SQL Query")
            st.code(sql_query, language="sql")
            if sql_query.lower() != "error":
                try:
                    result = sqldf(sql_query, {"df": df})
                    st.subheader("Query Result")
                    st.dataframe(result)
                    explain_prompt = f"""
Explain the following result in simple English.
Question:
{user_question}
Result:
{result.head().to_string()}
"""
                    explanation = llm.invoke(explain_prompt).content.strip()
                    st.subheader("Explanation")
                    st.write(explanation)
                except Exception as e:
                    st.error(f"SQL Execution Error: {e}")
            else:
                st.error("LLM could not generate SQL for this question")