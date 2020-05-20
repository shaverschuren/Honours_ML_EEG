# plot_model_performance.py
#
# This script performs a quality analysis plot for the final model
#
# Author:   S.H.A. Verschuren
# Date:     20-5-2020

import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import InputLayer, Dense, Dropout
from sklearn.metrics import mean_absolute_error
import os
import train_models

X_train, X_val, y_train, y_val, X_test, y_test = train_models.load_dataset()

# model = train_models.get_model()

model = Sequential()
model.add(InputLayer(input_shape=(20,)))
model.add(Dense(25, activation='relu'))
model.add(Dropout(0.05))
model.add(Dense(50, activation='relu'))
model.add(Dropout(0.05))
model.add(Dense(50, activation='relu'))
model.add(Dropout(0.05))
model.add(Dense(75, activation='relu'))
model.add(Dropout(0.05))
model.add(Dense(50, activation='relu'))
model.add(Dropout(0.05))
model.add(Dense(25, activation='relu'))
model.add(Dropout(0.05))
model.add(Dense(10, activation='relu'))
model.add(Dropout(0.05))
model.add(Dense(1, activation='linear'))

model.load_weights("logs\\tryout_logs\\model_20000iter_adadelta_float_y_nosigm\\20200520-015141\\model_20000iter_adadelta_float_y_nosigm_weights.hdf5")
model.compile(loss='MSE', optimizer='adadelta', metrics=['MAE'])

score = model.evaluate(X_test, y_test, verbose=0)
print("MSE: ", score[0])
print("MAE: ", score[1])

predictions = model.predict(X_test, verbose=0)

df = pd.DataFrame()
df['predictions'] = list(predictions)
df['labels'] = y_test

# plt.scatter(predictions, y_test)
plot = sns.jointplot(x="predictions", y="labels", data=df)
plot.ax_marg_x.set_xlim(0, 1)
plot.ax_marg_y.set_ylim(0, 1)

plt.show()