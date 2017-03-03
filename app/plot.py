import matplotlib 
matplotlib.use('Agg')

from matplotlib import pyplot as plt
from matplotlib import units
from matplotlib import patheffects
from matplotlib.dates import WeekdayLocator, DayLocator, HourLocator, DateFormatter, drange, MONDAY
from matplotlib import rcParams as rcp
import numpy as np
from user import User
from database import *
import multiprocessing as mp
import thread
import pandas as pd
import logging
import time
import glob


class Plotter:

    def __init__(self):
        logging.info("Plotter started!")
        self.joblist = list()
        self.active = True
        thread.start_new_thread(self.refresh, ())

    def refresh(self):
        ptime = 0
        while self.active:
            logging.info("Plotter plotting stuff")
            logfiles = list()
            logfiles += glob.glob("app/static/logdata*.csv")
            logfiles.append("/tmp/baroness_logdata_fast.csv")
            print logfiles
            if logfiles:
                plot_log(logfiles, hours = 4)

            # plotter not fully integrated yet
            #if ptime % 30 or self.joblist:
            #    plot_total()
            #    plot_list(4)
            #    for u in self.joblist:
            #        plot_total(u)
            #    self.joblist = list()

            ptime += 1
            time.sleep(10)

    def addplot(self, user):
        logging.info("Plotter add user " + user.name)
        self.joblist.append(user)

    def stop(self):
        logging.info("Plotter stop!")
        self.active = False


def plot_all_thread(user=None):
    if user is not None:
        proc = mp.Process(target=plot_all, args=(user,))
    else:
        proc = mp.Process(target=plot_all, args=())
    proc.start()


def plot_all(user=None):
    if user is not None:
        plot_total(user)
    plot_total()
    plot_list(4)
    logging.info('plot_all')


def plot_total(user=None):
    logging.info("start plot_total")

    today = datetime.date.today()
    delta = datetime.timedelta(days=1)
    begin = today - datetime.timedelta(weeks=2)
    dates = drange(begin, today + delta, delta)

    products = get_products()
    allconsumptions = [[0 for x in range(len(dates))] for product in products]

    consumed = get_consumed()
    for consumption in consumed:
        if user == None or consumption.consumer == user.id:
            i = 1
            for consumptions in allconsumptions:
                if consumption.prodnr == i:
                    if consumption.time.date() > begin:
                        consumptions[(consumption.time.date() - begin).days] += 1
                i += 1
    plt.xkcd()

    #print allconsumptions
    fig, ax = plt.subplots()

    i = 0
    for consumptions in allconsumptions:
        ax.plot(dates, consumptions, linestyle='-', marker='', label=products[i].name)
        i += 1

    ax.legend(loc=2,prop={'size':15})

   # ax.axes.margins = 1  # x margin.  See `axes.Axes.margins`
   # ax.axes.ymargin = 1  # y margin See `axes.Axes.margins`

    plt.xticks(rotation='vertical')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    plt.tick_params(which='minor', length=4)
    plt.tick_params(which='major', length=5)

    #ax.xaxis.set_major_locator(WeekdayLocator(MONDAY))
    #ax.xaxis.set_major_locator(DayLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%d.%m'))
    #ax.xaxis.set_minor_formatter(DateFormatter('%d.%m'))

    #ax.fmt_xdata = DateFormatter('%d.%m')
    fig.autofmt_xdate()

    plt.xlabel('Datum')
    plt.ylabel('Konsumate')

    if user == None:
        tit = "Bierkonsum FET"
        fils = "app/static/total.png"
        fill = "app/static/total_big.png"
    else:
        tit = "Bierkonsum %s" % user.name
        fils = "app/static/total%03d.png" % user.id
        fill = "app/static/total%03d_big.png" % user.id
    plt.title(tit)
    logging.info("Plot plot_total " + str(datetime.datetime.now()))
    #480x320
    fig.set_size_inches(4.8, 3.2)
    plt.savefig(fils, dpi=100)
    logging.info("Plot: End plot_total " + str(datetime.datetime.now()))
    #fig.set_size_inches(4.8, 3.2)
    #plt.savefig(fill, dpi=400)


