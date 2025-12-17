import streamlit as st, os, requests, json
from dotenv import load_dotenv
load_dotenv()
st.set_page_config(
    page_title="LLM Chat App",
    layout="wide"
)
model_choice = st.sidebar.radio(
    "Choose LLM:",
    ["Groq", "LM Studio"]
)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
def ask_lm(prompt):
    api_key = "dummy-key"
    url = "http://127.0.0.1:1234/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    req_data = {
        "model": "google/gemma-3-4b",
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(url, json=req_data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]
def ask_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    groq_api_key = os.getenv("GROQ_API_KEY")
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }
    req_data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(url, json=req_data, headers=headers)
    return response.json()['choices'][0]['message']['content']
st.title("ChatBot")
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(chat["question"])
    with st.chat_message("assistant"):
        st.markdown(chat["answer"])
user_question = st.chat_input("Ask your question...")
if user_question:
    with st.chat_message("user"):
        st.markdown(user_question)
    if model_choice == "Groq":
        model_response = ask_groq(user_question)
    else:
        model_response = ask_lm(user_question)
    with st.chat_message("assistant"):
        st.markdown(model_response)
    st.session_state.chat_history.append({
        "model": model_choice,
        "question": user_question,
        "answer": model_response
    })