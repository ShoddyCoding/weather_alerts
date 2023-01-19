import fn_weather as fn
import utilities as u
import eventlogger as e
import texting as t
import os
import dbconnections as db


def main():
    u.initialize_log()
    e.add_events("PROGRAM START - Gather Current Weather Data")
    __location__ = u.get_local_file_path()
    config = u.read_json(os.path.join(__location__, 'config.json'))
    db.setupdbs(config["MYSQL"]["HOSTNAME"],config["MYSQL"]["PORT"]
            ,config["MYSQL"]["WEATHER_USERNAME"],config["MYSQL"]["WEATHER_PASS"])
    ap = fn.get_air_pollution(config["WEATHER"]["OPENWEATHERAPI"],config["WEATHER"]["LAT"],config["WEATHER"]["LONG"])
    fn.store_air_pollution(ap)
    cw = fn.get_current_weather(config["WEATHER"]["OPENWEATHERAPI"],config["WEATHER"]["LAT"],config["WEATHER"]["LONG"])
    fn.store_current_weather(cw)
    fn.get_weather_forecast(config["WEATHER"]["OPENWEATHERAPI"],config["WEATHER"]["LAT"],config["WEATHER"]["LONG"])
    e.add_events("PROGRAM END")
    e.close_log()
    db.close_dbs()

main()