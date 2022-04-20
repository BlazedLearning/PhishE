import re
import pandas as pd
import csv

class URLFinder:
    def __init__(self, string):
        self.string = string

    def Find(self):
        # findall() has been used
        # with valid conditions for urls in string
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex,self.string)
        return [x[0] for x in url]

#l = []
#for s in ss:
#    l.append(URLFinder(s).Find()[0])

#print(l)

#data = pd.read_csv("Domains_SMS.csv")
#data = data.reset_index()

#for index, row in data.iterrows():
#    print(data.at[index, "SMS"])

#print(l)
