from db_scripts import *

gwas = getPath("gwas_trimmed.tsv")
pop  = getPath("population_variation_noSpecial.tsv")
func = getPath('Func_data_clean.tsv')
# ont  = getPath('ontology.tsv')

DB=DBpath()

if os.path.exists(DB):      # If the file exists,
    os.remove(DB)           # delete it.

pdDB(gwas, "gwas",       {"SNPS":"INTEGER PRIMARY KEY"})
pdDB(pop,  "population", {"SNP_rsID":"INTEGER REFERENCES gwas(SNPS)"})
pdDB(func, "functional", {"Uploaded_variation":"INTEGER REFERENCES gwas(SNPS)"})
# pdDB(ont,  "ontology",   {"foo":"INTEGER REFERENCES gwas(SNPS)"})

conn = sqlite3.connect(DB)  # Opens db file
cur = conn.cursor()         # Sets cursor

cur.execute("ALTER TABLE gwas DROP COLUMN `Unnamed: 0`")        # Remove index column - pandas stubbornly refuses to not include it
cur.execute("ALTER TABLE population DROP COLUMN `Unnamed: 0`")  # Remove index column - pandas stubbornly refuses to not include it
cur.execute("ALTER TABLE functional DROP COLUMN `Unnamed: 0`")  # Remove index column - pandas stubbornly refuses to not include it

print("\ndone\n")