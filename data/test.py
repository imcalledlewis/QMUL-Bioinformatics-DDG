# ### Sandbox for testing ideas and functions. Very much subject to change.

from db_scripts import *
import json

filepath=getPath('Func_data.tsv')
data=pd.read_csv(filepath,sep='\t')

# print(data) # multiple duplicate rs values, need to decide way to break ties
dupeList = data.duplicated(subset=['#Uploaded_variation',],keep=False)   # Get list of duplicate values
clear()
# print(data[dupeList])
print("")
print(data[~dupeList])