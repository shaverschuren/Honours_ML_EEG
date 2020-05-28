# merge_data.py
#
# This script performs the post-processing and data merging for all subjects.
#
# Author:   S.H.A. Verschuren
# Date:     14-5-2020

from glob import glob
import pandas
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import datetime
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


def str2time(timestamp):
    time = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")

    return time


def generate_timestamp_data():
    timestamp_list = []
    timestamp_list_wrong = []

    for i in range(len(df_game['TimeStamp'])):
        time_passed = str2time(df_game['TimeStamp'][i]) - start_time
        if df_game['correct'][i] == 1:
            timestamp_list.append(time_passed.seconds)
        else:
            timestamp_list_wrong.append(time_passed.seconds)

    return timestamp_list


def merge_data(timestamp_list, bin_size):

    global final_df

    score_list = []
    score_list_norm = []

    for i in range(len(final_df)):
        timestamp = str2time(final_df['TimeStamp'][i+start_index])
        passed_time = timestamp - start_time

        passed_seconds = float(passed_time.seconds)
        passed_micros = passed_time.microseconds/1000000
        passed_time_float = passed_seconds + passed_micros

        min_border = passed_time_float - bin_size/2
        max_border = passed_time_float + bin_size/2

        points_in_bin = len([item for item in timestamp_list if min_border <= item < max_border])

        score_list.append(points_in_bin)

    min_hist = min(score_list)
    max_hist = max(score_list)

    for j in range(len(score_list)):
        score_norm = (score_list[j] - min_hist) / (max_hist - min_hist)
        score_list_norm.append(score_norm)

    conv_footprint = 2 * bin_size
    score_list_smoothed = np.convolve(score_list_norm, np.ones((conv_footprint,)) / conv_footprint, mode='same')

    final_df['Performance_'+str(bin_size)] = score_list_smoothed

    return score_list, score_list_norm, score_list_smoothed


def plot_data(save_figs=False):
    fig, ax = plt.subplots(3, 1)
    fig.subplots_adjust(top=0.8)
    fig.suptitle(str(log_folder), size=8, y=0.99, x=0.16)

    ax[0].set_title('Score over Time (binsize = 20s)')
    ax[0].plot(range(len(score_list_norm_20)), score_list_norm_20, color='royalblue')
    ax[0].plot(range(len(score_list_smoothed_20)), score_list_smoothed_20, color='navy')
    ax[0].legend(['Raw', 'Smoothed'], fontsize=5, loc='upper right')

    ax[1].set_title('Score over Time (binsize = 40s)')
    ax[1].plot(range(len(score_list_norm_40)), score_list_norm_40, color='lightcoral')
    ax[1].plot(range(len(score_list_smoothed_40)), score_list_smoothed_40, color='red')
    ax[1].legend(['Raw', 'Smoothed'], fontsize=5, loc='upper right')

    ax[2].set_title('Score - Density Plot')
    sns.kdeplot(score_list_norm_20, ax=ax[2], color="blue", linestyle="--")
    sns.kdeplot(score_list_smoothed_20, ax=ax[2], color="blue")
    sns.kdeplot(score_list_norm_40, ax=ax[2], color="red", linestyle="--")
    sns.kdeplot(score_list_smoothed_40, ax=ax[2], color="red")

    custom_lines = [Line2D([0], [0], color="blue", linestyle="--"),
                    Line2D([0], [0], color="blue"),
                    Line2D([0], [0], color="red", linestyle="--"),
                    Line2D([0], [0], color="red")]
    ax[2].legend(custom_lines, ['Binsize = 20 (raw)', 'Binsize = 20 (smoothed)', 'Binsize = 40 (raw)', 'Binsize = 20 (smoothed)'],
                 fontsize=5, loc='upper right')

    plt.tight_layout()
    plt.show()

    if save_figs:
        fig.savefig(log_folder+'performance.png')


if __name__ == "__main__":
    # Obtain subject list by defining log folder
    subject_list = glob("..\\data\\logs_*\\")

    for log_folder in subject_list:

        fft_path = log_folder + 'fft.csv'
        game_path = log_folder + 'game.csv'

        df_fft = pandas.read_csv(fft_path)
        df_game = pandas.read_csv(game_path)

        # Get timestamps for beginning and end of game stream
        start_time = str2time(df_game['TimeStamp'][0])
        stop_time = str2time(df_game['TimeStamp'][(len(df_game))-1])

        # Trim EEG dataset to fit game-stream timeline
        start_index, fft_time = trim_fft_data()

        final_df = df_fft

        timestamp_list = generate_timestamp_data()

        # Run the performance analysis for binsizes 20 and 40.
        for bin_size in [20, 40]:
            if bin_size == 20:
                score_list_20, score_list_norm_20, score_list_smoothed_20 = merge_data(timestamp_list, bin_size)
            elif bin_size == 40:
                score_list_40, score_list_norm_40, score_list_smoothed_40 = merge_data(timestamp_list, bin_size)
            else:
                raise ValueError('Wrong bin size .. ')

        # Plot the data for quality check
        plot_data(save_figs=True)

        # Store dataset
        final_df.to_csv(log_folder+"merged.csv", index=False)
