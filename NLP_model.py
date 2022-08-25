#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Hadi El Karhani, Yorgo Bou Samra, Riad Jamal
"""
import pickle
import pandas as pd
import Configuration

class Detect_NLP:
    """
    Class used to load NLP model in the constructor
    and output predictions in the predic functiono
    """
    def __init__(self, datafile ,pickles = str(Configuration.NLPModelFile())):
        self.df = pd.read_csv(datafile)
        self.description_list = self.df['SMS'].tolist()
        self.X = self.df.values
        self.loaded_model,self.X_vector,self.X_transform = pickle.load(open(pickles, 'rb'))


    def predict(self):
        X_counts = self.X_vector.transform(self.description_list)
        X_tfidf = self.X_transform.transform(X_counts)

        result = self.loaded_model.predict(X_tfidf)
        list_result = result.tolist()
        for index in range(len(list_result)):
            if list_result[index] == 0:
                list_result[index] = "Malicious"
            elif list_result[index] == 1:
                list_result[index] = "Safe"
            else:
                pass

        return list_result
