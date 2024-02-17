import matplotlib.pyplot as plt
import matplotlib.dates as md
import Pi.db.db_utils as db
import json
import os
from pathlib import Path
import pandas as pd
from datetime import datetime, date, timedelta


def get_data(is_pi=False, date_filter=date.today() - timedelta(days=1)):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = "data.json"
    if not is_pi:
        # Get data from saved dir since we can't access db
        with open(f"{dir_path}/{file_path}", "r") as data_file:
            data = json.load(data_file)
        return data

    path = Path(dir_path)
    parent_path = path.parent.absolute()
    conn = db.connect_db(f"{parent_path}/db/mariadb_config.json")
    cur = conn.cursor()
    data = db.read_data(conn, cur, date_filter)
    conn.close()

    with open(f"{path}/{file_path}", "w") as data_file:
        json.dump(data, data_file, indent=4, sort_keys=True, default=str)
    return data


def preprocess_data(data):
    # Every 15 mins
    hours_period = 0.25
    dates = [x[1] for x in data]
    distance = [x[2] for x in data]
    df_all = pd.DataFrame({"TimestampString": dates, "Distance": distance})
    df_all["Timestamp"] = pd.to_datetime(df_all["TimestampString"], format="%Y-%m-%d %H:%M:%S")
    df_all.index = df_all["Timestamp"]
    # Smoothing the data
    df_all["Distance"] = df_all["Distance"].rolling(window=timedelta(hours=hours_period), center=True).mean()
    # Today's data, still needed for local data, would remove this redundant line later on
    min_date = date.today() - timedelta(days=1)
    df = df_all[(df_all["Timestamp"].dt.date >= min_date) & (date.today() > df_all["Timestamp"].dt.date)]
    df["on_pc"] = df["Distance"] < 90
    return df


def on_pc_plot(df, is_pi):
    ax = plt.subplot(111)
    ax.bar(df["Timestamp"], df["Distance"])
    ax.xaxis_date()
    if not is_pi:
        plt.show()


def sensor_plot(df, is_pi, color):
    # Adding threshold to detect if on PC
    df["on_pc"] = df["Distance"] < 70
    # Add the line over the area with the plot function
    fig = plt.figure(figsize=[14, 10])
    ax = plt.subplot(111)

    # Fill the area with fill_between
    l = ax.fill_between(df['Timestamp'], df['Distance'], alpha=1)

    # Control the title of each facet
    # set the basic properties
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Sensor Distance from Computer (in cm)')
    ax.set_title(f"Time Spent on Computer Yesterday")
    ax.set_xlim(df["Timestamp"].min(), df["Timestamp"].max())
    ax.set_ylim(0, df["Distance"].max() + 30)
    # set the grid on
    ax.grid('on')
    # change the edge color (bluish and transparentish) and thickness
    # l.set_edgecolors([[0, 0, .5, .3]])
    # ax.spines['right'].set_color((.8, .8, .8))
    # ax.spines['top'].set_color((.8, .8, .8))
    l.set_facecolors([[.5, .5, .8, .3]])
    l.set_linewidths([3])

    # remove tick marks
    ax.xaxis.set_tick_params(size=0)
    ax.yaxis.set_tick_params(size=0)

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

    # Fixing xlabels
    ax.xaxis.set_major_locator(md.MinuteLocator(byminute=[0, 60]))
    ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    # plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)
    fig.autofmt_xdate()
    # Save figure
    dir_path = os.path.dirname(os.path.realpath(__file__))
    plt.savefig(f"{dir_path}/graphs/{color}-plot-{datetime.now().strftime('%Y-%m-%d')}.png")
    # Show the graph
    if not is_pi:
        plt.show()


def light_plot(data, is_pi):
    sensor_plot(data, is_pi, "light")


def dark_plot(data, is_pi):
    plt.style.use('dark_background')
    sensor_plot(data, is_pi, "dark")


if __name__ == "__main__":
    # Check hostname
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = Path(dir_path)
    parent_path = path.parent.absolute()
    try:
        with open(f"{parent_path}/pi_info.json", "r") as pi_info_file:
            pi_info = json.load(pi_info_file)
        is_pi = os.uname().nodename == pi_info["hostname"]
    except FileNotFoundError:
        is_pi = False
    data = get_data(is_pi)
    light_plot(data, is_pi)
    dark_plot(data, is_pi)
