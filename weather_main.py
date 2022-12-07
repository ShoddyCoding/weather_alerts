import fn_weather as fn
import utilities as u
import eventlogger as e
import texting as t
import os


def main():
    u.initialize_log()
    e.add_events("PROGRAM START")
    __location__ = u.get_local_file_path()
    config = u.read_json(os.path.join(__location__, 'config.json'))
    forecasted_weather = fn.get_weather_forecast(config["WEATHER"]["OPENWEATHERAPI"],config["WEATHER"]["LAT"],config["WEATHER"]["LONG"])
    #fn.get_air_pollution(config["WEATHER"]["OPENWEATHERAPI"],config["WEATHER"]["LAT"],config["WEATHER"]["LONG"])
    #fn.get_current_weather(config["WEATHER"]["OPENWEATHERAPI"],config["WEATHER"]["LAT"],config["WEATHER"]["LONG"])
    if fn.have_Freezing_Conditions(forecasted_weather,config["FREEZINGCONDITIONS"]["TEMP"]) != False:
        e.add_events("Found - We have a freezing condition coming up!")
    e.add_events("PROGRAM END")
    e.close_log()

main()