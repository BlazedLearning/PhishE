# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import platform
import pandas as pd
import requests
EventDict = {}
path = ""
InputOption = ""

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *


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


os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

def dataHead(self):
    all_data = pd.read_csv("ClassifiedTELUS.csv")
    NumRows = len(all_data.index)
    widgets.table_csv_results.setColumnCount(len(all_data.columns))
    widgets.table_csv_results.setRowCount(NumRows)
    

    for i in range(NumRows):
        for j in range(len(all_data.columns)):
            widgets.table_csv_results.setItem(i, j, QTableWidgetItem(str(all_data.iat[i, j])))
    widgets.table_csv_results.setHorizontalHeaderLabels(["Domain", "Domain Classification", "SMS", "SMS Classification"])
    # widgets.table_csv_results.resizeColumnsToContents()
    widgets.table_csv_results.resizeRowsToContents()  

def dataHeadSMS(self):
    all_data = pd.read_csv("ClassifiedDomains_SMS.csv")
    NumRows = len(all_data.index)
    widgets.table_csv_results.setColumnCount(len(all_data.columns))
    widgets.table_csv_results.setRowCount(NumRows)
    

    for i in range(NumRows):
        for j in range(len(all_data.columns)):
            widgets.table_csv_results.setItem(i, j, QTableWidgetItem(str(all_data.iat[i, j])))
    widgets.table_csv_results.setHorizontalHeaderLabels(["Domain", "Domain Classification", "SMS", "SMS Classification"])
    # widgets.table_csv_results.resizeColumnsToContents()
    widgets.table_csv_results.resizeRowsToContents()  
    
