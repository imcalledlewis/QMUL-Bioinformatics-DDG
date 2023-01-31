import pandas as pd
import os
import re
import sqlite3
import requests

database = "snps.db"

def getPath(file): # Returns a path to a file relative to current script
    path = os.path.dirname(os.path.abspath(__file__))   # Gets current path of file
    filepath = os.path.join(path, file)                 # Sets path relative to current file 
    return filepath

def DBpath():   # Returns the absolute path to the database
    return(getPath(database))

def DBreq(request, request_type):
    filepath=DBpath()
    assert os.path.exists(filepath),"Database file not found"
    conn = sqlite3.connect(filepath)  # Opens db file
    cur = conn.cursor()             # Sets cursor
    request=(request,)
    if request_type=='SNPname':
        res = cur.execute("SELECT * FROM SNP WHERE SNPS LIKE ?",request)
    else:
        raise Exception(str(request_type)+" hasn't been added yet")
    return (res.fetchall())

def removeDupes(dataframe): # Removes duplicates from a dataframe, leaving only greatest p-value
    dupeList = dataframe.duplicated(subset='SNPS',keep=False)   # Get list of duplicate values
    dupes=dataframe[dupeList]                                   # Select dataframe using above list

    dupesDict={}
    for index,row in dupes.iterrows():              # Iterate through df of duplicates, one row at a time
        rsVal=row["SNPS"]                           # SNP name (rs value)
        snpTuple=(index,row["P_VALUE"])             # Tuple containing index and p-val 
        if rsVal in dupesDict:                      # If it's seen the snp before,
            dictList=dupesDict[rsVal]               # go to the value for the snp,
            dictList.append(snpTuple)               # and add the index/ p-val tuple.
        else:                                       # If it hasn't seen the snp before,
            dupesDict.update({rsVal:[snpTuple]})    # create a listing for it.

    naughtyList=[]                                  # List of (index, p-val) we want to drop
    for i in dupesDict:
        snp = dupesDict[i]                          # Get list of (index, pVal)
        sortByP=sorted(snp,key=lambda x: 0-x[1])    # Sort by p-value
        sortByP=sortByP[1:]                         # Select all but greatest p value
        naughtyList.append(sortByP)

    dropList=[]     # List of indices for rows we want to drop
    for i in naughtyList:
        for j in i:
            dropList.append(j[0])       # Add the index

    return(dataframe.drop(dropList))    # Return dataframe without duplicate values