import numpy as np
import math
import matplotlib as mpl
from matplotlib import ticker, cm
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from decimal import Decimal
import datetime
from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange, date2num)

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
        print('Proceeding with ' + data)

        with open(data, 'r') as data:
            # Graph data
            datx = []
            daty = []
            datz = []
            for line in data:
                p = line.split()
                try:
                    day_ini= int(p[0])

                    month_ini = p[1]
                    if month_ini == 'Jan':
                        month_ini = int(1)
                    elif month_ini == 'Feb':
                        month_ini = int(2)
                    elif month_ini == 'Mar':
                        month_ini = int(3)
                    elif month_ini == 'Apr':
                        month_ini = int(4)
                    elif month_ini == 'May':
                        month_ini = int(5)
                    elif month_ini == 'Jun':
                        month_ini = int(6)
                    elif month_ini == 'Jul':
                        month_ini = int(7)
                    elif month_ini == 'Aug':
                        month_ini = int(8)
                    elif month_ini == 'Sep':
                        month_ini = int(9)
                    elif month_ini == 'Oct':
                        month_ini = int(10)
                    elif month_ini == 'Nov':
                        month_ini = int(11)
                    elif month_ini == 'Dec':
                        month_ini = int(12)
                    else:
                        print('No month')

                    year_ini = int(p[2])
                    time_ini = p[3]
                    time_ini_vect = time_ini.split(':')
                    hour_ini = int(time_ini_vect[0])
                    min_ini = int(time_ini_vect[1])

                    duration = float(p[8])

                    date1 = datetime.datetime(year_ini, month_ini, day_ini, hour_ini, min_ini)


                    datx.append(date1)
                    datz.append(duration)
                except:
                    a=0

            x.append(datx)
            z.append(datz)

    color  = ['tab:blue','tab:orange','tab:green','tab:purple','tab:grey','tab:red']
    formatter = DateFormatter('%d/%m/%y')

    if lines_to_plot == []:
        lines_to_plot = range(len(x))

    fig, ax = plt.subplots()
    for i in lines_to_plot:
            date = date2num(x[i])
            duration = z[i]
            plt.scatter(date,duration,color=color[i%len(color)],s=20)
            ax.set_xlabel('Date')
            ax.set_ylabel('Contact time(s)')
            ax.xaxis.set_major_formatter(formatter)
            ax.xaxis.set_tick_params(rotation=30, labelsize=10)


        #####################################################################

    plt.grid()
    lgd = plt.legend(legend)
    plt.savefig(name+'.png')
    plt.close('all')

