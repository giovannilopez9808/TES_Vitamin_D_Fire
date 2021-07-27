import pandas as pd


def select_data_from_date_period(data, day_initial, day_final):
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


def obtain_xticks(dates):
    months = [obtain_first_date_for_month(dates[0])]
    for date in dates:
        if months[-1].month != date.month:
            date = obtain_first_date_for_month(date)
            months.append(date)
    year = months[-1].year
    month = months[-1].month+1
    if month > 12:
        month = 1
        year += 1
    date = obtain_first_date_for_month(months[-1])
    months.append(date)
    months_names = obtain_month_names(months)
    return months, months_names


def obtain_first_date_for_month(date):
    year = date.year
    month = date.month
    date = pd.to_datetime("{}-{}-01".format(year,
                                            str(month).zfill(2)))
    return date


def obtain_month_names(dates):
    months_names = []
    for date in dates:
        months_names.append(date.strftime("%b"))
    return months_names


def read_data(path="", file=""):
    data = pd.read_csv("{}{}".format(path,
                                     file))
    data = format_data(data)
    return data


def format_data(data: pd.DataFrame()):
    data.index = pd.to_datetime(data["Date"])
    data = data.drop("Date", 1)
    return data


def select_dataset_parameters_AOD(id_dataset=""):
    dataset = {"0.30": {"Filename": "03",
                        "title": "AOD=0.30"},
               "Binary search": {"Filename": "binary_search",
                                 "title": "AOD=BS"},
               }
    return dataset[id_dataset]


def select_dataset_parameters_Ozone(id_dataset=""):
    dataset = {"260": {"Filename": "260",
                       "title": "260 DU"},
               "OMI": {"Filename": "OMI",
                       "title": "OMI"},
               }
    return dataset[id_dataset]
