
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS145 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
""" 

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)


def cleanQuotes(s):
    if(s is None):
        return "" 
    if('"' not in s):
        return s
    else:
        index = s.find('"')
        newString = s[:index] + '"' + s[index:]
        return newString[:index+2] + cleanQuotes(newString[index+2:])

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file,Bid, Auction, Users, Category):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        for item in items:
            ItemID = item['ItemID']
            first_Name = item['Name']
            Categories = item['Category']
            Currently = transformDollar(item['Currently'])
            Buy_Price = transformDollar(item['Buy_Price']) if 'Buy_Price' in item.keys() else 'NULL'
            First_Bid = transformDollar(item["First_Bid"])
            Number_of_Bids = item['Number_of_Bids']
            Bids = item['Bids']
            first_Location = item['Location']
            Country = item['Country']
            Started = transformDttm(item['Started'])
            End_Time = transformDttm(item['Ends'])
            Seller = item['Seller']
            first_Description = item['Description'] if 'Description' in item.keys() else 'NULLi'
            Location = '"' + cleanQuotes(first_Location) + '"'
            Name = '"' + cleanQuotes(first_Name) + '"'
            Description = '"' + cleanQuotes(first_Description)+ '"'
            if Bids is not None:
                for bid in Bids:
                    Bid.write(ItemID +columnSeparator+ bid['Bid']['Bidder']['UserID']+columnSeparator+ transformDttm(bid['Bid']['Time']) +columnSeparator+ transformDollar(bid['Bid']['Amount']) + '\n')
                    location = 'NULL' if 'Location' not in bid['Bid']['Bidder'].keys() else '"' + cleanQuotes(bid['Bid']['Bidder']['Location']) + '"'
                    country = 'NULL' if 'Country' not in bid['Bid']['Bidder'].keys() else bid['Bid']['Bidder']['Country'] 
                    Users.write(bid['Bid']['Bidder']['UserID'] +columnSeparator+ bid['Bid']['Bidder']['Rating'] +columnSeparator+ location  +columnSeparator+ country +'\n')
            for category in Categories:
                Category.write(ItemID +columnSeparator+ category+'\n')
                description = 'NULL' if Description is None else Description
            Auction.write(ItemID +columnSeparator+ Seller['UserID'] +columnSeparator+ Name  +columnSeparator+ Buy_Price +columnSeparator+ First_Bid +columnSeparator+ Currently+columnSeparator)
            Auction.write(Number_of_Bids +columnSeparator+ Started +columnSeparator+ End_Time +columnSeparator+ description + '\n')
            Users.write(Seller['UserID'] +columnSeparator+ Seller['Rating'] +columnSeparator+ Location +columnSeparator+ Country + '\n')
            pass

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
     # loops over all .json files in the argument
    Bid = open('Bids.dat', 'w')
    Auction = open('Items.dat', 'w')
    Users = open('Users.dat', 'w')
    Category = open('Categories.dat', 'w')
    for f in argv[1:]:
        if isJson(f):
            parseJson(f, Bid, Auction, Users, Category)
            print "Success parsing " + f

if __name__ == '__main__':
    main(sys.argv)
