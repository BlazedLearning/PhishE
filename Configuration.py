# Extracting info from the txt file

File_in = open('Configuration.txt', 'r')
Lines = File_in.read().split('\n')

Index = []
for line in Lines:
    if line != "":
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

def ClassificationsFile3(): # Name of the output CSV file with classified domains and SMSs from MISP
    return str(Dictionnary['ClassificationsFile3'])

def ClassificationsFile4(): # Name of the output CSV file with classified domains and SMSs from MISP
    return str(Dictionnary['ClassificationsFile4'])

def MISP_SMS(): # Name of the file where SMS from MISP will be put before going into the NLP model
    return str(Dictionnary['MISP_SMS'])

def MISP_outfile(): # Name of the CSV file where info from MISP will be put when requested
    return str(Dictionnary['MISP_outfile'])

def Requests(): # Number of requests per run
    return int(Dictionnary['Requests'])

def MISP_URL(): # MISP URL
    return str(Dictionnary['MISP_URL'])

def MISP_Key(): # MISP Auth Key
    return str(Dictionnary['MISP_Key'])

def Set_MISP_URL(URL): # Set MISP URL
    Dictionnary['MISP_URL'] = URL
    with open("Configuration.txt", 'w') as f:
        f.truncate(0)
        for k in Dictionnary:
            f.write(str(k) + "=" + str(Dictionnary[k]) + "\n")

def Set_MISP_Key(Key): # Set MISP Auth Key
    Dictionnary['MISP_Key'] = Key
    with open("Configuration.txt", 'w') as f:
        f.truncate(0)
        for k in Dictionnary:
            f.write(str(k) + "=" + str(Dictionnary[k]) + "\n")