def plot_log(logfiles, hours):
    end = datetime.datetime.now()
    begin = end - datetime.timedelta(hours=hours)

    #load all logfiles
    data = None
    for logfile in logfiles:
        try:
            d = pd.read_csv(logfile, parse_dates=[0])
            if data is not None:
                data = pd.concat((data, d))
            else:
                data = d
        except:
            logging.error("error while loading file " + logfile)
            return 0

    #ipdb.set_trace()
    data = data.sort('time')
    data = data[data.time > begin]
    data = data.set_index(pd.DatetimeIndex(data.time))
    data = data.drop("time", axis=1)
    #ipdb.set_trace()
    plt.xkcd()
    rcp['path.effects'] = [patheffects.withStroke(linewidth=0)]
    #all columns
      
    for item, frame in data.iteritems():
        if frame is None or frame.empty or frame.isnull().values.all():
            continue
        f = plt.figure()
        #f.patch.set_facecolor("#ccefff")
        #f.patch.set_alpha("0.0")
        logging.debug("column " + str(item) + " " + frame.name)
        plt.plot(data.index.to_pydatetime(), frame)#"b"
        ax = plt.gca()
        #ax.grid(True, linewidth=1.0)
        #plt.xlim(begin, end)
        #ax.spines['right'].set_visible(False)
        #ax.spines['top'].set_visible(False)
        ax.yaxis.set_ticks_position('none')#('left')
        ax.xaxis.set_ticks_position('none')#('bottom')

        try: #might not work if few data available
	    f.autofmt_xdate()
            #plt.tick_params(which='minor', length=4)
            #plt.tick_params(which='major', length=5)
            #ipdb.set_trace()
            #ax.fmt_xdata = AutoDateFormatter('%d.%m/%H')
            #ax.xaxis.set_major_locator(WeekdayLocator(MONDAY))
   	    ax.xaxis.set_major_locator(AutoDateLocator())
            ax.xaxis.set_major_formatter(AutoDateFormatter(defaultfmt='%d.%m'))
            #f.autofmt_xdate()
        except:
            logging.warning("Plot: Few data!")
        #plt.xlabel('Datum')
        #plt.ylabel('Temperatur / C')
        outfile = "app/static/log_" + str(item) + ".png"
        logging.info("Plot plot_log " + str(datetime.datetime.now()))
        #480x320
        plt.gcf().set_size_inches(5.3, 2.4)
        plt.tight_layout()
        plt.savefig(outfile, dpi=70, transparent=True, bbox_inches='tight')
        plt.close()

    logging.info("Plot: End plot_log " + str(datetime.datetime.now()))


def plot_list(duration):
    logging.info("Plot: Start plot_list " + str(datetime.datetime.now()))
    end = datetime.datetime.now()
    begin = end - datetime.timedelta(weeks=duration)

    users = get_users()
    products = get_products()
    #consumptions = [0 for user in users]
    allconsumptions = [[0 for user in users] for product in products]

    consumed = get_consumed(startdate=begin)

    for consumption in consumed:
        allconsumptions[consumption.prodnr-1][consumption.consumer-1] += 1

    #cumulate consumptions for cumulative bar graph
    i = 0
    for consumptions in allconsumptions:
        if i > 0:
            j = 0
            for consumption in consumptions:
                allconsumptions[i][j] += allconsumptions[i-1][j]
                j += 1
        i += 1

    plt.xkcd()

    fig, ax = plt.subplots()
    ax.grid(True, linewidth=0.5)
    ax.grid(True, linewidth=0.5, which='minor')
    ax.yaxis.grid(False, which='major')
    ax.yaxis.grid(True, which='minor')

    colors = ['blue', 'green', 'red', 'yellow', 'orange' , 'black']

    #plot reversed to print longest bar lowest
    i = len(allconsumptions) - 1
    for consumptions in reversed(allconsumptions):
        x = list()
        y = list()
        for j, consumption in enumerate(consumptions):
            x += list(np.arange(1, consumption+1)-0.5)
            y += list(np.multiply(j, np.ones(consumption)))
        ax.scatter(x, y, marker='x', s=70, color = colors[i], label=products[i].name)
        #ax.barh(np.arange(len(consumptions)), consumptions, label=products[i].name, align='center', height=(0.5), color=colors[i])
        i -= 1

    names = list()

    for user in users:
        names.append(user.longname)

    #ticks
    plt.yticks(np.arange(len(names)), names)
    ax.set_yticks(np.arange(len(names))-0.5, minor=True)
    #limits
    plt.ylim(-0.5, len(names)-0.5)
    plt.xlim(0)
    plt.gca().set_xlim(right=30)
    #legend = auto
    ax.legend(loc=0)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticks_position('none')

    plt.subplots_adjust(left=0.15)
    #plt.tick_params(which='minor', length=4)
    #plt.tick_params(which='major', length=5)

    plt.xlabel('Konsumate')
    #plt.ylabel('Konsumate')

    plt.title("Bierliste ("+ str(duration) + " Wochen)")

    logging.info("Plot plot_list " + str(datetime.datetime.now()))
    #800x600
    fig.set_size_inches(15, 10)
    plt.savefig('app/static/bierliste_small.png', dpi=72, bbox_inches='tight')
    #1024x768
    #fig.set_size_inches(10.24, 7.68)
    #plt.savefig('app/static/bierliste.png', dpi=100)
    logging.info("Plot: End plot_list " + str(datetime.datetime.now()))
