import matplotlib.pyplot as plt
from functions import *
import pandas as pd


def read_data(path="", file=""):
    data = pd.read_csv("{}{}".format(path,
                                     file))
    date = obtain_date_from_filename(file)
    data = format_data(data,
                       date)
    return data


def obtain_date_from_filename(file=""):
    date = file.split("_")[0]
    return date


def format_data(data=pd.DataFrame(), date=""):
    data = format_hour(data)
    data.index = pd.to_datetime(date+" "+data["Hour"])
    data = data.drop("Hour", 1)
    return data


def format_hour(data=pd.DataFrame()):
    data["Minute"] = (data["Hour"]-data["Hour"]//1)*60
    data["Minute"] = data["Minute"].round()
    data["Minute"] = data["Minute"].astype(int)
    data["Minute"] = data["Minute"].astype(str).str.zfill(2)
    data["Hour"] = data["Hour"].astype(int)
    data["Hour"] = data["Hour"].astype(str).str.zfill(2)
    data["Hour"] = data["Hour"]+":"+data["Minute"]
    data = data.drop("Minute", 1)
    return data


parameters = {"path data": "../Results/TUV/",
              "date initial": "2020-08-01",
              "date final": "2020-08-10",
              "dataset": {"AOD": "0.30",
                          "Ozone": "260"}, }
files, ID = obtain_files_for_dataset_and_ID(parameters,
                                            parameters["dataset"])
for file in files:
    date = obtain_date_from_filename(file)
    if date >= parameters["date initial"] and date <= parameters["date final"]:
        data = read_data(parameters["path data"],
                         file)
        plt.plot(data.index, data["UVI"])
plt.xlim(pd.to_datetime(parameters["date initial"]),
         pd.to_datetime(parameters["date final"]))
plt.ylim(2, 4)
plt.xticks(fontsize=7)
plt.show()
