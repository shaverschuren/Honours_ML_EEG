# OSC_stream_tryout.py
#
# This code is a tryout for the setup of an OSC stream with the muse headset via mindMonitor.
#
# Author: S.H.A. Verschuren
# Date:   17-4-2020
# TODO: Fix timestamping ...

import argparse
import numpy as np
import pandas as pd
import csv
import time
import datetime
import os
from pythonosc import dispatcher, osc_server


def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4):
    # print("EEG per channel: ", ch1, ch2, ch3, ch4)
    values = (ch1, ch2, ch3, ch4)
    update_data('EEG', values)
    write_data('raw')


def alpha_handler(unused_addr, args, ch1, ch2, ch3, ch4):
    # print("Alpha amp per channel: ", ch1, ch2, ch3, ch4)
    values = (ch1, ch2, ch3, ch4)
    update_data('alpha', values)


def beta_handler(unused_addr, args, ch1, ch2, ch3, ch4):
    # print("Beta amp per channel: ", ch1, ch2, ch3, ch4)
    values = (ch1, ch2, ch3, ch4)
    update_data('beta', values)


def gamma_handler(unused_addr, args, ch1, ch2, ch3, ch4):
    # print("Gamma amp per channel: ", ch1, ch2, ch3, ch4)
    values = (ch1, ch2, ch3, ch4)
    update_data('gamma', values)


def delta_handler(unused_addr, args, ch1, ch2, ch3, ch4):
    # print("Delta amp per channel: ", ch1, ch2, ch3, ch4)
    values = (ch1, ch2, ch3, ch4)
    update_data('delta', values)


def theta_handler(unused_addr, args, ch1, ch2, ch3, ch4):
    # print("Theta amp per channel: ", ch1, ch2, ch3, ch4)
    values = (ch1, ch2, ch3, ch4)
    update_data('theta', values)
    write_data('fft')


# def jaw_handler(unused_addr, args, ch1):
#     # print("Jaw clench? : ", ch1)


def update_data(data_type="", values=()):

    if data_type == "EEG":
        global eeg_data
        eeg_data = values
        # print(eeg_data)
    elif data_type == "alpha":
        global alpha_data
        alpha_data = values
    elif data_type == "beta":
        global beta_data
        beta_data = values
    elif data_type == "gamma":
        global gamma_data
        gamma_data = values
    elif data_type == "delta":
        global delta_data
        delta_data = values
    elif data_type == "theta":
        global theta_data
        theta_data = values
    else:
        raise ValueError('Wrong data type ...')

    # print('data updated: ', data_type, '=', values)


def write_data(frame_type=''):
    global raw_data
    global fft_data

    global raw_record_nr
    global fft_record_nr

    append_row = [time.perf_counter()]

    if frame_type == 'raw':
        data_point = eeg_data
        for channel in range(4):
            append_row.append(data_point[channel])

        append_df = pd.DataFrame([append_row], columns=raw_columns)
        raw_data = pd.concat([raw_data, append_df], ignore_index=True)
        raw_record_nr += 1
        # print("RAW: ", raw_data.shape)
        if raw_record_nr % 2000 == 0:
            raw_data.to_csv(raw_path, mode='a', index=False, header=False)
            print("Saved RAW data to", raw_path)

    elif frame_type == 'fft':
        for data_type in ["alpha", "beta", "gamma", "delta", "theta"]:
            if data_type == "alpha":
                data_point = alpha_data
            elif data_type == "beta":
                data_point = beta_data
            elif data_type == "gamma":
                data_point = gamma_data
            elif data_type == "delta":
                data_point = delta_data
            elif data_type == "theta":
                data_point = theta_data
            else:
                raise ValueError('Wrong data type ...')

            for channel in range(4):
                append_row.append(data_point[channel])

        append_df = pd.DataFrame([append_row], columns=fft_columns)
        fft_data = pd.concat([fft_data, append_df], ignore_index=True)
        fft_record_nr += 1
        # print("FFT: ", fft_data.shape)
        if fft_record_nr % 100 == 0:
            fft_data.to_csv(fft_path, mode='a', index=False, header=False)
            print("Saved FFT data to", fft_path)
    else:
        raise ValueError('Wrong frame type ...')


raw_columns = ["TimeStamp", "EEG_0", "EEG_1", "EEG_2", "EEG_3"]

fft_columns = ["TimeStamp", "alpha_0", "alpha_1", "alpha_2", "alpha_3", "beta_0",
           "beta_1", "beta_2", "beta_3", "gamma_0", "gamma_1", "gamma_2", "gamma_3", "delta_0", "delta_1", "delta_2",
           "delta_3", "theta_0", "theta_1", "theta_2", "theta_3"]

raw_data = pd.DataFrame(columns=raw_columns)
fft_data = pd.DataFrame(columns=fft_columns)

eeg_data = (0,0,0,0)
alpha_data = (0,0,0,0)
beta_data = (0,0,0,0)
gamma_data = (0,0,0,0)
delta_data = (0,0,0,0)
theta_data = (0,0,0,0)

raw_record_nr = 0
fft_record_nr = 0

# csv init
logs_date = str(datetime.datetime.now()).replace(':', '-')
log_folder = r'data\logs_' + logs_date[:10] + '_' + logs_date[11:19]
raw_path = log_folder + '\\raw.csv'
fft_path = log_folder + '\\fft.csv'

os.mkdir(log_folder)

raw_data.to_csv(raw_path, index=False)
fft_data.to_csv(fft_path, index=False)

if __name__ == '__main__':
    print('======== INIT OSC STREAM ========')
    ip_address = "0.0.0.0"
    Port = 5000
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=ip_address)
    parser.add_argument("--port", default=Port)
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/debug", print)
    dispatcher.map("/muse/eeg", eeg_handler, "EEG")
    # dispatcher.map("/muse/elements/jaw_clench", jaw_handler, "JAW")
    dispatcher.map("/muse/elements/alpha_absolute", alpha_handler, "Alpha")
    dispatcher.map("/muse/elements/beta_absolute", beta_handler, "Beta")
    dispatcher.map("/muse/elements/gamma_absolute", gamma_handler, "Gamma")
    dispatcher.map("/muse/elements/delta_absolute", delta_handler, "Delta")
    dispatcher.map("/muse/elements/theta_absolute", theta_handler, "Theta")

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print('\nListening at ', ip_address, ' {', Port, '}')
    server.serve_forever()
