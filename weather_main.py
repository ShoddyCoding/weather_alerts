import fn_weather as fn
import utilities as u
import eventlogger as e
import os


def main():
    u.initialize_log()
    e.add_events("PROGRAM START")
    __location__ = u.get_local_file_path()
    config = u.read_json(os.path.join(__location__, 'config.json'))
    fn.get_weather_forecast(config["WEATHER"]["OPENWEATHERAPI"],config["WEATHER"]["LAT"],config["WEATHER"]["LONG"])
    fn.get_air_pollution(config["WEATHER"]["OPENWEATHERAPI"],config["WEATHER"]["LAT"],config["WEATHER"]["LONG"])
    fn.get_current_weather(config["WEATHER"]["OPENWEATHERAPI"],config["WEATHER"]["LAT"],config["WEATHER"]["LONG"])
    e.add_events("PROGRAM END")
    e.close_log()

main()