import streamlit as st
import pandas as pd
import os
from datetime import datetime

user_csv = "users.csv"
file_csv = "userfiles.csv"
uploads = "uploads"

os.makedirs(uploads, exist_ok=True)

# ---------- CSV INITIALIZATION ----------
def init_csv(file, columns):
    if not os.path.exists(file):
        pd.DataFrame(columns=columns).to_csv(file, index=False)

init_csv(user_csv, ["userid", "username", "password"])
init_csv(file_csv, ["userid", "filename", "uploaded_at"])

# ---------- HELPERS ----------
def load_users():
    return pd.read_csv(user_csv)

def save_users(df):
    df.to_csv(user_csv, index=False)

def save_upload_history(userid, filename):
    df = pd.read_csv(file_csv)
    df.loc[len(df)] = {
        "userid": userid,
        "filename": filename,
        "uploaded_at": datetime.now()
    }
    df.to_csv(file_csv, index=False)

# ---------- SESSION ----------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ---------- SIDEBAR ----------
st.sidebar.title("Menu")
if not st.session_state.authenticated:
    menu = st.sidebar.radio("Navigation", ["Home", "Login", "Register"])
else:
    menu = st.sidebar.radio("Navigation", ["Explore CSV", "See History", "Logout"])

# ---------- PAGES ----------
if menu == "Home":
    st.title("Welcome")
    st.write("Please login or register to continue.")

elif menu == "Register":
    st.title("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        users = load_users()

        if username in users["username"].values:
            st.error("Username already exists")
        else:
            userid = len(users) + 1
            users.loc[len(users)] = {
                "userid": userid,
                "username": username,
                "password": password
            }
            save_users(users)
            st.success("Registration successful")

elif menu == "Login":
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_users()
        user = users[
            (users.username == username) &
            (users.password == password)
        ]

        if not user.empty:
            st.session_state.authenticated = True
            st.session_state.userid = int(user.userid.values[0])
            st.session_state.username = username
            st.success("Logged in successfully")
        else:
            st.error("Invalid credentials")

elif menu == "Explore CSV":
    st.title("Upload & Explore CSV")

    uploaded_file = st.file_uploader("Upload CSV file", type="csv")
    if uploaded_file:
        file_path = os.path.join(uploads, uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        save_upload_history(st.session_state.userid, uploaded_file.name)

        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully")
        st.dataframe(df)

elif menu == "See History":
    st.title("Upload History")

    df = pd.read_csv(file_csv)
    df = df[df.userid == st.session_state.userid]

    if df.empty:
        st.info("No uploads yet")
    else:
        st.dataframe(df)

elif menu == "Logout":
    st.session_state.clear()
    st.success("Logged out")
