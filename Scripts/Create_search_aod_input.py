from Class_list import *


def read_dates_list(path, file):
    dates = pd.read_csv("{}{}".format(path,
                                      file))
    dates.index = pd.to_datetime(dates["Date"])
    dates = dates.drop("Date", 1)
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


parameters = {"path data": "../Data/",
              "file Dates": "dates_select.dat",
              "file OMI": "data_OMI_OMT03",
              "path input TUV": "../Data/",
              "file input TUV": "Search_AOD_input.csv",
              "day initial": "2020-05-11",
              "day final": "2020-09-30",
              "Ozone column": "Ozone",
              "Use OMI Ozone": True,
              "Ozone value": 260,
              }
data_input = read_dates_list(parameters["path data"],
                             parameters["file Dates"])
OMI = OMI_data(parameters["path data"],
               parameters["file OMI"],
               parameters["day initial"],
               parameters["day final"])
Ozone_data = obtain_ozone_data(OMI,
                               parameters["Ozone column"])
Ozone_data = obtain_data_from_dates(Ozone_data,
                                    data_input.index)
file_TUV = open("{}{}".format(parameters["path input TUV"],
                              parameters["file input TUV"]),
                "w")
file_TUV.write("Date,Ozone,RD,Delta\n")
for date in data_input.index:
    try:
        if parameters["Use OMI Ozone"]:
            ozone_value = Ozone_data[date]
        else:
            ozone_value = parameters["Ozone value"]
    except:
        ozone_value = parameters["Ozone value"]
    file_TUV.write("{},{:.2f},{},{}\n".format(date.date(),
                                              ozone_value,
                                              data_input["RD"][date],
                                              data_input["Delta"][date]))
file_TUV.close()
