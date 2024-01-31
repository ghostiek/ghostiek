import mariadb
import sys
import os
import json


def get_creds():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = f"{dir_path}/mariadb_config.json"

    # MariaDB configs
    with open(config_path, "r") as file:
        creds = json.load(file)
    return creds


def read_data(creds):
    try:
        conn = mariadb.connect(
            user=creds["user"],
            password=creds["password"],
            host=creds["host"],
            port=creds["port"],
            database=creds["database"]
        )
    except mariadb.Error as e:
        print(e)
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM sensordb.time_on_pc;")
    result = cur.fetchall()
    conn.close()
    return result
