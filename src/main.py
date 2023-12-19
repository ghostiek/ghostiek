# Module Imports
import mariadb
import sys
import json
from src.utils import connect_db, send_data


conn = connect_db()
cur = conn.cursor()
send_data(conn, cur, (12, False))


cur.execute('SELECT * FROM time_on_pc;')
print(cur.fetchall())

