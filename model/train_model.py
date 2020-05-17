# train_model.py
#
# This script trains the actual model based on the EEG and performance data from ..\\data\\dataset.csv
#
# Author:   S.H.A. Verschuren
# Date:     17-5-2020

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense, InputLayer
from tensorflow.keras.callbacks import TensorBoard
import os
import warnings
import datetime


warnings.simplefilter("ignore")             # Suppress run-time warnings etc ...
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'    # Suppress debugging info ...

dataset_full = pd.read_csv("..\\data\\dataset.csv")

dataset_train = dataset_full[:len(dataset_full)//5]
dataset_test = dataset_full[len(dataset_full)//5:]

train_data = dataset_train.to_numpy()
test_data = dataset_train.to_numpy()

X_train = train_data[:, range(1, 21)]
y_train = train_data[:, 22]
X_test = test_data[:, range(1, 21)]
y_test = test_data[:, 22]

# derive a validation set from the training set
# the original training set is split into
# new training set (90%) and a validation set (10%)
X_train, X_val = train_test_split(X_train, test_size=0.10, random_state=101)
y_train, y_val = train_test_split(y_train, test_size=0.10, random_state=101)

# convert the datatype to float32
X_train = X_train.astype('float32')
X_val = X_val.astype('float32')
X_test = X_test.astype('float32')


model = Sequential()
model.add(InputLayer(input_shape=(20,)))
# model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))


# compile the model
model.compile(loss='mean_absolute_error', optimizer='sgd', metrics=['accuracy'])

# use this variable to name your model
model_name="my_first_model"

# create a way to monitor our model in Tensorboard

log_dir = os.path.join(
    "logs",
    model_name,
    datetime.datetime.now().strftime("%Y%m%d-%H%M%S"),
)
tensorboard = TensorBoard(log_dir)

# train the model
model.fit(X_train, y_train, batch_size=32, epochs=10, verbose=1, validation_data=(X_val, y_val), callbacks=[tensorboard])

