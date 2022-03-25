#!/usr/local/cs/bin/python3                                                                         
import csv
import argparse
import re

board = { 'Marshall E':15, "Carl Bartender":99}
filetable ={}
legend = {}

def checkAdd(string):
    flag = re.findall("\([A-Za-z]+(,[A-Za-z]+)*\)\s([0-9]+|[A-Za-z]+)",string)
    if not flag: #flag is an empty list and regex doesn't match
        print("error: incorrect option format")
        exit()
    return flag #TODO parse into list 

def file2board(filetable):
    for f in filetable:
        if f in board:
            temp = board[f]+filetable[f]
            board[f]=temp
        else:
            board[f]=filetable[f]

def csv2dict(fname, ind1, ind2, destdict):
    reader = csv.DictReader(fname)
    for row in reader:
        destdict[row[ind1]]= int(row[ind2])

def update(adict, instr_str):
    print('hi')#TODO over here yeet

parser = argparse.ArgumentParser()
parser.add_argument("legend", help='for table of action-point value pair', type=argparse.FileType('r+'))
parser.add_argument("-l","--load",help="load info from file into dict",type=argparse.FileType('r+', encoding='latin-1'))
parser.add_argument("-a","--add",help='for adding the same points to a list of people') #TODO wrong format for option
#add argument for top 5 point earners
args=parser.parse_args()

csv2dict(args.legend, 'Action','value', legend)
if args.add:
    checked= checkAdd(args.add)
    update(board, checked)

if args.load:
    csv2dict(args.load, 'Name','points', board)
file2board(filetable)

print(board)
print(legend)
#print(sorted(board))
#print(sorted(board.items(), key=lambda x:x[1], reverse=True))

# regex for  add func \([A-Za-z]+(,[A-Za-z]+)*\)\s([0-9]+|[A-Za-z]+)