def dataHeadMisp(self):
    all_data = pd.read_csv("ClassifiedMISP.csv")
    NumRows = len(all_data.index)
    widgets.table_misp_results.setColumnCount(len(all_data.columns))
    widgets.table_misp_results.setRowCount(NumRows)
    

    for i in range(NumRows):
        for j in range(len(all_data.columns)):
            widgets.table_misp_results.setItem(i, j, QTableWidgetItem(str(all_data.iat[i, j])))
    widgets.table_misp_results.setHorizontalHeaderLabels(["Domain", "Domain Classification", "SMS", "SMS Classification"])
    # widgets.table_misp_results.resizeColumnsToContents()
    widgets.table_misp_results.resizeRowsToContents()  

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "Project X"
        description = "PhishE"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.table_csv_results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        widgets.table_csv_results.setFont("Cascadia Code")
        widgets.table_csv_results.setColumnCount(2)
        widgets.table_csv_results.setRowCount(10)
        widgets.table_csv_results.setHorizontalHeaderLabels(["Domain", "Classification"])
        widgets.table_csv_results.resizeColumnsToContents()
        #widgets.table_csv_results.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)

        widgets.table_csv_results.show()


        widgets.table_misp_results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        widgets.table_misp_results.setFont("Cascadia Code")
        widgets.table_misp_results.setColumnCount(4)
        widgets.table_misp_results.setRowCount(10)
        widgets.table_misp_results.setHorizontalHeaderLabels(["Domain", "Domain Classification", "SMS", "SMS Classification"])
        # widgets.table_misp_results.resizeColumnsToContents()
        widgets.table_misp_results.show()

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.new_page)
        UIFunctions.resetStyle(self, "btn_new") # RESET ANOTHERS BUTTONS SELECTED
        widgets.btn_new.setStyleSheet(UIFunctions.selectMenu(widgets.btn_new.styleSheet())) # SELECT MENU
        # PROGRESS BARS
        widgets.progress_csv_classify.setValue(0)
        widgets.progress_pull.setValue(0)
        widgets.progress_misp_classify.setValue(0)
        widgets.progress_push.setValue(0)


        # LEFT MENUS
        #widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_browse.clicked.connect(self.buttonClick)
        widgets.btn_csv_classify.clicked.connect(self.fyp_csv)
        widgets.btn_pull_classify.clicked.connect(self.misp_pull_classify)
        widgets.btn_push.clicked.connect(self.misp_push)
        widgets.btn_set_param.clicked.connect(self.set_param)
        #widgets.btn_save.clicked.connect(self.buttonClick)



        # Radio CLICK
        # ///////////////////////////////////////////////////////////////
        widgets.radio_1.clicked.connect(self.radioClick)
        widgets.radio_2.clicked.connect(self.radioClick)
        widgets.radio_3.clicked.connect(self.radioClick)
        
        widgets.misp_server_address.setText(Configuration.MISP_URL())


        
        
        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
      

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
       

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        
        # widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))


    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        if btnName == "btn_save":
            print("Save BTN clicked!")
        
        if btnName == "btn_browse":
            filename = QFileDialog.getOpenFileName()
            global path
            path = filename[0]
            widgets.lbl_path.setText(path)
            print(path)

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')

                        

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

    def radioClick(self):
            # GET BUTTON CLICKED
        rad = self.sender()
        radName = rad.objectName()
        global InputOption
        if radName == "radio_1":
            InputOption = "1"
            # widgets.table_csv_results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            widgets.table_csv_results.setColumnCount(4)
            widgets.table_csv_results.setRowCount(10)
            widgets.table_csv_results.setHorizontalHeaderLabels(["Domain", "Domain Classification", "SMS", "SMS Classification"])
            #widgets.table_csv_results.resizeColumnsToContents()
            widgets.table_csv_results.show()
        if radName == "radio_2":
            InputOption = "2"
            # widgets.table_csv_results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            widgets.table_csv_results.setColumnCount(2)
            widgets.table_csv_results.setRowCount(10)
            widgets.table_csv_results.setHorizontalHeaderLabels(["Domain", "Classification"])
            #widgets.table_csv_results.resizeColumnsToContents()
            widgets.table_csv_results.show()
        if radName == "radio_3":
            InputOption = "3"
            # widgets.table_csv_results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            widgets.table_csv_results.setColumnCount(4)
            widgets.table_csv_results.setRowCount(10)
            widgets.table_csv_results.setHorizontalHeaderLabels(["Domain", "Domain Classification", "SMS", "SMS Classification"])
            #widgets.table_csv_results.resizeColumnsToContents()
            widgets.table_csv_results.show()
        print(InputOption)



    def fyp_csv(self):
        widgets.progress_csv_classify.setValue(2)
        widgets.textBrowser.append("Classification Started")
        if path == "":
            widgets.textBrowser.append("Please Choose CSV File")
            return

        if InputOption == "1":
            
            widgets.textBrowser.append("Reading File...")
            TELUS_CSV_file = str(path)
            # Training-data-TSIRT-labeled-phish.csv
            try:
                data = CSV_Dataset_Cleanup(TELUS_CSV_file).Cleanup()
            except FileNotFoundError:
                widgets.textBrowser.append("The file/path you entered cannot be found.")
             

            columns_features = ["having_IP_Address", "URL_Length", "Shortining_Service", "having_At_Symbol", "double_slash_redirecting", "Prefix_Suffix", "having_Sub_Domain", "SSLfinal_State", "Domain_registeration_length", "Favicon", "port", "HTTPS_token", "Request_URL", "URL_of_Anchor", "Links_in_tags", "SFH", "Submitting_to_email", "Abnormal_URL", "Redirect", \
                                "on_mouseover", "RightClick", "popUpWidnow", "Iframe", "age_of_domain", "DNSRecord", "web_traffic", "Page_Rank", "Google_Index", "Links_pointing_to_page", "Statistical_report"]
            widgets.textBrowser.append("Extracting Features...")

            with open(str(Configuration.FExtractFile()), 'a') as f:
                write = csv.writer(f)

                # Check if file exist and it is empty
                try:
                    if os.path.exists(Configuration.FExtractFile()) and os.stat(Configuration.FExtractFile()).st_size == 0:
                        write.writerow(columns_features)

                except Exception as e:
                    widgets.textBrowser.append(e)

                Requests = 0
                Domains = []
                for index, row in data.iterrows():
                    if Requests < int(Configuration.Requests()): # For unlimited requests please check googlesearch as a service

                        try:
                            features = FExtract(index, data).generate_data_set(URLFinder(row['attrib_value']).Find()[0])

                        except requests.exceptions.HTTPError:
                            widgets.textBrowser.append("Request limit with googlesearch is hit, try again in 30 minutes.")
                            break

                        if type(features) == dict: # Check if output is a dictionnary

                            values = features.values()
                            values_list = list(values)

                            """ The below commented code was used for training purposes """
                            #if data.at[index, 'event_tags'] == "Yes":
                            #    values_list.append(-1)
                            #else:
                            #    values_list.append(1)
                            QApplication.processEvents()
                            Requests += 1
                            Domains.append(URLFinder(row['attrib_value']).Find()[0])
                            write.writerow(values_list)
                            widgets.progress_csv_classify.setValue(Requests / int(Configuration.Requests()) * 100)
                            widgets.textBrowser.append("Processing domain number: %s" %(Requests))
                            

                        else:
                            pass

                    else:
                        widgets.textBrowser.append("Request limit asked for has been hit. (If not, then request limit with googlesearch has been hit) ")
                        break
            widgets.textBrowser.append("Running Classifier")
            Classifications = Detect(str(Configuration.FExtractFile())).predict()
            SMSs = []
            for index, row in data.iterrows():
                SMSs.append(data.at[index, "attrib_value"])

            data.rename(columns = {'attrib_value':'SMS'}, inplace = True)

            data.to_csv("TELUS_SMS.csv", index = False)

            NLP_Classifications = Detect_NLP("TELUS_SMS.csv").predict()

            with open(str(Configuration.ClassificationsFile4()), 'a') as g:
                write = csv.writer(g)

                headers = ['Domain', 'Domain model', 'SMS', 'NLP model']
                # Check if file exist and it is empty
                try:
                    if os.path.exists(Configuration.ClassificationsFile4()) and os.stat(Configuration.ClassificationsFile4()).st_size == 0:
                        write.writerow(headers)

                except Exception as e:
                    widgets.textBrowser.append(e)

                for i in range(len(Domains)):
                    row = [Domains[i], Classifications[i], SMSs[i], NLP_Classifications[i]]
                    write.writerow(row)

            widgets.textBrowser.append("Done.")
            widgets.progress_csv_classify.setValue(100)
            dataHead(self)
            os.remove(str(Configuration.FExtractFile()))

        elif InputOption == "2":
            # widgets.textBrowser.append("Classification Started")
            widgets.textBrowser.append("Reading File...")
            CSV_file = str(path)

            #read csv file in Pandas
            data = pd.read_csv(CSV_file)

            for index, row in data.iterrows():
                data.at[index, 'DOMAINS'] = (data.at[index, 'DOMAINS']).lower()

            data.drop_duplicates(subset='DOMAINS', inplace = True)

            columns_features = ["having_IP_Address", "URL_Length", "Shortining_Service", "having_At_Symbol", "double_slash_redirecting", "Prefix_Suffix", "having_Sub_Domain", "SSLfinal_State", "Domain_registeration_length", "Favicon", "port", "HTTPS_token", "Request_URL", "URL_of_Anchor", "Links_in_tags", "SFH", "Submitting_to_email", "Abnormal_URL", "Redirect", \
                                "on_mouseover", "RightClick", "popUpWidnow", "Iframe", "age_of_domain", "DNSRecord", "web_traffic", "Page_Rank", "Google_Index", "Links_pointing_to_page", "Statistical_report"]
            widgets.textBrowser.append("Extracting File...")
            with open(str(Configuration.FExtractFile()), 'a') as f:
                write = csv.writer(f)

                # Check if file exist and it is empty
                try:
                    if os.path.exists(Configuration.FExtractFile()) and os.stat(Configuration.FExtractFile()).st_size == 0:
                        write.writerow(columns_features)

                except Exception as e:
                    widgets.textBrowser.append(e)

                Requests = 0
                Domains = []
                for index, row in data.iterrows():
                    if Requests < int(Configuration.Requests()): # For unlimited requests please check googlesearch as a service

                        try:
                            features = FExtract(index, data).generate_data_set(data.at[index, 'DOMAINS'])

                        except requests.exceptions.HTTPError:
                            widgets.textBrowser.append("Request limit with googlesearch is hit, try again in 30 minutes.")
                            return

                        if type(features) == dict: # Check if output is a dictionnary

                            values = features.values()
                            values_list = list(values)

                            """ The below commented code was used for training purposes """
                            # values_list.append(data.at[index, "Result"])
                            QApplication.processEvents()
                            Requests += 1
                            widgets.progress_csv_classify.setValue(Requests / int(Configuration.Requests()) * 100)
                            Domains.append(data.at[index, 'DOMAINS'])
                            write.writerow(values_list)
                            widgets.progress_csv_classify.setValue(Requests / int(Configuration.Requests()) * 100)
                            widgets.textBrowser.append("Processing domain number: %s" %(Requests))

                        else:
                            pass

                    else:
                        widgets.textBrowser.append("Request limit asked for has been hit. (If not, then request limit with googlesearch has been hit) ")
                        break
            widgets.textBrowser.append("Running Classifier...")
            Classifications = Detect(str(Configuration.FExtractFile())).predict()
            with open(str(Configuration.ClassificationsFile()), 'a') as g:
                write = csv.writer(g)

                for i in range(len(Domains)):
                    QApplication.processEvents()
                    row = [Domains[i], Classifications[i]]
                    write.writerow(row)
            widgets.textBrowser.append("Done.")
            widgets.progress_csv_classify.setValue(100)
            dataHeadSMS(self)
            os.remove(str(Configuration.FExtractFile()))
        elif InputOption == "3":
            # widgets.textBrowser.append("Classification Started")
            CSV_file = str(path)
            widgets.textBrowser.append("Reading File...")
            #read csv file in Pandas
            data = pd.read_csv(CSV_file)

            data.drop_duplicates(subset='SMS', inplace = True)

            data = data.reset_index()

            columns_features = ["having_IP_Address", "URL_Length", "Shortining_Service", "having_At_Symbol", "double_slash_redirecting", "Prefix_Suffix", "having_Sub_Domain", "SSLfinal_State", "Domain_registeration_length", "Favicon", "port", "HTTPS_token", "Request_URL", "URL_of_Anchor", "Links_in_tags", "SFH", "Submitting_to_email", "Abnormal_URL", "Redirect", \
                                "on_mouseover", "RightClick", "popUpWidnow", "Iframe", "age_of_domain", "DNSRecord", "web_traffic", "Page_Rank", "Google_Index", "Links_pointing_to_page", "Statistical_report"]
            widgets.textBrowser.append("Extracting Features...")
            with open(str(Configuration.FExtractFile()), 'a') as f:
                write = csv.writer(f)

                # Check if file exist and it is empty
                try:
                    if os.path.exists(Configuration.FExtractFile()) and os.stat(Configuration.FExtractFile()).st_size == 0:
                        write.writerow(columns_features)

                except Exception as e:
                    widgets.textBrowser.append(e)

                Requests = 0
                Domains = []
                for index, row in data.iterrows():
                    if Requests < int(Configuration.Requests()): # For unlimited requests please check googlesearch-python as a service

                        try:
                            features = FExtract(index, data).generate_data_set(URLFinder(row['SMS']).Find()[0])

                        except requests.exceptions.HTTPError:
                            widgets.textBrowser.append("Request limit with googlesearch is hit, try again in 30 minutes.")
                            break

                        if type(features) == dict: # Check if output is a dictionnary

                            values = features.values()
                            values_list = list(values)
                            QApplication.processEvents()

                            Requests += 1
                            widgets.progress_csv_classify.setValue(Requests / int(Configuration.Requests()) * 100)
                            Domains.append(URLFinder(row['SMS']).Find()[0])
                            write.writerow(values_list)
                            widgets.progress_csv_classify.setValue(Requests / int(Configuration.Requests()) * 100)
                            widgets.textBrowser.append("Processing domain number: %s" %(Requests))

                        else:
                            pass

                    else:
                        widgets.textBrowser.append("Request limit asked for has been hit. (If not, then request limit with googlesearch has been hit) ")
                        break
            widgets.textBrowser.append("Running Classifier...")
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
            widgets.progress_csv_classify.setValue(100)
            dataHeadSMS(self)
            os.remove(str(Configuration.FExtractFile()))
            widgets.textBrowser.append("Done.")
        else: 
            widgets.textBrowser.append("Please Choose the Type of CSV")




    def misp_pull_classify(self):
        widgets.misp_output.append("Pulling Started")
        Getter(Misp_types = 'text').Get()
        widgets.misp_output.append("Done Pulling.")
        widgets.progress_pull.setValue(100)
        widgets.misp_output.append("Classification Started")
        df = pd.read_csv(Configuration.MISP_outfile())
        events2pop = []
        for index, row in df.iterrows():
            if str(df.at[index, 'category']) == "External analysis":
                events2pop.append(df.at[index, 'event_id'])

        events2pop = list(set(events2pop))

        for index, row in df.iterrows():
            if df.at[index, 'event_id'] in events2pop:
                df.drop([index], axis = 0, inplace = True)

        if df.empty:
            widgets.misp_output.append("All MISP events are classified.")
            return

        global EventDict
        EventDict = {}
        for index, row in df.iterrows():
            EventDict[df.at[index, 'event_id']] = df.at[index, 'value']
        widgets.misp_output.append("Reading Pulled Data...")
        with open("SMS_MISP.csv", "a") as f:
            write = csv.writer(f)

            # Check if file exist and it is empty
            try:
                if os.path.exists(Configuration.MISP_SMS()) and os.stat(Configuration.MISP_SMS()).st_size == 0:
                    write.writerow(["SMS"])

            except Exception as e:
                widgets.misp_output.append(e)

            for key in EventDict:
                write.writerow([EventDict[key]])

        columns_features = ["having_IP_Address", "URL_Length", "Shortining_Service", "having_At_Symbol", "double_slash_redirecting", "Prefix_Suffix", "having_Sub_Domain", "SSLfinal_State", "Domain_registeration_length", "Favicon", "port", "HTTPS_token", "Request_URL", "URL_of_Anchor", "Links_in_tags", "SFH", "Submitting_to_email", "Abnormal_URL", "Redirect", \
                            "on_mouseover", "RightClick", "popUpWidnow", "Iframe", "age_of_domain", "DNSRecord", "web_traffic", "Page_Rank", "Google_Index", "Links_pointing_to_page", "Statistical_report"]
        widgets.misp_output.append("Extracting Features...")
        with open(str(Configuration.FExtractFile()), 'a') as f:
            write = csv.writer(f)

            # Check if file exist and it is empty
            try:
                if os.path.exists(Configuration.FExtractFile()) and os.stat(Configuration.FExtractFile()).st_size == 0:
                    write.writerow(columns_features)

            except Exception as e:
                widgets.misp_output.append(e)

            Requests = 0
            Domains = []
            for index, row in df.iterrows():
                if Requests < int(Configuration.Requests()): # For unlimited requests please check googlesearch-python as a service

                    try:
                        features = FExtract(index, df.at[index, 'value']).generate_data_set(URLFinder(df.at[index, 'value']).Find()[0])

                    except requests.exceptions.HTTPError:
                        widgets.misp_output.append("Request limit with googlesearch is hit, try again in 30 minutes.")
                        break

                    if type(features) == dict: # Check if output is a dictionnary

                        values = features.values()
                        values_list = list(values)

                        Requests += 1
                        Domains.append(URLFinder(df.at[index, 'value']).Find()[0])
                        write.writerow(values_list)
                        widgets.progress_misp_classify.setValue(Requests / int(Configuration.Requests()) * 100)
                        widgets.misp_output.append("Processing domain number: %s" %(Requests))

                    else:
                        pass

                else:
                    widgets.misp_output.append("Request limit asked for has been hit. (If not, then request limit with googlesearch has been hit) ")
                    break
        widgets.misp_output.append("Running Classifier...")
        Classifications = Detect(str(Configuration.FExtractFile())).predict()
        NLP_Classifications = Detect_NLP(Configuration.MISP_SMS()).predict()

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
                widgets.misp_output.append(e)

            i = 0
            for key in EventDict:
                EventDict[key] = (Classifications[i], NLP_Classifications[i])
                row = [Domains[i], Classifications[i], SMSs[i], NLP_Classifications[i]]
                write.writerow(row)
                i += 1
        dataHeadMisp(self)
        widgets.misp_output.append("Done.")
        widgets.progress_misp_classify.setValue(100)
        os.remove(str(Configuration.FExtractFile()))

    def misp_push(self):
        widgets.misp_output.append("Pushing Started")
        for key in EventDict:
            DomainResult = str(EventDict[key][0]) + " - Domain model result"
            NLPResult = str(EventDict[key][1]) + " - NLP model result"
            Pusher('text', DomainResult, 'External analysis', 'This is the result of the domain ML model', int(key)).create_attribute()
            Pusher('text', NLPResult, 'External analysis', 'This is the result of the NLP ML model', int(key)).create_attribute()
        widgets.misp_output.append("Pushing Done.")
        widgets.progress_push.setValue(100)

    def set_param(self):
        key = widgets.auth_key.text()
        url = widgets.misp_server_address.text()
        flg = 0
        if key != "":
            Configuration.Set_MISP_Key(key)
            widgets.misp_output.append("Auth Key Set")
            flg = 1
        if url != "":
            Configuration.Set_MISP_URL(url)
            widgets.misp_output.append("Server URL Set")
            flg =1
        if flg == 1:
            widgets.misp_output.append("Please restart the program for your changes to take effect")
            
        
        
            

      
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
