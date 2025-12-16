import streamlit as st
import requests
import os
from dotenv import load_dotenv
load_dotenv()
api_key = "Api_key"

if "login" not in st.session_state:
    st.session_state.login = False
if not st.session_state.login:
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login") and user == password:
        st.session_state.login = True
else:
    city = st.text_input("City")
    if st.button("Get Weather"):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        data = requests.get(url)
        out = data.json()
        st.write(out)
        # st.write("Temp : ", data["weather"]["temp"])
    if st.button("Logout"):
        st.session_state.login = False
        st.write("Thanks")