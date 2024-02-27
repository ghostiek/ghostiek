# Currently we don't have much data, what would make the most sense would be to simply use a 4 day moving average will
# iterate more on it in the future
import pandas as pd
from datetime import date, timedelta
from Pi.db.db_utils import connect_db, read_aggregate_data


def moving_average_prediction(data: list):
    total = sum([x[2] for x in data])
    return total/len(data)


if __name__ == "__main__":
    conn = connect_db()
    dt_now = date.today()
    data = read_aggregate_data(conn, dt_now)
    result = moving_average_prediction(data)
    print(result)



