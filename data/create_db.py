from db_scripts import *

gwas = getPath("gwas_trimmed.tsv")
# gwas = getPath("SNPS_filled_clean.tsv")
pop  = getPath("population_variation_noSpecial.tsv")
func = getPath('Func_trimmed.tsv')
# ont  = getPath("GO_trimmed_clean.tsv")
ont  = getPath("GO_new.tsv")

DB=DBpath()

if os.path.exists(DB):      # If the file exists,
    os.remove(DB)           # delete it.

pdDB(gwas, "gwas",       {"rsid":"TEXT PRIMARY KEY"})
pdDB(pop,  "population", {"rsid":"TEXT REFERENCES gwas(rsid)"})
pdDB(func, "functional", {"rsid":"TEXT REFERENCES gwas(rsid)"})
pdDB(ont,  "ontology",   {"rsid":"INTEGER REFERENCES gwas(rsid)"})

conn = sqlite3.connect(DB)  # Opens db file
cur = conn.cursor()         # Sets cursor

print("\ndone\n")