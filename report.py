#!/usr/bin/env python3
import pandas as pd

COVID_GIT_BASE = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"
COVID_CONF     = "time_series_covid19_confirmed_global.csv"
COVID_DEATH    = "time_series_covid19_deaths_global.csv"
COVID_REC      = "time_series_covid19_recovered_global.csv"

df_conf = pd.read_csv(f'{COVID_GIT_BASE}{COVID_CONF}')
df_death = pd.read_csv(f'{COVID_GIT_BASE}{COVID_DEATH}')
df_rec = pd.read_csv(f'{COVID_GIT_BASE}{COVID_REC}')

data_sources = [df_conf, df_death, df_rec]
discard_cols = ['Lat', 'Long']
countries = ['United Kingdom', 'Italy', 'France', 'Germany', 'US', 'Switzerland', 'China', 'Iran', 'Korea, South', 'Turkey']

[i.drop([x for x in discard_cols], axis=1, inplace=True) for i in data_sources]
[i.rename(columns={'Country/Region' : 'Country'}, inplace=True) for i in data_sources]

df_conf=df_conf[df_conf['Country'].isin(countries)]
df_death=df_death[df_death['Country'].isin(countries)]
df_rec=df_rec[df_rec['Country'].isin(countries)]


df_conf = df_conf.groupby(['Country']).agg('sum')
df_death = df_death.groupby(['Country']).agg('sum')
df_rec = df_rec.groupby(['Country']).agg('sum')

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df_conf)
    print(df_death)
    print(df_rec)
