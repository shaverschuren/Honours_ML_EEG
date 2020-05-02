# level_tryout.py
#
# This script runs through 3 tryout levels to get a baseline on the subject's performance.
#
# Author:   S.H.A. Verschuren
# Date:     02-05-2020

import os
import game_gui
import time


def main():

    # level tryout module ...
    for level in [1, 2, 3]:
        game_gui.main_gui(selected_level=level, tryout_opt=True, num_tryouts=(9-2*level))
        time.sleep(0.2)

    os._exit(0)


if __name__ == "__main__":
    main()