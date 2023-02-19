from db_scripts import *
import numpy as np

# reqs=["rs705705", "rs653178", "rs9585056", "rs1456988", "rs56994090"]

# request="rs1770"
# request_type="rsid"

#r"chr\d:\d*"

# reqRes=DBreq(request, request_type)
# assert reqRes, "empty response"
# assert isinstance(reqRes, dict),"idk what to do with multiple entries yet"	# returns dict if only one entry, otherwise returns list of dicts
# print(reqRes)


# fileIn=getPath('gwas_trimmed_beeg.tsv')
# df=pd.read_csv("g:\My Drive\QMUL\QMUL-Bioinformatics-DDG\data\TSVs\gwas_trimmed_beeg.tsv",sep='\t')

# # df = df.loc[data.STUDY.str.contains(r'(type 1 diabetes)')]         # Nadia's code

# df=df[(df.STUDY.str.contains("Genetic architecture of") == False)]

# mask=df.apply(lambda row: row.astype(str).str.contains(r"chr\d:\d*").any(), axis=1)
# print (df[mask])


# fileIn=getPath('Func_trimmed.csv')
# df=pd.read_csv(fileIn)

print(DBreq("6:0000-6:19999000", "coords"))