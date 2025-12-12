import requests
api_key="ecd07db5932261fb1bda49504f9602c8"
city = input("Enter city: ")
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
response = requests.get(url)
print("status:", response.status_code)
weather = response.json()
print("Temperature: ", weather["main"]["temp"])
print("Humidity: ", weather["main"]["humidity"])
print("Wind Speed: ", weather["wind"]["speed"])