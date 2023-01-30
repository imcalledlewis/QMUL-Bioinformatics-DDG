# import pandas as pd
# import sqlite3
# import os
# import re
from db_scripts import *

fileIn = "gwas_trimmed.tsv"
fileOut = 'snps.db'

path = os.path.dirname(os.path.abspath(__file__))   # Gets current path of file
filepath = os.path.join(path, fileIn)               # Sets path relative to current file
df = pd.read_csv(filepath, sep='\t')

colName=""
for col in df.columns[1:]:  # Ignore first column (index)
    badChar = re.search(r'\W+', col)                            # Searches for special characters,
    assert not badChar,"Found special character: "+str(col)     # raise exception if any are found.
    colName+=(col)      # Add another name column name
    colName+=(", ")     # Add a comma separator

colName=colName[:-2]    # removes last ' ,'

filepath = os.path.join(path, fileOut)
if os.path.exists(filepath):        # If the file exists:
    os.remove(filepath)             # delete it.
conn = sqlite3.connect(filepath)    # Opens (or creates) a db file
cur = conn.cursor()                 # Sets cursor

# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
df.to_sql(name="SNP", con=conn, index=False, dtype={'SNPS': 'TEXT PRIMARY KEY'})

cur.execute("ALTER TABLE SNPs DROP COLUMN `Unnamed: 0`") # remove index column - pandas refuses to not include it
#print(cur.execute("PRAGMA table_info('SNP')").fetchall()) # display info about table
res = cur.execute("SELECT * FROM SNP")
print(res.fetchone())   # prints first entry, to confirm database is working