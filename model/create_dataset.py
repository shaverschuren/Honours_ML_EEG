# create_dataset.py
#
# This script merges all subjects into one model-ready dataset.
#
# Author:   S.H.A. Verschuren
# Date:     17-5-2020

import pandas
from glob import glob


if __name__ == "__main__":

    subject_list = glob("..\\data\\logs_*\\")

    merged_df = pandas.DataFrame()

    for subject in subject_list:
        data_path = subject + "merged.csv"
        subject_df = pandas.read_csv(data_path)

        subject_df['subject'] = subject

        if subject_list.index(subject) == 0:
            merged_df = subject_df
        else:
            merged_df = merged_df.append(subject_df, ignore_index=True)

    merged_df = merged_df.sample(frac=1)

    merged_df.to_csv("..\\data\\dataset.csv", index=False)


