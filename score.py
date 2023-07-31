
'''
parse arguments

event based loop that reads in requests and updates the scoreboard as appropriate
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
        if (keyword == "new"):            
            try:
                new_row = format_row(column_headers, request) #make new row
                df.loc[len(df)]=new_row #add new row into the dataframe
            except length_mismatch:
                print("Error: length mismatch between row and request")
        elif (keyword == "read"):
            try:
                if (df[column_headers[0]]==request[0]).any() == False:
                    raise data_missing
                print(column_headers)#yeet
                print(df[df[column_headers[0]]==request[0]])
            except data_missing:
                print("Error: name does not appear in the scoreboard")
        elif (keyword == "set"): #rewrite a cell
            try:
                if len(request) != 3: raise invalid_request
                df.loc[df[column_headers[0]]==request[0],request[1]]=request[2]
            except invalid_request:
                print("set must be of the form Name,Column,Value")
            except KeyError:
                print("Error: name does not appear in the scoreboard")
        elif (keyword=="add"): #modify a cell based on a previous value
            try:
                if len(request) != 3: raise invalid_request
                oldval=df.loc[df[column_headers[0]]==request[0],request[1]]
                if (request[2].isnumeric()) :
                    newval = oldval+ int(request[2])
                else:
                    newval = oldval + [" "]+request[2]
                df.loc[df[column_headers[0]]==request[0],request[1]] = newval
                # df.loc[df[column_headers[0]]==request[0],request[1]] = newval
            except invalid_request:
                print("set must be of the form Name,Column,Value")
            except KeyError:
                print("Error: name does not appear in the scoreboard")

        elif (keyword == "delete"):
            try:
                if len(request)<=0: raise invalid_request
                df.drop(df[df[column_headers[0]] == request[0]].index, inplace=True)
            except invalid_request:
                print("Error: delete must have key argument")

        elif (keyword == "exit"): break
        elif(keyword == "print" or keyword == "sort" or keyword == "top"): 
            try:
                if (keyword == "sort"):
                    df.sort_values(inplace=True, by=[column_headers[0]])
                elif(keyword == "top"):
                    df.sort_values(inplace=True, by=[column_headers[1]],ascending=False)

                if len(request)==1 and request[0]!='':
                    if request[0].isnumeric():
                        print(request[0])
                        print(df.head(int(request[0])))
                    else:
                        raise invalid_request
                else:
                    print(df)
            except invalid_request:
                print("Error: print's optional argument must be a number")
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

#score("ledge.csv")
score("sample.csv")