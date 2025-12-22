from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import os
import requests
 
load_dotenv()

@tool
def calculator(expression: str) -> str:
    """
    Solves basic arithmetic expressions.
    Supports +, -, *, /, ().
    """
    try:
        return str(eval(expression))
    except:
        return "Error: Cannot solve expression"


@tool
def get_weather(city: str) -> str:
    """
    Returns current temperature and weather condition of a city.
    """
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?appid={api_key}&units=metric&q={city}"
        )

        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return "Error: City not found"

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]

        return f"{city.title()}: {temp}°C, {desc}"

    except:
        return "Error: Unable to fetch weather"

 
llm = init_chat_model(
    model="google/gemma-3-4b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed"
)
 

agent = create_agent(
    model=llm,
    tools=[calculator, get_weather],
    system_prompt=(
        "Use tools when required. "
        "Return ONLY the final answer. "
        "Keep it short. No explanations."
    )
)
 

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    result = agent.invoke({
        "messages": [
            {"role": "user", "content": user_input}
        ]
    })

    print("AI:", result["messages"][-1].content)
