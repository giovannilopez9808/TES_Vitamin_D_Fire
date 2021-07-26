from os import listdir
import numpy as np


def obtain_doses(hour, data, lim):
    maximum = len(data)
    var = False
    dosis = 0
    n = 0
    while var == False and n < maximum:
        dosis += data[n]*60
        if dosis > lim:
            var = True
        else:
            n += 1
    if n != maximum:
        time = int((hour[n]-hour[0])*60)+1
    else:
        time = ""
    return time


def select_files(parameters={}):
    files = sorted(listdir(parameters["path data"]))
    files = [file for file in files if parameters["which file"] in file]
    return files


parameters = {"path data": "../Results/TUV/",
              "path results": "../Data/",
              "file results": "Doses_time",
              "which file": "Ozone_OMI",
              "Vitamin Doses": 136,
              "1/4 MED": 250/4,
              "1 MED": 250,
              }
files = select_files(parameters)
file_result = open("{}{}_{}.csv".format(parameters["path results"],
                                        parameters["file results"],
                                        parameters["which file"]),
                   "w")
file_result.write("Date,vitamin,1/4 MED,1 MED\n")
for file in files:
    date = file.replace("_{}.csv".format(parameters["which file"]), "")
    hour, uv_list, vitamin_list = np.loadtxt("{}{}".format(parameters["path data"],
                                                           file),
                                             delimiter=",",
                                             skiprows=1,
                                             usecols=[0, 2, 3],
                                             unpack=True)
    time_vitamin = obtain_doses(hour,
                                vitamin_list,
                                parameters["Vitamin Doses"])
    time_med_14 = obtain_doses(hour,
                               uv_list/40,
                               parameters["1/4 MED"])
    time_med_1 = obtain_doses(hour,
                              uv_list/40,
                              parameters["1 MED"])
    file_result.write("{},{},{},{}\n".format(date,
                                             time_vitamin,
                                             time_med_14,
                                             time_med_1))
file_result.close()
