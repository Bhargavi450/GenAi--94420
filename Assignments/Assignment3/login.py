import streamlit as st
from dotenv import load_dotenv
import os
import requests
 
load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")

if not api_key:
    st.error("API key not found. Add OPENWEATHER_API_KEY")
    st.stop()
 
if "page" not in st.session_state:
    st.session_state.page = "Login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
 
def weather_page():
    st.title("Weather App")

    city = st.text_input("Enter city name")

    if city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        weather = response.json()

        if weather.get("main"):
            st.success(f"Weather in {city}")
            st.write(f"Temperature: {weather['main']['temp']} °C")
            st.write(f"Humidity: {weather['main']['humidity']} %")
        else:
            st.error("City not found")

    st.button("Logout", on_click=logout)

 
def login_page():
    st.title("Login Page")

    with st.form("login_form"):
        name = st.text_input("Name")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        if name and password:
            st.session_state.logged_in = True
            st.session_state.page = "Weather"
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Please enter name and password")
     
def logout():
    st.session_state.logged_in = False
    st.session_state.page = "Login"
    st.rerun()


with st.sidebar:
    if st.session_state.logged_in:
        if st.button("Weather", use_container_width=True):
            st.session_state.page = "Weather"
        if st.button("Logout", use_container_width=True):
            logout()
    else:
        if st.button("Login", use_container_width=True):
            st.session_state.page = "Login"
 
if st.session_state.page == "Login":
    login_page()
elif st.session_state.page == "Weather":
    weather_page()
