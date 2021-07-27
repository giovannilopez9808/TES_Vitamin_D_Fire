from Class_list import OMI_data
import pandas as pd


def format_data(data: pd.DataFrame()):
    data = select_only_ozone_data(data)
    data = clean_data(data)
    data = obtain_daily_mean(data)
    data = data.fillna(-1)
    return data


def clean_data(data: pd.DataFrame()):
    data = data[data["Ozone"] <= 400]
    data = data[data["Ozone"] >= 200]
    return data


def select_only_ozone_data(data: pd.DataFrame()):
    columns = data.columns
    columns = columns.drop("Ozone")
    return data.drop(columns, 1)


def obtain_daily_mean(data: pd.DataFrame()):
    return data.resample("D").mean()


def obtain_mean(numero1, numero2):
    return (numero1+numero2)/2


parameters = {"path data": "../Data/",
              "Ozone data": "data_OMI_OMT03",
              "file results": "Ozone_data.csv",
              "date initial": "2019-04-01",
              "date final": "2020-10-01"}
OMI = OMI_data(parameters["path data"],
               parameters["Ozone data"],
               parameters["date initial"],
               parameters["date final"])
Ozone_data = OMI.data
Ozone_data = format_data(Ozone_data)
for date in Ozone_data.index:
    if Ozone_data["Ozone"][date] == -1:
        index_i = date+pd.Timedelta(days=-1)
        index_f = date+pd.Timedelta(days=1)
        mean = obtain_mean(Ozone_data["Ozone"][index_i],
                           Ozone_data["Ozone"][index_f])
        Ozone_data["Ozone"][date] = mean
Ozone_data.to_csv("{}{}".format(parameters["path data"],
                                parameters["file results"]),
                  float_format="%.2f")
