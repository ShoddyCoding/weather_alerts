import json
import sys,os
import time

def initialize_log():
    global log_events
    log_events = ""

def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def error_collector():
    """Take str and adds it to global error variable"""

def get_local_file_path():
    """returns file path of the local files"""
    return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def remove_old_log_files(folder, daysold):
    dir = os.path.join(get_local_file_path(), folder)
    now = time.time()
    for f in os.listdir(dir):
        file_path = os.path.join(dir, f)
        if os.stat(file_path).st_mtime < now - daysold * 86400:
            if os.path.isfile(file_path):
                os.remove(file_path)

if __name__ == "__main__":
    remove_old_log_files("logs",30)