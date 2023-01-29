# Simple script for testing database/ proof of concept

import pandas as pd
import sqlite3
import os

fileIn = "snps.db"
SNPname_req = ('rs1770',)

path = os.path.dirname(os.path.abspath(__file__))   # Gets current path of file
filepath = os.path.join(path, fileIn)               # Sets path relative to current file

assert os.path.exists(filepath),"Database file not found"
conn = sqlite3.connect(filepath)    # Opens db file
cur = conn.cursor()                 # Sets cursor
res = cur.execute("SELECT * FROM SNP WHERE SNPS LIKE ?",SNPname_req)
print(res.fetchall())