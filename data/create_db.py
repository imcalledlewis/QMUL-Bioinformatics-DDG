from db_scripts import *

gwas = getPath("gwas_trimmed.tsv")
population = getPath("population_variation_noSpecial.tsv")
DB=DBpath()

if os.path.exists(DB):      # If the file exists,
    os.remove(DB)           # delete it.

conn = sqlite3.connect(DB)  # Opens  db file
cur = conn.cursor()         # Sets cursor


pdDB(gwas, "gwas", {"SNPS":"TEXT PRIMARY KEY"})
pdDB(population, "population", {"SNP_rsID":"TEXT REFERENCES gwas(SNPS)"})
# pdDB(ontology, "ontology", {"foo":"TEXT REFERENCES gwas(SNPS)"})

cur.execute("ALTER TABLE gwas DROP COLUMN `Unnamed: 0`")        # Remove index column - pandas stubbornly refuses to not include it
cur.execute("ALTER TABLE population DROP COLUMN `Unnamed: 0`")  # Remove index column - pandas stubbornly refuses to not include it

print("\ndone\n")