from Class_list import *


def read_dates_list(path, file):
    dates = pd.read_csv(path+file)
    dates = [pd.to_datetime(date) for date in dates["Dates"]]
    dates = pd.DataFrame(dates, columns=["Dates"])
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
    "file Dates": "dates_select.txt",
    "file OMI": "data_OMI_OMT03",
    "path input TUV": "../Data/",
    "file input TUV": "dates_data.csv",
    "day initial": "2020-05-11",
    "day final": "2020-09-30",
    "Ozone column": "Ozone"
}
dates = read_dates_list(inputs["path data"],
                        inputs["file Dates"])
OMI = OMI_data(inputs["path data"],
               inputs["file OMI"],
               inputs["day initial"],
               inputs["day final"])
Ozone_data = obtain_ozone_data(OMI,
                               inputs["Ozone column"])
Ozone_data = obtain_data_from_dates(Ozone_data, dates["Dates"])
file_TUV = open(inputs["path input TUV"]+inputs["file input TUV"],
                "w")
file_TUV.write("Date,Ozone\n")
for date in Ozone_data.index:
    ozone_value = Ozone_data[date]
    date = date.date()
    file_TUV.write("{},{:.2f}\n".format(date,
                                        ozone_value))
file_TUV.close()