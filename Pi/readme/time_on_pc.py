from Pi.readme.visualisation import get_data
from datetime import datetime, timedelta


def get_cumulative_times():
    data = get_data()

    max_time = datetime.today()
    max_time = max_time.replace(hour=0, minute=0, second=0, microsecond=0)
    current_time = max_time - timedelta(days=1)

    # Turn dataframe to list of list for optimized looping
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
