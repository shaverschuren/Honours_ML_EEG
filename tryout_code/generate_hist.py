# import csv
# import pandas
# import scipy.signal
# import numpy as np
# import matplotlib.pyplot as plt
# import datetime
# import math
# import seaborn as sns
#
# # path = 'data\\museMonitor_2020-03-17--11-06-08_3392211170804580360.csv'
# path = '../data/logs_2020-05-13_16-02-30/game.csv'
#
# df = pandas.read_csv(path)
#
# print(df['TimeStamp'])
#
# timestamp_list = []
# timestamp_list_wrong = []
#
# for i in range(len(df['TimeStamp'])):
#     time_passed = datetime.datetime.strptime(df['TimeStamp'][i], "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime.strptime(df['TimeStamp'][0], "%Y-%m-%d %H:%M:%S.%f")
#     if df['correct'][i] == 1:
#         timestamp_list.append(time_passed.seconds)
#     else:
#         timestamp_list_wrong.append(time_passed.seconds)
#
# print(timestamp_list)
# print(timestamp_list_wrong)
#
# bin_size = 30
#
# min_border = 0
# max_border = bin_size
#
# hist_list = []
#
# while min_border < max(timestamp_list):
#     score = len([item for item in timestamp_list if min_border <= item < max_border])
#     min_border += bin_size
#     max_border += bin_size
#     hist_list.append(score)
#
# print(hist_list)
#
# min_hist = min(hist_list)
# max_hist = max(hist_list)
# score_list = []
# for j in range(len(hist_list)):
#     score = (hist_list[j] - min_hist) / (max_hist - min_hist)
#     score_list.append(score)
#
# fig, ax = plt.subplots(3,1)
#
# ax[0].bar(range(len(hist_list)), score_list)
# ax[1].plot(range(len(hist_list)), score_list)
# sns.kdeplot(score_list, ax=ax[2])
# # plt.hist(timestamp_list, bins=timestamp_list[-1]//30)
# # sns.kdeplot(timestamp_list)
# plt.show()
