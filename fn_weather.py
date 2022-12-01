import requests
import json

def get_current_weather(api, lat, long):
    """takes an api token, latitude, and longitude; returns the current weather from openweather API"""
    API_URL = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={key}'
    current_weather = requests.get(API_URL.format(
                                       key=api,
                                       lat=lat,
                                       long=long))
    current_weather_data = json.loads(current_weather.content.decode('utf-8'))

def get_air_pollution(api, lat, long):
    """takes an api token, latitude, and longitude; returns the air pollution from openweather API"""
    API_URL = 'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={long}&appid={key}'
    air_pollution = requests.get(API_URL.format(
                                       key=api,
                                       lat=lat,
                                       long=long))
    current_air_pollution = json.loads(air_pollution.content.decode('utf-8'))

def get_weather_forecast(api, lat, long):
    """takes an api token, latitude, and longitude; returns the air pollution from openweather API"""
    API_URL = 'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={long}&appid={key}'
    weather_forecast = requests.get(API_URL.format(
                                       key=api,
                                       lat=lat,
                                       long=long))
    weather_data = json.loads(weather_forecast.content.decode('utf-8'))
   