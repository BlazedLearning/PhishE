#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors: Hadi El Karhani, Yorgo Bou Samra, Riad Jamal
"""

import pandas as pd #pip install pandas

class CSV_Dataset_Cleanup:
    def __init__(self, CSV_file):
        self.CSV_file = CSV_file

    def Cleanup(self):
        #read csv file in Pandas
        data = pd.read_csv(self.CSV_file)

        # Drop unwanted columns
        data.drop(['index', 'event_ts', 'event_id', 'event_tags', 'attrib_type', 'event_tags', 'attrib_ts', 'attrib_tags'], inplace=True, axis=1)

        # Iterate through the dataset to clean it up
        # for index, row in data.iterrows():

            # Change the values of domains to URLs only
            # data.at[index, 'info'] = (data.at[index, 'info'].split(' - ')[1]).lower()

            # Change the values of event_tags to Phishing or not (Phishing = Yes, Non-Phishing = No)
            #for x in data.at[index, 'event_tags'].split('|'):

                # If False Positive then put No
            #    if x == 'False Positive':
            #        data.at[index, 'event_tags'] = 'No'

                # If Validated Threat then put Yes
            #    elif x == 'Validated Threat':
            #        data.at[index, 'event_tags'] = 'Yes'

                # If Suspicious then drop row because it doesn't matter to us
            #    elif x == 'Suspicious':
            #        data.drop([index], inplace = True)

            #    else:
            #        pass


        # Drop duplicate rows
        # data.drop_duplicates(subset='info', inplace = True)

        # Return Pandas csv file
        return data
