#!/usr/bin/env python3
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from functools import reduce

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
[pd.to_datetime(i.index) for i in data_sources]

df_covid = reduce(lambda left,right: pd.merge(left,right), data_sources)

#df_covid = df_conf.merge(df_death, on='Date', how='left')
#df_covid = df_covid.merge(df_rec, on='Date', how='left')
#df_covid =df_conf.set_index('Date').join(df_death.set_index('Date'))

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    
    print(df_covid)
    #print(df_conf)
    #print(df_death)
    #print(df_rec)
    #print(df_covid)

fig, ax = plt.subplots(figsize=(12, 8))
df_death.plot(ax=ax)
plt.show()
