from functions import *
import pandas as pd
pd.options.mode.chained_assignment = None


class Davis_data:
    def __init__(self, path_data, file_name, day_initial, day_final):
        """
        Lectura de los datos de Davis recompilados.
        Información de parametros:
        path_data -------> Direccion donde se encuetran los datos
        file_name -------> Nombre del archivo que contiene los datos
        day_initial -----> Dia inicial del perido de analisis
        day_final -------> Dia final del perido de analisis
        """
        self.path_data = path_data
        self.file_name = file_name
        self.day_initial = pd.to_datetime(day_initial)
        self.day_final = pd.to_datetime(day_final)
        self.read_data()

    def read_data(self):
        """
        Funcion que realiza la lectura de los datos y aplica el formato 
        a las fechas
        """
        self.data = pd.read_csv("{}{}".format(self.path_data,
                                              self.file_name),
                                low_memory=False)
        # Formateo de fechas
        self.format_data_date()
        # Eliminacion de columnas que no son el UV
        self.obtain_only_UV_data()
        # Corte de los datos por el perido de las fechas
        self.cut_data_from_dates()

    def format_data_date(self):
        """
        Funcion que realiza el formato de fechas a los datos
        """
        self.data["Date"] = pd.to_datetime(self.data["Date"],
                                           format="%d/%m/%y")
        self.data["Hour"] = self.data["Hour"].astype(str).str.zfill(5)
        self.data["Date"] = self.data["Date"].astype(
            str)+" "+self.data["Hour"]
        self.data.index = pd.to_datetime(self.data["Date"])
        self.data = self.data.drop(["Date", "Hour"], 1)

    def obtain_only_UV_data(self):
        """
        Funcion que elimina todas las columnas excepto la del UV
        """
        columns = list(self.data.columns)
        columns.remove("UV")
        self.data = self.data.drop(columns, 1)

    def cut_data_from_dates(self):
        """
        Funcion que corta los datos en un periodo
        """
        self.data = cut_data_from_date_period(self.data,
                                              self.day_initial,
                                              self.day_final)


class OMI_data:
    def __init__(self, path_data, file_name, day_initial, day_final):
        """
        Lectura de los datos de OMI recompilados.
        Información de parametros:
        path_data -------> Direccion donde se encuetran los datos
        file_name -------> Nombre del archivo que contiene los datos
        day_initial -----> Dia inicial del perido de analisis
        day_final -------> Dia final del perido de analisis
        """
        self.path_data = path_data
        self.file_name = file_name
        self.day_initial = pd.to_datetime(day_initial)
        self.day_final = pd.to_datetime(day_final)
        self.read_data()

    def read_data(self):
        """
        Funcion que realiza la lectura de los datos y aplica el formato 
        a las fechas
        """
        self.data = pd.read_fwf("{}{}.dat".format(self.path_data,
                                                  self.file_name),
                                skiprows=27)
        self.date_format()
        self.cut_data_from_dates()

    def date_format(self):
        """
        Funcion que realiza el formato de fechas a los datos
        """
        self.data["Date"] = self.data["Datetime"].str[0:4]+"-" + \
            self.data["Datetime"].str[4:6]+"-"+self.data["Datetime"].str[6:8]
        self.data["Date"] = pd.to_datetime(self.data["Date"])
        self.data.index = self.data["Date"]
        self.data = self.data.drop(["Date", "Datetime"], 1)

    def cut_data_from_dates(self):
        """
        Funcion que corta los datos en un periodo
        """
        self.data = cut_data_from_date_period(self.data,
                                              self.day_initial,
                                              self.day_final)
