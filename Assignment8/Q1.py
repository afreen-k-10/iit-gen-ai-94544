from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import json
import requests
from langchain.agents.middleware import wrap_model_call
st.title("Tool based Agent with Middleware")
@tool
def calculator(expression: str):
    """
    Solves arithmetic expressions using +, -, *, / and parentheses.
    Input: arithmetic expression as string
    Output: result as string
    """
    try:
        return str(eval(expression))
    except:
        return "Error : Cannot be solved"
@tool
def get_weather(city: str):
    """
    Fetches current weather for the given city using OpenWeather API.
    Input: city name
    Output: weather data in JSON format
    """
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&units=metric&q={city}"
        response = requests.get(url)
        return json.dumps(response.json())
    except:
        return "Error"
@tool
def read_file(filepath: str):
    """
    Reads a text file from the given path.
    Input: file path
    Output: file content as string
    """
    try:
        with open(filepath, 'r') as file:
            return file.read()
    except:
        return "Error"
@tool
def knowledge_lookup(topic: str):
    """
    Looks up predefined knowledge based on topic.
    Input: topic keyword
    Output: explanation if available
    """
    data = {
        "python": "Python is a high level programming language",
        "http": "HTTP is used for web communication"
    }
    return data.get(topic.lower(), "No data found")
llm = init_chat_model(
    model="google/gemma-3-4b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="non-needed"
)
@wrap_model_call
def limit_model_context(request, handler):
    """
    Middleware to limit context size and log messages.
    """
    request.messages = request.messages[-10:]
    print("Middleware Log:", request.messages)
    response = handler(request)
    return response
agent = create_agent(
    model=llm,
    tools=[
        calculator,
        get_weather,
        read_file,
        knowledge_lookup
    ],
    system_prompt="You are a helpful assistant."
)
if "messages" not in st.session_state:
    st.session_state.messages = []
user_input = st.text_input("You : ")
if st.button("Send") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    result = agent.invoke({"messages": st.session_state.messages})
    st.session_state.messages = result["messages"]
    ai_msg = result["messages"][-1]
    st.markdown("AI response :")
    st.write(ai_msg.content)
st.markdown("Chat History")
for msg in st.session_state.messages:
    st.write(f"{msg.type.upper()} : {msg.content}")