import datetime

import mariadb
import sys
import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


def connect_db(config_path=f"{dir_path}/mariadb_config.json"):
    with open(config_path, "r") as file:
        creds = json.load(file)

    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user=creds["user"],
            password=creds["password"],
            host=creds["host"],
            port=creds["port"],
            database=creds["database"]

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return conn


def log_distance(conn, dist):
    cur = conn.cursor()
    cur.execute("INSERT INTO time_on_pc(distance) VALUES (?);", dist)
    conn.commit()


def log_aggregate(conn, time_on):
    cur = conn.cursor()
    cur.execute("INSERT INTO aggregate_table(time_on_pc) VALUES (?);", time_on)
    conn.commit()


def read_data(conn, cur, start_date):
    start_date = start_date.strftime("%Y-%m-%d")
    # Get Cursor
    cur.execute(f"SELECT * FROM sensordb.time_on_pc WHERE timestamp_column > '{start_date}';")
    result = cur.fetchall()
    return result
