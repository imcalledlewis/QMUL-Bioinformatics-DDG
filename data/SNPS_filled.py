import pandas as pd

# filter for variants with no chromosomal coordinates and created a separated list of variants and dataframe
df = pd.read_table('SNPS_BS.tsv.txt') 
df2 = df
df2 = df2.drop(df2[df2['SNPS'].str.contains('rs')].index)
df2 = df2.reset_index()
df2 = df2.drop('index', axis=1)
variant_list = df2["SNPS"].tolist() 

# create lists for API
chrom_list = []
chrom_pos_list = []
for variant in variant_list:
    variant_split = variant.split(":")
    chrom_list.append(variant_split[0].replace("chr", ""))
    chrom_pos_list.append(variant_split[1])
    
# assign coordinate values to correct columns of each SNP
for ind in df2.index:
    df2.loc[ind,'CHR_POS'] = chrom_pos_list[ind]
    df2.loc[ind,'CHR_ID'] = chrom_list[ind]
    
# API for requesting variant information based on SNP chromosomal coordinates
def variant_search_API(chrom,chrom_pos):
    import requests, sys

    server = "https://rest.ensembl.org"
    ext = f"/overlap/region/human/{chrom}:{chrom_pos}-{chrom_pos}?feature=variation"

    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

    if not r.ok:
      r.raise_for_status()
      sys.exit()

    decoded = r.json()
    return decoded

# empty dataframe
variant_df = pd.DataFrame(columns=['SNPS','CHR_POS','CHR_ID']) 
# list for variants that cannot be found
invalid_variant = []
# loop to build dataframe
for chrom,chrom_pos in zip(chrom_list,chrom_pos_list):
    try:
        decoded = variant_search_API(chrom,chrom_pos)
        rsID = decoded[0]['id']
    except:
        invalid_variant.append(chrom + ":" + chrom_pos)
        continue
    variant_list = [rsID, chrom_pos, chrom]
    variant_row = pd.DataFrame(variant_list).T
    variant_row.columns = variant_df.columns
    variant_df = pd.concat([variant_df, variant_row])

invalid_variant = list(dict.fromkeys(invalid_variant)) # remove duplicates from list
print(f"Couldn't get rsids for variants: {invalid_variant}")   
# merge modified dataset with dataframe containing new SNP rsIDs
df2 = df2.drop('SNPS', axis=1) # drop SNPS column from modified dataset
df_filled = pd.merge(variant_df, df2, on=['CHR_POS','CHR_ID']).drop_duplicates() # merge based on 'CHR_POS' and 'CHR_ID' columns

# create another separate dataset with row that have rsID SNPs
df3 = df
df3 = df3.loc[df3['CHR_POS'].notnull()]

# concat df originally containg SNP rsIDs with new df corrected with additional SNP rsIDs
df_corrected = pd.concat([df3, df_filled])
df_corrected

# Export corrected dataframe as a TSV file
df_corrected.to_csv('SNPS_filled.tsv', sep="\t", index=False )