# Simple script for testing database/ proof of concept

from db_scripts import *

SNPname_req = ('rs1770',)
#SNPname_req = ('bad_request',)

r=DBreq(SNPname_req, 'SNPname')

if r:  # If it found anything
    print(r)
else:
    print("nothing found")