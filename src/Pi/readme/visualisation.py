import matplotlib.pyplot as plt
import src.Pi.db.db_utils as db
import json


conn = db.connect_db()
cur = conn.cursor()
data = db.read_data(conn, cur)
conn.close()

with open("data.json", "w") as data_file:
    json.dump(data, data_file)

x = [0,1,2,3]
y=[0,2,4,6]
plt.plot(x,y)
plt.show()