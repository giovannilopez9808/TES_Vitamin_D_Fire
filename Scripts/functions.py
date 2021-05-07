import pandas as pd


def cut_data_from_date_period(data, day_initial, day_final):
    data = data[data.index.date >= day_initial]
    data = data[data.index.date <= day_final]
    return data
