import matplotlib.pyplot as plt
from functions import *
import pandas as pd


parameters = {"path data": "../Data/",
              "path graphics": "../Graphics/",
              "file data": "Doses_time",
              "file OMI": "Ozone_OMI",
              "file binary search": "binary_search",
              "file clear sky": "clear_sky",
              "date initial": "2020-06-01",
              "date final": "2020-08-01",
              "dataset": "1/4 MED"
              }
OMI_data = read_data(parameters["path data"],
                     "{}_{}.csv".format(parameters["file data"],
                                        parameters["file OMI"]))
binary_search_data = read_data(parameters["path data"],
                               "{}_{}.csv".format(parameters["file data"],
                                                  parameters["file binary search"]))
clear_sky_data = read_data(parameters["path data"],
                           "{}_{}.csv".format(parameters["file data"],
                                              parameters["file clear sky"]))
months, months_names = obtain_xticks(OMI_data.index)
plt.scatter(OMI_data.index, OMI_data[parameters["dataset"]],
            label="Ozone OMI",
            lw=1.5)
plt.scatter(binary_search_data.index, binary_search_data[parameters["dataset"]],
            label="Binary search",
            lw=1.5)
plt.scatter(clear_sky_data.index, clear_sky_data[parameters["dataset"]],
            label="Clear sky",
            lw=1.5)
plt.xticks(months,
           months_names)
plt.xlim(pd.to_datetime(parameters["date initial"]),
         pd.to_datetime(parameters["date final"]))
plt.xlabel("Periodo 2019-2020",
           fontsize=12)
plt.ylim(0, 40)
plt.yticks([tick for tick in range(0, 50, 10)])
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