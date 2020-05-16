# inspect_subjects.py
#
# This script generates inspection plots for all subjects, based on the merged datasets.
# Plots are generated based on EEG and performance data.
#
# Author:   S.H.A. Verschuren
# Date:     16-5-2020

from glob import glob
import pandas
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import datetime
import seaborn as sns


def generate_eeg_plot(data):
    plot_df = pandas.DataFrame()

    for channel in ['AF', 'TP']:
        for wave in ['alpha', 'beta', 'gamma', 'delta', 'theta']:
            column_name = channel + '_' + wave
            if channel == 'AF':
                channel_ns = ['1', '2']
            elif channel == 'TP':
                channel_ns = ['0', '3']
            else:
                raise ValueError('Wrong channel name')

            PSD_value_list = (data[wave+'_'+channel_ns[0]] + data[wave+'_'+channel_ns[1]]) / 2

            conv_footprint = 100
            PSD_smoothed = np.convolve(PSD_value_list, np.ones((conv_footprint,)) / conv_footprint, mode='same')

            plot_df[column_name] = PSD_value_list
            plot_df[column_name+'_smoothed'] = PSD_smoothed

    return plot_df


def plot_data(plot_data, save_figs=False):

    fig, ax = plt.subplots(3, 1)
    fig.subplots_adjust(top=0.8)
    fig.suptitle(str(log_folder), size=8, y=0.99, x=0.16)

    ax[0].set_title('EEG (AF7-AF8)')
    ax[0].plot(range(len(plot_data)), plot_data['AF_alpha_smoothed'], linewidth=1)
    ax[0].plot(range(len(plot_data)), plot_data['AF_beta_smoothed'], linewidth=1)
    ax[0].plot(range(len(plot_data)), plot_data['AF_gamma_smoothed'], linewidth=1)
    ax[0].plot(range(len(plot_data)), plot_data['AF_delta_smoothed'], linewidth=1)
    ax[0].plot(range(len(plot_data)), plot_data['AF_theta_smoothed'], linewidth=1)
    ax[0].plot(range(len(plot_data)), plot_data['AF_alpha'], linewidth=0.5, alpha=0.2)
    ax[0].plot(range(len(plot_data)), plot_data['AF_beta'], linewidth=0.5, alpha=0.2)
    ax[0].plot(range(len(plot_data)), plot_data['AF_gamma'], linewidth=0.5, alpha=0.2)
    ax[0].plot(range(len(plot_data)), plot_data['AF_delta'], linewidth=0.5, alpha=0.2)
    ax[0].plot(range(len(plot_data)), plot_data['AF_theta'], linewidth=0.5, alpha=0.2)
    ax[0].legend(['Alpha', 'Beta', 'Gamma', 'Delta', 'Theta'], fontsize=5, loc='upper right')
    ymax_0 = max([max(plot_data['AF_alpha_smoothed']), max(plot_data['AF_beta_smoothed']),
                  max(plot_data['AF_gamma_smoothed']), max(plot_data['AF_delta_smoothed']),
                  max(plot_data['AF_theta_smoothed'])])
    ymin_0 = min([min(plot_data['AF_alpha_smoothed']), min(plot_data['AF_beta_smoothed']),
                  min(plot_data['AF_gamma_smoothed']), min(plot_data['AF_delta_smoothed']),
                  min(plot_data['AF_theta_smoothed'])])
    ax[0].set_ylim([ymin_0*1.1, ymax_0*1.1])

    ax[1].set_title('EEG (TP9-TP10)')
    ax[1].plot(range(len(plot_data)), plot_data['TP_alpha_smoothed'], linewidth=1)
    ax[1].plot(range(len(plot_data)), plot_data['TP_beta_smoothed'], linewidth=1)
    ax[1].plot(range(len(plot_data)), plot_data['TP_gamma_smoothed'], linewidth=1)
    ax[1].plot(range(len(plot_data)), plot_data['TP_delta_smoothed'], linewidth=1)
    ax[1].plot(range(len(plot_data)), plot_data['TP_theta_smoothed'], linewidth=1)
    ax[1].plot(range(len(plot_data)), plot_data['TP_alpha'], linewidth=0.5, alpha=0.2)
    ax[1].plot(range(len(plot_data)), plot_data['TP_beta'], linewidth=0.5, alpha=0.2)
    ax[1].plot(range(len(plot_data)), plot_data['TP_gamma'], linewidth=0.5, alpha=0.2)
    ax[1].plot(range(len(plot_data)), plot_data['TP_delta'], linewidth=0.5, alpha=0.2)
    ax[1].plot(range(len(plot_data)), plot_data['TP_theta'], linewidth=0.5, alpha=0.2)
    ax[1].legend(['Alpha', 'Beta', 'Gamma', 'Delta', 'Theta'], fontsize=5, loc='upper right')
    ymax_1 = max([max(plot_data['TP_alpha_smoothed']), max(plot_data['TP_beta_smoothed']),
                  max(plot_data['TP_gamma_smoothed']), max(plot_data['TP_delta_smoothed']),
                  max(plot_data['TP_theta_smoothed'])])
    ymin_1 = min([min(plot_data['TP_alpha_smoothed']), min(plot_data['TP_beta_smoothed']),
                  min(plot_data['TP_gamma_smoothed']), min(plot_data['TP_delta_smoothed']),
                  min(plot_data['TP_theta_smoothed'])])
    ax[1].set_ylim([ymin_1 * 1.1, ymax_1 * 1.1])

    ax[2].set_title('Performance')
    ax[2].plot(range(len(df)), df['Performance_20'], color='lightcoral')
    ax[2].plot(range(len(df)), df['Performance_40'], color='red')
    ax[2].legend(['Kernel = 20s', 'Kernel = 40s'], fontsize=5, loc='upper right')

    plt.tight_layout()
    plt.show()

    if save_figs:
        fig.savefig(log_folder+'inspection.png')


if __name__ == "__main__":

    subject_list = glob("..\\data\\logs_*\\")

    for log_folder in subject_list:

        data_path = log_folder + 'merged.csv'
        df = pandas.read_csv(data_path)

        # AF_alpha, AF_beta, AF_gamma, AF_delta, AF_theta, \
        # TP_alpha, TP_beta, TP_gamma, TP_delta, TP_theta = generate_eeg_plot(df)

        plot_df = generate_eeg_plot(df)

        plot_data(plot_df, True)
