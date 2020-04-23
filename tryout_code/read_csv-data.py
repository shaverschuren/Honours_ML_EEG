# # read_csv_files.py
# #
# # This code takes in a single csv file, as created by museMonitor, extracts the data and stores it in
# # a more usable format.
# # It is, however, more for prototyping purposes. might rewrite to function later.
# #
#
# import csv
# import pandas
# import scipy.signal
# import numpy as np
# import matplotlib.pyplot as plt
# import math
#
# # path = 'data\\museMonitor_2020-03-17--11-06-08_3392211170804580360.csv'
# path = 'data\\logs_2020-04-20_13-42-49\\fft.csv'
#
# df = pandas.read_csv(path)
#
# column_names = list(df.columns)
# data = df.to_numpy()
# print(column_names)
#
# # NaN filtering
# # for column in column_names:
# #     if column not in ['TimeStamp', 'Elements']:
# #         for i in range(len(df[column])):
# #             if math.isnan(df[column][i]):
# #                 df[column][i] = np.mean(df[column][i-2:i+2])
# #
# #
# # df['Alpha_AF7_med'] = scipy.signal.medfilt(df['Alpha_AF7'], 15)
# # print(df['Alpha_AF7'])
# fig = plt.figure()
# ax1 = fig.add_subplot(4, 1, 1)
# ax2 = fig.add_subplot(4, 1, 2)
# ax3 = fig.add_subplot(4, 1, 3)
# ax4 = fig.add_subplot(4, 1, 4)
#
# ax1.plot(range(len(df)), df['alpha_2'], 'b-', linewidth=1)
# ax2.plot(range(len(df)), df['beta_2'], 'r-', linewidth=1)
# ax3.plot(range(len(df)), df['gamma_2'], 'c-', linewidth=1)
# ax4.plot(range(len(df)), df['theta_2'], 'g-', linewidth=1)
#
# plt.show()
#
#
#
