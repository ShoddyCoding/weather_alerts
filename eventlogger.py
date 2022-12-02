import os
import datetime
import utilities as u


def add_events(event):
    s =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    u.log_events += "{0} - {1} \n".format(s, event)

def close_log():
    s = datetime.datetime.now().strftime("%Y-%m-%d")
    isExist = os.path.exists("logs")
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs("logs")
    filename = os.path.join(u.get_local_file_path(),"logs\\weather_alert_log_{}.txt".format(s))
        #"weather_alert_log_{}".format(s),'logs\\')
    with open(filename, 'a+') as file:
            file.write(u.log_events)
    