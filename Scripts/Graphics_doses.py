import matplotlib.pyplot as plt
from functions import *
import pandas as pd


def obtain_filename_data(parameters={}, ID=""):
    filename = "{}{}.csv".format(parameters["file data"],
                                 ID)
    return filename


parameters = {"path data": "../Data/",
              "path graphics": "../Graphics/",
              "file data": "Doses_time",
              "graphics name": "dosis_vitamin.png",
              "date initial": "2020-06-01",
              "date final": "2020-10-01",
              "Vitamin color": "#f9c74f",
              "Vitamin label": "Dosis pre-vitamina D 136 J/m$^2$",
              "1/4 MED color": "#f48c06",
              "1/4 MED label": "Dosis eritémica mínima 62.5 J/m$^2$",
              "1 MED color": "#dc2f02",
              "1 MED label": "Dosis eritémica mínima 250 J/m$^2$",
              "dataset": {"AOD": "0.30",
                          "Ozone": "OMI"},
              }
ID, title = obtain_id_and_title_parameters(parameters["dataset"]["Ozone"],
                                           parameters["dataset"]["AOD"])
parameters["file data"] = obtain_filename_data(parameters,
                                               ID)
data = read_data(parameters["path data"],
                 parameters["file data"])
months, months_names = obtain_xticks(data.index)
plt.plot(data.index, data["vitamin"],
         color=parameters["Vitamin color"],
         label=parameters["Vitamin label"],
         lw=1.5)
plt.fill_between(data.index, data["vitamin"],
                 data["1/4 MED"],
                 color="#faa307",
                 alpha=0.5)
plt.plot(data.index, data["1/4 MED"],
         color=parameters["1/4 MED color"],
         label=parameters["1/4 MED label"],
         lw=1.5)
plt.fill_between(data.index, data["1/4 MED"],
                 data["1 MED"],
                 color="#e85d04",
                 alpha=0.5)
plt.plot(data.index, data["1 MED"],
         color=parameters["1 MED color"],
         label=parameters["1 MED label"],
         lw=1.5)
plt.xticks(months,
           months_names)
plt.xlim(pd.to_datetime(parameters["date initial"]),
         pd.to_datetime(parameters["date final"]))
plt.xlabel("Periodo 2019-2020",
           fontsize=12)
plt.ylim(0, 100)
plt.yticks([tick for tick in range(0, 110, 10)])
plt.ylabel("TES (minutos)",
           fontsize=12)
plt.title(title)
plt.grid(ls="--",
         color="grey",
         alpha=0.5)
plt.subplots_adjust(top=0.917,
                    bottom=0.132,
                    left=0.106,
                    right=0.958,
                    hspace=0.248,
                    wspace=0.2)
plt.legend(frameon=False,
           fontsize=11)
# plt.savefig("{}{}".format(parameters["path graphics"],
#                           parameters["graphics name"]),
#             dpi=400)
plt.show()
