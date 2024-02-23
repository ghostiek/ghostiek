import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
import matplotlib.dates as md
import Pi.db.db_utils as db
import Pi.readme.time_on_pc as tp
import json
import os
from pathlib import Path
import pandas as pd
from datetime import date, timedelta

LOWER_LIMIT = 10
HIGHER_LIMIT = 70


def get_data(is_pi=False, day=1):
    date_filter = date.today() - timedelta(days=day)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = "data.json"
    if not is_pi:
        # Get data from saved dir since we can't access db
        with open(f"{dir_path}/{file_path}", "r") as data_file:
            data = json.load(data_file)
    else:
        path = Path(dir_path)
        parent_path = path.parent.absolute()
        conn = db.connect_db(f"{parent_path}/db/mariadb_config.json")
        cur = conn.cursor()
        data = db.read_data(conn, cur, date_filter)
        conn.close()

        with open(f"{path}/{file_path}", "w") as data_file:
            json.dump(data, data_file, indent=4, sort_keys=True, default=str)
    df = pd.DataFrame.from_records(data)
    df = preprocess_data(df, date_filter)
    return df


def preprocess_data(df, date_filter):
    min_date = date_filter
    max_date = date_filter + timedelta(days=1)
    df.columns = ["id", "TimestampString", "Distance"]
    # Every 15 mins
    hours_period = 0.25
    df["Timestamp"] = pd.to_datetime(df["TimestampString"], format="%Y-%m-%d %H:%M:%S")
    df.index = df["Timestamp"]
    df = df[(df["Timestamp"].dt.date >= min_date) & (df["Timestamp"].dt.date < max_date)]
    # Smoothing the data
    df["DistanceSmooth"] = df["Distance"].rolling(window=timedelta(hours=hours_period), center=True).mean()
    df["on_pc"] = (df["DistanceSmooth"] > LOWER_LIMIT) & (df["DistanceSmooth"] < HIGHER_LIMIT)
    return df


def sensor_plot(df, is_pi, color):
    # Add the line over the area with the plot function
    fig = plt.figure(figsize=[14, 10])
    ax = plt.subplot(111)

    # Fill the area with fill_between
    l = ax.fill_between(df['Timestamp'], df['DistanceSmooth'], where=~df["on_pc"], alpha=1)
    l2 = ax.fill_between(df['Timestamp'], df['DistanceSmooth'], where=df["on_pc"], facecolor="red", alpha=0.5)

    # Control the title of each facet
    # set the basic properties
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Sensor Distance from Computer (in cm)')
    ax.set_title(f"Time Spent on Computer Yesterday")
    ax.set_xlim(df["Timestamp"].min(), df["Timestamp"].max())
    ax.set_ylim(0, df["DistanceSmooth"].max() + 30)
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
    plt.axhline(y=HIGHER_LIMIT, color="orange")
    plt.axhline(y=LOWER_LIMIT, color="orange")
    fig.autofmt_xdate()

    # Legend
    ax.legend(["Time Off PC", "Time On PC"], loc="best", edgecolor="black")
    # Save figure
    dir_path = os.path.dirname(os.path.realpath(__file__))
    plt.savefig(f"{dir_path}/graphs/lineplot/{color}-plot-{df['Timestamp'].min().strftime('%Y-%m-%d')}.png")
    # Show the graph
    if not is_pi:
        plt.show()


def percentage_plot(df, data, is_pi, color):
    HEIGHT = 0.2
    LABELS = ["On PC", "Not on PC"]
    COLORS = {"On PC": [1,0,0,0.5], "Not on PC": [.5, .5, .8]}
    # Not on PC
    time1 = data[0].total_seconds()
    # On PC
    time2 = data[1].total_seconds()
    total = time1 + time2
    # plt.bar(["On PC", "Not On PC"], [x1.total_seconds() for x1 in x])
    # Make thinner, remove grid, add title maybe? fix colors
    fig = plt.figure(figsize=[14, 10])
    ax = plt.subplot(111)
    hbar = ax.barh([0], 100 * time1 / total, height=HEIGHT, facecolor="red", alpha=0.5)
    ax.bar_label(hbar, fmt='%.0f%%', label_type="center", fontsize=16)
    ax.barh([0], 100 * time2 / total, height=HEIGHT, color=[.5, .5, .8], left=100 * time1 / total)
    plt.xlim(0, 100)
    plt.ylim(0, 0.5)
    frame1 = plt.gca()
    ax.spines[['left', 'top', 'right']].set_visible(False)
    # frame1.axes.get_xaxis().set_visible(False)
    frame1.axes.get_yaxis().set_visible(False)
    plt.xlabel('Percentage', fontsize=16)
    handles = [plt.Rectangle((0, 0), 1, 1, color=COLORS[label]) for label in LABELS]
    plt.legend(handles, LABELS, bbox_to_anchor=(0, 0.06), loc="lower right")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    plt.savefig(f"{dir_path}/graphs/barplot/{color}-plot-{df['Timestamp'].min().strftime('%Y-%m-%d')}.png", bbox_inches=Bbox([[0, 0.5], [14, 3]]))
    if not is_pi:
        plt.show()


def light_plot(df, cumulative_times, is_pi):
    sensor_plot(df, is_pi, "light")
    percentage_plot(df, cumulative_times, is_pi, "light")


def dark_plot(df, cumulative_times, is_pi):
    plt.style.use('dark_background')
    sensor_plot(df, is_pi, "dark")
    percentage_plot(df, cumulative_times, is_pi, "dark")


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
    data = get_data(is_pi, 1)
    cumulative_times = tp.get_cumulative_times(data, is_pi)
    light_plot(data, cumulative_times, is_pi)
    dark_plot(data, cumulative_times, is_pi)
