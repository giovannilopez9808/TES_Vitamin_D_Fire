from Class_list import *


def data_format(data):
    data = date_format(data)
    data["Outname"] = "a"
    data["Year"] = "a"
    data["Month"] = "a"
    data["Day"] = "a"
    return data


def date_format(data):
    data.index = pd.to_datetime(data["Date"])
    data = data.drop("Date", 1)
    return data


def apply_date_to_yymmdd(data):
    for index in data.index:
        date = index.date()
        outname, year, month, day = date_to_yymmdd(date)
        data["Outname"][index] = outname
        data["Year"][index] = year
        data["Month"][index] = month
        data["Day"][index] = day
    return data


def date_to_yymmdd(date):
    year = str(date.year)[2:4]
    month = str(date.month).zfill(2)
    day = str(date.day).zfill(2)
    date = year+month+day
    return date, year, month, day


inputs = {
    "path data": "../Data/",
    "file data": "dates_data.csv",
    "file Davis": "data_Davis.csv",
    "day initial": "2020-05-11",
    "day final": "2020-09-30",
    "AOD initial": 0,
    "AOD final": 1,
}
Davis = Davis_data(inputs["path data"],
                   inputs["file Davis"],
                   inputs["day initial"],
                   inputs["day final"])
Davis.data["Erythemal"] = Davis.data["UV"]/40
data_TUV = pd.read_csv(inputs["path data"]+inputs["file data"])
data_TUV = data_format(data_TUV)
data_TUV = apply_date_to_yymmdd(data_TUV)
print(data_TUV)
