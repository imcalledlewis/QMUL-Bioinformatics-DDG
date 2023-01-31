# import pandas as pd
# import sqlite3
# import os
# import re
from db_scripts import *

fileIn = "gwas_trimmed.tsv"

filepath=getPath(fileIn)

df = pd.read_csv(filepath, sep='\t')

colName=""
for col in df.columns[1:]:  # Ignore first column (index)
    badChar = re.search(r'\W+', col)                            # Searches for special characters,
    assert not badChar,"Found special character: "+str(col)     # raise exception if any are found.
    colName+=(col)      # Add another name column name
    colName+=(", ")     # Add a comma separator

colName=colName[:-2]    # removes last ' ,'

filepath=DBpath()
if os.path.exists(filepath):        # If the file exists:
    os.remove(filepath)             # delete it.
conn = sqlite3.connect(filepath)    # Opens (or creates) a db file
cur = conn.cursor()                 # Sets cursor

df.to_sql(name="SNP", con=conn, index=False, dtype={'SNPS': 'TEXT PRIMARY KEY'})

cur.execute("ALTER TABLE SNP DROP COLUMN `Unnamed: 0`") # remove index column - pandas refuses to not include it
res = cur.execute("SELECT * FROM SNP")
assert res.fetchone(), "unknown error"
print("\ndone\n")