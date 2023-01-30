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

def DBreq(request, request_type):
    DBpath=getPath(database)
    assert os.path.exists(DBpath),"Database file not found"
    conn = sqlite3.connect(DBpath)  # Opens db file
    cur = conn.cursor()             # Sets cursor
    if request_type=='SNPname':
        res = cur.execute("SELECT * FROM SNP WHERE SNPS LIKE ?",request)
    else:
        raise Exception(str(request_type)+" hasn't been added yet")
    return (res.fetchall())

#res = cur.execute("SELECT * FROM SNP WHERE SNPS LIKE ?",SNPname_req)