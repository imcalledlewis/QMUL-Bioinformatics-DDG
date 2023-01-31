import pandas as pd

df = pd.read_table('gwas_trimmed.tsv') # Load GWAS catalogue dataset (currently using dataset with Chr6 T1DM SNPs)
rsID_list = df["SNPS"].tolist() # Extract column values in 'SNPS' column of dataframe into a single list

# Create empty dataframe with column names
variant_pop_df = pd.DataFrame(columns=['SNP rsID',
                                       'Finland', 'Alt allele', 
                                       'Italy (Toscani)', 'Alt allele', 
                                       'British', 'Alt allele',]) 

# API for requesting population data based on SNP rsID query
def variant_frequency_API(rsID):
    import requests, sys

    server = "https://rest.ensembl.org"
    ext = f"/variation/human/{rsID}?pops=1"

    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

    if not r.ok:
      r.raise_for_status()
      sys.exit()

    decoded = r.json()
    return decoded

# Extracts alternate allele(s) from population data
def find_alt_allele(population_data):
    allele_pair = decoded['mappings'][0]['allele_string'] # extract reference and alternate allele(s) from population data
    allele_list = allele_pair.split('/') # split alleles into a list
    allele_list.pop(0) # remove reference allele
    return allele_list

# Extracts list of dictionaries containing population data from each chosen study population for alternate allele(s)
def filter_pop_data(alt_allele,population_data):
    
    pop_dictlist = []

    for dictionary in population_data: 
        if '1000GENOMES:phase_3:TSI' in dictionary['population'] and dictionary['allele'] in alt_allele: # Italian (Toscani) - 1000 Genomes Project
            pop_dictlist.append(dictionary) 
        elif '1000GENOMES:phase_3:FIN' in dictionary['population'] and dictionary['allele'] in alt_allele: # Finnish - 1000 Genomes Project
            pop_dictlist.append(dictionary) 
        elif '1000GENOMES:phase_3:GBR' in dictionary['population'] and dictionary['allele'] in alt_allele: # British (England and Scotland) - 1000 Genomes Project
            pop_dictlist.append(dictionary)         
    return pop_dictlist

# Collects variant frequencies for populations of interest and stores them in a list with SNP rsID and alternate allele
def variant_frequencies_by_pop(rsID,alt_allele,pop_dictlist):
    # Assign default values to variables
    FIN_freq = '' 
    FIN_alt  = ''
    TSI_freq = ''
    TSI_alt  = '' 
    GBR_freq = ''
    GBR_alt  = ''
    # Search for values and store into variables   
    for dictionary in pop_dictlist: 
        if 'FIN' in dictionary['population']: # Variant frequency for Finnish population 
            FIN_freq = dictionary['frequency']
            FIN_alt  = dictionary['allele']
        elif 'TSI' in dictionary['population']: # Variant frequency for Italian (Tuscani) population 
            TSI_freq = dictionary['frequency']
            TSI_alt  = dictionary['allele']
        elif 'GBR' in dictionary['population']:  # Variant frequency for Middle Eastern population
            GBR_freq = dictionary['frequency'] 
            GBR_alt  = dictionary['allele']
    # Combine values into a list
    freq_list = [rsID, 
                 FIN_freq, FIN_alt, 
                 TSI_freq, TSI_alt, 
                 GBR_freq, GBR_alt]
    return freq_list

# Turn variant frequencies list into a pandas dataframe with correct columns and combine with main dataframe
def create_SNP_row(rowlist,variant_pop_df):
    row = pd.DataFrame(row_list).T
    row.columns = variant_pop_df.columns # assigns columns based on main dataframe
    variant_pop_df = pd.concat([variant_pop_df, row]) # add row to main dataframe
    return variant_pop_df

# Iterate through rsID list and dictionary list to create row dataframes to be appended to the main dataframe
for rsID in rsID_list:
    decoded = variant_frequency_API(rsID) # request data for SNP by rsID
    population_data = decoded['populations'] # extract variant frequency data
    alt_allele = find_alt_allele(decoded) # find alternate allele
    pop_dictlist = filter_pop_data(alt_allele,population_data) # filter population data by study and allele
    row_list = variant_frequencies_by_pop(rsID,alt_allele,pop_dictlist) # create list of variant frequencies for dataframe row
    variant_pop_df = create_SNP_row(row_list,variant_pop_df) # create pandas dataframe from list and combine with main dataframe

# Write out dataframe as TSV file
variant_pop_df.to_csv('population_variation.tsv', sep="\t", index=False )
