from Class_list import TUV_model
from functions import *
import pandas as pd
import os


def print_header_terminal(date):
    text = "Calculando dia {}".format(date.date())
    print("="*len(text))
    print(text)


def select_dates(data_AOD=pd.DataFrame(), data_ozone=pd.DataFrame(), parameters={}):
    if parameters["which date"] == "Ozone":
        return data_ozone.index
    if parameters["which date"] == "AOD":
        return data_AOD.index


def which_AOD(parameters={}, data=pd.DataFrame(), date=pd.Timestamp(2000, 1, 1)):
    try:
        value = data["AOD"][date]
    except:
        value = 0.3
    dataset = {"0.30": {"Filename": "03",
                        "AOD": 0.30},
               "Binary search": {"Filename": "binary_search",
                                 "AOD": value},
               }
    return dataset[parameters["which AOD"]]


def which_Ozone(parameters={}, data=pd.DataFrame(), date=pd.Timestamp(2000, 1, 1)):
    dataset = {"260": {"Filename": "260",
                       "Ozone": 260},
               "OMI": {"Filename": "OMI",
                       "Ozone": data["Ozone"][date]},
               }
    return dataset[parameters["which ozone"]]


def print_TUV_parameters(ozone, aod):
    print("\tCon los parametros:")
    print("\tAOD = {}".format(aod))
    print("\tOzone = {}".format(ozone))


parameters = {
    "path data": "../Data/",
    "file AOD data": "Dates_AOD.csv",
    "file OMI data": "Ozone_data.csv",
    "path results": "../Results/TUV/",
    "which AOD": "0.30",
    "which ozone": "OMI",
    "which date": "Ozone",
    "hour initial": 11,
    "hour final": 19,
    "max rows": 60}
ozone_data = read_data(parameters["path data"],
                       parameters["file OMI data"])
AOD_data = read_data(parameters["path data"],
                     parameters["file AOD data"])
dates = select_dates(AOD_data,
                     ozone_data,
                     parameters)
for date in dates:
    if date >= pd.to_datetime("2019-12-02"):
        AOD_dataset = which_AOD(parameters,
                                AOD_data,
                                date)
        ozone_dataset = which_Ozone(parameters,
                                    ozone_data,
                                    date)
        print_header_terminal(date)
        file = open("{}{}_{}_{}.csv".format(parameters["path results"],
                                            date.date(),
                                            ozone_dataset["Filename"],
                                            AOD_dataset["Filename"]),
                    "w")
        file.write("Hour,SZA,UVI,Vitamin D\n")
        print_TUV_parameters(ozone_dataset["Ozone"],
                             AOD_dataset["AOD"])
        for hour in range(parameters["hour initial"], parameters["hour final"]):
            TUV = TUV_model(parameters["path results"],
                            date,
                            ozone_dataset["Ozone"],
                            AOD_dataset["AOD"],
                            hour,
                            hour+1,
                            parameters["max rows"])
            TUV.run()
            for TUV_hour, TUV_sza, TUV_uvi, TUV_vitamin in zip(TUV.hours, TUV.sza, TUV.uvi, TUV.vitamin):
                file.write("{},{},{},{}\n".format(TUV_hour,
                                                  TUV_sza,
                                                  TUV_uvi,
                                                  TUV_vitamin))
        file.close()
os.system("rm {}*.txt".format(parameters["path results"]))
print("\n")
