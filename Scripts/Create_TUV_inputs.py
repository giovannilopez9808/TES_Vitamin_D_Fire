from Class_list import *


def read_dates_list(path, file):
    dates = pd.read_csv(path+file)
    dates = [pd.to_datetime(date) for date in dates["Date"]]
    dates = pd.DataFrame(dates, columns=["Date"])
    dates.index = pd.to_datetime(dates["Date"])
    dates = dates.drop("Date",
                       1)
    return dates


def obtain_ozone_data(OMI, column):
    Ozone_data = OMI.data[column]
    Ozone_data = obtain_daily_mean(Ozone_data)
    return Ozone_data


def obtain_daily_mean(data):
    data = data.resample("D").mean()
    return data


def obtain_data_from_dates(data, dates):
    data = data[dates]
    data = data.dropna()
    return data


inputs = {
    "path data": "../Data/",
    "file Dates": "dates_select.dat",
    "file OMI": "data_OMI_OMT03",
    "path input TUV": "../Data/",
    "file input TUV": "dates_data.csv",
    "day initial": "2020-05-11",
    "day final": "2020-09-30",
    "Ozone column": "Ozone",
    "Use OMI Ozone": False,
    "Ozone value": 260,
}
dates = read_dates_list(inputs["path data"],
                        inputs["file Dates"])
OMI = OMI_data(inputs["path data"],
               inputs["file OMI"],
               inputs["day initial"],
               inputs["day final"])
Ozone_data = obtain_ozone_data(OMI,
                               inputs["Ozone column"])
Ozone_data = obtain_data_from_dates(Ozone_data,
                                    dates.index)
file_TUV = open("{}{}".format(inputs["path input TUV"],
                              inputs["file input TUV"]),
                "w")
file_TUV.write("Date,Ozone\n")
for date in dates.index:
    try:
        if inputs["Use OMI Ozone"]:
            ozone_value = Ozone_data[date]
        else:
            ozone_value = inputs["Ozone value"]
    except:
        ozone_value = inputs["Ozone value"]
    date = date.date()
    file_TUV.write("{},{:.2f}\n".format(date,
                                        ozone_value))
file_TUV.close()
