import mariadb
import os
import sys
import json
from sshtunnel import SSHTunnelForwarder

dir_path = os.path.dirname(os.path.realpath(__file__))
config_path = f"{dir_path}/mariadb_ga_config.json"
ssh_path = f"{dir_path}/ssh_config.json"

# SSH configs
with open(ssh_path, "r") as ssh_config_file:
    ssh_config = json.load(ssh_config_file)

# MariaDB configs
with open(config_path, "r") as file:
    creds = json.load(file)

host = ssh_config["host"]
port = ssh_config["port"]
username = ssh_config["username"]
password = ssh_config["password"]
remote_bind_address = ssh_config["remote_bind_address"]
remote_port = ssh_config["remote_port"]

tunnel = SSHTunnelForwarder((host, port), ssh_password=password, ssh_username=username,
                            remote_bind_address=(remote_bind_address, remote_port))
tunnel.start()
# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user=creds["user"],
        password=creds["password"],
        host=remote_bind_address,
        port=tunnel.local_bind_port,
        database=creds["database"]
    )
except mariadb.Error as e:
    print(e)
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

cur.execute("SELECT * FROM sensordb.time_on_pc;")
x = cur.fetchall()
print(x)
conn.close()
tunnel.stop()
