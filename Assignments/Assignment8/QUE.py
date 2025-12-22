from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import streamlit as st
import os
import requests

load_dotenv()
st.title("Smart Agent")
 
@tool
def calculator(expression: str) -> str:
    """Solves basic arithmetic expressions."""
    try:
        return str(eval(expression))
    except:
        return "Error: Cannot solve expression"

@tool
def get_weather(city: str) -> str:
    """Returns current temperature and weather condition of a city."""
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        res = requests.get(url)
        data = res.json()

        if data.get("cod") != 200:
            return "City not found"

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"{city.title()}: {temp}°C, {desc}"

    except:
        return "Weather fetch failed"
 
llm = init_chat_model(
    model="google/gemma-3-4b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed"
)

agent = create_agent(
    model=llm,
    tools=[calculator, get_weather],
    system_prompt="Use tools if needed. Reply shortly. No explanations."
)
 
if "messages" not in st.session_state:
    st.session_state.messages = []
 
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
 
user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
 
    response = agent.invoke({
        "messages": [{"role": "user", "content": user_input}]
    })

    ai_msg = response["messages"][-1].content

    st.session_state.messages.append({"role": "assistant", "content": ai_msg})
    with st.chat_message("assistant"):
        st.write(ai_msg)
