import matplotlib.pyplot as plt
import matplotlib.dates as dts
import Pi.db.db_utils as db
import json
import os
from pathlib import Path
import seaborn as sns
import pandas as pd


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


def pretty_plot(data):
    dates = [x[1] for x in data]
    distance = [x[2] for x in data]
    df = pd.DataFrame({"TimestampString":dates, "Distance": distance})
    df["Timestamp"] = pd.to_datetime(df["TimestampString"], format="%Y-%m-%d %H:%M:%S")
    # Add the line over the area with the plot function
    fig = plt.figure(figsize=[7, 5])
    ax = plt.subplot(111)

    # Fill the area with fill_between
    l = ax.fill_between(df['Timestamp'], df['Distance'], alpha=0.2)

    # Control the title of each facet
    # set the basic properties
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Distance from Computer')
    ax.set_title("Time Spent on Computer")
    ax.set_xlim(df["Timestamp"].iloc[-50], df["Timestamp"].iloc[-10])
    ax.set_ylim(0, max(distance[-50:-10])+30)
    # set the grid on
    ax.grid('on')

    l.set_facecolors([[.5, .5, .8, .3]])
    #
    # # change the edge color (bluish and transparentish) and thickness
    l.set_edgecolors([[0, 0, .5, .3]])
    l.set_linewidths([3])

    # remove tick marks
    ax.xaxis.set_tick_params(size=0)
    ax.yaxis.set_tick_params(size=0)

    # change the color of the top and right spines to opaque gray

    ax.spines['right'].set_color((.8, .8, .8))
    ax.spines['top'].set_color((.8, .8, .8))

    # tweak the axis labels
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()

    xlab.set_style('italic')
    xlab.set_size(10)
    ylab.set_style('italic')
    ylab.set_size(10)

    # tweak the title
    ttl = ax.title
    ttl.set_weight('bold')
    # Show the graph
    plt.show()


data = get_data(True)
pretty_plot(data)
