import numpy as np
import math
import matplotlib as mpl
from matplotlib import ticker, cm
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from decimal import Decimal
import datetime
from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange)

import os
import subprocess
import matplotlib.image as image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Getting data functions

def readdata(data):
    # List of graphs data (list of lists)
    all_x = []
    all_y = []
    all_z = []
    z_reshape = 0
    with open(data, 'r') as data:
        # Graph data
        x = []
        y = []
        z = []
        for line in data:
            if line != "\n" and line != "\t":
                if '%' in line:             #Add new graph
                    if len(x) != 0:
                        all_x.append(x)
                        x=[]
                    if len(y) != 0:
                        all_y.append(y)
                        y=[]
                    if len(z) != 0:
                        all_z.append(z)
                        z=[]
                else:
                    p = line.split()
                    try:
                        if 'Nan' in p[0]:
                            z.append(float(p[-1]))
                            z_reshape = 1
                        else:
                            if len(p) > 1:
                                x.append(float(p[0]))
                                y.append(float(p[1]))
                            if len(p) > 2:
                                z.append(float(p[2]))
                    except:
                        print('Data is not a number (?)')

    # Add last graph
    if len(x) != 0:
        all_x.append(x)
        x=[]
    if len(y) != 0:
        all_y.append(y)
        y=[]
    if len(z) != 0:
        all_z.append(z)
        z=[]
    if z_reshape == 1:
        for j in range(len(all_x)):
            all_z[j] = np.reshape(all_z[j],(len(all_x[j]),len(all_y[j])))

    return all_x, all_y, all_z


## Plot functions

def plotline(data,name,legend=[],lines_to_plot = []):

    print('Proceeding with ' + name)

    x,y,z = readdata(data)

    color  = ['tab:blue','tab:orange','tab:green','tab:purple','tab:grey']

    if lines_to_plot == []:
        lines_to_plot = range(len(x))

    for i in lines_to_plot:
        if z!= []:
            from mpl_toolkits.mplot3d import Axes3D
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot(x[i],y[i],z[i])
        else:
            plt.plot(x[i],y[i],color=color[i%len(color)])

    #####################################################################

    plt.grid()
    lgd = plt.legend(legend,bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig(name+'.png',bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.cla()
    plt.close('all')

def contacts(datas,name,legend=[],lines_to_plot = []):

    print('Proceeding with ' + name)
    x = []
    y = []
    z = []
    for data in datas:

        with open(data, 'r') as data:
            # Graph data
            datx = []
            daty = []
            datz = []
            for line in data:
                p = line.split()
                try:
                    day_ini=p[0]
                    month_ini = p[1]
                    year_ini = p[2]
                    #print(p[3])
                    day_fin=p[4]
                    month_fin = p[5]
                    year_fin = p[6]
                    #print(p[7])
                    duration = p[8]

                    #
                    date1 = datetime.date(year_ini, month_ini, day_ini)
                    #date2 = datetime.date(year_fin, month_fin, day_fin)
                    print(date1)

                    #datx.append(date1)
                    #daty.append(date2)
                    #datz.append(duration)

                except:
                    a=0

        x.append(datx)
        y.append(daty)
        z.append(datz)

    print(x)
    color  = ['tab:blue','tab:orange','tab:green','tab:purple','tab:grey']
    rule = rrulewrapper(YEARLY, byeaster=1, interval=5)
    loc = RRuleLocator(rule)
    formatter = DateFormatter('%d/%m/%y')

    if lines_to_plot == []:
        lines_to_plot = range(len(x))

    for i in lines_to_plot:
            fig, ax = plt.subplots()
            plt.plot_date(x[i],z[i],color=color[i%len(color)])
            ax.xaxis.set_major_locator(loc)
            ax.xaxis.set_major_formatter(formatter)
            ax.xaxis.set_tick_params(rotation=30, labelsize=10)

    #####################################################################

    plt.grid()
    lgd = plt.legend(legend,bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig(name+'.png',bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.cla()
    plt.close('all')


## Altitude

Altitude = 'no'
if Altitude == 'yes':

    source = ['./REPORTS/altitude_1500_flyby.txt','./REPORTS/altitude_1500_06.txt','./REPORTS/altitude_1500_01.txt','./REPORTS/altitude_600_flyby.txt','./REPORTS/altitude_600_06.txt','./REPORTS/altitude_600_01.txt']

    for i in range(len(source)):
        plt.xlabel('time(s)')
        plt.ylabel('altitude(km)')
        plotline(source[i],source[i],[],lines_to_plot=[0])


Eclipses = 'no'
if Eclipses == 'yes':

    source = ['./REPORTS/eclipses_1500_flyby.txt','./REPORTS/eclipses_1500_06.txt','./REPORTS/eclipses_1500_01.txt','./REPORTS/eclipses_600_flyby.txt','./REPORTS/eclipses_600_06.txt','./REPORTS/eclipses_600_01.txt']

    plt.xlabel('time(s)')
    plt.ylabel('eclipse time(s)')
    eclipses(source,'Eclipses',['Rp=1500,fly-by','Rp=1500,e=0.6','Rp=1500,e=0.1','Rp=600,fly-by','Rp=600,e=0.6','Rp=600,e=0.1'])

Contacts = 'yes'
if Contacts == 'yes':

    source = ['./REPORTS/contacts_1500_06.txt','./REPORTS/contacts_1500_01.txt','./REPORTS/contacts_600_06.txt','./REPORTS/contacts_600_01.txt']

    plt.xlabel('Date')
    plt.ylabel('contact time(s)')
    contacts(source,'Contacts',['Rp=1500,fly-by','Rp=1500,e=0.6','Rp=1500,e=0.1','Rp=600,fly-by','Rp=600,e=0.6','Rp=600,e=0.1'])
