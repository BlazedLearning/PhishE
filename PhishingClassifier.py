#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors: Hadi El Karhani, Yorgo Bou Samra, Riad Jamal
"""

from Dataset_Cleanup import CSV_Dataset_Cleanup
from FeaturesExtraction import FExtract
from model import Detect
import Configuration
import csv

print("1: Check new entries on MISP platform.")
print("2: Take a CSV of threats and classify them.")
print("3: Exit program.\n")

while True:
    option = input("Choose your option: ")
    if option == "1":
        print("Still in progress of finalzing.")

    elif option == "2":
        CSV_file = str(input("Write the CSV file name with the extension: "))
        # Training-data-TSIRT-labeled-phish.csv
        try:
            data = CSV_Dataset_Cleanup(CSV_file).Cleanup()
        except FileNotFoundError:
            print("The file/path you entered cannot be found.")
            break

        columns_features = ["having_IP_Address", "URL_Length", "Shortining_Service", "having_At_Symbol", "double_slash_redirecting", "Prefix_Suffix", "having_Sub_Domain", "SSLfinal_State", "Domain_registeration_length", "Favicon", "port", "HTTPS_token", "Request_URL", "URL_of_Anchor", "Links_in_tags", "SFH", "Submitting_to_email", "Abnormal_URL", "Redirect", \
                            "on_mouseover", "RightClick", "popUpWidnow", "Iframe", "age_of_domain", "DNSRecord", "web_traffic", "Page_Rank", "Google_Index", "Links_pointing_to_page", "Statistical_report"]


        with open(str(Configuration.FExtractFile()), 'a') as f:
            write = csv.writer(f)
            write.writerow(columns_features) # Just for the first run

            Requests = 0
            Domains = []
            for index, row in data.iterrows():
                if Requests < int(Configuration.Requests()) and Requests < 80: # For unlimited requests please check googlesearch as a service

                    try:
                        features = FExtract(index, data).generate_data_set(data.at[index, 'info'])

                    except requests.exceptions.HTTPError:
                        print("Request limit with googlesearch is hit, try again in 30 minutes.")


                    if type(features) == dict: # Check if output is a dictionnary

                        values = features.values()
                        values_list = list(values)

                        """ The below commented code was used for training purposes """
                        #if data.at[index, 'event_tags'] == "Yes":
                        #    values_list.append(-1)
                        #else:
                        #    values_list.append(1)

                        Requests += 1
                        Domains.append(data.at[index, 'info'])
                        write.writerow(values_list)

                    else:
                        pass

                else:
                    print("Request limit asked for has been hit. (If not, then request limit with googlesearch has been hit) ")
                    break

        Classifications = Detect(str(Configuration.FExtractFile())).predict()
        with open(str(Configuration.ClassificationsFile()), 'a') as g:
            write = csv.writer(g)

            for i in range(len(Domains)):
                row = [Domains[i], Classifications[i]]
                write.writerow(row)


    elif option == "3":
        break

    else:
        print("Unavailable option.")
