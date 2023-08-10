
'''
parse arguments

event based loop that reads in requests and updates the scoreboard as appropriate
'''
import pandas as pd

verbose = False


def file_preprocessing(scorefile):
    if (len(scorefile)==0):
        dataframe = pd.DataFrame({"Name":[], "Points":[]})
        if (verbose):
            print("New scoreboards are automatically created with 2 columns 'Name' and 'Points'")
        newcols = input("Please specify any additional columns you would like to add:")
        
        newcols=newcols.split(",")
        if (newcols[0]!=""):
            for n in range(len(newcols)):
              dataframe.insert(2+n, newcols[n],[])
        return dataframe
    else:
        dataframe = pd.read_csv(scorefile)
    return dataframe

def score(scoredf, scorefile_name):
    #read in the inputfile into dataframe
    df = scoredf
    legdf = pd.DataFrame({"Action":[], "Points":[]})
    legendfile_name = '' #setup
    column_headers = list(df.columns.values)
    currently_using_score = True

    while(True):
        request = input("Enter request: ") #read input
        keyword = (request.split(" "))[0]
        request = request[len(keyword)+1:].split(",")
        #process input

        #assume requests are well formatted
        if (keyword == "exit"): break
            
        elif(keyword == "show"):
            if (currently_using_score):
                print("score: "+ scorefile_name)
            else:
                print("legend: "+ legendfile_name)

        elif(keyword == "switch"):
            currently_using_score = not currently_using_score
            if (currently_using_score):
                print("now operating on scorefile "+scorefile_name)
                df= scoredf
            else:
                print("now operating on legendfile: "+legendfile_name)
                df=legdf
            column_headers = list(df.columns.values)


        elif (keyword == "new"):            
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
                print("add must be of the form Name,Column,Value")
            except KeyError:
                print("Error: name does not appear in the scoreboard")

        elif (keyword == "delete"):
            try:
                if request[0]=="": raise invalid_request
                df.drop(df[df[column_headers[0]] == request[0]].index, inplace=True)
            except invalid_request:
                print("Error: delete must have key argument")

        elif (keyword == "load"): #load legend file
            try:
                if request[0]=="": raise invalid_request
                legdf = pd.read_csv(request[0])
                legendfile_name = request[0]
            except invalid_request:
                print("Error load requires a filename")

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
        
        elif (keyword == "save"):
            if (request[0]!=""):
                df.to_csv(request[0], index=False)
            elif (len(scorefile_name)!=0 and request[0]==""):
                df.to_csv(scorefile_name, index=False)
            else:
                print("Error, need to specify file to save to")
            
        else:
            print("Invalid request, please try again")
            if (verbose):
                print('''The supported operations are: new row, read row, set cell, 
                      add sell,value, delete row, exit, print, top n, sort n, save.
                      Please consult the README for more details.''')

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

def main():
    scorefile = input("Enter scorefilename (optional): ")
    score_df= file_preprocessing(scorefile)
    # legendfile = input("Enter legend file name (optional): ")
    # if (len(legendfile) !=0 ):
    #     legend_df = file_preprocessing(legendfile)
    score(score_df,scorefile)


#score("ledge.csv")
#score("sample.csv")

if __name__ == "__main__":
    main()