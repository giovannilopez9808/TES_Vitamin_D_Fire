import matplotlib.pyplot as plt
from functions import *

parameters = {"path data": "../Data/",
              "file data": "Dates_AOD.csv",
              "date initial": pd.to_datetime("2020-05-01"),
              "date final": pd.to_datetime("2020-10-01"),
              }
data = read_data(parameters["path data"],
                 parameters["file data"])
plt.scatter(data.index, data["AOD"])
plt.plot([parameters["date initial"],
          parameters["date final"]],
         [0.3, 0.3],
         color="red")
plt.xlim(parameters["date initial"],
         parameters["date final"])
plt.ylim(0, 1.4)
plt.yticks([tick/10 for tick in range(0, 16, 2)])
plt.grid(ls="--",
         color="#000000",
         alpha=0.5)
plt.show()
