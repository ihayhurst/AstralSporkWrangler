#!/usr/bin/env python3
#Ian M. Hayhurst 2020
#John Hopkins datasets: Script to generate animated bubbleplot of CoVID19 progression

import pandas as pd
from datetime import datetime, timedelta
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import animation as animation
import numpy as np
mpl.use('agg')

COVID_GIT_BASE = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"
COVID_CONF     = "time_series_covid19_confirmed_global.csv"
COVID_DEATH    = "time_series_covid19_deaths_global.csv"
COVID_REC      = "time_series_covid19_recovered_global.csv"

df_conf = pd.read_csv(f'{COVID_GIT_BASE}{COVID_CONF}')
df_death = pd.read_csv(f'{COVID_GIT_BASE}{COVID_DEATH}')
df_rec = pd.read_csv(f'{COVID_GIT_BASE}{COVID_REC}')

data_sources = [df_conf, df_death, df_rec]
discard_cols = ['Province/State', 'Lat', 'Long']
countries = ['United Kingdom', 'Italy', 'France', 'Germany', 'US', 'Switzerland', 'China', 'Iran', 'Korea, South', 'Spain']
countries_pop = {'United Kingdom':67886011, 'Italy':60461826, 'France':65273511
, 'Germany':83783942, 'US':331002651, 'Switzerland':8654622, 'China':1439323776, 'Iran':83992949, 'Korea, South':51269185, 'Spain':46754778}

[i.drop([x for x in discard_cols], axis=1, inplace=True) for i in data_sources]
[i.rename(columns={'Country/Region' : 'Country'}, inplace=True) for i in data_sources]

df_conf=df_conf[df_conf['Country'].isin(countries)]
df_death=df_death[df_death['Country'].isin(countries)]
df_rec=df_rec[df_rec['Country'].isin(countries)]


df_conf = df_conf.groupby(['Country']).agg('sum')
df_death = df_death.groupby(['Country']).agg('sum')
df_rec = df_rec.groupby(['Country']).agg('sum')

df_conf  = df_conf.transpose().rename_axis('Date', axis=1)
df_death = df_death.transpose().rename_axis('Date', axis=1)
df_rec   = df_rec.transpose().rename_axis('Date', axis=1)

#[pd.to_datetime(i.index) for i in data_sources]
[i.reset_index(inplace=True) for i in data_sources]
#df_conf.reset_index(inplace=True)


'''Show the tables to see what we have'''
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    
    print(df_conf)
    print(df_death)
    print(df_rec)

'''bubble plot and animate'''

time_count = len(df_conf)
colors = ["red", "orange", "yellow", "green", "blue", "purple", "magenta", "black", "cyan", "teal"]
#China(Red)  France(Orange),  Germany(Yellow),   Iran(Green),  Italy(Blue),  Korea, South(purple)  Spain(Magenta), Switzerland(black), US(Cyan), United Kingdom (Teal)
x = np.arange(0, len(countries))
x = [0] * len(countries)
x = np.array(x)
pop = df_conf.columns.values
pop = ([countries_pop[f'{i}']for i in pop])
y = df_conf.iloc[0, 0:]
y = np.divide(y,pop)
s = df_death.iloc[0, 0:]/3
print(f'x={x} y={y}') #Debug to show plotting data
fig, ax = plt.subplots(figsize=(12, 8))
pic = ax.scatter(x, y, s, c=colors, alpha=0.3)
#ax.axis([0,10,0,1000])
ann_list = []
def init():
    #pic.set_offsets([[np.nan]*len(colors)]*2)
    pic.set_offsets([])
    return pic,

def updateData(i):
    for j, a in enumerate(ann_list):
        a.remove()
    ann_list[:] = []
    pop = df_conf.columns.values
    pop = ([countries_pop[f'{i}']for i in pop])
    y = df_conf.iloc[i, 0:]
    y = np.divide(y,pop)
    s = df_death.iloc[i, 0:]/3
    x = [i] * len(countries)
    x = np.array(x)
    y = np.array(y)
    print(f'x={x} y={y}')
    pic = ax.scatter(x, y, s, c=colors, alpha =0.3, edgecolors="grey")
    pic.set_offsets(np.c_[x, y])
    for xx,yy,txt in np.broadcast(x,y,df_conf.columns.values):
        ann = plt.annotate(txt,xy=(xx,yy), xytext=(5, 2), textcoords="offset points", ha="right", fontsize=14)
        ann_list.append(ann)
    ax.autoscale()
    return pic,

ani = animation.FuncAnimation(fig, updateData, frames=time_count, interval = 100, blit=True, init_func=init) 
Writer = animation.FFMpegWriter
writer = Writer(fps = 5, bitrate = 8000)
plt.draw()
#plt.show()
#uncomment next line to write video
ani.save('covid.mp4', writer)
