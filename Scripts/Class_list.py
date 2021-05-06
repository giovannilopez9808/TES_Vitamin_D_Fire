import pandas as pd


class Davis_data:
    def __init__(self, path_data, file_name):
        self.path_data = path_data
        self.file_name = file_name
        self.read_data()

    def read_data(self):
        self.data = pd.read_csv("{}{}".format(self.path_data,
                                              self.file_name),
                                delimiter="\t",
                                low_memory=False)
        self.format_data_date()

    def format_data_date(self):
        self.data["Date"] = pd.to_datetime(self.data["Date"],
                                           format="%d/%m/%y")
        self.data["Hour"] = self.data["Hour"].astype(str).str.zfill(5)
        self.data["Date"] = self.data["Date"].astype(
            str)+" "+self.data["Hour"]
        self.data.index = pd.to_datetime(self.data["Date"])
        self.data = self.data.drop(["Date", "Hour"], 1)
