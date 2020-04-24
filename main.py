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


def generate_log_folder():
    # generate log folder name based on current time
    logs_date = str(datetime.datetime.now()).replace(':', '-')
    log_folder = 'data\\logs_' + logs_date[:10] + '_' + logs_date[11:19]
    os.mkdir(log_folder)

    return log_folder


if __name__ == "__main__":

    # ### Define several user options ###
    level_tryout = True  # Do you want to try a couple of sets from each level first?
    # ###################################

    # generate log folder based on current time
    log_folder = generate_log_folder()

    # level tryout module ...
    if level_tryout:
        for level in [1, 2, 3]:
            game_gui.main_gui(selected_level=level, tryout_opt=True, num_tryouts=(10-2*level))
            time.sleep(1.5)

    # GUI for level selection ...
    level_selection = selection_gui.main()

    # eeg_thread = threading.Thread(target=osc_stream.init_osc_stream, args=(log_folder, False))
    game_thread = threading.Thread(target=game_gui.main_gui, args=(log_folder, 1, True))

    osc_stream.init_osc_stream(log_folder, False)
    game_thread.start()