import pandas as pd
from datetime import datetime, timedelta
from matplotlib.transforms import Bbox
import Pi.db.db_utils as db


def get_cumulative_times(data: pd.DataFrame, delay: int = 0, is_pi=False):
    max_time = datetime.today() - timedelta(days=delay)
    max_time = max_time.replace(hour=0, minute=0, second=0, microsecond=0)
    current_time = max_time - timedelta(days=1 + delay)

    # Turn dataframe to list of list for optimized looping, 10x speedup over iloc loop
    elements = list(map(list, data.itertuples(index=False)))

    # Get column indexes
    timestamp_idx = data.columns.get_loc("Timestamp")
    on_pc_idx = data.columns.get_loc("on_pc")

    # Tally up times
    time_on_pc = timedelta()
    time_off_pc = timedelta()
    on_pc = False
    for element in elements:
        timestamp = element[timestamp_idx]
        on_pc = element[on_pc_idx]
        if on_pc:
            time_on_pc += timestamp - current_time
        else:
            time_off_pc += timestamp - current_time
        current_time = timestamp

    # Now we have looped through the data, there may be a few remaining seconds that need to be accounted for before we
    # hit the 24 hour mark so we will give it to the latest on_pc status
    if on_pc:
        time_on_pc += max_time - current_time
    else:
        time_off_pc += max_time - current_time

    if is_pi:
        conn = db.connect_db()
        seconds_per_day = 86400
        perc_time_on = time_on_pc.total_seconds()/seconds_per_day
        db.log_aggregate(conn, (perc_time_on,))
    return time_on_pc, time_off_pc


if __name__ == "__main__":
    HEIGHT = 0.2
    from Pi.readme.visualisation import get_data
    import matplotlib.pyplot as plt

    data = get_data(False, 1)

    x = get_cumulative_times(data)
    # Not on PC
    time1 = x[0].total_seconds()
    # On PC
    time2 = x[1].total_seconds()
    total = time1 + time2
    # plt.bar(["On PC", "Not On PC"], [x1.total_seconds() for x1 in x])
    # Make thinner, remove grid, add title maybe? fix colors
    plt.style.use('dark_background')
    fig = plt.figure(figsize=[14, 10])
    ax = plt.subplot(111)
    ax.barh([0], 100 * time1 / total, height=HEIGHT, facecolor="red", alpha=0.5)
    ax.barh([0], 100 * time2 / total, height=HEIGHT, color=[.5, .5, .8], left=100 * time1 / total)
    plt.xlim(0, 100)
    plt.ylim(0, 0.5)
    frame1 = plt.gca()
    ax.spines[['left', 'top', 'right']].set_visible(False)
    # frame1.axes.get_xaxis().set_visible(False)
    frame1.axes.get_yaxis().set_visible(False)
    plt.xlabel('Percentage', fontsize=16)
    plt.savefig("graphs/tmp.png", bbox_inches=Bbox([[0.5, 0.5], [14, 3]]))
    plt.show()
