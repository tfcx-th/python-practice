import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser
from pandas.plotting import register_matplotlib_converters
from sklearn.svm import SVR
from scipy.optimize import fsolve
register_matplotlib_converters()

df_ferrara = pd.read_csv('WeatherData/ferrara_270615.csv')
df_milano = pd.read_csv('WeatherData/milano_270615.csv')
df_mantova = pd.read_csv('WeatherData/mantova_270615.csv')
df_ravenna = pd.read_csv('WeatherData/ravenna_270615.csv')
df_torino = pd.read_csv('WeatherData/torino_270615.csv')
df_asti = pd.read_csv('WeatherData/asti_270615.csv')
df_bologna = pd.read_csv('WeatherData/bologna_270615.csv')
df_piacenza = pd.read_csv('WeatherData/piacenza_270615.csv')
df_cesena = pd.read_csv('WeatherData/cesena_270615.csv')
df_faenza = pd.read_csv('WeatherData/faenza_270615.csv')

dist = [
    df_ravenna['dist'][0],
    df_cesena['dist'][0],
    df_faenza['dist'][0],
    df_ferrara['dist'][0],
    df_bologna['dist'][0],
    df_mantova['dist'][0],
    df_piacenza['dist'][0],
    df_milano['dist'][0],
    df_asti['dist'][0],
    df_torino['dist'][0]
]

temp_max = [
    df_ravenna['temp'].max(),
    df_cesena['temp'].max(),
    df_faenza['temp'].max(),
    df_ferrara['temp'].max(),
    df_bologna['temp'].max(),
    df_mantova['temp'].max(),
    df_piacenza['temp'].max(),
    df_milano['temp'].max(),
    df_asti['temp'].max(),
    df_torino['temp'].max()
]
temp_min = [
    df_ravenna['temp'].min(),
    df_cesena['temp'].min(),
    df_faenza['temp'].min(),
    df_ferrara['temp'].min(),
    df_bologna['temp'].min(),
    df_mantova['temp'].min(),
    df_piacenza['temp'].min(),
    df_milano['temp'].min(),
    df_asti['temp'].min(),
    df_torino['temp'].min()
]

# 靠近海
dist1 = dist[0:5]
dist1 = [[x] for x in dist1]
temp_max1 = temp_max[0:5]
# 远离海
dist2 = dist[5:10]
dist2 = [[x] for x in dist2]
temp_max2 = temp_max[5:10]

svr_lin1 = SVR(kernel='linear', C=1e3)
svr_lin2 = SVR(kernel='linear', C=1e3)

svr_lin1.fit(dist1, temp_max1)
svr_lin2.fit(dist2, temp_max2)

xp1 = np.arange(10, 100, 10).reshape((9, 1))
xp2 = np.arange(50, 400, 50).reshape((7, 1))
yp1 = svr_lin1.predict(xp1)
yp2 = svr_lin2.predict(xp2)

fig, ax = plt.subplots()
ax.set_xlim(0, 400)

ax.plot(xp1, yp1, c='b', label='Strong sea effect')
ax.plot(xp2, yp2, c='g', label='Light sea effect')
ax.plot(dist, temp_max, 'ro')

print(svr_lin1.coef_)
print(svr_lin1.intercept_)
print(svr_lin2.coef_)
print(svr_lin2.intercept_)

plt.show()