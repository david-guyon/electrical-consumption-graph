import time
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

peak_price = 0.1683
off_peak_price = 0.1683

def generate_graph():
    dates = []
    peak_consumptions = []
    off_peak_consumptions = []

    # get data from DATA file
    with open('DATA', 'r') as data_file:
        data_file.readline()  # ignore first line
        for line in data_file:
            date, peak_consumption, off_peak_consumption = line.split()
            dates.append(date)
            peak_consumptions.append(int(peak_consumption))
            off_peak_consumptions.append(int(off_peak_consumption))


    x = [dt.datetime.strptime(d,'%d/%m/%Y').date() for d in dates]

    previous_day = None
    previous_peak = None
    previous_off_peak = None
    date_axis = []
    peak_axis = []
    off_peak_axis = []
    for day, peak, off_peak in zip(x, peak_consumptions, off_peak_consumptions):
        if previous_day is None or previous_peak is None or previous_off_peak is None:
            pass
        else:
            nb_days = (day-previous_day).days
            delta_peak = peak - previous_peak
            delta_off_peak = off_peak - previous_off_peak
            peak_per_day = delta_peak / nb_days
            off_peak_per_day = delta_off_peak / nb_days
            print(nb_days, delta_peak, peak_per_day)
            print(nb_days, delta_off_peak, off_peak_per_day)
            for i in np.arange(0, nb_days):
                date = previous_day + dt.timedelta(days=int(i))
                date_axis.append(date)
                peak_axis.append(peak_per_day)
                off_peak_axis.append(off_peak_per_day)

        previous_day = day
        previous_peak = peak
        previous_off_peak = off_peak

    def converter(x, _):
        """
        Convert data value into a neat format
        :param x: data value
        :param _: position on the x axis (not used)
        :return: formatted data value
        """
        return '%1.fKWh' % (x*1e-3)

    # first plot stands for the peak consumption
    fig, ax1 = plt.subplots(figsize=(9, 6))
    ax1.grid()
    ax1.set_ylim([0, 30])
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    # plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    ax1.plot(date_axis, peak_axis, 'b-')
    # ax1.yaxis.set_major_formatter(FuncFormatter(converter))
    ax1.set_ylabel('Énergie HP (Wh)', color='b')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')

    # second plot stands for the off-peak consumption
    ax2 = ax1.twinx()
    ax2.set_ylim([0, 30])
    ax2.plot(date_axis, off_peak_axis, 'g-')
    # ax2.yaxis.set_major_formatter(FuncFormatter(converter))
    ax2.set_ylabel('Énergie HC (Wh)', color='g')
    for tl in ax2.get_yticklabels():
        tl.set_color('g')
    # align grids
    ax1.set_yticks(np.linspace(ax1.get_ybound()[0], ax1.get_ybound()[1], 5))
    ax2.set_yticks(np.linspace(ax2.get_ybound()[0], ax2.get_ybound()[1], 5))
    plt.gcf().autofmt_xdate()  # neat display of the dates on the x-axis
    plt.tight_layout()
    plt.savefig("./static/consumption.png")

    return time.strftime("%d/%m/%Y")
