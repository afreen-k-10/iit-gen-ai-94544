import streamlit as st
import requests
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
load_dotenv()
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("groq_api")
)
st.title("Weather Explanation App")
city = st.text_input("Enter city name")
if st.button("Get Weather"):
    if city.strip() == "":
        st.warning("Enter a city name")
    else:
        api_key = os.getenv("weather_api")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()
        if response.get("cod") != 200:
            st.error("City not found")
        else:
            temp = response["main"]["temp"]
            humidity = response["main"]["humidity"]
            description = response["weather"][0]["description"]
            st.write("Temperature:", temp, "°C")
            st.write("Humidity:", humidity, "%")
            st.write("Condition:", description)
            prompt = f"""
Explain the following weather conditions in simple English.
City: {city}
Temperature: {temp} °C
Humidity: {humidity}%
Condition: {description}
"""
            explanation = llm.invoke(prompt).content
            st.subheader("Weather Explanation")
            st.write(explanation)