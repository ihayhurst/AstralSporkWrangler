#!/usr/bin/env python3
import pandas as pd
from datetime import datetime, timedelta
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
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
countries = ['United Kingdom', 'Italy', 'France', 'Germany', 'US', 'Switzerland', 'China', 'Iran', 'Korea, South', 'Turkey']

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

#df_covid = reduce(lambda left,right: pd.merge(left,right), data_sources)
'''Join the frames here '''

#df_covid = df_conf.merge(df_death, on='Date',  how='left')
#df_covid = df_covid.merge(df_rec, on='Date', how='left')
#df_covid =df_conf.set_index('Date').join(df_death.set_index('Date'))
'''Show the tables to see what we have'''
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    
    print(df_conf)
    #print(df_death)
    #print(df_rec)

'''bubble plot and animate'''

time_count = len(df_conf)
max_radius = 25
#colors =np.arange(1, len(countries)+1, 5)
colors = ["red", "orange", "yellow", "green", "blue", "purple", "magenta", "black", "cyan", "teal"]
x = np.arange(0, len(countries))
x = [0] * len(countries)
x = np.array(x)
y = df_conf.iloc[0, 0:]
z = np.column_stack((x, y))
s = df_death.iloc[0, 0:]
print(f'x={x} y={y}')
fig, ax = plt.subplots(figsize=(12, 8))
plt.legend(df_conf.iloc[0, 0:])
pic = ax.scatter(x, y, s, c=colors, alpha=0.4)
#pic.set_offsets([[np.nan]*len(colors)]*2)
#pic.set_offsets([z])
#ax.axis([)

def init():
    #pic.set_offsets([[np.nan]*len(colors)]*2)
    pic.set_offsets([])
    return pic,

def updateData(i):
    y = df_conf.iloc[i, 0:]
    s = df_death.iloc[i, 0:]
    x = [i] * len(countries)
    x = np.array(x)
    print(f'x={x} y={y}')
    pic = ax.scatter(x, y, s, c=colors, alpha =0.2)
    pic.set_offsets(np.c_[x, y])
    return pic,

#plt.scatter(x, y, s=z*2000, c=x, cmap="Blues", alpha=0.4, edgecolors="grey", linewidth=2)
ani = animation.FuncAnimation(fig, updateData, frames=time_count, interval = 100, blit=True, init_func=init) 
Writer = animation.FFMpegWriter
writer = Writer(fps = 5, bitrate = 8000)
plt.draw()
#plt.show()
#uncomment next line to write video
ani.save('covid.mp4', writer)
