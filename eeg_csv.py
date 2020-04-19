import pandas as pd
import time
import main_test


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

    global raw_columns
    global fft_columns

    global raw_path
    global fft_path
    # TODO: Fix time-stamping... (datetime.datetime.now() ?)
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