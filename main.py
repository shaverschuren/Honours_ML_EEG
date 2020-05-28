# main.py
#
# This script is the main protocol for taking measurements, and runs through all necessary functions.
# It uses several threads to keep the program running.
#
# Author:   S.H.A. Verschuren
# Date:     23-04-2020

import os
import osc_stream
import game_gui
import selection_gui
import time
import datetime
import threading
import pandas


def generate_log_folder():
    # generate log folder name based on current time
    logs_date = str(datetime.datetime.now()).replace(':', '-')
    log_folder = 'data\\logs_' + logs_date[:10] + '_' + logs_date[11:19]
    os.mkdir(log_folder)

    return log_folder


def main():

    # ### Define several user options ###
    level_tryout = False  # Do you want to try a couple of sets from each level first?
    # ###################################

    # generate log folder based on current time
    log_folder = generate_log_folder()

    # level tryout module ...
    if level_tryout:
        for level in [1, 2, 3]:
            game_gui.main_gui(selected_level=level, tryout_opt=True, num_tryouts=(9-2*level))
            time.sleep(1)

    # GUI for level selection ...
    level_selection = selection_gui.main()

    game_thread = threading.Thread(target=game_gui.main_gui, args=(log_folder, int(level_selection), False))
    game_thread.start()

    osc_stream.init_osc_stream(log_folder=log_folder, animate_eeg=False)

    # Wait until game is closed
    while game_thread.is_alive():
        time.sleep(5)

    print("\nGame thread terminated..\n")

    osc_stream.store_results()

    print("\n======== Experiment completed ========")

    fft_path = log_folder + "\\fft.csv"
    raw_path = log_folder + "\\raw.csv"
    game_path = log_folder + "\\game.csv"

    df_fft = pandas.read_csv(fft_path)
    df_raw = pandas.read_csv(raw_path)
    df_game = pandas.read_csv(game_path)

    print("FFT:  ", len(df_fft))
    print("RAW:  ", len(df_raw))
    print("GAME: ", len(df_game))

    os._exit(0)


if __name__ == "__main__":
    main()