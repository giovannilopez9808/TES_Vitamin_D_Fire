from functions import *
from os import listdir
import numpy as np


def obtain_solar_noon_hour(data: list):
    return np.where(data == np.max(data))[0][0]


def obtain_doses(hour: list, data: list, lim: float, n: int):
    """
    Obtiene el tiempo de exposición solar en base a la dosis y los valores de irradiancia
    """
    maximum = len(data)
    var = True
    dosis = 0
    hour_initial = hour[n]
    while var and n < maximum:
        dosis += data[n]*60
        if dosis > lim:
            var = False
        else:
            n += 1
    if n != maximum:
        time = (hour[n]-hour_initial)*60+1
    else:
        time = ""
    return time


parameters = {"path data": "../Results/TUV/",
              "path results": "../Data/",
              "file results": "Doses_time",
              "dataset": {"AOD": "Binary search",
                          "Ozone": "260"},
              "Vitamin Doses": 136,
              "1/4 MED": 250/4,
              "1 MED": 250}
files, ID = obtain_files_for_dataset_and_ID(parameters,
                                            parameters["dataset"])
file_result = open("{}{}{}.csv".format(parameters["path results"],
                                       parameters["file results"],
                                       ID),
                   "w")
file_result.write("Date,vitamin,1/4 MED,1 MED\n")
hours_initial = []
for file in files:
    date = file.replace("{}.csv".format(ID), "")
    hour, uv_list, vitamin_list = np.loadtxt("{}{}".format(parameters["path data"],
                                                           file),
                                             delimiter=",",
                                             skiprows=1,
                                             usecols=[0, 2, 3],
                                             unpack=True)
    hour_initial = obtain_solar_noon_hour(uv_list)
    hours_initial.append(hour[hour_initial])
    time_vitamin = obtain_doses(hour,
                                vitamin_list,
                                parameters["Vitamin Doses"],
                                hour_initial)
    time_med_14 = obtain_doses(hour,
                               uv_list/40,
                               parameters["1/4 MED"],
                               hour_initial)
    time_med_1 = obtain_doses(hour,
                              uv_list/40,
                              parameters["1 MED"],
                              hour_initial)
    file_result.write("{},{:.0f},{:.0f},{:.0f}\n".format(date,
                                                         time_vitamin,
                                                         time_med_14,
                                                         time_med_1))
file_result.close()
print("✅ Se ha creado el archivo {}{}.csv".format(parameters["file results"],
                                                  ID))
