import streamlit as st
import pandas as pd
import pandasql as ps
from datetime import datetime
import os
 
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = ""
 
USERS_FILE = "users.csv"
HISTORY_FILE = "userfiles.csv"
 
if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["username", "password", "email"]).to_csv(USERS_FILE, index=False)

if not os.path.exists(HISTORY_FILE):
    pd.DataFrame(columns=["username", "filename", "datetime"]).to_csv(HISTORY_FILE, index=False)
 
with st.sidebar:
    st.title("Menu")

    if not st.session_state.logged_in:
        page = st.radio("Navigate", ["Home", "Login", "Register"])
    else:
        page = st.radio("Navigate", ["Explore CSV", "See History", "Logout"])
 
def home_page():
    st.title("Home")
    st.write("Welcome to the CSV Explorer Application")
 
def login_page():
    st.title("Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        users = pd.read_csv(USERS_FILE)
        match = users[
            (users["username"] == username) &
            (users["password"] == password)
        ]

        if not match.empty:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success("Login successful")
        else:
            st.error("Invalid credentials")
 
def registration_page():
    st.title("Register")

    with st.form("register_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        email = st.text_input("Email")
        submit = st.form_submit_button("Register")

    if submit:
        users = pd.read_csv(USERS_FILE)

        if username in users["username"].values:
            st.error("Username already exists")
        else:
            new_user = pd.DataFrame(
                [[username, password, email]],
                columns=["username", "password", "email"]
            )
            users = pd.concat([users, new_user])
            users.to_csv(USERS_FILE, index=False)
            st.success("Registration successful")
 
def csv_uploader():
    st.title("CSV UPLOADER")

    data_file = st.file_uploader("Choose a file", type=["csv"])

    if data_file is not None:
        df = pd.read_csv(data_file)
        st.dataframe(df)
 
        if "price" in df.columns:
            query = "SELECT * FROM df WHERE price > 100"
            result = ps.sqldf(query, {"df": df})

            st.write("Query Result")
            st.dataframe(result)
        else:
            st.warning("Column 'price' not found in CSV")
 
        history = pd.read_csv(HISTORY_FILE)
        new_entry = pd.DataFrame(
            [[st.session_state.user, data_file.name, datetime.now()]],
            columns=["username", "filename", "datetime"]
        )
        history = pd.concat([history, new_entry])
        history.to_csv(HISTORY_FILE, index=False)
 
def history_page():
    st.title("Upload History")

    history = pd.read_csv(HISTORY_FILE)
    user_history = history[history["username"] == st.session_state.user]
    st.dataframe(user_history)
 
def logout():
    st.session_state.logged_in = False
    st.session_state.user = ""
    st.success("Logged out successfully")
 
if not st.session_state.logged_in:
    if page == "Home":
        home_page()
    elif page == "Login":
        login_page()
    elif page == "Register":
        registration_page()
else:
    if page == "Explore CSV":
        csv_uploader()
    elif page == "See History":
        history_page()
    elif page == "Logout":
        logout()
