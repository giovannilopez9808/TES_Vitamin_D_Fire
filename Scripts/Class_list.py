from functions import *
import pandas as pd
import numpy as np
import os
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


class TUV_model:
    """
    Clase que realiza la ejecucion del modelo TUV y acopla un AOD
    dada un RD ,una medición y una fecha.
    """

    def __init__(self, date, ozone, data, aod_i, aod_f, RD, delta_RD, results):
        self.delta_RD = delta_RD
        self.results = results
        self.ozone = ozone
        self.aod_i = aod_i
        self.aod_f = aod_f
        self.data = data
        self.date = date
        self.RD = RD
        self.obtain_yymmdd_from_date()

    def obtain_yymmdd_from_date(self):
        """
        Obtiene el nombre de salida, año, mes y día a partir de la fecha
        """
        self.outfile, self.year, self.month, self.day = date_to_yymmdd(
            self.date)

    def run(self):
        """
        Ejecucion del algoritmo de busqueda del AOD con el modelo TUv
        """
        for date in self.data.index:
            self.data_measurement = self.data[date]
            if self.data_measurement != 0:
                print("{}".format(date))
                self.print_header_results()
                run, attempt, print_bool = self.initialize_search()
                self.obtain_hour_and_minute(date)
                while run:
                    self.obtain_aod()
                    self.create_TUV_input()
                    os.system("./TUV_model/tuv_rosario.out")
                    self.results.read_results(self.outfile)
                    RD = calculate_RD(self.data_measurement,
                                      self.results.data[self.minute])
                    run, print_bool = self.aod_binary_search(RD,
                                                             run,
                                                             print_bool)
                    attempt += 1
                    self.print_date_results(RD,
                                            self.aod,
                                            self.data_measurement,
                                            self.results.data[self.minute])
                    run = self.excess_of_attempts(attempt, run)
                self.results.write_AOD_results(date,
                                               self.aod,
                                               RD,
                                               print_bool)

    def initialize_search(self):
        """
        Inicialización de los valores iniciales en el algoritmo de 
        busqueda
        """
        self.aod_i_n = self.aod_i
        self.aod_f_n = self.aod_f
        run = True
        attempt = 0
        print_bool = False
        return run, attempt, print_bool

    def obtain_hour_and_minute(self, date):
        """
        Obtiene la hora inicial y final en la que se ejecutara el modelo
        TUV a partir de la medición. Incluye el minuto en el cual se comparara
        el valor de UVI
        """
        self.hour_i = date.hour  # -15/60
        self.hour_f = self.hour_i+1
        self.minute = date.minute//5

    def aod_binary_search(self, RD, run, print_bool):
        """
        Decision del cambio en los limites de la busqueda del AOD
        dependiendo la RD obtenida.
        """
        if RD > self.RD+self.delta_RD:
            self.aod_i_n = self.aod
        elif RD < self.RD-self.delta_RD:
            self.aod_f_n = self.aod
        else:
            run = False
            print_bool = True
        return run, print_bool

    def obtain_aod(self):
        """
        Calculo del AOD con el que se ejecutara el modelo TUV
        """
        self.aod = (self.aod_i_n+self.aod_f_n)/2

    def create_TUV_input(self):
        """
        Creación del TUV input con el formato
        Outfile Ozone AOD Year Month Day Hour_initial Hour_final
        """
        input_file = open("TUV_input.txt",
                          "w")
        input_file.write("{} {} {} 20{} {} {} {} {}".format(self.outfile,
                                                            self.ozone,
                                                            self.aod,
                                                            self.year,
                                                            self.month,
                                                            self.day,
                                                            self.hour_i,
                                                            self.hour_f))
        input_file.close()

    def excess_of_attempts(self, attempt, run):
        """
        Limite de intentos en el algoritmo de busqueda
        """
        if attempt >= 10:
            run = False
        return run

    def print_header_results(self):
        """
        Escritura de los headers en la terminal
        """
        print("\t{}\t{}\t{}\t{}".format("RD",
                                        "AOD",
                                        "Davis",
                                        "TUV"))

    def print_date_results(self, RD, AOD, measurement, data):
        """
        Escritura de los resultados en la terminal
        """
        print("\t{:.2f}\t{:.3f}\t{:.3f}\t{:.3f}".format(RD,
                                                        AOD,
                                                        measurement,
                                                        data))


class TUV_Results:
    def __init__(self, path):
        self.path = path
        self.path_file = path.replace("TUV/", "")
        self.write_AOD_results
        self.write_Header_Results_file()

    def read_results(self, name):
        skiprows = 132
        self.hours, self.data = np.loadtxt("{}{}.txt".format(self.path,
                                                             name),
                                           skiprows=skiprows,
                                           max_rows=13,
                                           usecols=[0, 2],
                                           unpack=True)

    def write_Header_Results_file(self):
        self.file_results = open("{}{}.csv".format(self.path_file,
                                                   "Dates_AOD"),
                                 "w")
        self.file_results.write("Date,AOD,RD\n")
        self.file_results.close()

    def write_AOD_results(self, date, AOD, RD, print_bool):
        if print_bool:
            self.file_results = open("{}{}.csv".format(self.path_file,
                                                       "Dates_AOD"),
                                     "a")
            self.file_results.write("{},{:.3f},{:.2f}\n".format(date,
                                                                AOD,
                                                                RD))
            self.file_results.close()
