import pandas as pd
from datetime import datetime, timedelta


def get_cumulative_times(data: pd.DataFrame, delay: int = 0):
    max_time = datetime.today() - timedelta(days=delay)
    max_time = max_time.replace(hour=0, minute=0, second=0, microsecond=0)
    current_time = max_time - timedelta(days=1+delay)

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
    return time_on_pc, time_off_pc


if __name__ == "__main__":
    from Pi.readme.visualisation import get_data
    import matplotlib.pyplot as plt
    data = get_data(False, 2)
    result = -data['Timestamp'].where(data['on_pc']).diff(periods=-1).sum()
    print(result)

    x = get_cumulative_times(data, 1)
    # Not on PC
    time1 = x[0].total_seconds()
    # On PC
    time2 = x[1].total_seconds()
    total = time1+time2
    #plt.bar(["On PC", "Not On PC"], [x1.total_seconds() for x1 in x])
    # Make thinner, remove grid, add title maybe? fix colors
    plt.barh([0], (time1 + time2) / total, color="black")
    plt.barh([0], time2/total, color="red")


    #my_pie, _, _ = plt.pie([x1.total_seconds() for x1 in x], radius=1.2, colors=["red", "black"], autopct="%.1f%%")
    plt.show()