from Class_list import *


def read_TUV_input(parameters={}):
    data = pd.read_csv("{}{}".format(parameters["path data"],
                                     parameters["file data"]))
    data = date_format(data)
    return data


def date_format(data):
    data.index = pd.to_datetime(data["Date"])
    data = data.drop("Date", 1)
    return data


def obtain_data(data, parameters, date):
    data = obtain_data_per_day(data.data["UV"],
                               date)
    data = obtain_data_into_hours(data,
                                  parameters["hour initial"],
                                  parameters["hour final"])
    return data


def obtain_data_per_day(data, date):
    data = data[data.index.date == date]
    return data


def obtain_data_into_hours(data, hour_i, hour_f):
    data = data[data.index.hour >= hour_i]
    data = data[data.index.hour < hour_f]
    return data


parameters = {"path data": "../Data/",
              "file data": "TUV_dates_input.csv",
              "file Davis": "data_Davis.csv",
              "path results": "../Results/TUV/",
              "day initial": "2020-05-01",
              "day final": "2020-09-30",
              "Attempt limit": 15,
              "hour initial": 9,
              "hour final": 16,
              "AOD initial": 0,
              "AOD final": 4,
              "source data": "Davis",
              }
TUV_data_input = read_TUV_input(parameters)
data = Davis_data(parameters["path data"],
                  parameters["file Davis"],
                  parameters["day initial"],
                  parameters["day final"])
hours = [hour for hour in range(parameters["hour initial"],
                                parameters["hour final"])]
write_file = Write_Results(parameters["path results"])
for date in TUV_data_input.index:
    print("\n{}\n".format("="*50))
    print("Analizando fecha {}".format(date.date()))
    data_date = obtain_data(data,
                            parameters,
                            date)
    Search_script = Search_AOD(parameters["path results"],
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
print("="*50)
