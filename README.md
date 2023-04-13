# PhishE
Phishing & Smishing Classifier with MISP

Authors: Hadi El Karhani, Riad Jamal, Yorgo Bou Samra

Advisors: Imad Elhajj, Ayman Kayssi

Python 3.8+, MISP 2.4+ compatible

This project was done in collaboration with TELUS Communication Inc. in an effort to automate and improve Smishing detection using Machine Learning techniques. The program smartly extracts 30 features from each domain and takes the SMS text, then uses two classifiers (Decision Trees and SVC) to classify domains / SMS as malicious or safe.

To run this project on your machine, please run: "pip3 install -r requirements.txt". Then run the code file named "main.py".

You can switch some parameters in the "Configuration.txt" file without having to hardcode them, don't touch them if you don't know what you are doing; FeaturesFile: where the domain-specific features get extracted and saved as a CSV file. ClassificationsFile: where the final output of domains and their classifications get saved as a CSV file. ModelFile: the saved Machine Learning model that gets loaded to the program. Requests: How many googlesearch requests/domain classifications do you want per run, etc...

If you are still struggling with dependencies, type python3 -m pip install and then the name of the library you are missing.
There are 2 modes in this program, you can see some examples in the modes folder. Walkthrough in the GUI: 

1- MISP pulling, classification, and pulling
![alt text](https://github.com/HadiElKarhani/PhishE/blob/main/GuidancePics/MISP_Pic.png)

When you pull from your MISP instance:
![alt text](https://github.com/HadiElKarhani/PhishE/blob/main/GuidancePics/MISP2_Pic.png)

When you push to your MISP instance:
![alt text](https://github.com/HadiElKarhani/PhishE/blob/main/GuidancePics/MISP3_Pic.png)

What gets pushed to each new event on your MISP instance:
![alt text](https://github.com/HadiElKarhani/PhishE/blob/main/GuidancePics/MISP4_Pic.png)

2- Passing CSV files, classification, and save
![alt text](https://github.com/HadiElKarhani/PhishE/blob/main/GuidancePics/CSV_Pic.png)
