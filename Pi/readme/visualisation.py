import matplotlib.pyplot as plt
import matplotlib.dates as dts
import Pi.db.db_utils as db
import json
import os
from pathlib import Path


def get_data(cached=False):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = "data.json"
    if cached:
        with open(f"{dir_path}/{path}", "r") as data_file:
            data = json.load(data_file)
        return data

    path = Path(dir_path)
    parent_path = path.parent.absolute()
    conn = db.connect_db(f"{parent_path}/db/mariadb_config.json")
    cur = conn.cursor()
    data = db.read_data(conn, cur)
    conn.close()

    with open(path, "w") as data_file:
        json.dump(data, data_file, indent=4, sort_keys=True, default=str)
    return data


def plot(data):
    dates0 = [x[1] for x in data]
    dates = dts.date2num(dates0)
    distance = [x[2] for x in data]
    ax = plt.plot_date(dates, distance)
    plt.xlim(dates[-75], dates[-5])
    plt.show()


data = get_data(True)
plot(data)
