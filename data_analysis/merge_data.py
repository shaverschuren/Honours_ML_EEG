import os
import csv
import pandas
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
import datetime
import math
import seaborn as sns


def trim_fft_data():
    global df_fft

    fft_time = str2time(df_fft['TimeStamp'][0])

    i = j = 0
    while fft_time < start_time:
        fft_time = str2time(df_fft['TimeStamp'][i])
        i += 1
    while fft_time < stop_time:
        fft_time = str2time(df_fft['TimeStamp'][j])
        j += 1

    df_fft = df_fft[i:j]

    return i, fft_time


def generate_perf_data(bin_size=30):
    timestamp_list = []
    timestamp_list_wrong = []

    for i in range(len(df_game['TimeStamp'])):
        time_passed = str2time(df_game['TimeStamp'][i]) - start_time
        if df_game['correct'][i] == 1:
            timestamp_list.append(time_passed.seconds)
        else:
            timestamp_list_wrong.append(time_passed.seconds)

    min_border = 0
    max_border = bin_size

    hist_list = []

    while min_border < max(timestamp_list):
        score = len([item for item in timestamp_list if min_border <= item < max_border])
        min_border += bin_size
        max_border += bin_size
        hist_list.append(score)

    min_hist = min(hist_list)
    max_hist = max(hist_list)
    score_list = []
    for j in range(len(hist_list)):
        score = (hist_list[j] - min_hist) / (max_hist - min_hist)
        score_list.append(score)

    return score_list


def str2time(timestamp):
    time = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")

    return time


def merge_data():

    final_df = df_fft

    score_list = []
    score_list_interpol = []

    for i in range(len(final_df)):
        timestamp = str2time(final_df['TimeStamp'][i+start_index])
        passed_time = timestamp - start_time

        passed_seconds = float(passed_time.seconds)
        passed_micros = passed_time.microseconds/1000000
        passed_time_float = passed_seconds + passed_micros

        time_bin = int(passed_time_float//bin_size)
        score = perf_list[time_bin]

        score_list.append(score)

        time_mod = passed_time_float % bin_size
        linear_factor = 0.5 - time_mod/bin_size

        if time_bin != len(perf_list)-1 and time_bin != 0:
            if linear_factor >= 0:
                score_list_interpol.append(linear_factor*perf_list[time_bin-1]+(1-linear_factor)*score)
            else:
                score_list_interpol.append(-linear_factor*perf_list[time_bin+1]+(1+linear_factor)*score)
        else:
            score_list_interpol.append(score)

    conv_footprint = 7*bin_size
    score_list_smoothed = np.convolve(score_list_interpol, np.ones((conv_footprint,))/conv_footprint, mode='same')

    final_df['Performance'] = score_list_smoothed

    return final_df, score_list,score_list_interpol, score_list_smoothed


def plot_data():
    fig, ax = plt.subplots(3, 1)

    ax[0].bar(range(len(perf_list)), perf_list)
    ax[1].plot(range(len(score_list)), score_list)
    ax[1].plot(range(len(score_list_interpol)), score_list_interpol)
    ax[1].plot(range(len(score_list_smoothed)), score_list_smoothed)
    sns.kdeplot(score_list, ax=ax[2])
    sns.kdeplot(score_list_interpol, ax=ax[2])
    sns.kdeplot(score_list_smoothed, ax=ax[2])
    # plt.hist(timestamp_list, bins=timestamp_list[-1]//30)
    # sns.kdeplot(timestamp_list)
    plt.show()


if __name__ == "__main__":
    bin_size = 30
    log_folder = '..\\data\\logs_2020-05-12_12-52-22\\'

    fft_path = log_folder + 'fft.csv'
    game_path = log_folder + 'game.csv'

    df_fft = pandas.read_csv(fft_path)
    df_game = pandas.read_csv(game_path)

    start_time = str2time(df_game['TimeStamp'][0])
    stop_time = str2time(df_game['TimeStamp'][(len(df_game))-1])

    start_index, fft_time = trim_fft_data()

    perf_list = generate_perf_data(bin_size)

    merged_df, score_list, score_list_interpol, score_list_smoothed = merge_data()

    merged_df.to_csv(log_folder+"merged.csv")

    plot_data()