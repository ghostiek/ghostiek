import matplotlib.pyplot as plt
import matplotlib.dates as dts
import Pi.db.db_utils as db
import json
import os
from pathlib import Path
import pandas as pd
from datetime import datetime, date


def get_data(is_pi=False):
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
    data = db.read_data(conn, cur)
    conn.close()

    with open(f"{path}/{file_path}", "w") as data_file:
        json.dump(data, data_file, indent=4, sort_keys=True, default=str)
    return data

def light_plot(data, is_pi):
    dates = [x[1] for x in data]
    distance = [x[2] for x in data]
    df_all = pd.DataFrame({"TimestampString":dates, "Distance": distance})
    df_all["Timestamp"] = pd.to_datetime(df_all["TimestampString"], format="%Y-%m-%d %H:%M:%S")
    # Smoothing the data
    df_all["Distance"] = df_all["Distance"].rolling(window=100).mean()
    # Today's data
    df = df_all[df_all["Timestamp"].dt.date >= date.today()]

    # Add the line over the area with the plot function
    fig = plt.figure(figsize=[7, 5])
    ax = plt.subplot(111)

    # Fill the area with fill_between
    l = ax.fill_between(df['Timestamp'], df['Distance'], alpha=0.2)

    # Control the title of each facet
    # set the basic properties
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Sensor Distance from Computer (in cm)')
    ax.set_title("Time Spent on Computer")
    ax.set_xlim(df["Timestamp"].min(), df["Timestamp"].max())
    ax.set_ylim(0, df["Distance"].max()+30)
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
    
    # Fixing xlabels
    fig.autofmt_xdate()
    # Save figure
    dir_path = os.path.dirname(os.path.realpath(__file__))
    plt.savefig(f"{dir_path}/graphs/light-plot-{datetime.now().strftime('%Y-%m-%d_%H')}.png")
    # Show the graph
    if not is_pi:
        plt.show()

def dark_plot(data, is_pi):
    return


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
