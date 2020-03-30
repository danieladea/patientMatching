#!/usr/bin/env python
# coding: utf-8


from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("--threshold", action="store", type=int, default=86, help="threshold,\
    default is 86. Higher values mean profiles will be less likely to be grouped together")
parser.add_argument("-w", action="store_true", dest="equalWeight",help="weigh columns equally \
    so that profiles with missing columns are more likely to be grouped", default=False,)
parser.add_argument("--csv", action="store", type=str, default="Patient Matching Data.csv", help="filename,\
     be grouped together")


options = parser.parse_args()
eqWeight = bool(options.equalWeight)

filename = options.csv

import pandas as pd
patients = pd.read_csv(filename)

cleanPatients = patients.drop(["MI"], axis =1)
cleanPatients.head()

######
#Data Cleaning
def validateAcc(acc):
    if len(str(acc)) != 11:
        return ''
    else:
        if acc[9] != "-":
            return ''
        else:
            return acc

cleanPatients["Patient Acct #"] = cleanPatients["Patient Acct #"].apply(validateAcc)



def lowerstr(string):
       return(str(string).lower())
   
cleanPatients["First Name"] = cleanPatients['First Name'].apply(lowerstr)
cleanPatients["Last Name"] = cleanPatients['Last Name'].apply(lowerstr)

cleanPatients.head()


# https://gist.github.com/rogerallen/1583593
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))


def convert_state(state):
    if state in us_state_abbrev:
        return us_state_abbrev[state]
    
    return state

def convert_state_code(state):
    if state in abbrev_us_state:
        return abbrev_us_state[state]
    
    return state

cleanPatients["Current State"] = cleanPatients["Current State"].apply(convert_state_code)
cleanPatients["Previous State"] = cleanPatients["Previous State"].apply(convert_state_code)


import re
def convert_address_2(address):
    address = str(address).lower()
    apt_no = re.match("(apt|apartment)?\s*#?\s*(\d+)", address)
    
    return apt_no.group(2) if apt_no else ''

cleanPatients['Current Street 2'] = cleanPatients['Current Street 2'].apply(convert_address_2)



cleanPatients['Previous Street 2'] = cleanPatients['Previous Street 2'].apply(convert_address_2)



street_abv = {
    "ave": "avenue",
    "ln": "lane",
    "st": "street",
    "dr": "drive",
    "rd": "road",
    "cir": "circle",
    "pt": "point",
    "pkway": "parkway",
    "ct": "court",
}




import string
def clean_address(address):
    address = str(address).lower()
    table = str.maketrans(dict.fromkeys(string.punctuation))
    
    address = address.translate(table)
    
    if address == 'nan':
        return ''
    
    tokens = address.split()
    if len(tokens) >= 3:
        if tokens[-1] in street_abv:
            tokens[-1] = street_abv[tokens[-1]]
        return " ".join(tokens)
    
    return address

cleanPatients["Current Street 1"] = cleanPatients["Current Street 1"].apply(clean_address)

cleanPatients["Previous Street 1"] = cleanPatients["Previous Street 1"].apply(clean_address)


def clean_sex(sex):
    sex = str(sex).lower()
    
    if sex and sex[0] == 'm':
        return 'm'
    elif sex and sex[0] == 'f':
        return 'f'
    
    return ''


cleanPatients["Sex"] = cleanPatients["Sex"].apply(clean_sex)


from metaphone import doublemetaphone
from enum import Enum

class Threshold(Enum):
    WEAK = 0
    NORMAL = 1
    STRONG = 2

def double_metaphone(value):
    #print(doublemetaphone(value))
    return doublemetaphone(value)

#(Primary Key = Primary Key) = Strongest Match
#(Secondary Key = Primary Key) = Normal Match
#(Primary Key = Secondary Key) = Normal Match
#(Alternate Key = Alternate Key) = Minimal Match
def double_metaphone_compare(tuple1,tuple2,threshold):
    if threshold == Threshold.WEAK:
        if tuple1[1] == tuple2[1]:
            return True
    elif threshold == Threshold.NORMAL:
        if tuple1[0] == tuple2[1] or tuple1[1] == tuple2[0]:
            return True
    else:
        if tuple1[0] == tuple2[0]:
            return True
    return False


# def getMetaphone(string):
#     met = double_metaphone(string)
#     return met[0]
# cleanPatients["metFirst"] = cleanPatients["First Name"].apply(getMetaphone)


