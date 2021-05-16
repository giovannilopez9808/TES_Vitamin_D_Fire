from Class_list import *


def date_format(data):
    data.index = pd.to_datetime(data["Date"])
    data = data.drop("Date", 1)
    return data


def obtain_data_per_day(data, date):
    data = data[data.index.date == date]
    return data


def obtain_data_into_hours(data, hour_i, hour_f):
    data = data[data.index.hour >= hour_i]
    data = data[data.index.hour < hour_f]
    return data


inputs = {
    "path data": "../Data/",
    "file data": "dates_data.csv",
    "file Davis": "data_Davis.csv",
    "path results": "../Results/TUV/",
    "day initial": "2020-05-11",
    "day final": "2020-09-30",
    "hour initial": 9,
    "hour final": 10,
    "RD limit": 10,
    "RD delta": 1,
    "AOD initial": 0,
    "AOD final": 1,
}
Davis = Davis_data(inputs["path data"],
                   inputs["file Davis"],
                   inputs["day initial"],
                   inputs["day final"])
data_TUV = pd.read_csv(inputs["path data"]+inputs["file data"])
data_TUV = date_format(data_TUV)
Results = TUV_Results(inputs["path results"])
for date in data_TUV.index:
    data = obtain_data_per_day(Davis.data["UV"],
                               date)
    data = obtain_data_into_hours(data,
                                  inputs["hour initial"],
                                  inputs["hour final"])
    TUV = TUV_model(date,
                    data_TUV["Ozone"][date],
                    data,
                    inputs["AOD initial"],
                    inputs["AOD final"],
                    inputs["RD limit"],
                    inputs["RD delta"],
                    Results)
    TUV.run()
