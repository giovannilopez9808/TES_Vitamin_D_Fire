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


parameters = {"path data": "../Results/",
              "file data": "Dates_AOD.csv",
              "path results": "../Results/TUV/",
              "hour initial": 7,
              "hour final": 19}
data = read_data(parameters["path data"],
                 parameters["file data"])
for date in data.index:
    print_header_terminal(date)
    file = open("{}{}.csv".format(parameters["path results"],
                                  date.date()),
                "w")
    file.write("Hour,Data\n")
    for hour in range(parameters["hour initial"], parameters["hour final"]):
        TUV = TUV_model(parameters["path results"],
                        date,
                        data["Ozone"][date],
                        data["AOD"][date],
                        hour,
                        hour+1)
        TUV.run()
        for TUV_hour, TUV_value in zip(TUV.hours, TUV.data):
            file.write("{},{}\n".format(TUV_hour,
                                        TUV_value))
    file.close()
print("\n")
