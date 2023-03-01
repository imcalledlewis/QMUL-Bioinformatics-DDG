import pandas as pd
import os
import sqlite3

_database = "snps.db"

def pdDB(tsv_path,table_name,dtype): # Adds tsv to SQL database
    conn = sqlite3.connect(DBpath()) # Opens (or creates) a db file
    cur = conn.cursor() # Sets cursor
    df = pd.read_csv(tsv_path, sep='\t')
    df.to_sql(name=table_name, con=conn, index=False, dtype=dtype)

def getPath(file,tsv=None): # Returns the absolute path to a file that is in same folder as script
    filenames={'tsv', 'csv', 'txt'} # Set of table storing files
    ext=file.split('.') # Splits by '.'
    ext=ext[-1].lower() # Uses this information to get extension of file
    path = os.path.dirname(os.path.abspath(__file__)) # Gets current path of file
    if (tsv==True) or (tsv==None and ext in filenames): # If it's a table storing file:
            filepath = os.path.join(path,"TSVs",file) # Sets path relative to current file, inside 'TSVs' folder
    else:
            filepath = os.path.join(path,file) # Sets path relative to current file
    return filepath

def DBpath(): # Returns the absolute path to the database
    return(getPath(_database))