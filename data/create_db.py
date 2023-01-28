import pandas as pd
import sqlite3
import os
import re
fileIn = "gwas_trimmed.tsv"
fileOut = 'snps.db'

path = os.path.dirname(os.path.abspath(__file__))       # sets path relative to current file
filepath = os.path.join(path, fileIn)        
df = pd.read_csv(filepath, sep='\t')

colName=""              # Empty string that will be filled later
for col in df.columns[1:]:
    colName+=(col)      # Add another name column name
    colName+=(", ")     # Add a comma separator 
colName=colName[:-2]    # removes last ' ,'
#print(colName)

badChar = re.search(r'[\W]+', colName)  # Searches for special characters
if badChar:                             # If any special chars are found
    print("\nFound special character") 
    print (colName[badChar.start()-5:badChar.end()+5], '\n')   # Prints 10 character string, cantered on special character


# path = os.path.dirname(os.path.abspath(__file__))       # sets path relative to current file
# filepath = os.path.join(path, fileOut)                  
# conn = sqlite3.connect(filepath)                        # Opens (or creates) a db file
# cur = conn.cursor()                                     # Sets cursor
# cur.execute("CREATE TABLE SNP(" + colName + ")")
# res = cur.execute("SELECT name FROM sqlite_master")
# print(res.fetchone())