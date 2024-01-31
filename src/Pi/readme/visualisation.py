import matplotlib.pyplot as plt
import src.Pi.db.db_utils as db
import json
import os
from pathlib import Path


def run():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = Path(dir_path)
    parent_path = path.parent.absolute()
    conn = db.connect_db(f"{parent_path}/db//mariadb_config.json")
    cur = conn.cursor()
    data = db.read_data(conn, cur)
    conn.close()

    with open("data.json", "w") as data_file:
        json.dump(data, data_file)

    x = [0, 1, 2, 3]
    y = [0, 2, 4, 6]
    plt.plot(x, y)
    plt.show()


if __name__ == "__main__":
    run()
