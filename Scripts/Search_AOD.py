from Class_list import *
from functions import *


def obtain_data(data=pd.DataFrame(), parameters={}, date=pd.Timestamp(2000, 1, 1)):
    data = obtain_data_per_day(data.data["UV"],
                               date)
    data = obtain_data_into_hours(data,
                                  parameters["hour initial"],
                                  parameters["hour final"])
    return data


def obtain_data_per_day(data=pd.DataFrame(), date=pd.Timestamp(2000, 1, 1)):
    data = data[data.index.date == date]
    return data


def obtain_data_into_hours(data=pd.DataFrame(), hour_i=0, hour_f=24):
    data = data[data.index.hour >= hour_i]
    data = data[data.index.hour < hour_f]
    return data


parameters = {"path data": "../Data/",
              "file data": "Search_AOD_input.csv",
              "file Davis": "data_Davis.csv",
              "path TUV results": "../Results/TUV/",
              "day initial": "2020-05-01",
              "day final": "2020-09-30",
              "Attempt limit": 15,
              "hour initial": 9,
              "hour final": 16,
              "AOD initial": 0,
              "AOD final": 4,
              "source data": "Davis",
              }
TUV_data_input = read_data(parameters["path data"],
                           parameters["file data"])
data = Davis_data(parameters["path data"],
                  parameters["file Davis"],
                  parameters["day initial"],
                  parameters["day final"])
hours = [hour for hour in range(parameters["hour initial"],
                                parameters["hour final"])]
write_file = Write_Results(parameters["path data"])
for date in TUV_data_input.index:
    data_date = obtain_data(data,
                            parameters,
                            date)
    Search_script = Search_AOD(parameters["path TUV results"],
                               hours,
                               TUV_data_input["Ozone"][date],
                               date,
                               parameters["AOD initial"],
                               parameters["AOD final"],
                               TUV_data_input["RD"][date],
                               TUV_data_input["Delta"][date],
                               data_date,
                               parameters["Attempt limit"],
                               write_file)
os.system("rm {}*.txt".format(parameters["path TUV results"]))
print("="*50)
