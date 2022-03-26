#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors: Hadi El Karhani, Yorgo Bou Samra, Riad Jamal
"""
import pandas as pd
import numpy as np
import sklearn # pip3 install scikit-learn==0.23.2
from sklearn import svm , preprocessing
import pickle
import Configuration

class Detect:
    def __init__(self, datafile ,weights = Configuration.ModelFile()):
        self.df = pd.read_csv(datafile)
        self.df = self.df.fillna(self.df.median()).clip(-1e11,1e11)
        self.X = self.df.values
        self.loaded_model = pickle.load(open(weights, 'rb'))

    def predict(self):
        result = self.loaded_model.predict(self.X)
        list_result = result.tolist()
        for index in range(len(list_result)):
            if list_result[index] == -1:
                list_result[index] = "Phishing attack"
            elif list_result[index] == 1:
                list_result[index] = "Safe"
            else:
                pass

        return list_result

#if __name__ == '__main__':
#    filename = input("Please Enter File Path Here: ")
#    model_instance = Detect(filename)
#    print(model_instance.predict())
