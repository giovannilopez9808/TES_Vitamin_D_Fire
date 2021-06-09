import matplotlib.pyplot as plt
from Class_list import *


def obtain_daily_mean(data):
    """
    Funcion que obtiene el promedio diario
    """
    daily_mean = data.resample("D").mean()
    return daily_mean


def read_dates_select(path, name):
    return pd.read_csv("{}{}".format(path, name))


def select_only_in_the_period(data, date_i, date_f):
    data = data[data["Dates"] >= date_i]
    data = data[data["Dates"] <= date_f]
    return data


def plot_daily_data(data, date, cloud_factor):
    """
    Funcion que plotea los datos diarios junto con el cloud factor
    """
    plt.plot(data)
    ticks, hour_tick = obtain_tick(date)
    plt.xlabel("Time Local (h)")
    plt.ylabel("UV Index")
    plt.xticks(hour_tick, ticks)
    plt.xlim(pd.to_datetime("{} 07:00".format(date)),
             pd.to_datetime("{} 19:00".format(date)))
    plt.ylim(0, 14)
    plt.yticks(np.arange(0, 15))
    plt.grid(ls="--",
             color="#000000",
             alpha=0.5)
    plt.title("Date {}\n Cloud factor {:.3f}".format(date,
                                                     cloud_factor))
    plt.subplots_adjust(top=0.879,
                        bottom=0.121,
                        left=0.097,
                        right=0.963,
                        hspace=0.2,
                        wspace=0.2)
    plt.show()


def obtain_tick(date):
    """
    Obtener las etiquetas en el eje x de acuerdo a la hora
    """
    # Hora inicial
    hour_i = 7
    # Hora final
    hour_f = 20
    # Lista con los labels en el formato datetime
    hour_tick = []
    # Lista con las labels de las horas
    ticks = []
    for hour in range(hour_i,
                      hour_f):
        # Hora
        ticks.append(hour)
        hour = str(hour).zfill(2)
        # Formato de datetime
        hour_tick.append(pd.to_datetime("{} {}:00".format(date,
                                                          hour)))
    return ticks, hour_tick


inputs = {
    "Dates clear sky": "dates_select.dat",
    "path data": "../Data/",
    "file Davis": "data_Davis.csv",
    "file OMI": "data_OMI_OMT03",
    "day initial": "2020-08-01",
    "day final": "2020-09-30",
    "Cloud factor column": "Cld. F."
}
Davis = Davis_data(inputs["path data"],
                   inputs["file Davis"],
                   inputs["day initial"],
                   inputs["day final"])
OMI = OMI_data(inputs["path data"],
               inputs["file OMI"],
               inputs["day initial"],
               inputs["day final"])
dates_select = read_dates_select(inputs["path data"],
                                 inputs["Dates clear sky"])
dates_select = select_only_in_the_period(dates_select,
                                         inputs["day initial"],
                                         inputs["day final"])
print(dates_select)
# Obtiene el promedio diario de Cloud Factor
Cf_data = obtain_daily_mean(OMI.data[inputs["Cloud factor column"]])
for date in dates_select["Dates"]:
    # Valor diario del cloud factor
    Cf_value = Cf_data[date]
    # Lista de los datos diarios UVI para una fecha
    daily_data = Davis.data[Davis.data.index.date == pd.to_datetime(date)]
    # Ploteo de los datos diarios
    plot_daily_data(daily_data,
                    date,
                    Cf_value)
