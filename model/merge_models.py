# (NOT USED) merge_models.py
#
# This script performs the decision merging for the pre-trained models and evaluates their performance.
#
# Author:   S.H.A. Verschuren
# Date:     20-5-2020

# import pandas as pd
# import numpy as np
# # import tensorflow as tf
# from sklearn.metrics import mean_absolute_error
# import os
# import train_models
#
# X_train, X_val, y_train, y_val, X_test, y_test = train_models.load_dataset()
#
# predictions = [[]]*5
#
# for model_nr in range(5):
#     print("\nModel nr.", model_nr)
#     model = train_models.get_model()
#     model.load_weights("logs\\merge_models\\merge_model_"+str(model_nr)+"\\merge_model_"+str(model_nr)+"_weights.hdf5")
#     model.compile(loss='MSE', optimizer='adadelta', metrics=['MAE'])
#
#     score = model.evaluate(X_test, y_test, verbose=0)
#     print("MSE: ", score[0])
#     print("MAE: ", score[1])
#
#     predictions[model_nr] = model.predict(X_test, verbose=0)
#
# predictions_avg = []
#
# for i in range(len(predictions[0])):
#     predictions_list = []
#     for j in range(5):
#         predictions_list.append(float(predictions[j][i]))
#     predictions_avg.append(np.mean(predictions_list))
#
# # Calc MAE
# MAE = mean_absolute_error(y_test, predictions_avg)
# print("\n\nCombined MAE: "+str(MAE))


