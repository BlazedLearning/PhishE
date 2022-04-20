#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors: Hadi El Karhani, Yorgo Bou Samra, Riad Jamal
"""

from Dataset_Cleanup import CSV_Dataset_Cleanup
from FeaturesExtraction import FExtract
from FindURL import URLFinder
from model import Detect
from NLP_model import Detect_NLP
from get_csv import Getter
from Update_event import Pusher
import Configuration
import pandas as pd
import csv
import os

print("1: Check new entries on MISP platform. (Only on Ubuntu)")
print("2: Take a CSV of threats and classify them.")
print("3: Exit program.\n")

while True:
    option = input("Choose your option: ")
    if option == "1":
        Getter(Misp_types = 'text').Get()
        df = pd.read_csv(Configuration.MISP_outfile())

        EventDict = {}
        for index, row in df.iterrows():
            EventDict[df.at[index, 'event_id']] = df.at[index, 'value']

        with open("SMS_MISP.csv", a) as f:
            write = csv.writer(f)

            # Check if file exist and it is empty
            try:
                if os.path.exists(Configuration.FExtractFile()) and os.stat(Configuration.FExtractFile()).st_size == 0:
                    write.writerow("SMS")

            except Exception as e:
                print(e)

            for key in EventDict:
                write.writerow(EventDict[key])

        columns_features = ["having_IP_Address", "URL_Length", "Shortining_Service", "having_At_Symbol", "double_slash_redirecting", "Prefix_Suffix", "having_Sub_Domain", "SSLfinal_State", "Domain_registeration_length", "Favicon", "port", "HTTPS_token", "Request_URL", "URL_of_Anchor", "Links_in_tags", "SFH", "Submitting_to_email", "Abnormal_URL", "Redirect", \
                            "on_mouseover", "RightClick", "popUpWidnow", "Iframe", "age_of_domain", "DNSRecord", "web_traffic", "Page_Rank", "Google_Index", "Links_pointing_to_page", "Statistical_report"]

        with open(str(Configuration.FExtractFile()), 'a') as f:
            write = csv.writer(f)

            # Check if file exist and it is empty
            try:
                if os.path.exists(Configuration.FExtractFile()) and os.stat(Configuration.FExtractFile()).st_size == 0:
                    write.writerow(columns_features)

            except Exception as e:
                print(e)

            Requests = 0
            Domains = []
            for index, row in df.iterrows():
                if Requests < int(Configuration.Requests()) and Requests < 2000: # For unlimited requests please check googlesearch-python as a service

                    try:
                        features = FExtract(index, df.at[index, 'value']).generate_data_set(URLFinder(df.at[index, 'value']).Find()[0])

                    except requests.exceptions.HTTPError:
                        print("Request limit with googlesearch is hit, try again in 30 minutes.")
                        break

                    if type(features) == dict: # Check if output is a dictionnary

                        values = features.values()
                        values_list = list(values)

                        Requests += 1
                        Domains.append(URLFinder(df.at[index, 'value']).Find()[0])
                        write.writerow(values_list)

                    else:
                        pass

                else:
                    print("Request limit asked for has been hit. (If not, then request limit with googlesearch has been hit) ")
                    break

        Classifications = Detect(str(Configuration.FExtractFile())).predict()
        NLP_Classifications = Detect_NLP("SMS_MISP.csv").predict()

        SMSs = []
        for key in EventDict:
            SMSs.append(EventDict[key])

        with open(str(Configuration.ClassificationsFile3()), 'a') as g:
            write = csv.writer(g)

            headers = ['Domain', 'Domain model', 'SMS', 'NLP model']
            # Check if file exist and it is empty
            try:
                if os.path.exists(Configuration.ClassificationsFile3()) and os.stat(Configuration.ClassificationsFile3()).st_size == 0:
                    write.writerow(headers)

            except Exception as e:
                print(e)

            i = 0
            for key in EventDict:
                EventDict[key] = (Classifications[i], NLP_Classifications[i])
                row = [Domains[i], Classifications[i], SMSs[i], NLP_Classifications[i]]
                write.writerow(row)
                i += 1

        OptionalPush = input("Do you want to push the results to MISP? (Y/n)")

        if OptionalPush == "Y":
            for key in EventDict:
                DomainResult = str(EventDict[key][0]) + " - Domain model result"
                NLPResult = str(EventDict[key][1]) + " - NLP model result"
                Pusher('text', DomainResult, 'External analysis', 'This is the result of the domain ML model', int(key)).create_attribute()
                Pusher('text', NLPResult, 'External analysis', 'This is the result of the NLP ML model', int(key)).create_attribute()

        elif OptionalPush == "n":
            break

        else:
            break

    elif option == "2":
        print("1: TELUS specific CSV file.")
        print("2: Domains only CSV file.")
        print("3: Domains and SMS CSV file.")
        print("4: exit.")
        InputOption = input("Choose your option: ")

        if InputOption == "1":
            TELUS_CSV_file = str(input("Write the TELUS-like CSV file name with the extension: "))
            # Training-data-TSIRT-labeled-phish.csv
            try:
                data = CSV_Dataset_Cleanup(TELUS_CSV_file).Cleanup()
            except FileNotFoundError:
                print("The file/path you entered cannot be found.")
                break

            columns_features = ["having_IP_Address", "URL_Length", "Shortining_Service", "having_At_Symbol", "double_slash_redirecting", "Prefix_Suffix", "having_Sub_Domain", "SSLfinal_State", "Domain_registeration_length", "Favicon", "port", "HTTPS_token", "Request_URL", "URL_of_Anchor", "Links_in_tags", "SFH", "Submitting_to_email", "Abnormal_URL", "Redirect", \
                                "on_mouseover", "RightClick", "popUpWidnow", "Iframe", "age_of_domain", "DNSRecord", "web_traffic", "Page_Rank", "Google_Index", "Links_pointing_to_page", "Statistical_report"]


            with open(str(Configuration.FExtractFile()), 'a') as f:
                write = csv.writer(f)

                # Check if file exist and it is empty
                try:
                    if os.path.exists(Configuration.FExtractFile()) and os.stat(Configuration.FExtractFile()).st_size == 0:
                        write.writerow(columns_features)

                except Exception as e:
                    print(e)

                Requests = 0
                Domains = []
                for index, row in data.iterrows():
                    if Requests < int(Configuration.Requests()) and Requests < 500: # For unlimited requests please check googlesearch as a service

                        try:
                            features = FExtract(index, data).generate_data_set(data.at[index, 'info'])

                        except requests.exceptions.HTTPError:
                            print("Request limit with googlesearch is hit, try again in 30 minutes.")
                            break

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

        elif InputOption == "2":
            CSV_file = str(input("Write the domains-only CSV file name with the extension: "))

            #read csv file in Pandas
            data = pd.read_csv(CSV_file)

            for index, row in data.iterrows():
                data.at[index, 'DOMAINS'] = (data.at[index, 'DOMAINS']).lower()

            data.drop_duplicates(subset='DOMAINS', inplace = True)

            columns_features = ["having_IP_Address", "URL_Length", "Shortining_Service", "having_At_Symbol", "double_slash_redirecting", "Prefix_Suffix", "having_Sub_Domain", "SSLfinal_State", "Domain_registeration_length", "Favicon", "port", "HTTPS_token", "Request_URL", "URL_of_Anchor", "Links_in_tags", "SFH", "Submitting_to_email", "Abnormal_URL", "Redirect", \
                                "on_mouseover", "RightClick", "popUpWidnow", "Iframe", "age_of_domain", "DNSRecord", "web_traffic", "Page_Rank", "Google_Index", "Links_pointing_to_page", "Statistical_report"]

            with open(str(Configuration.FExtractFile()), 'a') as f:
                write = csv.writer(f)

                # Check if file exist and it is empty
                try:
                    if os.path.exists(Configuration.FExtractFile()) and os.stat(Configuration.FExtractFile()).st_size == 0:
                        write.writerow(columns_features)

                except Exception as e:
                    print(e)

                Requests = 0
                Domains = []
                for index, row in data.iterrows():
                    if Requests < int(Configuration.Requests()) and Requests < 500: # For unlimited requests please check googlesearch as a service

                        try:
                            features = FExtract(index, data).generate_data_set(data.at[index, 'DOMAINS'])

                        except requests.exceptions.HTTPError:
                            print("Request limit with googlesearch is hit, try again in 30 minutes.")
                            break

                        if type(features) == dict: # Check if output is a dictionnary

                            values = features.values()
                            values_list = list(values)

                            """ The below commented code was used for training purposes """
                            # values_list.append(data.at[index, "Result"])

                            Requests += 1
                            Domains.append(data.at[index, 'DOMAINS'])
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

        elif InputOption == "3":
            CSV_file = str(input("Write the CSV file name with the extension: "))

            #read csv file in Pandas
            data = pd.read_csv(CSV_file)

            data.drop_duplicates(subset='SMS', inplace = True)

            data = data.reset_index()

            columns_features = ["having_IP_Address", "URL_Length", "Shortining_Service", "having_At_Symbol", "double_slash_redirecting", "Prefix_Suffix", "having_Sub_Domain", "SSLfinal_State", "Domain_registeration_length", "Favicon", "port", "HTTPS_token", "Request_URL", "URL_of_Anchor", "Links_in_tags", "SFH", "Submitting_to_email", "Abnormal_URL", "Redirect", \
                                "on_mouseover", "RightClick", "popUpWidnow", "Iframe", "age_of_domain", "DNSRecord", "web_traffic", "Page_Rank", "Google_Index", "Links_pointing_to_page", "Statistical_report"]

            with open(str(Configuration.FExtractFile()), 'a') as f:
                write = csv.writer(f)

                # Check if file exist and it is empty
                try:
                    if os.path.exists(Configuration.FExtractFile()) and os.stat(Configuration.FExtractFile()).st_size == 0:
                        write.writerow(columns_features)

                except Exception as e:
                    print(e)

                Requests = 0
                Domains = []
                for index, row in data.iterrows():
                    if Requests < int(Configuration.Requests()) and Requests < 2000: # For unlimited requests please check googlesearch-python as a service

                        try:
                            features = FExtract(index, data).generate_data_set(URLFinder(row['SMS']).Find()[0])

                        except requests.exceptions.HTTPError:
                            print("Request limit with googlesearch is hit, try again in 30 minutes.")
                            break

                        if type(features) == dict: # Check if output is a dictionnary

                            values = features.values()
                            values_list = list(values)

                            Requests += 1
                            Domains.append(URLFinder(row['SMS']).Find()[0])
                            write.writerow(values_list)

                        else:
                            pass

                    else:
                        print("Request limit asked for has been hit. (If not, then request limit with googlesearch has been hit) ")
                        break

            Classifications = Detect(str(Configuration.FExtractFile())).predict()

            NLP_Classifications = Detect_NLP(str(CSV_file)).predict()

            SMSs = []
            for index, row in data.iterrows():
                SMSs.append(data.at[index, "SMS"])

            with open(str(Configuration.ClassificationsFile2()), 'a') as g:
                write = csv.writer(g)

                headers = ['Domain', 'Domain model', 'SMS', 'NLP model']
                # Check if file exist and it is empty
                try:
                    if os.path.exists(Configuration.ClassificationsFile2()) and os.stat(Configuration.ClassificationsFile2()).st_size == 0:
                        write.writerow(headers)

                except Exception as e:
                    print(e)

                for i in range(len(Domains)):
                    row = [Domains[i], Classifications[i], SMSs[i], NLP_Classifications[i]]
                    write.writerow(row)

        elif InputOption == "4":
            break

        else:
            print("Unavailable option.")
            break

    elif option == "3":
        break

    else:
        print("Unavailable option.")
