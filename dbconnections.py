import os
import pymysql
import eventlogger as er
import utilities as u

def setupdbs(hostname, port, user, pw):
    global conn_local_prod
    global conn_local_prod_cursor

    print("starting up the local connection")
    try: 
        conn_local_prod = pymysql.connect(
                                host = hostname,
                                port = int(port),
                                user = user,
                                password = pw,
                                autocommit=True
        )
        conn_local_prod_cursor = conn_local_prod.cursor()
    except Exception as e:
        er.add_events("ERROR: Unable to Setup DB: {}".format(e.string))

def close_dbs():
    print("closing db connections")
    try:
        conn_local_prod.close()
    except Exception as e:
        er.add_events("ERROR: Unable to Close DBs: {}".format(e.string))

if __name__ == "__main__":
    __location__ = u.get_local_file_path()
    config = u.read_json(os.path.join(__location__, 'config.json'))
    setupdbs(config["MYSQL"]["HOSTNAME"],config["MYSQL"]["PORT"]
            ,config["MYSQL"]["WEATHER_USERNAME"],config["MYSQL"]["WEATHER_PASS"])
    close_dbs()