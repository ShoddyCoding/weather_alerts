import json
import sys,os

def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def error_collector():
    """Take str and adds it to global error variable"""

def get_local_file_path():
    """returns file path of the local files"""
    return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))