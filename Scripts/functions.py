import pandas as pd


def cut_data_from_date_period(data, day_initial, day_final):
    data = data[data.index.date >= day_initial]
    data = data[data.index.date <= day_final]
    return data


def date_to_yymmdd(date):
    year = str(date.year)[2:4]
    month = str(date.month).zfill(2)
    day = str(date.day).zfill(2)
    date = year+month+day
    return date, year, month, day


def calculate_RD(measurement, model):
    RD = (model-measurement)*100/measurement
    return RD
