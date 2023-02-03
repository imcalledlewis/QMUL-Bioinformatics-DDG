import pandas as pd
import os
import re
import sqlite3
import requests

database = "snps.db"

def getPath(file,tsv=None): # Returns the absolute path to a file that is in same folder as script
    filenames=('.tsv', '.csv','.txt')
    path = os.path.dirname(os.path.abspath(__file__))   # Gets current path of file
    if (tsv==True) or (tsv==None and any([x in file for x in filenames])):
            filepath = os.path.join(path,"TSVs",file)                 # Sets path relative to current file
    else:
            filepath = os.path.join(path,file)                 # Sets path relative to current file
    return filepath

def DBpath():   # Returns the absolute path to the database
    return(getPath(database))

def DBreq(request, request_type):   # Makes SQL request
    filepath=DBpath()
    assert os.path.exists(filepath),"Database file not found"
    conn = sqlite3.connect(filepath)    # Opens db file
    cur = conn.cursor()                 # Sets cursor
    request=(request,)                  # Request must be in a tuple
    if request_type=='SNPname':
        res = cur.execute("SELECT * FROM gwas WHERE SNPS LIKE ?",request)
    else:
        raise Exception(str(request_type)+" hasn't been added yet")
    return (res.fetchall())

def removeDupeSNP(dataframe): # Removes duplicates from a pandas dataframe, leaving only greatest p-value
    dataframe.reset_index(drop=True)                                 # Resets index back to 0
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

    naughtyList=[]                                  # List of lists of (index, p-val) we want to drop
    for i in dupesDict:
        snp = dupesDict[i]                          # Get list of (index, pVal)
        sortByP=sorted(snp,key=lambda x: 0-x[1])    # Sort by p-value
        sortByP=sortByP[1:]                         # Select all but greatest p value
        naughtyList.append(sortByP)

    dropList=[]                         # List of indices for rows we want to drop
    for i in naughtyList:               # Enter first list
        for j in i:                     # Enter second list
            dropList.append(j[0])       # Add the index from each tuple

    return(dataframe.drop(dropList))    # Return dataframe without duplicate values

def removeDupeGeneMap(GeneMap):
    GeneMap=GeneMap.split(', ')
    uniques=""
    for item in GeneMap:
        if item not in uniques: # If the item hasn't been seen before, 
            uniques+=(item)     # add it to the list.
            uniques+=(", ")     # Also add ' ,'
    return (uniques[:-2])       # Remove last ' ,'


def removeSpecial(dataframe):     # Replaces special characters and whitespace with underscores
    renameDict={}
    for col in dataframe.columns:
        newCol = re.sub(r'\W+', '_', col)   
        renameDict.update({col:newCol})
    return(dataframe.rename(columns=renameDict))

def pdDB(tsv_path,table_name,dtype):    # Adds tsv to SQL database
    # tabName=(table_name,)
    conn = sqlite3.connect(DBpath())     # Opens (or creates) a db file
    cur = conn.cursor()                 # Sets cursor

    df = pd.read_csv(tsv_path, sep='\t')
    df.to_sql(name=table_name, con=conn, index=False, dtype=dtype)

    # No idea why the following don't work:
    # cur.execute("ALTER TABLE ? DROP COLUMN `Unnamed: 0`", tabName) # Remove index column - pandas stubbornly refuses to not include it
    # cur.execute("ALTER TABLE ? DROP COLUMN `Unnamed: 0`", (table_name,)) # Remove index column - pandas stubbornly refuses to not include it
    # res = cur.execute("SELECT * FROM SNP")
    # assert res.fetchone(), "error in database creation"

def castRS(dataframe,rnName):   # Receives a dataframe, returns df with "rs" removed from rs value
    pass
    # iterate through df rows with df.iterrows()
    # string.lstrip("rs")
    # cast as int
    # put back into df
    # return df

def clear():    # Clears screen, platform independent
    os.system('cls' if os.name=='nt' else 'clear')