cleanPatients["names"] = cleanPatients['First Name'].fillna('') + ' ' + cleanPatients['Last Name'].fillna('')
cleanPatients["names"] = cleanPatients['names'].apply(lambda x: x.strip())


from math import isnan
def convert_zip(z):
    if isnan(z):
        return ''
    
    return str(int(z))
  
cleanPatients['Current Zip Code'] = cleanPatients['Current Zip Code'].apply(convert_zip)



cleanPatients["address"] = cleanPatients['Current Street 1'].fillna('') + ' ' + cleanPatients['Current Street 2'] + ' '    + cleanPatients['Current City'].fillna('') + ' ' + cleanPatients['Current State'].fillna('') + ' '    + cleanPatients['Current Zip Code']
cleanPatients["address"] = cleanPatients["address"].apply(lowerstr)
cleanPatients["address"] = cleanPatients['address'].apply(lambda x: x.strip())

def clean_dob(date):
    return date.replace('/', '')

cleanPatients['Date of Birth'] = cleanPatients['Date of Birth'].apply(clean_dob)




######
#Analysis
from fuzzywuzzy import fuzz

import numpy as np
def compare(a,b):
    scores = []
    count = 0
    if a["names"] and b["names"]:
        a_met = double_metaphone(a["names"])
        b_met = double_metaphone(b["names"])
        
        name_scores = []
        if double_metaphone_compare(a_met, b_met, Threshold.STRONG):
            name_scores.append(100)
        
        name_scores.append(fuzz.token_sort_ratio(a["names"], b["names"]))
        scores.append(max(name_scores))
           
        
    if b["address"] == "":
        if eqWeight == False: 
            addressScore = 50
            scores.append(addressScore)
        else: 
            if a["address"] and b["address"]:
                addressScore = fuzz.token_sort_ratio(a["address"], b["address"])
                if addressScore > 80:
                    scores.append(addressScore)
                elif a["Current Street 1"] and b["Current Street 1"]:
                    scores.append(min(addressScore - 20 ,fuzz.token_sort_ratio(a["Current Street 1"], b["Current Street 1"])))

    elif a["address"] and b["address"]:
        addressScore = fuzz.token_sort_ratio(a["address"], b["address"])
        if addressScore > 80:
            scores.append(addressScore)
        elif a["Current Street 1"] and b["Current Street 1"]:
            scores.append(min(addressScore - 20 ,fuzz.token_sort_ratio(a["Current Street 1"], b["Current Street 1"])))
   
        
    
    if a["Sex"] and b["Sex"]:
        if a["Sex"] == b["Sex"]:
            scores.append(90)
        else:
            scores.append(60)
        
    if a["Date of Birth"] and b["Date of Birth"]:
        date_score = fuzz.token_sort_ratio(a["Date of Birth"], b["Date of Birth"])
        if (date_score < 60):
            date_score = 0
    
    
        scores.append(date_score)
        
#     if a["Patient Acct #"] and b["Patient Acct #"]:
#         scores.append(fuzz.token_sort_ratio(a["Patient Acct #"], b["Patient Acct #"])

#     if(len(scores) < 50):
    #print(scores)    
    return np.mean(scores)


cleanPatients["confidence"] = -1
cleanPatients["groupno"] = -1
groups = []
for index, row in cleanPatients.iterrows():
    for group_index, x in enumerate(groups):
        temp = compare(cleanPatients.loc[x[0]], row)
        if len(x)>1:
            temp = max(temp, compare(cleanPatients.loc[x[1]], row))
        #print(f'fuzz for {x[0]} and {row["names"]} = {temp},  index is {index}')
        if(temp > options.threshold):
            cleanPatients.loc[index,"groupno"] = group_index+1
            cleanPatients.loc[index,"confidence"] = temp
            groups[group_index].append(index)
            break
    else:
        groups.append([index])
        cleanPatients.loc[index,"groupno"] = len(groups)
        cleanPatients.loc[index,"confidence"] = options.threshold


cleanPatients.to_csv('predictions.csv', index = False, header = True)


# true_groups = []
# for i in range(1,66):
#     current_group = []
#     for index, row in cleanPatients.loc[cleanPatients['GroupID'] == i].iterrows():
#         current_group.append(index)
#     true_groups.append(current_group)

# for i, true_group in enumerate(true_groups):
#     print(true_group, groups[i])



# for i, true_group in enumerate(true_groups):
#     if true_group not in groups:
#         if i < len(groups):
#             print(true_group, groups[i])
#         else:
#             print(true_group)