def eclipses(datas,name,legend=[],lines_to_plot = []):

    print('Proceeding with ' + name)
    x = []
    y = []
    z = []
    x_penumbra = []
    y_penumbra = []
    z_penumbra = []
    for data in datas:
        print('Proceeding with ' + data)

        with open(data, 'r') as data:
            # Graph data
            datx = []
            daty = []
            datz = []
            datx_penumbra = []
            daty_penumbra = []
            datz_penumbra = []
            for line in data:
                p = line.split()
                try:
                    day_ini= int(p[0])

                    month_ini = p[1]
                    if month_ini == 'Jan':
                        month_ini = int(1)
                    elif month_ini == 'Feb':
                        month_ini = int(2)
                    elif month_ini == 'Mar':
                        month_ini = int(3)
                    elif month_ini == 'Apr':
                        month_ini = int(4)
                    elif month_ini == 'May':
                        month_ini = int(5)
                    elif month_ini == 'Jun':
                        month_ini = int(6)
                    elif month_ini == 'Jul':
                        month_ini = int(7)
                    elif month_ini == 'Aug':
                        month_ini = int(8)
                    elif month_ini == 'Sep':
                        month_ini = int(9)
                    elif month_ini == 'Oct':
                        month_ini = int(10)
                    elif month_ini == 'Nov':
                        month_ini = int(11)
                    elif month_ini == 'Dec':
                        month_ini = int(12)
                    else:
                        print('No month')

                    year_ini = int(p[2])
                    time_ini = p[3]
                    time_ini_vect = time_ini.split(':')
                    hour_ini = int(time_ini_vect[0])
                    min_ini = int(time_ini_vect[1])

                    duration = float(p[8])

                    date1 = datetime.datetime(year_ini, month_ini, day_ini, hour_ini, min_ini)

                    if 'Penumbra' in line:
                        datx_penumbra.append(date1)
                        datz_penumbra.append(duration)
                    elif 'Umbra' in line:
                        datx.append(date1)
                        datz.append(duration)

                except:
                    a=0

            x.append(datx)
            z.append(datz)
            x_penumbra.append(datx_penumbra)
            z_penumbra.append(datz_penumbra)

    color  = ['tab:blue','tab:orange','tab:green','tab:purple','tab:grey','tab:red']
    formatter = DateFormatter('%d/%m/%y')

    if lines_to_plot == []:
        lines_to_plot = range(len(x))

    fig, ax = plt.subplots()
    for i in lines_to_plot:
            date = date2num(x[i])
            duration = z[i]
            date_penumbra = date2num(x[i])
            duration_penumbra = z[i]
            plt.scatter(date,duration,color=color[i%len(color)],s=20)
            plt.scatter(date_penumbra,duration_penumbra,color=color[i%len(color)],s=20,marker="*")
            ax.set_xlabel('Date')
            ax.set_ylabel('Duration(s)')
            ax.xaxis.set_major_formatter(formatter)
            ax.xaxis.set_tick_params(rotation=30, labelsize=10)


        #####################################################################

    plt.grid()
    lgd = plt.legend(legend)
    plt.savefig(name+'.png')
    plt.close('all')


## Altitude

Altitude = 'no'
if Altitude == 'yes':

    source = ['./REPORTS/altitude_1500_flyby.txt','./REPORTS/altitude_1500_06.txt','./REPORTS/altitude_1500_01.txt','./REPORTS/altitude_600_flyby.txt','./REPORTS/altitude_600_06.txt','./REPORTS/altitude_600_01.txt']

    for i in range(len(source)):
        plt.xlabel('time(s)')
        plt.ylabel('altitude(km)')
        plotline(source[i],source[i],[],lines_to_plot=[0])


Eclipses = 'yes'
if Eclipses == 'yes':

    source = ['./REPORTS/eclipses_1500_flyby.txt','./REPORTS/eclipses_1500_06.txt','./REPORTS/eclipses_1500_01.txt','./REPORTS/eclipses_600_flyby.txt','./REPORTS/eclipses_600_06.txt','./REPORTS/eclipses_600_01.txt']

    eclipses(source,'Eclipses',['Umbra(Rp=1500,flyby)','Penumbra(Rp=1500,flyby)','Umbra(Rp=1500,e=0.6)','Umbra(Rp=1500,e=0.6)','Umbra(Rp=1500,e=0.1)','Penumbra(Rp=1500,e=0.1)','Umbra(Rp=600,flyby)','Penumbra(Rp=600,flyby)','Umbra(Rp=600,e=0.6)','Penumbra(Rp=600,e=0.6)','Umbra(Rp=600,e=0.1)','Penumbra(Rp=600,e=0.1)'])

Contacts = 'yes'
if Contacts == 'yes':

    source = ['./REPORTS/contacts_1500_flyby.txt','./REPORTS/contacts_1500_06.txt','./REPORTS/contacts_1500_01.txt','./REPORTS/contacts_600_flyby.txt','./REPORTS/contacts_600_06.txt','./REPORTS/contacts_600_01.txt']

    contacts(source,'Contacts',['Rp=1500,flyby','Rp=1500,e=0.6','Rp=1500,e=0.1','Rp=600,flyby','Rp=600,e=0.6','Rp=600,e=0.1'])
