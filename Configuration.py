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

def ClassificationsFile(): # Name of the output CSV file with classified domains
    return str(Dictionnary['ClassificationsFile'])

def ModelFile(): # The saved model file that will get loaded to the program
    return str(Dictionnary['ModelFile'])

def Requests(): # Number of requests per run
    return int(Dictionnary['Requests'])
