from os import listdir
import numpy as np
import datetime


def obtain_doses(hour, data, lim):
    var = False
    n = 0
    dosis = 0
    while var == False:
        dosis += data[n]*60
        if dosis > lim:
            var = True
        else:
            n += 1
    time = str(int((hour[n]-hour[0])*60)+1)
    return time


def obtain_date(file=""):
    date = file.replace(".csv", "")
    year = date[0:2]
    month = date[2:4]
    day = date[4:6]
    date = "{}-{}-{}".format(year,
                             month,
                             day)
    return date


parameters = {"path data": "../Results/TUV/",
              "path results": "../Data/",
              "Vitamin Doses": 136,
              "MED": 250,
              }
files = np.sort(listdir(parameters["path data"]))
file_result = open("{}{}".format(parameters["path results"],
                                 "time_doses.csv"),
                   "w")
file_result.write("Date,vitamin,MED\n")
for file in files:
    date = obtain_date(file)
    hour, uv_list, vitamin_list = np.loadtxt("{}{}".format(parameters["path data"],
                                                           file),
                                             delimiter=",",
                                             skiprows=1,
                                             unpack=True)
    time_vitamin = obtain_doses(hour,
                                vitamin_list,
                                parameters["Vitamin Doses"])
    time_med = obtain_doses(hour,
                            uv_list/40,
                            parameters["MED"])
    file_result.write("{},{},{}\n".format(date,
                                          time_vitamin,
                                          time_med))
file_result.close()
