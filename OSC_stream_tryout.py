# OSC_stream_tryout.py
#
# This code is a tryout for the setup of an OSC stream with the muse headset via mindMonitor.
#
# Author: S.H.A. Verschuren
# Date:   17-4-2020

import argparse
import numpy as np
import pandas as pd
import datetime
from pythonosc import dispatcher, osc_server


def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4):
    # print("EEG per channel: ", ch1, ch2, ch3, ch4)
    data['EEG_0'][data_id] = ch1
    data['EEG_1'][data_id] = ch2
    data['EEG_2'][data_id] = ch3
    data['EEG_3'][data_id] = ch4
    data_id += 1

def alpha_handler(unused_addr, args, ch1, ch2, ch3, ch4, id):
    print("Alpha amp per channel: ", ch1, ch2, ch3, ch4)
    data['alpha_0'].append(ch1)
    data['alpha_1'].append(ch2)
    data['alpha_2'].append(ch3)
    data['alpha_3'].append(ch4)


def beta_handler(unused_addr, args, ch1, ch2, ch3, ch4, id):
    # print("Beta amp per channel: ", ch1, ch2, ch3, ch4)
    data['beta_0'].append(ch1)
    data['beta_1'].append(ch2)
    data['beta_2'].append(ch3)
    data['beta_3'].append(ch4)


def gamma_handler(unused_addr, args, ch1, ch2, ch3, ch4, id):
    # print("Gamma amp per channel: ", ch1, ch2, ch3, ch4)
    data['gamma_0'].append(ch1)
    data['gamma_1'].append(ch2)
    data['gamma_2'].append(ch3)
    data['gamma_3'].append(ch4)


def delta_handler(unused_addr, args, ch1, ch2, ch3, ch4, id):
    # print("Delta amp per channel: ", ch1, ch2, ch3, ch4)
    data['delta_0'].append(ch1)
    data['delta_1'].append(ch2)
    data['delta_2'].append(ch3)
    data['delta_3'].append(ch4)


def theta_handler(unused_addr, args, ch1, ch2, ch3, ch4, id):
    # print("Theta amp per channel: ", ch1, ch2, ch3, ch4)
    data['theta_0'].append(ch1)
    data['theta_1'].append(ch2)
    data['theta_2'].append(ch3)
    data['theta_3'].append(ch4)


def jaw_handler(unused_addr, args, ch1):
    print("Jaw clench? : ", ch1)


data = pd.DataFrame()

columns = ["EEG_0", "EEG_1", "EEG_2", "EEG_3", "alpha_0", "alpha_1", "alpha_2", "alpha_3", "beta_0", "beta_1", "beta_2",
           "beta_3", "gamma_0", "gamma_1", "gamma_2", "gamma_3", "delta_0", "delta_1", "delta_2", "delta_3", "theta_0",
           "theta_1", "theta_2", "theta_3"]

for column in columns:
    data[column] = ""

data_id = 0

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
    # dispatcher.map("/muse/elements/alpha_absolute", alpha_handler, "Alpha")
    # dispatcher.map("/muse/elements/beta_absolute", beta_handler, "Beta")
    # dispatcher.map("/muse/elements/gamma_absolute", gamma_handler, "Gamma")
    # dispatcher.map("/muse/elements/delta_absolute", delta_handler, "Delta")
    # dispatcher.map("/muse/elements/theta_absolute", theta_handler, "Theta")

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print('\nListening at ', ip_address, ' {', Port, '}')
    server.serve_forever()
