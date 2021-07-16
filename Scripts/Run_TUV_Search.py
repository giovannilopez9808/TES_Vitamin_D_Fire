from Class_list import *


def read_data(isdavis, parameters):
    if isdavis:
        data = Davis_data(parameters["path data"],
                          parameters["file Davis"],
                          parameters["day initial"],
                          parameters["day final"])
    else:
        data = pd.read_csv("{}{}".format(parameters["path data"],
                                         parameters["file measurements"]))
        data = date_format(data)
    return data


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


def obtain_data(isdavis, data, parameters):
    if isdavis:
        data = obtain_data_per_day(data.data["UV"],
                                   date)
        data = obtain_data_into_hours(data,
                                      parameters["hour initial"],
                                      parameters["hour final"])
    else:
        data = data["Maximum"][date]
    return data


def is_davids_data(parameters={}):
    if parameters["source data"] == "Davis":
        return True
    else:
        return False


parameters = {
    "path data": "../Data/",
    "file data": "dates_data.csv",
    "file Davis": "data_Davis.csv",
    "file measurements": "dates_Maximum.csv",
    "path results": "../Results/TUV/",
    "day initial": "2020-05-01",
    "day final": "2020-09-30",
    "Attempt limit": 15,
    "hour initial": 9,
    "hour final": 16,
    "RD limit": 10,
    "RD delta": 1,
    "AOD initial": 0,
    "AOD final": 4,
    "source data": "Davis",
}
isdavis = is_davids_data(parameters)
data = read_data(isdavis,
                 parameters)
data_TUV = pd.read_csv("{}{}".format(parameters["path data"],
                                     parameters["file data"]))
data_TUV = date_format(data_TUV)
hours = [hour for hour in range(parameters["hour initial"],
                                parameters["hour final"])]
write_file = Write_Results(parameters["path results"])
for date in data_TUV.index:
    print("\n{}\n".format("="*50))
    print("Analizando fecha {}".format(date.date()))
    data_date = obtain_data(isdavis,
                            data,
                            parameters)
    Search_script = Search_AOD(parameters["path results"],
                               hours,
                               data_TUV["Ozone"][date],
                               date,
                               parameters["AOD initial"],
                               parameters["AOD final"],
                               parameters["RD limit"],
                               parameters["RD delta"],
                               data_date,
                               parameters["Attempt limit"],
                               write_file)
print("="*50)
