
'''
let's start by writing some pseudocode real quick

parse arguments

event based loop that reads in requests and updates the scoreboard as appropriate
add row (easy)
add column (hmmm)
'''
import csv
import pandas as pd

def score(scorefile_name):
    #read in the inputfile into dataframe
    df = pd.read_csv(scorefile_name)
    column_headers = list(df.columns.values)

    while(True):
        request = input("Enter request: ") #read input
        keyword = (request.split(" "))[0]
        request = request[len(keyword)+1:].split(",")
        #process input

        #assume requests are well formatted
        if (keyword == "add"):            
            try:
                new_row = format_row(column_headers, request) #make new row
                df.loc[len(df)]=new_row #add new row into the dataframe
            except length_mismatch:
                print("Error: length mismatch between row and request")
        elif (keyword == "read"):
            try:
                if (df['Name']==request[0]).any() == False:
                    raise data_missing
                print(df[df['Name']==request[0]])
            except data_missing:
                print("Error: name does not appear in the scoreboard")
        elif (keyword == "set"):
            print("hi update")
            try:
               if len(request) != 3: raise invalid_request
               df.loc[df['Name']==request[0],request[1]]=request[2]
            except invalid_request:
                print("set must be of the form Name,Column,Value")
            except KeyError:
                print("Error: name does not appear in the scoreboard")
        elif (keyword == "delete"):
            try:
                if len(request)<=0: raise invalid_request
                df.drop(df[df['Name'] == request[0]].index, inplace=True)
            except invalid_request:
                print("Error: delete must have key argument")

        elif (keyword == "exit"): break
        elif(keyword == "print"): print(df)
        elif (keyword == "save"): df.to_csv(scorefile_name, index=False)
        else:
            print("Invalid request, please try again")
            #will eventually add more info about correct request types

class length_mismatch(Exception):
    pass
class invalid_request(Exception):
    pass
class data_missing(Exception):
    pass

def format_row(columns, data):
    if len(columns)!=len(data): 
        raise length_mismatch
    
    row_dict = {}
    for i in range(len(columns)):
        row_dict[columns[i]] = data[i]
    return row_dict


score("sample.csv")