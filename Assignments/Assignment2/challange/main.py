import requests
from dotenv import load_dotenv
import os
import modules
 
load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")

if not api_key:
    raise SystemExit("API key not found. Please add OPENWEATHER_API_KEY to your .env file.")

city = input("Enter city name: ")

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

resp = requests.get(url)
weather = resp.json()

print("API Response:", weather)  

modules.print_temp(weather)
modules.print_humidity(weather)
modules.print_wind(weather)
modules.print_time(weather)    
