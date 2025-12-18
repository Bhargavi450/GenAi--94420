# Q2:
# Create a Streamlit application that takes a city name as input from the user.
# Fetch the current weather using a Weather API and use an LLM to explain the weather conditions in simple English.

import streamlit as st
import requests
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
 
load_dotenv()

st.title("Weather Chat")
 
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

weather_api_key = os.getenv("OPENWEATHER_API_KEY")
 
city = st.text_input("Enter city name")

if city:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
 
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"]
        wind = data["wind"]["speed"]
 
        st.subheader("Current Weather")
        st.write(f"Temperature: {temp} °C")
        st.write(f"Humidity: {humidity} %")
        st.write(f"Wind Speed: {wind} m/s")
        st.write(f"Condition: {condition}")
 
        prompt = f"""
Explain the weather in very simple English.

City: {city}
Temperature: {temp} °C
Humidity: {humidity} %
Condition: {condition}
Wind Speed: {wind} m/s
"""

        explanation = llm.invoke(prompt).content

        st.subheader("Weather Explanation")
        st.success(explanation)

    else:
        st.error("Invalid city name. Please try again.")
