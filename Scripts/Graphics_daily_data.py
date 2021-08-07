import matplotlib.pyplot as plt
from Class_list import *


def plot_daily_data(data_davis: pd.DataFrame, data_tuv: pd.DataFrame, parameters: dict):
    """
    Funcion que plotea los datos junto con los resultados del TUV
    """
    plt.subplots(figsize=(8, 5))
    plt.plot(data_davis.index, data_davis["UV"],
             label="UVI medido por estación meteológica",
             color="#0077b6",
             lw=2)
    plt.plot(data_tuv.index, data_tuv["UVI"],
             label="UVI calculado por el modelo TUV",
             color="#008000",
             lw=2)
    ticks, hour_tick = obtain_tick(parameters["date initial"])
    plt.xlabel("Hora local (h)",
               fontsize=parameters["fontsize"])
    plt.ylabel("UVI",
               fontsize=parameters["fontsize"])
    plt.xticks(ticks, hour_tick,
               fontsize=parameters["fontsize"])
    plt.xlim(pd.to_datetime("{} 12:00".format(parameters["date initial"])),
             pd.to_datetime("{} 14:00".format(parameters["date initial"])))
    plt.ylim(2, 5)
    plt.yticks(np.arange(2, 5.5, 0.5),
               fontsize=parameters["fontsize"])
    plt.grid(ls="--",
             color="#000000",
             alpha=0.5)
    plt.title("Fecha {}".format(parameters["date initial"]),
              fontsize=parameters["fontsize"])
    plt.subplots_adjust(top=0.879,
                        bottom=0.121,
                        left=0.097,
                        right=0.963,
                        hspace=0.2,
                        wspace=0.2)
    plt.legend(frameon=False,
               loc="lower center",
               fontsize=parameters["fontsize"])
    plt.tight_layout()
    plt.savefig("{}{}".format(parameters["path graphics"],
                              parameters["graphics name"]))


def obtain_tick(date: str):
    """
    Obtener las etiquetas en el eje x de acuerdo a la hora
    """
    # Hora inicial
    hour_i = 7
    # Hora final
    hour_f = 19
    # Lista con los labels en el formato datetime
    hour_tick = []
    # Lista con las labels de las horas
    ticks = []
    for hour in range(hour_i,
                      hour_f):
        # Hora
        hour_str = str(hour).zfill(2)
        for minute in [0, 15, 30, 45]:
            minute_str = str(minute).zfill(2)
            # Formato de datetime
            date_str = "{} {}:{}".format(date,
                                         hour_str,
                                         minute_str)
            date_with_time = pd.to_datetime(date_str)
            ticks.append(date_with_time)
            time = date_with_time.strftime("%H:%M")
            hour_tick.append(time)
    return ticks, hour_tick


parameters = {
    "path data": "../Data/",
    "path TUV": "../Results/TUV/",
    "path graphics": "../Graphics/",
    "graphics name": "daily_data.png",
    "file Davis": "data_Davis.csv",
    "date initial": "2020-08-15",
    "date final": "2020-08-28",
    "fontsize": 13,
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
                parameters)
