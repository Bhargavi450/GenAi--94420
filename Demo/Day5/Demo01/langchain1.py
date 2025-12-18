from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key=os.getenv("GEMINI_API_KEY")
if not api_key:
    print("API key not found")
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=api_key)

user_input=input("YOU:")
result=llm.invoke(user_input)
print("AI:",result.content)