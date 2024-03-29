import requests
import json
import eventlogger as er
import datetime
import dbconnections as db
import utilities as u
import os

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
    return current_weather_data

def get_air_pollution(api, lat, long):
    """takes an api token, latitude, and longitude; returns the air pollution from openweather API"""
    API_URL = 'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={long}&appid={key}'
    air_pollution = requests.get(API_URL.format(
                                       key=api,
                                       lat=lat,
                                       long=long))
    current_air_pollution = json.loads(air_pollution.content.decode('utf-8'))
    return current_air_pollution

def store_air_pollution(air_pollution_object):
    """take an air pollution object and stores the data in MySQL database"""
    try:
        print(air_pollution_object["list"][0]["components"]["co"])
        query = "INSERT INTO `weather`.`air_pollution` (`dt`, `main_air_quality_index`, \
                `carbon_monoxide`, `nitrogen_monoxide`, `nitrogen_dioxide`, `ozone`, `sulphur_dioxide`, \
                `fine_particulate`, `coarse_particulate`, `ammonia`) \
                VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}') \
                ON DUPLICATE KEY UPDATE `main_air_quality_index` = {1};".format(
                air_pollution_object["list"][0]["dt"], air_pollution_object["list"][0]["main"]["aqi"],
                air_pollution_object["list"][0]["components"]["co"],air_pollution_object["list"][0]["components"]["no"],
                air_pollution_object["list"][0]["components"]["no2"],air_pollution_object["list"][0]["components"]["o3"],
                air_pollution_object["list"][0]["components"]["so2"],air_pollution_object["list"][0]["components"]["pm2_5"],
                air_pollution_object["list"][0]["components"]["pm10"],air_pollution_object["list"][0]["components"]["nh3"]
                )
        db.conn_local_prod_cursor.execute(query)
    except Exception as e:
        er.add_events("ERROR: Issue converting datapoint into forecast object: {}".format(e.string))
    
def store_current_weather(dp):
    """takes an currenty weather object and store the data in MySQL"""
    try:
        if "rain" in dp:
            pit = forecastObj(dp["dt"], dp["main"]["temp"], dp["main"]["feels_like"], dp["main"]["temp_min"],
                            dp["main"]["temp_max"],  dp["main"]["pressure"], dp["main"]["humidity"],
                            dp["weather"][0]["main"], dp["weather"][0]["description"],dp["wind"]["speed"],
                            dp["wind"]["deg"], 0, dp["clouds"]["all"], dp["visibility"], dp["rain"]["1h"])
            query = "INSERT INTO `weather`.`weather_history` (`dt`, `temp`, `feel_like`, `temp_min`, \
                `temp_max`, `pressure`, `humidity`, `weather_keyword`, `weather_description`, `wind_speed`, \
                `wind_direction`, `clouds`, `visibility`, `rain`) \
                VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}',\
                '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}');".format(pit.dt, pit.t, pit.fl, pit.tmin, pit.tmax,
                pit.p, pit.h, pit.wk, pit.wd, pit.w_s, pit.w_d, pit.c, pit.v, pit.r)          
            db.conn_local_prod_cursor.execute(query)
        else:
            pit = forecastObj(dp["dt"], dp["main"]["temp"], dp["main"]["feels_like"], dp["main"]["temp_min"],
                            dp["main"]["temp_max"],  dp["main"]["pressure"], dp["main"]["humidity"],
                            dp["weather"][0]["main"], dp["weather"][0]["description"],dp["wind"]["speed"],
                            dp["wind"]["deg"], 0, dp["clouds"]["all"], dp["visibility"], 0)
            query = "INSERT INTO `weather`.`weather_history` (`dt`, `temp`, `feel_like`, `temp_min`, \
                `temp_max`, `pressure`, `humidity`, `weather_keyword`, `weather_description`, `wind_speed`, \
                `wind_direction`, `clouds`, `visibility`) \
                VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}',\
                '{7}', '{8}', '{9}', '{10}', '{11}', '{12}');".format(pit.dt, pit.t, pit.fl, pit.tmin, pit.tmax,
                pit.p, pit.h, pit.wk, pit.wd, pit.w_s, pit.w_d, pit.c, pit.v)  
            db.conn_local_prod_cursor.execute(query)
                
                
    except Exception as e:
        er.add_events("ERROR: Issue converting datapoint into forecast object: {}".format(e.string))

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
                    query = "INSERT INTO `weather`.`weather_forecast` (`dt`, `temp`, `feel_like`, `temp_min`, \
                    `temp_max`, `pressure`, `humidity`, `weather_keyword`, `weather_description`, `wind_speed`, \
                    `wind_direction`, `clouds`, `visibility`, `rain`) \
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}',\
                    '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}') \
                    ON DUPLICATE KEY UPDATE `temp` = '{1}', `feel_like` = '{2}', `temp_min` = '{3}', \
                    `temp_max` = '{4}', `pressure` = '{5}', `humidity` = '{6}', `weather_keyword` = '{7}', \
                    `weather_description`= '{8}', `wind_speed` = '{9}', `wind_direction` = '{10}',\
                    `clouds` = '{11}', `visibility`= '{12}', `rain` = '{13}';".format(pit.dt, pit.t, pit.fl, 
                    pit.tmin, pit.tmax, pit.p, pit.h, pit.wk, pit.wd, pit.w_s, pit.w_d, pit.c, pit.v, pit.r)          
                    db.conn_local_prod_cursor.execute(query)
                else:
                    pit = forecastObj(dp["dt"], dp["main"]["temp"], dp["main"]["feels_like"], dp["main"]["temp_min"],
                                    dp["main"]["temp_max"],  dp["main"]["pressure"], dp["main"]["humidity"],
                                    dp["weather"][0]["main"], dp["weather"][0]["description"],dp["wind"]["speed"],
                                    dp["wind"]["deg"], dp["wind"]["gust"], dp["clouds"]["all"], dp["visibility"], 0)
                    query = "INSERT INTO `weather`.`weather_forecast` (`dt`, `temp`, `feel_like`, `temp_min`, \
                    `temp_max`, `pressure`, `humidity`, `weather_keyword`, `weather_description`, `wind_speed`, \
                    `wind_direction`, `clouds`, `visibility`) \
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}',\
                    '{7}', '{8}', '{9}', '{10}', '{11}', '{12}') \
                    ON DUPLICATE KEY UPDATE `temp` = '{1}', `feel_like` = '{2}', `temp_min` = '{3}', \
                    `temp_max` = '{4}', `pressure` = '{5}', `humidity` = '{6}', `weather_keyword` = '{7}', \
                    `weather_description`= '{8}', `wind_speed` = '{9}', `wind_direction` = '{10}',\
                    `clouds` = '{11}', `visibility`= '{12}';".format(pit.dt, pit.t, pit.fl, 
                    pit.tmin, pit.tmax, pit.p, pit.h, pit.wk, pit.wd, pit.w_s, pit.w_d, pit.c, pit.v)          
                    db.conn_local_prod_cursor.execute(query)
                next_150_hours.append(pit)
    except Exception as e:
        er.add_events("ERROR: Issue converting datapoint into forecast object: {}".format(e.string))
    return next_150_hours

