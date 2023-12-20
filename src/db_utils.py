import mariadb
import sys
import json


def connect_db(config_path="../config.json"):
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


def send_data(conn, cur, vals):
    cur.execute("INSERT INTO time_on_pc(distance, on_pc) VALUES (?, ?);", vals)
    conn.commit()
