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

model = train_models.get_model()

model.load_weights("logs\\merge_models\\merge_model_0\\merge_model_0_weights.hdf5")
model.compile(loss='MSE', optimizer='adadelta', metrics=['MAE'])

score = model.evaluate(X_test, y_test, verbose=0)
print("MSE: ", score[0])
print("MAE: ", score[1])

predictions = model.predict(X_test, verbose=0)

df = pd.DataFrame()
df['Predictions'] = list(predictions)
df['Labels'] = y_test

plt.figure()

# plt.scatter(predictions, y_test)
ax = sns.jointplot(y="Predictions", x="Labels", data=df, xlim=[0, 1], ylim=[0, 1], color='blue', s=5, alpha=0.2)
# plot.ax_marg_x.set_xlim(0, 1)
# plot.ax_marg_y.set_ylim(0, 1)
# sns.lineplot([0, 1], [0, 100], color="red")
# plt.suptitle('Joint scatter/density plot for predicted data')
sns.lineplot([0, 1], [0, 1], color="red", ax=ax.ax_joint)
sns.lineplot([0, 1], [0+score[1], 1+score[1]], color="firebrick", ax=ax.ax_joint)
sns.lineplot([0, 1], [0+2*score[1], 1+2*score[1]], color="firebrick", ax=ax.ax_joint)
sns.lineplot([0, 1], [0-score[1], 1-score[1]], color="firebrick", ax=ax.ax_joint)
sns.lineplot([0, 1], [0-2*score[1], 1-2*score[1]], color="firebrick", ax=ax.ax_joint)
for i in [1,3]:
    ax.ax_joint.lines[i].set_linestyle("dashed")
for i in [2,4]:
    ax.ax_joint.lines[i].set_linestyle("dotted")

ax.ax_joint.legend(['Reference', '68% CI', '95% CI'])

plt.show()