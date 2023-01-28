import pandas as pd
import sqlite3
import os
import re
fileIn = "gwas_trimmed4.tsv"
fileOut = 'snps.db'

path = os.path.dirname(os.path.abspath(__file__))       # sets path relative to current file
filepath = os.path.join(path, fileIn)        
df = pd.read_csv(filepath, sep='\t')

colName=""              # Empty string that will be filled later
for col in df.columns:
    colName+=(col)      # Add another name column name
    colName+=(", ")     # Add a comma separator 
colName=colName[:-2]    # removes last ' ,'
# print(colName)

#colName = re.sub(r'[\W]', '_', colName)  # Replaces special characters and whitespace with underscores

colonPos = colName.find(':')

if colonPos:
    print("\nFUCK\n")
    print (colName[colonPos-5:colonPos+5])
else:
    print("\nYAY\n")


# path = os.path.dirname(os.path.abspath(__file__))       # sets path relative to current file
# filepath = os.path.join(path, fileOut)                  
# conn = sqlite3.connect(filepath)                        # Opens (or creates) a db file
# cur = conn.cursor()                                     # Sets cursor
# cur.execute("CREATE TABLE SNP(" + colName + ")")
# res = cur.execute("SELECT name FROM sqlite_master")
# print(res.fetchone())