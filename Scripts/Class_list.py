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
    Clase que ejecuta el modelo TUV dados el ozono,
    hora inicial, final, aod y fecha
    """

    def __init__(self, path, date, ozone, aod, hour_i, hour_f):
        self.hour_i = hour_i
        self.hour_f = hour_f
        self.ozone = ozone
        self.date = date
        self.path = path
        self.aod = aod
        self.obtain_yymmdd_from_date()

    def obtain_yymmdd_from_date(self):
        """
        Obtiene el nombre de salida, año, mes y día a partir de la fecha
        """
        self.outfile, self.year, self.month, self.day = date_to_yymmdd(
            self.date)

    def run(self):
        """
        Ejecucion del modelo TUv
        """
        self.create_TUV_input()
        os.system("./TUV_model/tuv_rosario.out")
        self.read_results()

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

    def read_results(self):
        """
        Lectura de los datos del TUV
        """
        skiprows = 132
        self.hours, self.data = np.loadtxt("{}{}.txt".format(self.path,
                                                             self.outfile),
                                           skiprows=skiprows,
                                           max_rows=12,
                                           usecols=[0, 2],
                                           unpack=True)


class Search_AOD:
    def __init__(self, path, hours, ozone, date, aod_i, aod_f, RD, delta_RD, data):
        self.delta_RD = delta_RD
        self.ozone = ozone
        self.aod_i = aod_i
        self.aod_f = aod_f
        self.hours = hours
        self.date = date
        self.path = path
        self.data = data
        self.RD = RD

    def run(self):
        run, attempt = self.initialize_search()
        self.print_header_results()
        data_max = self.data.max()
        while run:
            self.obtain_aod()
            TUV_model_results = self.run_for_all_hours()
            TUV_max = round(TUV_model_results.max(), 1)
            RD = calculate_RD(data_max,
                              TUV_max)
            attempt += 1
            self.print_date_results(RD,
                                    self.aod,
                                    data_max,
                                    TUV_max)
            run = self.aod_binary_search(RD,
                                         run)
            run = self.excess_of_attempts(attempt,
                                          run)

    def initialize_search(self):
        """
        Inicialización de los valores iniciales en el algoritmo de 
        busqueda
        """
        self.aod_i_n = self.aod_i
        self.aod_f_n = self.aod_f
        run = True
        attempt = 0
        return run, attempt

    def run_for_all_hours(self):
        TUV_model_results = np.array([])
        for hour in self.hours:
            hour_i = hour
            hour_f = hour+1
            TUV_model_script = TUV_model(self.path,
                                         self.date,
                                         self.ozone,
                                         self.aod,
                                         hour_i,
                                         hour_f)
            TUV_model_script.run()
            TUV_model_results = np.append(TUV_model_results,
                                          TUV_model_script.data)
        return TUV_model_results

    def aod_binary_search(self, RD, run):
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
        return run

    def obtain_aod(self):
        """
        Calculo del AOD con el que se ejecutara el modelo TUV
        """
        self.aod = (self.aod_i_n+self.aod_f_n)/2

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
                                        "Data",
                                        "TUV"))

    def print_date_results(self, RD, AOD, measurement, data):
        """
        Escritura de los resultados en la terminal
        """
        print("\t{:.2f}\t{:.3f}\t{:.2f}\t{:.2f}".format(RD,
                                                        AOD,
                                                        measurement,
                                                        data))


class Write_Results:
    def __init__(self, path):
        self.path = path
        self.path_file = path.replace("TUV/", "")
        self.write_AOD_results
        self.write_Header_Results_file()

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
