import matplotlib.pyplot as plt
import pandas as pd
import os


def select_data_from_date_period(data: pd.DataFrame, day_initial: str, day_final: str):
    """
    Selecciona los datos que se encuentren en un periodo de tiempo
    """
    data = data[data.index >= day_initial]
    data = data[data.index <= day_final]
    return data


def date_to_yymmdd(date: pd.Timestamp):
    """
    Convierte una fecha con formato yyyy-mm-dd a yymmdd
    """
    year = str(date.year)[2:4]
    month = str(date.month).zfill(2)
    day = str(date.day).zfill(2)
    date = year+month+day
    return date, year, month, day


def calculate_RD(measurement: float, model: float):
    """
    Calcula la diferencia relativa entre dos cantidades
    """
    RD = (model-measurement)*100/measurement
    return RD


def obtain_xticks(dates: list):
    """
    Crea una lista con el primer día del mes a partir de una lista que contiene los dias de los datos
    """
    months = [obtain_first_date_for_month(dates[0])]
    for date in dates:
        if months[-1].month != date.month:
            date = obtain_first_date_for_month(date)
            months.append(date)
    year = months[-1].year
    month = months[-1].month+1
    if month > 12:
        month = 1
        year += 1
    date = pd.to_datetime("{}-{}-01".format(year,
                                            str(month).zfill(2)))
    months.append(date)
    months_names = obtain_month_names(months)
    return months, months_names


def obtain_first_date_for_month(date: pd.Timestamp):
    """
    Obtiene el primer dia del mes a partir de una fecha dada
    """
    year = date.year
    month = date.month
    date = pd.to_datetime("{}-{}-01".format(year,
                                            str(month).zfill(2)))
    return date


def obtain_month_names(dates: list):
    """
    Obtiene los nombres de los meses contenidos en una lista de fechas
    """
    months_names = []
    for date in dates:
        months_names.append(date.strftime("%b"))
    return months_names


def read_data(path: str, file: str):
    """
    Lectura de datos donde la columna de las fechas lleva de nombre Date
    """
    data = pd.read_csv("{}{}".format(path,
                                     file))
    data = format_data(data)
    return data


def format_data(data: pd.DataFrame):
    """
    Formato de la columna de Date en formato `pd.Timestamp`
    """
    data.index = pd.to_datetime(data["Date"])
    data = data.drop(columns="Date")
    return data


def select_dataset_AOD(id_dataset: str):
    """
    Selecciona los parametros de nombre del archivo y titulo de los datos de AOD
    """
    dataset = {"0.30": {"Filename": "03",
                        "title": "AOD=0.30"},
               "Binary search": {"Filename": "binary_search",
                                 "title": "AOD=BS"},
               }
    return dataset[id_dataset]


def select_dataset_Ozone(id_dataset: str):
    """
    Selecciona los parametros de nombre del archivo y titulo de los datos de Ozono
    """
    dataset = {"260": {"Filename": "260",
                       "title": "Ozone=260 DU"},
               "OMI": {"Filename": "OMI",
                       "title": "Ozone=OMI"},
               }
    return dataset[id_dataset]


def obtain_id_and_title_parameters(id_Ozone: str, id_AOD: str):
    """
    Obtiene el ID y el titulo dependiendo de los parametros de ozono y AOD
    """
    AOD_dataset = select_dataset_AOD(id_AOD)
    Ozone_dataset = select_dataset_Ozone(id_Ozone)
    # Define ID
    ID = "_{}_{}".format(Ozone_dataset["Filename"],
                         AOD_dataset["Filename"])
    title = "{} {}".format(Ozone_dataset["title"],
                           AOD_dataset["title"])
    return ID, title


def obtain_files_for_dataset_and_ID(parameters: dict, dataset: dict):
    """
    Obtiene la lista de archivos dependiendo de los parametros de AOD y ozono seleccionados
    """
    files = sorted(os.listdir(parameters["path data"]))
    # AOD dataset
    AOD_dataset = select_dataset_AOD(dataset["AOD"])
    # Ozone dataset
    Ozone_dataset = select_dataset_Ozone(dataset["Ozone"])
    # ID de los datosas
    ID = "_{}_{}".format(Ozone_dataset["Filename"],
                         AOD_dataset["Filename"])
    # Filtrado de los archivos
    files = [file for file in files if ID in file]
    return files, ID


def plot_xgrid(months: list, ylimit: float):
    """
    Grafica el xgrid a a partir de una lista de primeros dias del mes y cuanto debe de dejar entre pestañas. Añade una linea cada día 15 de mes
    """
    for month in months:
        grid([month, month],
             [0, ylimit])
        year = month.year
        month = str(month.month).zfill(2)
        date = pd.to_datetime("{}-{}-15".format(year,
                                                month))
        grid([date, date],
             [0, ylimit])


def plot_ygrid(parameters: dict):
    """
    Grafica el ygrid a partir de parametros que definen la extension del grafico
    """
    ylabels = []
    dates = [pd.to_datetime(parameters["date initial"]),
             pd.to_datetime(parameters["date final"])]
    yticks = range(parameters["y limit"]+1)
    for ytick in range(parameters["y limit"]+1):
        if ytick % parameters["y delta"] == 0:
            grid(dates,
                 [ytick, ytick])
        else:
            ytick = ""
        ylabels.append(ytick)
    plt.yticks(yticks, ylabels,
               fontsize=parameters["fontsize"])


def grid(x: list, y: list):
    """
    Ploteo de cada linea del grid
    """
    plt.plot(x, y,
             ls="--",
             color="grey",
             alpha=0.5)
