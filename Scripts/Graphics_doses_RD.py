import matplotlib.pyplot as plt
from numpy import array
from functions import *
import pandas as pd


def obtain_data_for_dataset(dataset="", parameters={}):
    dataset = parameters["dataset parameters"][dataset]
    ID, title = obtain_id_and_title_parameters(dataset["Ozone"],
                                               dataset["AOD"])
    data = read_data(parameters["path data"],
                     "{}{}.csv".format(parameters["file data"],
                                       ID))
    return data


def select_same_period(data1=pd.DataFrame(), data2=pd.DataFrame()):
    dates_data1 = data1.index
    dates_data2 = data2.index
    dates_data2 = dates_data2.drop(dates_data1)
    data2 = data2.drop(dates_data2)
    return data1, data2


def obtain_RD(data1=pd.DataFrame(), data2=pd.DataFrame(), parameters={}):
    dates = data1.index
    data1 = array(data1[parameters["dataset doses"]])
    data2 = array(data2[parameters["dataset doses"]])
    RD = (data1-data2)*100/data2
    data = {"Smoke": data1,
            "Clear sky": data2,
            "RD": RD
            }
    data = pd.DataFrame(data, index=dates)
    return data


parameters = {"path data": "../Data/",
              "path graphics": "../Graphics/",
              "file data": "Doses_time",
              "file results": "Doses_time_RD.csv",
              "graphics name": "RD_doses.png",
              "date initial": "2020-06-01",
              "date final": "2020-09-01",
              "dataset doses": "1/4 MED",
              "y limit": 60,
              "y delta": 10,
              "fontsize": 13,
              # The first dataset is used for set the xticks
              "dataset parameters": {"dataset 1": {"AOD": "Binary search",
                                                   "Ozone": "OMI"},
                                     "dataset 2": {"AOD": "0.30",
                                                   "Ozone": "OMI"},
                                     },
              }
dataset1, dataset2 = parameters["dataset parameters"]
dataset1 = obtain_data_for_dataset(dataset1,
                                   parameters)
dataset2 = obtain_data_for_dataset(dataset2,
                                   parameters)
dataset1 = select_data_from_date_period(dataset1,
                                        parameters["date initial"],
                                        parameters["date final"])
dataset2 = select_data_from_date_period(dataset2,
                                        parameters["date initial"],
                                        parameters["date final"])
data1, data2 = select_same_period(dataset1,
                                  dataset2)
data = obtain_RD(data1,
                 data2,
                 parameters)
mean = data.mean()
dates = [pd.to_datetime(parameters["date initial"]),
         pd.to_datetime(parameters["date final"])]
data["RD"] = data["RD"].round(2)
data.to_csv("{}{}".format(parameters["path data"],
                          parameters["file results"]))
plt.subplots(figsize=(10, 6))
plt.plot(dates, [mean["RD"], mean["RD"]],
         color="#d90429",
         label="Promedio",
         lw=2)
plt.scatter(data.index, data["RD"],
            label="DR (%)",
            s=30)
months, months_names = obtain_xticks(data.index)
plt.xticks(months,
           months_names,
           fontsize=parameters["fontsize"])
plot_xgrid(months,
           parameters["y limit"])
plot_ygrid(parameters)
plt.xlim(dates[0],
         dates[1])
plt.xlabel("año 2020",
           fontsize=parameters["fontsize"])
plt.ylim(0,
         parameters["y limit"])
plt.ylabel("Diferencia Relativa (%)",
           fontsize=parameters["fontsize"])
plt.legend(frameon=False,
           ncol=2,
           loc="upper left",
           fontsize=parameters["fontsize"]+1)
plt.subplots_adjust(top=0.956,
                    bottom=0.132,
                    left=0.106,
                    right=0.958,
                    hspace=0.248,
                    wspace=0.2)
plt.savefig("{}{}".format(parameters["path graphics"],
                          parameters["graphics name"]),
            dpi=400)
