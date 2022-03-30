# FYP
Final Year Project - Smishing Classifier for TELUS - 2022

Authors: Hadi El Karhani - Yorgo Bou Samra - Riad Jamal

Supervisors: Imad Elhajj - Ayman Kayssi

Python 3.6+, MISP 2.4+ compatible

This project was done in collaboration with TELUS Communication Inc. in an effort to automate and improve Smishing detection using Machine Learning techniques. The program smartly extracts 30 features from each domain and takes the sms text, then uses two classifiers (HistogramGradientBoosting and SVC) to classify domains / sms as maliscious or safe.

To run this project on your machine, please run: pip3 install -r requirements.txt. Then run the code file named "PhishingClassifier.py".

You can switch some parameters in the "Configuration.txt" file without having to hardcode them, don't touch them if you don't know what you are doing; FeaturesFile: where the domain-specific features get extracted and saved as a CSV file. ClassificationsFile: where the final output of domains and their classifications get saved as a CSV file. ModelFile: the saved Machine Learning model that get loaded to the program. Requests: How many googlesearch requests / domain classifications you want per run (maximum of 80 requests per run / every 30 minutes unless you subscribe to the google service).
