import pandas as pd
import sqlite3
import os

path = os.path.dirname(os.path.abspath(__file__))       # sets path relative to current file
filepath = os.path.join(path, "gwas_trimmed2.tsv")        

df = pd.read_csv(filepath, sep='\t')
colName=""              # Empty string that will be filled later
for col in df.columns:
    colName+=(col)      # Add another name column name
    colName+=(", ")     # Add a comma separator 
colName=colName[:-2]    # removes last ' ,'
#print(colName)

if ' ' in colName:
    print("\nFUCK\n")

# path = os.path.dirname(os.path.abspath(__file__))       # sets path relative to current file
# db = os.path.join(path, 'snps.db')                  
# conn = sqlite3.connect(db)                              # Opens (or creates) a db file
# cur = conn.cursor()                                     # Sets cursor
# cur.execute("CREATE TABLE SNP(title, year, score)")
# res = cur.execute("SELECT name FROM sqlite_master")
# print(res.fetchone())