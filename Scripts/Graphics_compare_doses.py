import matplotlib.pyplot as plt
from functions import *
import pandas as pd


parameters = {"path data": "../Data/",
              "path graphics": "../Graphics/",
              "file data": "Doses_time",
              "date initial": "2020-06-01",
              "date final": "2020-10-01",
              "dataset doses": "1/4 MED",
              # The first dataset is used for set the xticks
              "dataset parameters": {"dataset 1": {"dataset AOD": "Binary search",
                                                   "dataset Ozone": "OMI"},
                                     #  "dataset 2": {"dataset AOD": "Binary search",
                                     #                "dataset Ozone": "260"},
                                     #  "dataset 3": {"dataset AOD": "0.30",
                                     #                "dataset Ozone": "260"},
                                     "dataset 4": {"dataset AOD": "0.30",
                                                   "dataset Ozone": "OMI"},
                                     },
              }
for i, dataset in enumerate(parameters["dataset parameters"]):
    dataset = parameters["dataset parameters"][dataset]
    ID, title = obtain_id_and_title_parameters(dataset["dataset Ozone"],
                                               dataset["dataset AOD"])
    data = read_data(parameters["path data"],
                     "{}{}.csv".format(parameters["file data"],
                                       ID))
    plt.scatter(data.index, data[parameters["dataset doses"]],
                label=title,
                lw=1.5)
    if i == 0:
        months, months_names = obtain_xticks(data.index)
        plt.xticks(months,
                   months_names)
plt.xlim(pd.to_datetime(parameters["date initial"]),
         pd.to_datetime(parameters["date final"]))
plt.xlabel("Periodo 2019-2020",
           fontsize=12)
plt.ylim(0, 40)
plt.yticks([tick for tick in range(0, 45, 5)])
plt.ylabel("TES (minutos)",
           fontsize=12)
plt.grid(ls="--",
         color="grey",
         alpha=0.5)
plt.subplots_adjust(top=0.956,
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
