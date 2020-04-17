# read_csv_files.py
#
# This code takes in a single csv file, as created by museMonitor, extracts the data and stores it in
# a more usable format.
# It is, however, more for prototyping purposes. might rewrite to function later.
#

import csv
import pandas
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
import math

# path = 'data\\museMonitor_2020-03-17--11-06-08_3392211170804580360.csv'
path = 'data\\museMonitor_2020-03-17--11-06-08_3392211170804580360.csv'

df = pandas.read_csv(path)

column_names = list(df.columns)
data = df.to_numpy()
print(column_names)

# NaN filtering
for column in column_names:
    if column not in ['TimeStamp', 'Elements']:
        for i in range(len(df[column])):
            if math.isnan(df[column][i]):
                df[column][i] = np.mean(df[column][i-2:i+2])


df['Alpha_AF7_med'] = scipy.signal.medfilt(df['Alpha_AF7'], 15)
print(df['Alpha_AF7'])
fig, ax = plt.subplots()

ax.plot(range(617), df['Alpha_AF7'])
ax.plot(range(617), df['Alpha_AF7_med'])

plt.show()

# # test plot
#
# x = []
# y1 = []
# y2 = []
# y3 = []
# y4 = []
#
# for i in range(len(data)):
#     timestamp = data[i][0]
#     RAW_TP9 = data[i][21]
#     RAW_AF7 = data[i][22]
#     RAW_AF8 = data[i][23]
#     RAW_TP10 = data[i][24]
#
#     # x.append(timestamp[15:])
#     x.append(i)
#     y1.append(RAW_TP9)
#     y2.append(RAW_AF7)
#     y3.append(RAW_AF8)
#     y4.append(RAW_TP10)
#
# fig, ax = plt.subplots(2,2)
#
# ax[0][0].plot(x, df['Delta_TP9'])
# ax[0][1].plot(x, y2)
# ax[1][0].plot(x, y3)
# ax[1][1].plot(x, y4)
#
# plt.show()


