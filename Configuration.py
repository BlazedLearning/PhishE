# Extracting info from the txt file

File_in = open('Configuration.txt', 'r')
Lines = File_in.read().split('\n')

Index = []
for line in Lines:
    Index.append(line.split('='))

Dictionnary = {}

for index in Index:
    Dictionnary[index[0]]=index[1]

def FExtractFile(): # Name of the output CSV file with extracted features
    return str(Dictionnary['FeaturesFile'])

def DomainsModelFile(): # The saved model file that will get loaded to the program
    return str(Dictionnary['DomainsModelFile'])

def NLPModelFile(): # The saved model file that will get loaded to the program
    return str(Dictionnary['NLPModelFile'])

def ClassificationsFile(): # Name of the output CSV file with classified domains
    return str(Dictionnary['ClassificationsFile'])

def ClassificationsFile2(): # Name of the output CSV file with classified domains and SMSs
    return str(Dictionnary['ClassificationsFile2'])

def ClassificationsFile3():
    return str(Dictionnary['ClassificationsFile3'])    

def MISP_outfile(): # Name of the CSV file where info from MISP will be put when requested
    return str(Dictionnary['MISP_outfile'])

def Requests(): # Number of requests per run
    return int(Dictionnary['Requests'])
