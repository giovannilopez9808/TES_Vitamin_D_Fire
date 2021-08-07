import matplotlib.pyplot as plt
from Class_list import *


def plot_daily_data(data_davis: pd.DataFrame, data_tuv: pd.DataFrame, date: str):
    """
    Funcion que plotea los datos diarios junto con el cloud factor
    """
    plt.plot(data_davis.index, data_davis["UV"],
             label="Davis")
    plt.plot(data_tuv.index, data_tuv["UVI"],
             label="TUV")
    ticks, hour_tick = obtain_tick(date)
    plt.xlabel("Time Local (h)")
    plt.ylabel("UV Index")
    plt.xticks(hour_tick, ticks)
    plt.xlim(pd.to_datetime("{} 11:00".format(date)),
             pd.to_datetime("{} 15:00".format(date)))
    plt.ylim(0, 7)
    plt.yticks(np.arange(0, 8))
    plt.grid(ls="--",
             color="#000000",
             alpha=0.5)
    plt.title("Fecha {}".format(date))
    plt.subplots_adjust(top=0.879,
                        bottom=0.121,
                        left=0.097,
                        right=0.963,
                        hspace=0.2,
                        wspace=0.2)
    plt.legend(frameon=False,
               ncol=2)
    plt.tight_layout()
    plt.show()


def obtain_tick(date: str):
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


parameters = {
    "path data": "../Data/",
    "path TUV": "../Results/TUV/",
    "file Davis": "data_Davis.csv",
    "date initial": "2020-08-15",
    "date final": "2020-08-28",
    "dataset": {"AOD": "Binary search",
                "Ozone": "260"}
}
Davis = Davis_data(parameters["path data"],
                   parameters["file Davis"],
                   parameters["date initial"],
                   parameters["date final"])
Davis_daily_data = Davis.data[Davis.data.index.date ==
                              pd.to_datetime(parameters["date initial"])]
ID, _ = obtain_id_and_title_parameters(parameters["dataset"]["Ozone"],
                                       parameters["dataset"]["AOD"])
TUV_file = "{}{}.csv".format(parameters["date initial"],
                             ID)
TUV = TUV_results(parameters["path TUV"],
                  TUV_file)
# Ploteo de los datos diarios
plot_daily_data(Davis_daily_data,
                TUV.data,
                parameters["date initial"])
