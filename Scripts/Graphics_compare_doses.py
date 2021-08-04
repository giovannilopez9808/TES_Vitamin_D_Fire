import matplotlib.pyplot as plt
from functions import *
import pandas as pd


def plot_grid(months=[], parameters={}):
    plot_xgrid(months)
    plot_ygrid(parameters)


def plot_xgrid(months=[]):
    for month in months:
        grid([month, month],
             [0, 36])
        year = month.year
        month = str(month.month).zfill(2)
        date = pd.to_datetime("{}-{}-15".format(year,
                                                month))
        grid([date, date],
             [0, 36])


def plot_ygrid(parameters={}):
    ylabels = []
    dates = [pd.to_datetime(parameters["date initial"]),
             pd.to_datetime(parameters["date final"])]
    yticks = range(parameters["y limit"]+1)
    for ytick in range(parameters["y limit"]+1):
        if ytick % parameters["y delta"] == 0:
            grid(dates,
                 [ytick, ytick])
        else:
            ytick = ""
        ylabels.append(ytick)
    plt.yticks(yticks, ylabels)


def grid(x, y):
    plt.plot(x, y,
             ls="--",
             color="grey",
             alpha=0.5)


parameters = {"path data": "../Data/",
              "path graphics": "../Graphics/",
              "file data": "Doses_time",
              "graphics name": "Dose_compare.png",
              "date initial": "2020-06-01",
              "date final": "2020-09-01",
              "dataset doses": "1/4 MED",
              "y limit": 35,
              "y delta": 5,
              # The first dataset is used for set the xticks
              "dataset parameters": {"dataset 1": {"AOD": "Binary search",
                                                   "Ozone": "OMI",
                                                   "Color": "#000000",
                                                   "Title": "Aire con presencia de humo"},
                                     #  "dataset 2": {"AOD": "Binary search",
                                     #                "Ozone": "260"},
                                     #  "dataset 3": {"AOD": "0.30",
                                     #                "Ozone": "260",
                                     #                "Color": "blue",
                                     #                "Title": "Clean"},
                                     "dataset 4": {"AOD": "0.30",
                                                   "Ozone": "OMI",
                                                   "Color": "#e85d04",
                                                   "Title": "Aire en condiciones típicas", },
                                     },
              }
for i, dataset in enumerate(parameters["dataset parameters"]):
    dataset = parameters["dataset parameters"][dataset]
    ID, title = obtain_id_and_title_parameters(dataset["Ozone"],
                                               dataset["AOD"])
    data = read_data(parameters["path data"],
                     "{}{}.csv".format(parameters["file data"],
                                       ID))
    plt.scatter(data.index, data[parameters["dataset doses"]],
                label=dataset["Title"],
                c=dataset["Color"],
                s=15,)
    if i == 0:
        months, months_names = obtain_xticks(data.index)
        plt.xticks(months,
                   months_names)
        plot_grid(months,
                  parameters)
plt.xlim(pd.to_datetime(parameters["date initial"]),
         pd.to_datetime(parameters["date final"]))
plt.xlabel("año 2020",
           fontsize=12)
plt.ylim(0, parameters["y limit"])
plt.ylabel("TES (minutos)",
           fontsize=12)
plt.subplots_adjust(top=0.956,
                    bottom=0.132,
                    left=0.106,
                    right=0.958,
                    hspace=0.248,
                    wspace=0.2)
plt.legend(frameon=False,
           fontsize=11,
           loc="lower left")
plt.savefig("{}{}".format(parameters["path graphics"],
                          parameters["graphics name"]),
            dpi=400)
plt.show()
