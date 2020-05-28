# create_dataset.py
#
# This script merges all subjects into one model-ready dataset.
#
# Author:   S.H.A. Verschuren
# Date:     17-5-2020

import pandas
import numpy as np
from glob import glob


if __name__ == "__main__":

    subject_list = glob("..\\data\\logs_*\\")

    merged_df = pandas.DataFrame()
    merged_df_avg = pandas.DataFrame()

    for subject in subject_list:
        data_path = subject + "merged.csv"
        subject_df = pandas.read_csv(data_path)

        subject_df_avg = subject_df[:(len(subject_df)//10)*10]
        subject_df_avg = subject_df_avg.groupby(np.arange(len(subject_df_avg)) // 10).mean()

        subject_df['subject'] = subject
        subject_df_avg['subject'] = subject

        if subject_list.index(subject) == 0:
            merged_df = subject_df
            merged_df_avg = subject_df_avg
        else:
            merged_df = merged_df.append(subject_df, ignore_index=True)
            merged_df_avg = merged_df_avg.append(subject_df_avg, ignore_index=True)

    merged_df = merged_df.sample(frac=1)
    merged_df_avg = merged_df_avg.sample(frac=1)

    # merged_df.to_csv("..\\data\\dataset.csv", index=False)
    merged_df_avg.to_csv("..\\data\\dataset_avg.csv", index=False)


