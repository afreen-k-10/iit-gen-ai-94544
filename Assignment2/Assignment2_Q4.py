#Exercise 4: Create a weather app that takes city input and displays forecast
import requests
api_key = "eabce7bbaeaffdd0f5f575ff7eea31c2"
city = input("Enter city name:")
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
response = requests.get(url)
if response.status_code == 200:
    print("weather data ")
    data = response.json()
    print("Tempreture:",data["main"]["temp"])
    print("humidity:",data["main"]["humidity"])