def have_Freezing_Conditions():
    """Queries the database for a freezing event in the next 24 hours
     in the next 24 hours and returns a detection object if condition is found"""
    try:
        query = "SELECT dt, temp,  weather_keyword, weather_description FROM weather.freezing_temps_in_next_24_hours_nearest_time;"
        db.conn_local_prod_cursor.execute(query)
        weather_event = db.conn_local_prod_cursor.fetchone()
        if weather_event != None:
            query2 = "SELECT dt FROM weather.next_thaw;"
            db.conn_local_prod_cursor.execute(query2)
            thaw = db.conn_local_prod_cursor.fetchone()
            
            earlist_freezing_temp = detectionOjb(weather_event[0], weather_event[1], weather_event[2], weather_event[3])
            first_thaw_after_freeze = thaw[0]

            formatted_message = format_weather_message(earlist_freezing_temp, first_thaw_after_freeze)
            return formatted_message
        else:
            return False
    except Exception as e:
        er.add_events("ERROR: Issue with adding a parsing or adding a detection: {}".format(e.string))
        return False

def find_lowest_value_in_forecast_condition(list):
    """finds the lowest valued object in list based on the time"""
    lowest_value_object = detectionOjb(26473669201,5000,'Clear','Probably Hot')
    try:
        for i in list:
            if i.dt < lowest_value_object.dt:
                lowest_value_object = i
        return lowest_value_object
    except Exception as e:
        er.add_events("ERROR: Issue with finding the lowest value in a list: {}".format(e.string))
        return False

def find_first_nonfreezing_condition(earliest_freeze, weather_objs):
    """Finds the first nonfreezing condition that occurs after a freeze and returns that weather object"""
    first_thaw = detectionOjb(26473669201,5000,'Clear','Probably Hot')
    try:
        for i in weather_objs:
            if i.dt > earliest_freeze.dt and i.t > 42 and i.dt < first_thaw.dt:
                first_thaw = i
        if first_thaw != detectionOjb(26473669201,5000,'Clear','Probably Hot'):
            return first_thaw
        else:
            return False
    except Exception as e:
        er.add_events("ERROR: Issue with finding the first thaw: {}".format(e.string))
        return False
        
def format_weather_message(weather_obj, first_thaw):
    """Takes weather objects and returns string of descriptive weather conditions"""
    try:
        time = datetime.datetime.fromtimestamp(weather_obj.dt)
        if first_thaw != False:
            first_thaw_time = datetime.datetime.fromtimestamp(first_thaw)
        else:
            first_thaw_time = "Unknown, this is a long freeze"
        weather_string = "Freezing Conditions coming up at:" \
            " {0}, temp: {1}, conditions: {2} \n Expected end at: {3}"\
                .format(time, weather_obj.t, weather_obj.wd, first_thaw_time)
        return weather_string
    except Exception as e:
        er.add_events("ERROR: Unable to convert weather object to string: {}".format(e.string))

if __name__ == "__main__":
    __location__ = u.get_local_file_path()
    
    config = u.read_json(os.path.join(__location__, 'config.json'))
    
    db.setupdbs(config["MYSQL"]["HOSTNAME"],config["MYSQL"]["PORT"]
            ,config["MYSQL"]["WEATHER_USERNAME"],config["MYSQL"]["WEATHER_PASS"])
    #forecasted_weather = get_weather_forecast(config["WEATHER"]["OPENWEATHERAPI"],config["WEATHER"]["LAT"],config["WEATHER"]["LONG"])
    freezing_forecasted_condition = have_Freezing_Conditions()
    db.close_dbs()