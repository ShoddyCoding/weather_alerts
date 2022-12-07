import requests
import json
import eventlogger as er
import datetime

class forecastObj:
    def __init__(self, date_time, temp, feels_like, temp_min, temp_max, pressure, humidity, weather_keyword,
                weather_descrip, wind_speed, wind_direction, wind_gust, clouds, visibility, rain):
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
                self.r = rain

class detectionOjb:
    def __init__(self, date_time, temp, weather_keyword, weather_descrip):
        self.dt = date_time
        self.t = temp
        self.wk = weather_keyword
        self.wd = weather_descrip

def get_current_weather(api, lat, long):
    """takes an api token, latitude, and longitude; returns the current weather from openweather API"""
    API_URL = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&units=imperial&appid={key}'
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
    try:
        API_URL = 'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={long}&units=imperial&appid={key}'
        weather_forecast = requests.get(API_URL.format(
                                        key=api,
                                        lat=lat,
                                        long=long))
        weather_data = json.loads(weather_forecast.content.decode('utf-8'))['list']
    except Exception as e:
        er.add_events("ERROR: Issue processing the API call for weather forecast: {}".format(e.string))
    try:
        for dp in weather_data:
            
                if "rain" in dp:
                    pit = forecastObj(dp["dt"], dp["main"]["temp"], dp["main"]["feels_like"], dp["main"]["temp_min"],
                                    dp["main"]["temp_max"],  dp["main"]["pressure"], dp["main"]["humidity"],
                                    dp["weather"][0]["main"], dp["weather"][0]["description"],dp["wind"]["speed"],
                                    dp["wind"]["deg"], dp["wind"]["gust"], dp["clouds"]["all"], dp["visibility"], dp["rain"]["3h"])
                else:
                    pit = forecastObj(dp["dt"], dp["main"]["temp"], dp["main"]["feels_like"], dp["main"]["temp_min"],
                                    dp["main"]["temp_max"],  dp["main"]["pressure"], dp["main"]["humidity"],
                                    dp["weather"][0]["main"], dp["weather"][0]["description"],dp["wind"]["speed"],
                                    dp["wind"]["deg"], dp["wind"]["gust"], dp["clouds"]["all"], dp["visibility"], 0)
                next_150_hours.append(pit)
    except Exception as e:
        er.add_events("ERROR: Issue converting datapoint into forecast object: {}".format(e.string))
    return next_150_hours

def have_Freezing_Conditions(forecast, temperature):
    """Takes a list of 150 hours of forecast objects and evaluates for freezing conditions
     in the next 6 hours and returns a detection object if condition is found"""
    listOfDetections = []
    try:
        for i in forecast:
            if i.t < temperature:
                detection = detectionOjb(i.dt, i.t, i.wk, i.wd)
                listOfDetections.append(detection)
        earlist_freezing_temp = find_lowest_value_in_forecast_condition(listOfDetections)
        return earlist_freezing_temp.dt
    except Exception as e:
        er.add_events("ERROR: Issue with adding a parsing or adding a detection: {}".format(e.string))
        return False

def find_lowest_value_in_forecast_condition(list):
    """finds the lowest valued object based on the time and within 24 hours"""
    lowest_value_object = detectionOjb(26473669201,5000,'Clear','Probably Hot')
    now_dt = datetime.datetime.now()
    try:
        for i in list:
            if i.dt < lowest_value_object.dt:
                lowest_value_object = i
        lowest_value_dt = datetime.datetime.fromtimestamp(lowest_value_object.dt)
        if (lowest_value_dt - now_dt).days == 0:
            return lowest_value_object
        else:
            return False
    except Exception as e:
        er.add_events("ERROR: Issue with finding the lowest value in a list: {}".format(e.string))
        return False
        
