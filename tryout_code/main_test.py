# # OSC_stream_tryout.py
# #
# # This code is a tryout for the setup of an OSC stream with the muse headset via mindMonitor.
# #
# # Author: S.H.A. Verschuren
# # Date:   17-4-2020
# # TODO: Implement Tkinter thread
#
# import datetime
# import os
# import tkinter
# import threading
# from eeg_stream import *
#
#
# def gui_func():
#     print("hi!")
#
#
# if __name__ == '__main__':
#     raw_columns = ["TimeStamp", "EEG_0", "EEG_1", "EEG_2", "EEG_3"]
#
#     fft_columns = ["TimeStamp", "alpha_0", "alpha_1", "alpha_2", "alpha_3", "beta_0",
#                "beta_1", "beta_2", "beta_3", "gamma_0", "gamma_1", "gamma_2", "gamma_3", "delta_0", "delta_1", "delta_2",
#                "delta_3", "theta_0", "theta_1", "theta_2", "theta_3"]
#
#     raw_data = pd.DataFrame(columns=raw_columns)
#     fft_data = pd.DataFrame(columns=fft_columns)
#
#     eeg_data = (0,0,0,0)
#     alpha_data = (0,0,0,0)
#     beta_data = (0,0,0,0)
#     gamma_data = (0,0,0,0)
#     delta_data = (0,0,0,0)
#     theta_data = (0,0,0,0)
#
#     raw_record_nr = 0
#     fft_record_nr = 0
#
#     # csv init
#     logs_date = str(datetime.datetime.now()).replace(':', '-')
#     log_folder = r'data\logs_' + logs_date[:10] + '_' + logs_date[11:19]
#     raw_path = log_folder + '\\raw.csv'
#     fft_path = log_folder + '\\fft.csv'
#
#     os.mkdir(log_folder)
#
#     raw_data.to_csv(raw_path, index=False)
#     fft_data.to_csv(fft_path, index=False)
#
#     osc_thread = threading.Thread(target=osc_stream)  # daemon = True / False
#     gui_thread = threading.Thread(target=gui_func)
#
#     osc_thread.start()
#     time.sleep(1)
#     gui_thread.start()