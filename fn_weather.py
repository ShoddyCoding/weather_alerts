import requests
import json

class forecastObj:
    def __init__(self, date_time, temp, feels_like, temp_min, temp_max, pressure, humidity, weather_keyword,
                weather_descrip, wind_speed, wind_direction, wind_gust, clouds, visibility):
                self.dt = date_time
                self.t = temp
                self.fl = feels_like
                self.tmin = temp_min
                self.tmax = temp_max
                self.p = pressure
                self.h = humidity
                self.wk = weather_keyword
                self.wd = weather_descrip
                self.w_s = wind_speed
                self.w_d = wind_direction
                self.w_g = wind_gust
                self.c = clouds
                self.v = visibility
    def normalize_datapoints():
        print('we are here')
        #change dt from GMT to EST


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
    """takes an api token, latitude, and longitude; returns the 
    forecaset in 3 h increments for 5 days from openweather API"""
    next_150_hours = []
    API_URL = 'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={long}&appid={key}'
    weather_forecast = requests.get(API_URL.format(
                                       key=api,
                                       lat=lat,
                                       long=long))
    weather_data = json.loads(weather_forecast.content.decode('utf-8'))['list']
    for dp in weather_data:
        pit = forecastObj(dp["dt"], dp["main"]["temp"], dp["main"]["feels_like"], dp["main"]["temp_min"],
                        dp["main"]["temp_max"],  dp["main"]["pressure"], dp["main"]["humidity"],
                        dp["weather"][0]["main"], dp["weather"][0]["description"],dp["wind"]["speed"],
                        dp["wind"]["deg"], dp["wind"]["gust"], dp["clouds"]["all"], dp["visibility"])
        next_150_hours.append(pit)
    return next_150_hours
