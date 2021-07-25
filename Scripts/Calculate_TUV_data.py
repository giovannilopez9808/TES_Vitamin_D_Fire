from Class_list import TUV_model
import pandas as pd


def read_data(path="", file=""):
    data = pd.read_csv("{}{}".format(path,
                                     file))
    data = format_data(data)
    return data


def format_data(data=pd.DataFrame()):
    data.index = pd.to_datetime(data["Date"])
    data = data.drop("Date", 1)
    return data


def print_header_terminal(date):
    text = "Calculando dia {}".format(date.date())
    print("="*len(text))
    print(text)


def which_AOD(parameters={}, data=pd.DataFrame(), date=pd.Timestamp(2000, 1, 1)):
    try:
        data_AOD = data["AOD"][date]
    except:
        data_AOD = 0.30
    dataset = {"0.30": {"Filename": "clear_sky",
                        "AOD": 0.30},
               "TUV": {"Filename": "binary_search",
                       "AOD": data_AOD},
               "OMI": {"Filename": "Ozone_OMI",
                       "AOD": 0.30}
               }
    return dataset[parameters["which AOD"]]


parameters = {
    # "path data": "../Results/",
    # "file data": "Dates_AOD.csv",
    "path data": "../Data/",
    "file data": "Ozone_data.csv",
    "path results": "../Results/TUV/",
    # "which AOD": "0.30",
    # "which AOD": "TUV",
    "which AOD": "OMI",
    "hour initial": 11,
    "hour final": 19,
    "max rows": 60}
data = read_data(parameters["path data"],
                 parameters["file data"])
for date in data.index:
    dataset = which_AOD(parameters,
                        data,
                        date)
    print_header_terminal(date)
    file = open("{}{}_{}.csv".format(parameters["path results"],
                                     date.date(),
                                     dataset["Filename"]),
                "w")
    file.write("Hour,UVI,Vitamin D\n")
    for hour in range(parameters["hour initial"], parameters["hour final"]):
        TUV = TUV_model(parameters["path results"],
                        date,
                        data["Ozone"][date],
                        dataset["AOD"],
                        hour,
                        hour+1,
                        parameters["max rows"])
        TUV.run()
        for TUV_hour, TUV_uvi, TUV_vitamin in zip(TUV.hours, TUV.uvi, TUV.vitamin):
            file.write("{},{},{}\n".format(TUV_hour,
                                           TUV_uvi,
                                           TUV_vitamin))
    file.close()
print("\n")
