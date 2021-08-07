from Class_list import TUV_results
import matplotlib.pyplot as plt
from functions import *
import pandas as pd

parameters = {"path data": "../Results/TUV/",
              "date initial": "2020-08-01",
              "date final": "2020-08-10",
              "dataset": {"AOD": "0.30",
                          "Ozone": "260"}, }
files, ID = obtain_files_for_dataset_and_ID(parameters,
                                            parameters["dataset"])
for file in files:
    TUV = TUV_results(parameters["path data"],
                      file)
    before_date = TUV.date >= parameters["date initial"]
    after_date = TUV.date <= parameters["date final"]
    if before_date and after_date:
        plt.plot(TUV.data.index, TUV.data["UVI"])
plt.xlim(pd.to_datetime(parameters["date initial"]),
         pd.to_datetime(parameters["date final"]))
plt.ylim(2, 4)
plt.xticks(fontsize=7)
plt.show()
