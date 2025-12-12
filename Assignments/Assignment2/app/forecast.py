import requests
api_key="f359737927c33c21ebfa1e736fb327c3"
city=input("Enter city name: ")
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
response = requests.get(url)
print("status:", response.status_code)
weather = response.json()
print("Temperature: ", weather["main"]["temp"])
print("Humidity: ", weather["main"]["humidity"])
print("Wind Speed: ", weather["wind"]["speed"])