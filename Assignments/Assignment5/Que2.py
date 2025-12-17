#2. ⁠Connect to Groq and Gemini AI using REST api. Send same prompt and compare results. Also compare the speed.
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()    

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not loaded. Check .env location.")

url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

user_prompt = input("Ask anything: ")

req_data = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {"role": "user", "content": user_prompt}
    ]
}

response = requests.post(  
    url,
    headers=headers,
    json=req_data    
)

print("Status:", response.status_code)
answer = response.json()["choices"][0]["message"]["content"]
print(answer)



