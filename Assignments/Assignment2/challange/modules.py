def print_temp(weather):
    print("Temperature: ",weather["main"]["temp"])

def print_humidity(weather):
    print("Humidity: ",weather["main"]["humidity"])

def print_wind(weather):
    print("Wind speed: ",weather["wind"]["speed"])

def print_time(weather):
    print("Timezone: ",weather["timezone"])