#!/usr/bin/env python3
# Ian M. Hayhurst 2020
# Uses John Hopkins datasets:
# Script to generate animated bubbleplot of CoVID19 progression

import functools
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import animation as animation
import numpy as np
mpl.use('agg')

COVID_GIT_BASE = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"
COVID_CONF     = "time_series_covid19_confirmed_global.csv"

df_conf = pd.read_csv(f'{COVID_GIT_BASE}{COVID_CONF}')

data_sources = [df_conf,]
discard_cols = ['Province/State', 'Lat', 'Long']
'''
countries = ['United Kingdom', 'Italy', 'France', 'Germany', 'US',
             'Switzerland', 'China', 'Iran', 'Korea, South', 'Spain']
'''
countries = ['United Kingdom', 'Spain', 'US']
[i.drop([x for x in discard_cols], axis=1, inplace=True) for i in data_sources]
[i.rename(columns={'Country/Region': 'Country'}, inplace=True) for i in data_sources]

df_conf = df_conf[df_conf['Country'].isin(countries)]
df_conf = df_conf.groupby(['Country']).agg('sum')

df_conf = df_conf.transpose().rename_axis('Date', axis=1)

[i.reset_index(inplace=True) for i in data_sources]


'''Build sub_table of 5 day means'''

daysMean = 5
df_conf_inc  = df_conf.diff() 
#df_conf_sub = df_conf.groupby(np.arange(len(df_conf))//daysMean).mean()
#print(df_conf_sub)
'''bubble plot and animate'''
df_conf_inc.fillna(0, inplace=True)
print(df_conf_inc)
time_count = len(df_conf_inc)
colors = ["red", "orange", "blue"]
x = df_conf_inc.iloc[0, 1:]
y = df_conf.iloc[0, 1:]
print(f'init x={x}init  y={y}')  # Debug to show plotting data
fig, ax = plt.subplots(figsize=(12, 8))
pic = ax.scatter(x, y)
ax.set_yscale('log')
ax.set_xscale('log')
ann_list = []

'''
def init():
    # pic.set_offsets([[np.nan]*len(colors)]*2)
    # pic.set_offsets([])
    # return (pic,)
'''


@functools.lru_cache(maxsize=128, typed=False)
def updateData(i):
    for _, a in enumerate(ann_list):
        a.remove()
    ann_list[:] = []
    y = df_conf_inc.iloc[i, 0:]
    x = df_conf.iloc[i, 0:]
    y = np.array(y)
    x = np.array(x)
    print(f'x={x} y={y}')
    ax.xlim = (0, 1.0e6)
    ax.ylim = (0, 1.0e5)
    pic = ax.scatter(x, y, color=colors)
    pic.set_offsets(np.c_[x, y])
    for xx, yy, txt in np.broadcast(x, y, df_conf.columns.values):
        ann = plt.annotate(txt, xy=(xx, yy), xytext=(5, 2), textcoords="offset points", ha="right", fontsize=14)
        ann_list.append(ann)
    #ax.autoscale()
    return (pic,)


#ani = animation.FuncAnimation(fig, updateData, frames=time_count, interval=100, blit=True, init_func=init)
ani = animation.FuncAnimation(fig, updateData, frames=time_count, interval=20)
Writer = animation.FFMpegWriter
writer = Writer(fps=6, bitrate=8000)
plt.draw()
# plt.show()
# uncomment next line to write video
ani.save('covid.mp4', writer)
