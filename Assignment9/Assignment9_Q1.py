import os
import streamlit as st
from langchain.chat_models import init_chat_model
import pandas as pd
from dotenv import load_dotenv
from pandasql import sqldf
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
load_dotenv()
st.set_page_config(page_title="Multi-Agent CSV & Web Explorer", layout="wide")
st.title("Afreen's Chatbot")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
def add_chat(role, message):
    st.session_state.chat_history.append({"role": role, "message": message})
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("groq_api")
)
agent = st.sidebar.radio("Choose Agent", ["CSV Question Answering Agent", "Sunbeam Web Scraping Agent"])
st.set_page_config(page_title="CSV Explorer", layout="wide")
st.title("CSV Explorer")
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("groq_api")
)
csv_file = st.file_uploader("Upload a CSV file", type=["csv"])
if csv_file:
    df = pd.read_csv(csv_file)
    st.subheader("CSV Schema")
    st.write(df.dtypes)
    question = st.text_input("Ask anything about this CSV")
    if question:
        llm_input = f"""
        You are an expert SQL developer.
        Table Name : df
        Table Schema : {df.dtypes}
        Question : {question}
        Instruction :
        - Generate ONLY a valid SQLite SQL query
        - Do NOT use markdown or code blocks
        - Do NOT explain anything
        """
        query = llm.invoke(llm_input).content.strip()
        query = query.replace("```sql", "").replace("```", "").strip()
        st.subheader("SQL Query ")
        st.code(query, language="sql")
        try:
            result = sqldf(query, {"df": df})
            st.subheader("Query Result")
            st.dataframe(result)
            explain_prompt = f"""
            Explain the following result in simple English.
            Question : {question}
            Result : {result.head().to_string(index=False)}
            """
            explanation = llm.invoke(explain_prompt).content.strip()
            st.subheader("Explanation")
            st.write(explanation)
        except Exception as e:
            st.error(f"SQL Error: {e}")
if agent == "Sunbeam Web Scraping Agent":
    st.header("Sunbeam Internship & Batch Agent")
    query = st.text_input("Ask about Sunbeam internships or batches")
    if st.button("Ask Web Agent") and query:
        add_chat("user", query)
        chrome_options = Options()
        chrome_options.add_argument("headless")
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 20)
        try:
            driver.get("https://sunbeaminfo.in/internship")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            plus_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseSix']")))
            plus_button.click()
            table = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='collapseSix']//table")))
            rows = table.find_elements(By.TAG_NAME, "tr")
            data = []
            for row in rows[1:]:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 4:
                    data.append({
                        "Technology": cols[0].text,
                        "Aim": cols[1].text,
                        "Prerequisite": cols[2].text,
                        "Learning Location": cols[3].text
                    })
            df_web = pd.DataFrame(data)
            st.subheader("Sunbeam Internship Details")
            st.dataframe(df_web)
            explanation_prompt = f"""
            User Question: {query}
            Data:
            {df_web.head().to_string(index=False)}
            Explain the answer in simple English.
            """
            explanation = llm.invoke(explanation_prompt).content.strip()
            st.subheader("Explanation")
            st.write(explanation)
            add_chat("assistant", explanation)
        except Exception as e:
            st.error(f"Web Scraping Error: {e}")
            add_chat("assistant", str(e))
        finally:
            driver.quit()
st.divider()
st.subheader("Chat History")
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"User: {chat['message']}")
    else:
        st.markdown(f"Agent: {chat['message']}")