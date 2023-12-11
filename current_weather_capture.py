import fn_weather as fn
import utilities as u
import eventlogger as e
import texting as t
import os
import dbconnections as db
import datetime


def main():
    u.initialize_log()
    __location__ = u.get_local_file_path()
    config = u.read_json(os.path.join(__location__, 'config.json'))
    e.add_events("PROGRAM START - Gather Current Weather Data")
    db.setupdbs(config["MYSQL"]["HOSTNAME"],config["MYSQL"]["PORT"]
            ,config["MYSQL"]["WEATHER_USERNAME"],config["MYSQL"]["WEATHER_PASS"])
    d = datetime.datetime.now()
    if d.hour == 15:
        e.add_events("BEGIN - CHECK FOR FREEZING WEATHER EVENTS")
        forecasted_weather = fn.get_weather_forecast(config["WEATHER"]["OPENWEATHERAPI"],config["WEATHER"]["LAT"],config["WEATHER"]["LONG"])
        freezing_forecasted_condition = fn.have_Freezing_Conditions()
        if freezing_forecasted_condition != False:
            e.add_events("INFO - We have a freezing condition coming up! Condition: {}".format(freezing_forecasted_condition))
            for recepient in config["RECEPIENTS"]["FREEZEALERTS"].split(","):
                t.send_message(recepient, freezing_forecasted_condition)
        else:
            e.add_events("INFO: No Freezing Events Found")
    ap = fn.get_air_pollution(config["WEATHER"]["OPENWEATHERAPI"],config["WEATHER"]["LAT"],config["WEATHER"]["LONG"])
    fn.store_air_pollution(ap)
    cw = fn.get_current_weather(config["WEATHER"]["OPENWEATHERAPI"],config["WEATHER"]["LAT"],config["WEATHER"]["LONG"])
    fn.store_current_weather(cw)
    fn.get_weather_forecast(config["WEATHER"]["OPENWEATHERAPI"],config["WEATHER"]["LAT"],config["WEATHER"]["LONG"])
    u.remove_old_log_files("logs",30)
    e.close_log()
    db.close_dbs()

main()