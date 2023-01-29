import pandas as pd
import sqlite3
import os
import re
fileIn = "gwas_trimmed.tsv"
fileOut = 'snps.db'

path = os.path.dirname(os.path.abspath(__file__))   # Gets current path of file
filepath = os.path.join(path, fileIn)               # Sets path relative to current file
df = pd.read_csv(filepath, sep='\t')

colName=""              # Empty string that will be filled later
for col in df.columns[1:]:
    badChar = re.search(r'\W+', col)                            # Searches for special characters
    if badChar:                                                 # If any special chars are found:
        raise Exception("Found special character "+str(col))    # Warns user about special character

    colName+=(col)      # Add another name column name
    colName+=(", ")     # Add a comma separator 
colName=colName[:-2]    # removes last ' ,'
#print(colName)

# badChar = re.search(r'\W+', colName)    # Searches for special characters
# if badChar:                             # If any special chars are found:
#     print("\nFound special character") 
#     print (colName[badChar.start()-5:badChar.start()+5], '\n')   # Prints 11 character string, centred on special character


colName = "column1, column2, column3"

filepath = os.path.join(path, fileOut)
if os.path.exists(filepath):        # If the file exists:
    print(filepath)
    os.remove(filepath)             # delete it.
conn = sqlite3.connect(filepath)    # Opens (or creates) a db file
cur = conn.cursor()                 # Sets cursor

query= "CREATE TABLE SNP({cols})".format(cols=colName)
query2= """
INSERT INTO SNP
VALUES (?, ?, ?)
"""

cur.execute(query)
# res = cur.execute("SELECT name FROM sqlite_master")
cur.execute(query2, ("data1","data2","data3"))
res = cur.execute("SELECT * FROM SNP")
print(res.fetchone())