#!/usr/bin/env python3
import pandas as pd

COVID_GIT_BASE = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"
COVID_CONF     = "time_series_covid19_confirmed_global.csv"
COVID_DEATH    = "time_series_covid19_deaths_global.csv"
COVID_REC      = "time_series_covid19_recovered_global.csv"

df_conf = pd.read_csv(f'{COVID_GIT_BASE}{COVID_CONF}')
df_death = pd.read_csv(f'{COVID_GIT_BASE}{COVID_DEATH}')
df_rec = pd.read_csv(f'{COVID_GIT_BASE}{COVID_REC}')
discard_cols = ['Lat', 'Long']
data_sources = [df_conf, df_death, df_rec]
[i.drop([x for x in discard_cols], axis=1, inplace=True) for i in data_sources]
countries = ['United Kingdom', 'Italy', 'France', 'Germany', 'US', 'Switzerland', 'China', 'Iran', 'Korea, South', 'Turkey']
#[i[i.groupby(['Country/Region']).sum()] for i in data_sources]

#[i[i['Country/Region'].isin(countries)] for i in data_sources]
df_conf = df_conf.groupby(['Country/Region']).agg('sum')
df_death = df_death.groupby(['Country/Region']).agg('sum')
df_rec = df_rec.groupby(['Country/Region']).agg('sum')

df_conf[df_conf['Country/Region'].isin(countries)]
print(df_conf)
print(df_death.head(10))
print(df_rec.head(10))
#print(df_conf.dtypes)
