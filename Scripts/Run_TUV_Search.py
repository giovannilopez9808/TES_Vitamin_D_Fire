from Class_list import *


def read_data(isdavis, inputs):
    if isdavis:
        data = Davis_data(inputs["path data"],
                          inputs["file Davis"],
                          inputs["day initial"],
                          inputs["day final"])
    else:
        data = pd.read_csv("{}{}".format(inputs["path data"],
                                         inputs["file measurements"]))
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


def obtain_data(isdavis, data, inputs):
    if isdavis:
        data = obtain_data_per_day(data.data["UV"],
                                   date)
        data = obtain_data_into_hours(data,
                                      inputs["hour initial"],
                                      inputs["hour final"])
    else:
        data = data["Maximum"][date]
    return data


inputs = {
    "path data": "../Data/",
    "file data": "dates_data.csv",
    "file Davis": "data_Davis.csv",
    "file measurements": "dates_Maximum.csv",
    "path results": "../Results/TUV/",
    "day initial": "2020-06-25",
    "day final": "2020-09-30",
    "hour initial": 9,
    "hour final": 16,
    "RD limit": 10,
    "RD delta": 1,
    "AOD initial": 0,
    "AOD final": 0.6,
    "source data": "Davis",
}
if inputs["source data"] == "Davis":
    isdavis = True
else:
    isdavis = False
data = read_data(isdavis,
                 inputs)
data_TUV = pd.read_csv("{}{}".format(inputs["path data"],
                                     inputs["file data"]))
data_TUV = date_format(data_TUV)
hours = [hour for hour in range(inputs["hour initial"], inputs["hour final"])]
for date in data_TUV.index:
    print("\n{}\n".format("="*50))
    print("Analizando fecha {}".format(date.date()))
    data_date = obtain_data(isdavis,
                            data,
                            inputs)
    Search_script = Search_AOD(inputs["path results"],
                               hours,
                               data_TUV["Ozone"][date],
                               date,
                               inputs["AOD initial"],
                               inputs["AOD final"],
                               inputs["RD limit"],
                               inputs["RD delta"],
                               data_date)
    Search_script.run()
print("="*50)
