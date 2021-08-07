import matplotlib.pyplot as plt
from functions import *
import pandas as pd


def plot_grid(months: list, parameters: dict):
    plot_xgrid(months)
    plot_ygrid(parameters)


parameters = {"path data": "../Data/",
              "path graphics": "../Graphics/",
              "file data": "Doses_time",
              "graphics name": "Dose_compare.png",
              "date initial": "2020-06-01",
              "date final": "2020-09-01",
              "dataset doses": "1/4 MED",
              "y limit": 25,
              "y delta": 5,
              "fontsize": 12,
              # The first dataset is used for set the xticks
              "dataset parameters": {"dataset 1": {"AOD": "Binary search",
                                                   "Ozone": "OMI",
                                                   "Color": "#000000",
                                                   "Title": "TES con presencia de humo"},
                                     #  "dataset 2": {"AOD": "Binary search",
                                     #                "Ozone": "260"},
                                     #  "dataset 3": {"AOD": "0.30",
                                     #                "Ozone": "260",
                                     #                "Color": "blue",
                                     #                "Title": "Clean"},
                                     "dataset 4": {"AOD": "0.30",
                                                   "Ozone": "OMI",
                                                   "Color": "#e85d04",
                                                   "Title": "TES en condiciones normales", },
                                     },
              }
plt.subplots(figsize=(10, 6))
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
                   months_names,
                   fontsize=parameters["fontsize"])
        plot_grid(months,
                  parameters)
plt.xlim(pd.to_datetime(parameters["date initial"]),
         pd.to_datetime(parameters["date final"]))
plt.xlabel("año 2020",
           fontsize=parameters["fontsize"])
plt.ylim(0, parameters["y limit"])
plt.ylabel("TES (minutos)",
           fontsize=parameters["fontsize"])
plt.subplots_adjust(top=0.956,
                    bottom=0.132,
                    left=0.106,
                    right=0.958,
                    hspace=0.248,
                    wspace=0.2)
plt.legend(frameon=False,
           fontsize=parameters["fontsize"]+2,
           loc="lower left")
plt.tight_layout()
plt.savefig("{}{}".format(parameters["path graphics"],
                          parameters["graphics name"]),
            dpi=400)
