from functions import *
import pandas as pd
import numpy as np
import os
pd.options.mode.chained_assignment = None


class Davis_data:
    def __init__(self, path_data="", file_name="", day_initial="2000-01-01", day_final="2001-01-01"):
        """
        Lectura de los datos de Davis recompilados.

        ### Inputs
        + `path_data` -> Direccion donde se encuetran los datos
        + `file_name` -> Nombre del archivo que contiene los datos
        + `day_initial` -> Dia inicial del perido de analisis
        + `day_final` -> Dia final del perido de analisis
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
    def __init__(self, path_data="", file_name="", day_initial="2000-01-01", day_final="2001-01-01"):
        """
        Lectura de los datos de OMI recompilados.

        ### Inputs
        + `path_data` -> Direccion donde se encuetran los datos
        + `file_name` -> Nombre del archivo que contiene los datos
        + `day_initial` -> Dia inicial del perido de analisis
        + `day_final` -> Dia final del perido de analisis
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
    """
    Algoritmo de busqueda del AOD por medio del modelo TUV

    #### Inputs
    + `path` -> direccion donde se guardaran los resultados 
    + `hours` -> lista con las horas que se obtendran los datos
    + `ozone` -> valor de la columna de ozono en DU
    + `date` -> fecha del analisis con formato pd.Timestamp()
    + `aod_i` -> limite inferior de la busqueda de AOD
    + `aod_f` -> limite superior de la busqueda de AOD
    + `RD` -> RD en el cual se centra la busqueda
    + `delta_RD` -> Ancho de la busquda del AOD
    + `data` -> Dataframe con las mediociones de irradiancia
    + `attempt_limit` -> Limite de intentos en la busqueda
    + `write_results` -> Clase Write_Results que contiene todos los métodos para la escritura
    de los resultados
    """

    def __init__(self, path="", hours=[], ozone=250.02, date=pd.Timestamp(2000, 1, 1), aod_i=0, aod_f=1, RD=10, delta_RD=1, data=pd.DataFrame(), attempt_limit=10, write_results=""):
        self.attempt_limit = attempt_limit
        self.write_results = write_results
        self.delta_RD = delta_RD
        self.ozone = ozone
        self.aod_i = aod_i
        self.aod_f = aod_f
        self.hours = hours
        self.date = date
        self.path = path
        self.data = data
        self.RD = RD
        self.run()

    def run(self):
        """
        Ejecución de la busqueda del AOD
        """
        # Inicializacion de las busqueda
        run, attempt, print_bool = self.initialize_search()
        self.print_header_results()
        # Maximo de los datos
        data_max = self.data.max()
        while run:
            # Calculo del AOD con un promedio
            self.obtain_aod()
            # Resultados del TUV
            TUV_model_results = self.run_TUV_for_all_hours()
            # Valor maximo del modelo TUV
            TUV_max = round(TUV_model_results.max(), 3)
            # Calculo de la RD
            RD = calculate_RD(data_max,
                              TUV_max)
            attempt += 1
            self.print_date_results(RD,
                                    self.aod,
                                    data_max,
                                    TUV_max)
            # Verificación si el RD esta en los limites de busqueda
            run, print_bool = self.aod_binary_search(RD,
                                                     run,
                                                     print_bool)
            # Imprime los resultados
            self.write_results.write_AOD_results(self.date.date(),
                                                 self.ozone,
                                                 self.aod,
                                                 RD,
                                                 print_bool)
            # Se detendra si los intentos superar el limite
            run = self.excess_of_attempts(attempt,
                                          run)

    def initialize_search(self):
        """
        Inicialización de los valores iniciales en el algoritmo de 
        busqueda
        """
        self.aod_i_n = self.aod_i
        self.aod_f_n = self.aod_f
        print_bool = False
        run = True
        attempt = 0
        return run, attempt, print_bool

    def run_TUV_for_all_hours(self):
        """
        Ejecuccion del TUV con los parametros datos
        """
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

    def aod_binary_search(self, RD=10, run=True, print_bool=True):
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

    def excess_of_attempts(self, attempt=1, run=True):
        """
        Limite de intentos en el algoritmo de busqueda
        """
        if attempt >= self.attempt_limit:
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

    def print_date_results(self, RD=10, AOD=0.5, measurement=5, data=3):
        """
        Escritura de los resultados en la terminal
        """
        print("\t{:.2f}\t{:.3f}\t{:.2f}\t{:.2f}".format(RD,
                                                        AOD,
                                                        measurement,
                                                        data))


class Write_Results:
    """
    Contiene los metodos para escribir los resultados de la busqueda del AOD
    """

    def __init__(self, path=""):
        self.path = path
        self.path_file = path.replace("TUV/", "")
        self.write_AOD_results
        self.write_Header_Results_file()

    def write_Header_Results_file(self):
        """
        Escritura del Header de los archivos de resultados
        """
        self.file_results = open("{}{}.csv".format(self.path_file,
                                                   "Dates_AOD"),
                                 "w")
        self.file_results.write("Date,Ozone,AOD,RD\n")
        self.file_results.close()

    def write_AOD_results(self, date=pd.Timestamp(2000, 1, 1), ozone=260.05, AOD=0.5, RD=10, print_bool=True):
        """
        Escritura de los resultados de ls busqueda de AOD
        """
        if print_bool:
            self.file_results = open("{}{}.csv".format(self.path_file,
                                                       "Dates_AOD"),
                                     "a")
            self.file_results.write("{},{:.3f},{:.3f},{:.2f}\n".format(date,
                                                                       ozone,
                                                                       AOD,
                                                                       RD))
        self.file_results.close()
