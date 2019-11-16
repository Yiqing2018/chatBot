import csv
from collections import defaultdict

trainDataPath = "quora-question-pairs/train.csv"
saveAllQas = "questions_for_word_vector.txt"
f = open(saveAllQas,'w')
f.close()

def loadCSV():
    columns = defaultdict(list) # each value in each column is appended to a list
    with open(trainDataPath) as f:
        reader = csv.DictReader(f) # read rows into a dictionary format
        for row in reader: # read a row as {column1: value1, column2: value2,...}
            for (k,v) in row.items(): # go over each column name and value 
                columns[k].append(v) # append the value into the appropriate list
    f.close()
    extracQuestion(columns['question1'])
    extracQuestion(columns['question2'])

def extracQuestion(myList):
    f = open(saveAllQas,'a')
    for i in range(50):
        item = myList[i]
        f.write(item+'\n')
    f.close()


loadCSV()
