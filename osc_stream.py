# OSC_stream_tryout.py
#
# This code is a tryout for the setup of an OSC stream with the muse headset via mindMonitor.
#
# Author: S.H.A. Verschuren
# Date:   17-4-2020
#

import argparse
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
from pythonosc import dispatcher, osc_server
import matplotlib
matplotlib.use("TkAgg")  # Enables live plotting (e.g. eeg stream)


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


def osc_stream(ip_address="0.0.0.0",port=5000):
    print('======== INIT OSC STREAM ========')
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=ip_address)
    parser.add_argument("--port", default=port)
    args = parser.parse_args()
    global dispatcher
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
    print('\nListening at ', ip_address, ' {', port, '}')
    server.serve_forever()


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
    global plot_raw_data

    global raw_data
    global fft_data

    global raw_record_nr
    global fft_record_nr
    # TODO: Fix time-stamping... (datetime.datetime.now() ?)
    append_row = [datetime.datetime.now()]

    if frame_type == 'raw':
        data_point = eeg_data
        for channel in range(4):
            append_row.append(data_point[channel])

        append_df = pd.DataFrame([append_row], columns=raw_columns)
        raw_data = pd.concat([raw_data, append_df], ignore_index=True)

        plot_raw_data = pd.concat([plot_raw_data, append_df], ignore_index=True)
        if len(plot_raw_data) > 1500:
            plot_raw_data = plot_raw_data[-1000:]
        raw_record_nr += 1

        # print("RAW: ", raw_data.shape)
        if raw_record_nr % 2000 == 0:
            raw_data.to_csv(raw_path, mode='a', index=False, header=False)
            raw_data = pd.DataFrame(columns=raw_columns)
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
            fft_data = pd.DataFrame(columns=fft_columns)
            print("Saved FFT data to", fft_path)
    else:
        raise ValueError('Wrong frame type ...')


def animate(i):
    start = datetime.datetime.now()
    plot_data = pd.concat([null_df, plot_raw_data], ignore_index=True)[-500:]
    xs = range(500)
    ys1 = plot_data['EEG_0']
    ys2 = plot_data['EEG_1']
    ys3 = plot_data['EEG_2']
    ys4 = plot_data['EEG_3']

    ax1.clear()
    ax1.set_xlim(0, 500)
    ax1.patch.set_facecolor('#000000')
    ax1.plot(xs, ys1, 'b-', linewidth=1, alpha=0.5)

    ax2.clear()
    ax2.set_xlim(0, 500)
    ax2.patch.set_facecolor('#000000')
    ax2.plot(xs, ys2, 'r-', linewidth=1, alpha=0.5)

    ax3.clear()
    ax3.set_xlim(0, 500)
    ax3.patch.set_facecolor('#000000')
    ax3.plot(xs, ys3, 'c-', linewidth=1, alpha=0.5)

    ax4.clear()
    ax4.set_xlim(0, 500)
    ax4.patch.set_facecolor('#000000')
    ax4.plot(xs, ys4, 'g-', linewidth=1, alpha=0.5)
    stop = datetime.datetime.now()
    print(stop-start)
    return [ax1, ax2, ax3, ax4]


def init_osc_stream(log_folder="data\\test_logs", animate_eeg=False):
    global raw_path, fft_path
    global raw_columns, fft_columns
    global raw_data, fft_data
    global null_df, plot_raw_data
    global eeg_data, alpha_data, beta_data, gamma_data, delta_data, theta_data
    global raw_record_nr, fft_record_nr
    global fig, ax1, ax2, ax3, ax4

    raw_columns = ["TimeStamp", "EEG_0", "EEG_1", "EEG_2", "EEG_3"]

    fft_columns = ["TimeStamp", "alpha_0", "alpha_1", "alpha_2", "alpha_3", "beta_0",
               "beta_1", "beta_2", "beta_3", "gamma_0", "gamma_1", "gamma_2", "gamma_3", "delta_0", "delta_1", "delta_2",
               "delta_3", "theta_0", "theta_1", "theta_2", "theta_3"]

    raw_data = pd.DataFrame(columns=raw_columns)
    fft_data = pd.DataFrame(columns=fft_columns)

    plot_raw_data = raw_data
    null_df = pd.DataFrame([[0,0,0,0,0]]*1000, columns=raw_columns)

    eeg_data = (0,0,0,0)
    alpha_data = (0,0,0,0)
    beta_data = (0,0,0,0)
    gamma_data = (0,0,0,0)
    delta_data = (0,0,0,0)
    theta_data = (0,0,0,0)

    raw_record_nr = 0
    fft_record_nr = 0

    raw_path = log_folder + '\\raw.csv'
    fft_path = log_folder + '\\fft.csv'

    raw_data.to_csv(raw_path, index=False)
    fft_data.to_csv(fft_path, index=False)

    osc_thread = threading.Thread(target=osc_stream)
    osc_thread.start()

    fig = plt.figure()
    fig.patch.set_facecolor('#000000')
    ax1 = fig.add_subplot(4, 1, 1)
    ax2 = fig.add_subplot(4, 1, 2)
    ax3 = fig.add_subplot(4, 1, 3)
    ax4 = fig.add_subplot(4, 1, 4)

    if animate_eeg:
        ani = animation.FuncAnimation(fig, animate, interval=50, blit=True)  # Don't use during actual data gathering !
        plt.show()


if __name__ == "__main__":
    init_osc_stream()