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
    # y = range(len(x)) # many thanks to Kyss Tao for setting me straight here

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
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    # plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    ax1.plot(x, peak_consumptions, 'bo-')
    ax1.yaxis.set_major_formatter(FuncFormatter(converter))
    ax1.set_ylabel('Énergie HP (KWh)', color='b')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')

    # second plot stands for the off-peak consumption
    ax2 = ax1.twinx()
    ax2.plot(x, off_peak_consumptions, 'go-')
    ax2.yaxis.set_major_formatter(FuncFormatter(converter))
    ax2.set_ylabel('Énergie HC (KWh)', color='g')
    for tl in ax2.get_yticklabels():
        tl.set_color('g')
    # align grids
    ax1.set_yticks(np.linspace(ax1.get_ybound()[0], ax1.get_ybound()[1], 5))
    ax2.set_yticks(np.linspace(ax2.get_ybound()[0], ax2.get_ybound()[1], 5))
    plt.gcf().autofmt_xdate()  # neat display of the dates on the x-axis
    plt.tight_layout()
    plt.savefig("./static/consumption.png")

    return time.strftime("%d/%m/%Y")
