import matplotlib.pyplot as plt
from functions import *
import pandas as pd

parameters = {"path data": "../Data/",
              "path graphics": "../Graphics/",
              "file data": "Doses_time",
              "file Fire data": "NI_real.csv",
              "graphics name": "Dose_fire_compare.png",
              "date initial": "2020-06-01",
              "date final": "2020-09-01",
              "dataset doses": "1/4 MED",
              "Doses y limit": 25,
              "Fire y limit": 550,
              "Doses y delta": 5,
              "Fire y delta": 50,
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
                                                   "Color": "#4361ee",
                                                   "Title": "TES en condiciones normales", },
                                     },
              }
fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()
for i, dataset in enumerate(parameters["dataset parameters"]):
    dataset = parameters["dataset parameters"][dataset]
    ID, title = obtain_id_and_title_parameters(dataset["Ozone"],
                                               dataset["AOD"])
    data = read_data(parameters["path data"],
                     "{}{}.csv".format(parameters["file data"],
                                       ID))
    ax1.scatter(data.index, data[parameters["dataset doses"]],
                label=dataset["Title"],
                c=dataset["Color"],
                s=15,)
data = read_data(parameters["path data"],
                 parameters["file Fire data"])
ax2.plot(data.index, data["NI"],
         label="Focos de incendios",
         color="#ae2012",
         marker="o"
         )
ax1.set_xlim(pd.to_datetime(parameters["date initial"]),
             pd.to_datetime(parameters["date final"]))
ax1.set_ylabel("TES (minutos)",
               fontsize=parameters["fontsize"])
ax2.set_ylabel("Focos de incendios diarios",
               fontsize=parameters["fontsize"],
               rotation=-90,
               labelpad=20)
ax1.set_ylim(0, parameters["Doses y limit"])
ax2.set_ylim(0, parameters["Fire y limit"])
ax1.set_yticks([i for i in range(0, parameters["Doses y limit"] +
               parameters["Doses y delta"], parameters["Doses y delta"])])
ax2.set_yticks([i for i in range(0, parameters["Fire y limit"] +
               parameters["Fire y delta"], parameters["Fire y delta"])])
fig.legend(frameon=False,
           fontsize=parameters["fontsize"]+2,
           loc="upper center",
           bbox_to_anchor=(0, 0, 0.9, 0.97),
           ncol=2)
fig.tight_layout()
plt.savefig("{}{}".format(parameters["path graphics"],
                          parameters["graphics name"]),
            dpi=400)
plt.show()
