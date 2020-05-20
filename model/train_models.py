# train_models.py
#
# This script trains the actual model based on the EEG and performance data from ..\\data\\dataset.csv
#
# Author:   S.H.A. Verschuren
# Date:     17-5-2020

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, InputLayer, Dropout
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping
import os


def load_dataset(data_path="..\\data\\dataset_avg.csv", train_test_ratio=5):
    dataset_full = pd.read_csv(data_path)

    dataset_train = dataset_full[len(dataset_full)//train_test_ratio:]
    dataset_test = dataset_full[:len(dataset_full)//train_test_ratio]

    train_data = dataset_train.to_numpy()
    test_data = dataset_test.to_numpy()

    # X_train = train_data[:, range(1, 21)]
    # y_train = train_data[:, 22]
    # X_test = test_data[:, range(1, 21)]
    # y_test = test_data[:, 22]

    X_train = train_data[:, range(0, 20)]
    y_train = train_data[:, 21]
    X_test = test_data[:, range(0, 20)]
    y_test = test_data[:, 21]

    # derive a validation set from the training set
    # the original training set is split into
    # new training set (90%) and a validation set (10%)
    X_train, X_val = train_test_split(X_train, test_size=0.20, random_state=101)
    y_train, y_val = train_test_split(y_train, test_size=0.20, random_state=101)

    # Convert data to tensorflow-compatible format
    X_train = np.asarray(X_train).astype(np.float32)
    X_val = np.asarray(X_val).astype(np.float32)
    y_train = np.asarray(y_train).astype(np.float32)
    y_val = np.asarray(y_val).astype(np.float32)

    X_test = np.asarray(X_test).astype(np.float32)
    y_test = np.asarray(y_test).astype(np.float32)

    return X_train, X_val, y_train, y_val, X_test, y_test


def get_model():
    model = Sequential()
    model.add(InputLayer(input_shape=(20,)))
    model.add(Dense(40, activation='relu'))
    model.add(Dropout(0.05))
    model.add(Dense(80, activation='relu'))
    model.add(Dropout(0.05))
    model.add(Dense(60, activation='relu'))
    model.add(Dropout(0.05))
    model.add(Dense(20, activation='relu'))
    model.add(Dropout(0.05))
    model.add(Dense(1, activation='linear'))
    # model.add(Dense(1, activation='sigmoid'))

    return model


if __name__ == "__main__":
    print("====== INIT train_models.py ======\n")

    print("Loading data ...")
    X_train, X_val, y_train, y_val, X_test, y_test = load_dataset()
    print("Loading complete. Found:")
    print("", len(X_train), "training datapoints\n", len(X_val), "validation datapoints\n", len(X_test), "test datapoints\n")

    n_models = 5

    print("-- Start training process on", n_models, "models --")
    for model_nr in range(n_models):
        print("\nInit training model nr.", model_nr)
        model = get_model()

        # compile the model
        model.compile(loss='MSE', optimizer='adadelta', metrics=['MAE'])

        # use this variable to name your model
        model_name = "merge_model_" + str(model_nr)

        log_dir = os.path.join("logs", "merge_models", model_name)
        weights_filepath = model_name + '_weights.hdf5'
        model_filepath = model_name + '.json'

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        else:
            log_dir = log_dir + "_2"
            os.makedirs(log_dir)

        # Store model structure in json file
        model_json = model.to_json()  # serialize model to JSON
        with open(os.path.join(log_dir, model_filepath), 'w') as json_file:
            json_file.write(model_json)

        # Callbacks
        tensorboard = TensorBoard(log_dir)
        checkpoint = ModelCheckpoint(os.path.join(log_dir, weights_filepath), monitor='val_loss',
                                     verbose=1, save_best_only=True, mode='min')
        earlystop_callback = EarlyStopping(monitor='val_loss', min_delta=0.000001, patience=100)

        callbacks_list = [checkpoint, tensorboard, earlystop_callback]

        # train the model
        model.fit(X_train, y_train, batch_size=16, epochs=50000, verbose=2, validation_data=(X_val, y_val), callbacks=callbacks_list)

        score = model.evaluate(X_test, y_test, verbose=0)
        print("\nMSE: ", score[0])
        print("MAE: ", score[1])

    print("\n-- END training process --")
    print("\nLogs may be found in", "..\\"+log_dir[:len(log_dir)]+"*")
    print("Bye!")

