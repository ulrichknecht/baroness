from matplotlib import pyplot as plt
from matplotlib.dates import WeekdayLocator, DayLocator, HourLocator, DateFormatter, drange, MONDAY
import numpy as np
from user import User
from database import *
import thread as th

def plot_all_thread(user = None):
    #if user != None:
    #    th.start_new_thread(plot_all, (user,))
    #else:
    #    th.start_new_thread(plot_all, ())
#def plot_all(user = None):
#
    if user != None:
        plot_total(user)
    plot_total()
    plot_list(4)
    print 'plot_all'

def plot_total(user = None):

    print 'plot_total'
    today = datetime.date.today()
    delta = datetime.timedelta(days=1)
    begin = datetime.date.today() - datetime.timedelta(weeks=2)
    dates = drange(begin, today + delta, delta)

    print begin
    print today
    print dates

    allconsumptions = [[0 for x in range(len(dates))] for product in get_products()]

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

    print allconsumptions
    fig, ax = plt.subplots()
    i=1

    for consumptions in allconsumptions:
        ax.plot(dates, consumptions, linestyle='-', marker='', label=get_product_by_id(i).name)
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

    plt.annotate(
        'THE DAY I REALIZED\nI COULD COOK BACON\nWHENEVER I WANTED',
        xy=(30, 1), arrowprops=dict(arrowstyle='->'), xytext=(15, -10))

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

    #480x320
    fig.set_size_inches(4.8, 3.2)
    plt.savefig(fils, dpi=100)

    fig.set_size_inches(4.8, 3.2)
    plt.savefig(fill, dpi=400)

def plot_list(duration):

    today = datetime.date.today()
    begin = datetime.date.today() - datetime.timedelta(weeks=duration)

    users = get_users()
    #consumptions = [0 for user in users]
    allconsumptions = [[0 for user in users] for product in get_products()]

    consumed = get_consumed()
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

    colors = ['blue', 'green', 'red', 'yellow', 'orange' , 'black']

    #plot reversed to print longest bar lowest
    i = len(allconsumptions)
    for consumptions in reversed(allconsumptions):
        ax.barh(np.arange(len(consumptions)), consumptions, label=get_product_by_id(i).name, align='center', height=(0.5), color=colors[i-1])
        i -= 1

    names = list()

    for user in users:
        names.append(user.longname)

    plt.yticks(np.arange(len(names)), names)

    ax.legend(loc=2)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticks_position('none')
    plt.subplots_adjust(left=0.15)
    #plt.tick_params(which='minor', length=4)
    #plt.tick_params(which='major', length=5)

    #plt.annotate(
    #    'THE DAY I REALIZED\nI COULD COOK BACON\nWHENEVER I WANTED',
    #    xy=(30, 1), arrowprops=dict(arrowstyle='->'), xytext=(15, -10))

    plt.xlabel('Konsumate')
    #plt.ylabel('Konsumate')

    plt.title("Bierliste")

    #1024x768
    fig.set_size_inches(10.24, 7.68)
    plt.savefig('app/static/bierliste.png', dpi=100)
    #800x600
    fig.set_size_inches(15, 10)
    plt.savefig('app/static/bierliste_small.png', dpi=72)