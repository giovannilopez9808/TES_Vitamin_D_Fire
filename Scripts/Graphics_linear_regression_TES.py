import matplotlib.pyplot as plt
from numpy import array, polyfit
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


def obtain_linear_regression(data1=pd.DataFrame(), data2=pd.DataFrame(), parameters={}):
    dates = data1.index
    data1 = array(data1[parameters["dataset doses"]])
    data2 = array(data2[parameters["dataset doses"]])
    fit = polyfit(data1, data2, 1)
    data = {"Smoke": data1,
            "Clear sky": data2,
            }
    data = pd.DataFrame(data, index=dates)
    return data, fit


def obtain_line(parameters={}, fit=[]):
    line = []
    for x in parameters["x limit"]:
        point = fit[0]*x+fit[1]
        line.append(point)
    return line


def print_equation_from_fit(fit=[]):
    if fit[1] > 0:
        sign = "+"
    else:
        sign = "-"
    equation = "y={:.4f}x{}{:.4f}".format(fit[0],
                                          sign,
                                          abs(fit[1]))
    print("La ecuación de la regresión lineal es\n{}".format(equation))


def obtain_ticks(limits: list, delta: float):
    ticks = []
    for tick in range(limits[0], limits[1]+delta, delta):
        ticks.append(tick)
    return ticks


parameters = {"path data": "../Data/",
              "path graphics": "../Graphics/",
              "file data": "Doses_time",
              "graphics name": "linear_regression_TES.png",
              "date initial": "2020-06-01",
              "date final": "2020-09-01",
              "dataset doses": "1/4 MED",
              "x limit": [16, 32],
              "x delta": 2,
              "y limit": [10, 30],
              "y delta": 2,
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

data, fit = obtain_linear_regression(data1,
                                     data2,
                                     parameters)
line = obtain_line(parameters,
                   fit)
print_equation_from_fit(fit)
plt.subplots(figsize=(10, 6))
plt.scatter(data["Smoke"], data["Clear sky"],
            c="#b5179e",
            label="TES",
            s=20)
plt.plot(parameters["x limit"], line,
         label="Regresión lineal",
         color="#3a0ca3",
         lw=2)
plt.xlim(parameters["x limit"][0],
         parameters["x limit"][1])
plt.xlabel("TES con presencia de humo (min)",
           fontsize=parameters["fontsize"])
plt.xticks(obtain_ticks(parameters["x limit"],
                        parameters["x delta"]))
plt.ylim(parameters["y limit"][0],
         parameters["y limit"][1])
plt.ylabel("TES en condiciones típicas (min)",
           fontsize=parameters["fontsize"])
plt.yticks(obtain_ticks(parameters["y limit"],
                        parameters["y delta"]))
plt.legend(frameon=False,
           loc="upper left",
           fontsize=parameters["fontsize"]+1)
plt.grid(ls="--",
         color="#000000",
         alpha=0.5)
plt.subplots_adjust(top=0.956,
                    bottom=0.132,
                    left=0.106,
                    right=0.958,
                    hspace=0.248,
                    wspace=0.2)
plt.tight_layout()
plt.savefig("{}{}".format(parameters["path graphics"],
                          parameters["graphics name"]),
            dpi=400)
