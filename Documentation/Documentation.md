# Project documentation

# Introduction

This web application prototype is designed to retrieve information on
Single Nucleotide Polymorphisms (SNPs) seen in Type 1 Diabetes patients
identified by Genome wide association studies (GWAS). The database will
use information from the GWAS catalogue, along with population data from
Ensembl and the 1000 Genomes Project and functional information and Gene
Ontology information obtained through Ensembl's VEP tool which is all is
retrievable through a user friendly interface through the input of an
rsID, Chromosome position or a Gene name. The site also allows the user
to calculate Linkage Disequilibrium (LD) of SNPs selected for each
population producing a text file containing the LD values and plot these
values as a LD heatmap. The user is also able to enter multiple SNPs and
return a Manhattan plot of the p-values.

# Prerequisites:

## Functions used throughout:

A number of functions were used throughout the code such as ...

[code here]


+-----------------------------------------------------------------------+
| [   naughtyList=\[\]                                  ]{.c0}[\# List  |
| of lists of (index, p-val) we want to drop]{.c21 .c15}[\              |
|   ]{.c0}[for]{.c13 .c15}[ i ]{.c0}[in]{.c13 .c15}[ dupesDict:\        |
|       snp = dupesDict\[i\]                          ]{.c0}[\# Get     |
| list of (index, pVal)]{.c21 .c15}[\                                   |
|       sortByP=sorted(snp,key=]{.c0}[lambda]{.c13 .c15}[ x:            |
| ]{.c0}[0]{.c18 .c15}[-x\[]{.c0}[1]{.c18 .c15}[\])    ]{.c0}[\# Sort   |
| by p-value]{.c21 .c15}[\                                              |
|       sortByP=sortByP\[]{.c0}[1]{.c18 .c15}[:\]                       |
|   ]{.c0}[\# Select all but greatest p value]{.c21 .c15}[\             |
|       naughtyList.append(sortByP)\                                    |
| \                                                                     |
| \                                                                     |
|   dropList=\[\]                         ]{.c0}[\# List of indices for |
| rows we want to drop]{.c21 .c15}[\                                    |
|   ]{.c0}[for]{.c13 .c15}[ i ]{.c0}[in]{.c13 .c15}[ naughtyList:       |
|         ]{.c0}[\# Enter first list]{.c21 .c15}[\                      |
|       ]{.c0}[for]{.c13 .c15}[ j ]{.c0}[in]{.c13 .c15}[ i:             |
|         ]{.c0}[\# Enter second list]{.c21 .c15}[\                     |
|           dropList.append(j\[]{.c0}[0]{.c15 .c18}[\])       ]{.c0}[\# |
| Add the index from each tuple]{.c21 .c15}[\                           |
| \                                                                     |
| \                                                                     |
|   ]{.c0}[return]{.c13 .c15}[(dataframe.drop(dropList))    ]{.c0}[\#   |
| Return dataframe without duplicate values]{.c21 .c15}                 |
+-----------------------------------------------------------------------+

[\
\
\
]{.c0}

[]{#t.59b2d73cce28e0f846926b398a5396f1238f472c}[]{#t.2}

+-----------------------------------------------------------------------+
| [def]{.c13 .c15}[ removeDupeGeneMap(GeneMap):\                        |
|   ]{.c0}[try]{.c13 .c15}[:\                                           |
|       GeneMap=GeneMap.split(]{.c0}[\', \']{.c35 .c15}[)\              |
|       uniques=]{.c0}[\"\"]{.c35 .c15}[\                               |
|       ]{.c0}[for]{.c13 .c15}[ item ]{.c0}[in]{.c13 .c15}[ GeneMap:\   |
|           ]{.c0}[if]{.c13 .c15}[ item ]{.c0}[not]{.c13                |
| .c15}[ ]{.c0}[in]{.c13 .c15}[ uniques: ]{.c0}[\# If the item hasn\'t  |
| been seen before,]{.c21 .c15}[\                                       |
|               uniques+=(item)     ]{.c0}[\# add it to the list.]{.c21 |
| .c15}[\                                                               |
|               uniques+=(]{.c0}[\", \"]{.c35 .c15}[)     ]{.c0}[\#     |
| Also add \' ,\']{.c21 .c15}[\                                         |
|       ]{.c0}[return]{.c13 .c15}[ (uniques\[:]{.c0}[-2]{.c18 .c15}[\]) |
|       ]{.c0}[\# Remove last \' ,\']{.c21 .c15}[\                      |
|   ]{.c0}[except]{.c13 .c15}[:\                                        |
|       ]{.c0}[return]{.c13 .c15}[ (]{.c0}[\"Data unavailable\"]{.c35   |
| .c15}[)     ]{.c0}[\# Return this if geneMap is empty]{.c21 .c15}     |
+-----------------------------------------------------------------------+

# []{.c30} {#h.vhchvtb4vp8x .c9 .c12 .c31 .c34}

# Structure: {#h.exepwhhdz8ou .c9 .c12 .c31}

[![](images/image4.png){style="width: 601.70px; height: 412.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 601.70px; height: 412.00px;"}

[]{.c2}

## [GWAS:]{.c10} {#h.9yfmc6qy2clu .c8}

[This information was downloaded from the GWAS catalogue where a TSV
file was downloaded and then trimmed using the following code;]{.c2}

[]{#t.b1af7d7bc328582cfe763ff0e0cbb9d8bcbeb335}[]{#t.3}

+-----------------------------------------------------------------------+
| [fileIn = getPath(]{.c4                                               |
| .c23}[\'gwas_catalog_v1.0-associations_e108_r2023-01-14.tsv\']{.c3}[) |
| ]{.c4 .c23}[\# https://www.ebi.ac.uk/gwas/docs/file-downloads]{.c21   |
| .c23}[\                                                               |
| fileOut = getPath(]{.c4 .c23}[\'gwas_trimmed.tsv\']{.c3}[)\           |
| \                                                                     |
| data = pd.read_csv(fileIn, sep=]{.c4 .c23}[\'\\t\']{.c3}[,            |
| low_memory=]{.c4 .c23}[False]{.c13 .c23}[)    ]{.c4 .c23}[\# Reads    |
| gwas tsv]{.c21 .c23}[\                                                |
| data=removeSpecial(data)    ]{.c4 .c23}[\# removes special characters |
| in column names]{.c21 .c23}                                           |
+-----------------------------------------------------------------------+

[This code uses pandas to open the TSV file, creates a dataframe called
data, and removes any special characters from the column names, as SQL
does not interact with special characters very well.]{.c2}

[]{#t.638fb5b406f87bace7364f8ea9275d9a6c56f7f3}[]{#t.4}

+-----------------------------------------------------------------------+
| [data=data.query(]{.c4}[\"disease_trait==\'Type 1 diabetes\' or       |
| study.str.contains(\'type 1 diabetes\')\"]{.c35}[)\                   |
| data =                                                                |
| data.loc\[data.snps.str.contains(]{.c4}[r\'rs\[0-9\]+\']{.c35}[)\]    |
|      ]{.c4}[\# get only snps with rsids]{.c21}[\                      |
| ]{.c4}[#data = data.loc\[data\[\'CHR_ID\'\]==\'6\'\]                  |
|        # Select only rows for chromosome 6]{.c21}                     |
+-----------------------------------------------------------------------+

The data frame is then filtered further so that it only has data that
references T1D in the "disease_trait" column so that only T1D data
remains in the dataframe. Next all SNPs that don\'t have rsIDs are
removed, as some cells had incompatible data in this column.



  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  [data = data\[\[]{.c4 .c23}[\"snps\"]{.c3}[,]{.c4 .c23}[\"region\"]{.c3}[,]{.c4 .c23}[\"chr_pos\"]{.c3}[,]{.c4 .c23}[\"chr_id\"]{.c3}[,]{.c4 .c23}[\"p_value\"]{.c3}[,]{.c4 .c23}[\"mapped_gene\"]{.c3}[\]\]]{.c4 .c23}
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The dataframe is then trimmed again so that it contains only the
columns of interest   \"snps\", \"region\", \"chr_pos\", \"chr_id\",
\"p_value\", \"mapped_gene\". ]{.c2}



+-----------------------------------------------------------------------+
| [data=removeDupeSNP(data)    ]{.c4}[\# Remove duplicates (leaving the |
| entry with largest p value)]{.c21}[\                                  |
| newCol=\[removeDupeGeneMap(r\[]{.c4}[\"mapped_gene\"]{.c35}[\])       |
| ]{.c4}[for]{.c13}[ i, r ]{.c4}[in]{.c13}[ data.iterrows()\]]{.c4}     |
|                                                                       |
| [data\[]{.c4}[\"mapped_gene\"]{.c35}[\]=newCol]{.c4}                  |
+-----------------------------------------------------------------------+

[Duplicate mapped_gene information is then removed.]{.c2}

[]{.c2}

[]{#t.efbc0c483d3f71e27abdb0a27605856edba6693c}[]{#t.7}

+-----------------------------------------------------------------------+
| [data.rename(columns = {]{.c4 .c23}[\'snps\']{.c3}[:]{.c4             |
| .c23}[\'rsid\']{.c3}[}, inplace = ]{.c4 .c23}[True]{.c13 .c23}[)\     |
| \                                                                     |
| ]{.c4 .c23}[\# if os.path.exists(fileOut): \# If the file             |
| exists,]{.c21 .c23}[\                                                 |
| ]{.c4 .c23}[\#     os.remove(fileOut)     \# delete it.]{.c21 .c23}[\ |
| data.to_csv(fileOut, sep=]{.c4 .c23}[\'\\t\']{.c3}[, index=]{.c4      |
| .c23}[False]{.c13 .c23}[)]{.c4 .c23}                                  |
+-----------------------------------------------------------------------+

Next the column \'snps\' was renamed to \'rsid\' and made the change
directly to the dataframe by setting inplace=True.

## Functional information and Gene Ontology:

We have used Ensembl\'s Variant Effect Predictor web tool to gather the
Functional and Ontology data by submitting a job with the rsIDs as input
from the above GWAS TSV file. After running the job, we get an output of
text file with columns like:

rsid: the reference SNP identifier for the variant.

[Allele: the alternative allele observed at the variant site.]{.c2}

[impact: the impact of the variant on the affected gene]{.c2}

[consequence: the consequence of the variant on the affected gene]{.c2}

[location: the location of the variant within the affected gene]{.c2}

[Gene: the Ensembl gene ID of the affected gene.]{.c2}

[Symbol: the gene symbol or name.]{.c2}

[Feature_Type: the type of genomic feature the variant is located
in]{.c2}

[Feature: the Ensembl ID of the specific feature the variant is located
in]{.c2}

[Exon: the exon number(s) affected by the variant.]{.c2}

[Intron: the intron number(s) affected by the variant.]{.c2}

[HGVSc: the HGVS nomenclature for the variant at the cDNA .]{.c2}

[HGVSp: the HGVS nomenclature for the variant at the protein
level.]{.c2}

[cDNA_position: the position of the variant within the cDNA sequence of
the affected gene.]{.c2}

[CDS_position: the position of the variant within the coding sequence of
the affected gene.]{.c2}

[Protein_position: the position of the variant within the protein
sequence of the affected gene.]{.c2}

[Amino_acids: the amino acid change resulting from the variant.]{.c2}

[Codons: the DNA codon change resulting from the variant.]{.c2}

[Existing_variation: additional identifiers for the variant in other
databases.]{.c2}

[Distance: the distance to the nearest feature in the same or opposite
strand.]{.c2}

[Strand: the genomic strand the variant is located on.]{.c2}

[FLAGS: additional information about the variant .]{.c2}

[SYMBOL_SOURCE: the source of the gene symbol or name.]{.c2}

[HGNC_ID: the HGNC gene ID of the affected gene.]{.c2}

[MANE_SELECT: indication of whether this transcript is the MANE (Matched
Annotation from NCBI and EMBL-EBI) Select transcript.]{.c2}

[MANE_PLUS_CLINICAL: indication of whether this transcript is the MANE
Select Plus Clinical (MPC) transcript.]{.c2}

[TSL: transcript support level (a measure of transcript annotation
confidence).]{.c2}

[APPRIS: annotation of principal isoforms for each gene.]{.c2}

[ENSP: the Ensembl protein ID of the affected protein.]{.c2}

[SIFT: prediction of the effect of the variant on protein
function.]{.c2}

[PolyPhen: prediction of the effect of the variant on protein
function.]{.c2}

[CLIN_SIG: clinical significance of the variant.]{.c2}

[SOMATIC: indication of whether the variant is somatic or
germline.]{.c2}

[PHENO: phenotype association of the variant.]{.c2}

[PUBMED: PubMed ID of publications reporting functional evidence of the
variant.]{.c2}

[MOTIF_NAME: name of the DNA motif affected by the variant.]{.c2}

[MOTIF_POS: position of the variant within the affected DNA motif.]{.c2}

[HIGH_INF_POS: indication of whether the variant falls in a highly
conserved position within the DNA motif.]{.c2}

[MOTIF_SCORE_CHANGE: the effect of the variant on the score of the
affected DNA motif.]{.c2}

[TRANSCRIPTION_FACTORS: transcription factors that bind the affected DNA
motif.]{.c2}

[CADD_PHRED: Phred-scaled CADD score (Combined Annotation-Dependent
Depletion), which predicts the deleteriousness of variants.]{.c2}

[CADD_RAW: the raw CADD score, which is a measure of the deleteriousness
of variants.]{.c2}

[GO Terms: Gene Ontology (GO) terms associated with the affected
gene.]{.c2}

[The VEP file provides detailed information about the functional and
ontological consequences of genetic variants, including their impact on
genes, proteins, and pathways.]{.c2}

[We have converted the text file to a tsv file and trimmed down the file
to include only the rsID, Alleles, CADD_PHRED and CADD_RAW scores
columns for the functional data and the rsID, location, gene, symbol, GO
terms columns for the Ontology data. We have further used these TSV
files in our database.]{.c2}

[CADD (Combined Annotation Dependent Depletion) is a tool used for
predicting the potential harm caused by genetic variants. The tool
generates a score that indicates the likelihood of a variant being
deleterious.]{.c2}

[One advantage of CADD over SIFT and PolyPhen is that CADD integrates a
larger and more diverse set of functional annotations. It also considers
the effects of variants on non-coding regions of the genome, which can
be important for understanding the functional consequences of variants
that are not in protein-coding regions.]{.c2}

[]{.c2}

------------------------------------------------------------------------

## []{.c10} {#h.bob8u1u023ib .c8 .c32}

## [Linkage Disequilibrium:]{.c10} {#h.x88z4oadkpbf .c8}

Linkage disequilibrium (LD) is the degree of non-random association of
the allele of one SNP with the allele of another SNP within a
population. LD is typically measured by two metrics: D' and r[2]{.c16}[.
]{.c2}

[D' is the normalised values of D, the coefficient of linkage
disequilibrium, where A and B are alleles of two SNPs in different
loci:]{.c2}

![](images/image1.png)[ ]{.c39 .c42}

![](images/image2.png)[  ]{.c16}[is the correlation coefficient between
two loci:]{.c2}

![](images/image3.png)

## [Collecting data]{.c41 .c39} {#h.9g8mzey51un2 .c45}

Linkage disequilibrium data was obtained from LDlink using the LDmatrix
tool. D' and r[2]{.c16} values for SNPs were calculated using 1000
Genomes Project data for all three populations. LD data was obtained by
inputting a list of SNPs from the same chromosome and selecting the
population which would be used for allele frequency data for LD
calculations. LDmatrix would produce two text files containing a matrix
of results for D' and r[2]{.c16}[ values calculated between all SNPs
pair combinations in the input list. This was performed separately for
each population. Some SNPs did not have any LD data due to a lack of
allele frequency data for those SNPs in the 1000 Genomes Project.]{.c2}

LD datasets containing D' and r[2]{.c16}[ values for Finnish, Toscani
and British populations are loaded in with pandas as separate
dataframes. Each dataframe has their index set to the first column which
contains SNP rsIDs.]{.c2}

[]{#t.2d68cf246bdeee4863dcdfbc42860528c30c8e2e}[]{#t.8}

+-----------------------------------------------------------------------+
| [import]{.c24}[ pandas ]{.c1}[as]{.c24}[ pd\                          |
| ]{.c1}[\# Finland (FIN)]{.c6}[\                                       |
| LD_D\_FIN = pd.read_table(]{.c1}[\'FIN_D.txt\']{.c26}[)\              |
| LD_D\_FIN = LD_D\_FIN.set_index(]{.c1}[\'RS_number\']{.c26}[)\        |
| LD_r2_FIN = pd.read_table(]{.c1}[\'FIN_r2.txt\']{.c26}[)\             |
| LD_r2_FIN = LD_r2_FIN.set_index(]{.c1}[\'RS_number\']{.c26}[)\        |
| ]{.c1}[\# Italy - Tuscany (TSI)]{.c6}[\                               |
| LD_D\_TSI = pd.read_table(]{.c1}[\'TSI_D.txt\']{.c26}[)\              |
| LD_D\_TSI = LD_D\_TSI.set_index(]{.c1}[\'RS_number\']{.c26}[)\        |
| LD_r2_TSI = pd.read_table(]{.c1}[\'TSI_r2.txt\']{.c26}[)\             |
| LD_r2_TSI = LD_r2_TSI.set_index(]{.c1}[\'RS_number\']{.c26}[)\        |
| ]{.c1}[\# British (GBR)]{.c6}[\                                       |
| LD_D\_GBR = pd.read_table(]{.c1}[\'GBR_D.txt\']{.c26}[)\              |
| LD_D\_GBR = LD_D\_GBR.set_index(]{.c1}[\'RS_number\']{.c26}[)\        |
| LD_r2_GBR = pd.read_table(]{.c1}[\'GBR_r2.txt\']{.c26}[)\             |
| LD_r2_GBR = LD_r2_GBR.set_index(]{.c1}[\'RS_number\']{.c26}[)]{.c1}   |
+-----------------------------------------------------------------------+

[]{.c17}

[This function uses the itertools combination function to create a list
of tuples containing all unique pairs of SNPs possible from a list of
SNPs. The list is then separated into two lists containing the first and
second element of each tuple.]{.c2}

[]{#t.3cd888f33c1969e34d6e88ae1b5769c14c614333}[]{#t.9}

+-----------------------------------------------------------------------+
| [\# Take list of SNPs and creates a pair of lists containing the 1st  |
| and 2nd SNP of each combination  ]{.c6}[\                             |
| ]{.c1}[def]{.c24}[ ]{.c1}[SNP_pair_lists]{.c40}[(SNP_list):\          |
|    SNP_combinations =                                                 |
| list(itertools.combinations(SNP_list,]{.c1}[2]{.c7}[))\               |
|    SNP_1\_list = \[\]\                                                |
|    SNP_2\_list = \[\]\                                                |
|    ]{.c1}[for]{.c24}[ SNP_pair ]{.c1}[in]{.c24}[ SNP_combinations:\   |
|        SNP_1\_list.append(SNP_pair\[]{.c1}[0]{.c7}[\])\               |
|        SNP_2\_list.append(SNP_pair\[]{.c1}[1]{.c7}[\])\               |
|    ]{.c1}[return]{.c24}[ SNP_1\_list, SNP_2\_list\                    |
| \                                                                     |
| SNP_1\_list, SNP_2\_list = SNP_pair_lists(SNP_list)]{.c1}             |
+-----------------------------------------------------------------------+

[]{.c17}

[An empty dataframe is created to be filled with rows containing data
from all six dataframes. This loop uses the two lists created from the
SNP list to index each dataframe and extract the respective LD value.
These are used to create a list which is converted into a single row
pandas dataframe which is added to the empty dataframe using pandas
concat until data for all relevant pairwise LD calculations have been
added. The completed dataframe is then outputted as a TSV file.]{.c2}

[]{#t.a0d21dcccdcbe0c4a56237beb3046f132352f165}[]{#t.10}

+-----------------------------------------------------------------------+
| [\# Create Empty dataframe ]{.c6}[\                                   |
| LD_dataset = pd.DataFrame(columns=\[]{.c1}[\'SNP_1\']{.c26}[,         |
| ]{.c1}[\'SNP_2\']{.c26}[, ]{.c1}[\'FIN_D\\\'\']{.c26}[,               |
| ]{.c1}[\'FIN_r2\']{.c26}[, ]{.c1}[\'TSI_D\\\'\']{.c26}[,              |
| ]{.c1}[\'TSI_r2\']{.c26}[, ]{.c1}[\'GBR_D\\\'\']{.c26}[,              |
| ]{.c1}[\'GBR_r2\']{.c26}[\])\                                         |
| ]{.c1}[\# Indexes the respective LD calculation for each pair and     |
| adds it to the data]{.c6}[\                                           |
| ]{.c1}[for]{.c24}[ SNP_1,SNP_2                                        |
| ]{.c1}[in]{.c24}[ zip(SNP_1\_list,SNP_2\_list):\                      |
|    ]{.c1}[\# Finland]{.c6}[\                                          |
|    FIN_D = LD_D\_FIN\[SNP_1\].loc\[SNP_2\]\                           |
|    FIN_r2 = LD_r2_FIN\[SNP_1\].loc\[SNP_2\]\                          |
|    ]{.c1}[\# Italy - Tuscany]{.c6}[\                                  |
|    TSI_D = LD_D\_TSI\[SNP_1\].loc\[SNP_2\]\                           |
|    TSI_r2 = LD_r2_TSI\[SNP_1\].loc\[SNP_2\]\                          |
|    ]{.c1}[\# British]{.c6}[\                                          |
|    GBR_D = LD_D\_GBR\[SNP_1\].loc\[SNP_2\]\                           |
|    GBR_r2 = LD_r2_GBR\[SNP_1\].loc\[SNP_2\]\                          |
|    ]{.c1}[\# Create row of data and combine with LD dataset           |
| dataframe]{.c6}[\                                                     |
|    row_list = \[SNP_1, SNP_2, FIN_D, FIN_r2, TSI_D, TSI_r2, GBR_D,    |
| GBR_r2\]\                                                             |
|    row = pd.DataFrame(row_list).T\                                    |
|    row.columns = LD_dataset.columns\                                  |
|    LD_dataset = pd.concat(\[LD_dataset, row\])\                       |
| ]{.c1}[\# Write out LD dataset as a TSV]{.c6}[\                       |
| LD_dataset.to_csv(]{.c1}[\'LD_T1DM_Chr6.tsv\']{.c26}[,                |
| sep=]{.c1}[\"\\t\"]{.c26}[, index=]{.c1}[False]{.c24}[)]{.c1}         |
+-----------------------------------------------------------------------+

[]{.c17}

[]{.c17}

------------------------------------------------------------------------

## []{.c41 .c39} {#h.czvflz3vh9cw .c27}

## [Outputting LD results:]{.c39 .c41} {#h.2wm5ip20i7c1 .c37 .c31}

[When a user searches by gene name or chromosomal coordinates, if
multiple SNPs are returned, a list of SNPs is used to filter the LD
dataset for all rows with entries for all pairwise LD calculations of
SNPs in the list and output a results dataframe.]{.c2}

[]{.c2}

[Before filtering, the list is checked for any SNPs which are not in the
LD dataset due to lack of LD data and any offending SNPs are removed
from the list. ]{.c2}

[]{#t.2485981c42700898c52a2bdcff2edf8fc12f566c}[]{#t.11}

+-----------------------------------------------------------------------+
| [def]{.c24}[ ]{.c1}[remove_invalid_SNPs]{.c40}[(SNP_list,             |
| LD_dataset_file = ]{.c1}[\"data/TSVs/LD_T1DM_Chr6.tsv\"]{.c26}[):\    |
| ]{.c1}[\# remove SNPs returned from query which have no LD values in  |
| LD dataset]{.c6}[\                                                    |
|    ]{.c1}[\# Load LD dataset as pandas dataframe]{.c6}[\              |
|    LD_df = pd.read_table(LD_dataset_file)\                            |
|    ]{.c1}[\# checks for SNPs in subset which are not in LD            |
| dataset]{.c6}[\                                                       |
|    invalid_list = \[\]\                                               |
|    ]{.c1}[for]{.c24}[ SNP ]{.c1}[in]{.c24}[ SNP_list:\                |
|        ]{.c1}[if]{.c24}[ SNP                                          |
| ]{.c1}[not]                                                           |
| {.c24}[ ]{.c1}[in]{.c24}[ LD_df\[]{.c1}[\'SNP_1\']{.c26}[\].tolist(): |
| ]{.c1}[\# check if SNP is in LD dataset]{.c6}[\                       |
|            invalid_list.append(SNP) ]{.c1}[\# add to list of invalid  |
| SNPs]{.c6}[\                                                          |
|    print(invalid_list)\                                               |
|    ]{.c1}[\# remove invalid SNPs from SNP list passed to LD           |
| plot]{.c6}[\                                                          |
|    ]{.c1}[for]{.c24}[ SNP ]{.c1}[in]{.c24}[ invalid_list:\            |
|        SNP_list.remove(SNP)\                                          |
|    ]{.c1}[return]{.c24}[ SNP_list\                                    |
| \                                                                     |
| SNP_list = remove_invalid_SNPs(SNP_list)]{.c1 .c39}                   |
+-----------------------------------------------------------------------+

[]{.c2}

[The SNP list is then used to create two lists containing the first and
second element of each tuple using the SNP_pair_lists() function defined
earlier.]{.c2}

[]{#t.467397c9bfe0b58ffeebec61aad4b21b644362e1}[]{#t.12}

+-----------------------------------------------------------------------+
| [\# create a pair of lists containing the 1st and 2nd SNP of each     |
| combination]{.c6}[\                                                   |
| SNP_1\_list, SNP_2\_list = SNP_pair_lists(SNP_list)]{.c1}             |
+-----------------------------------------------------------------------+

[]{.c2}

[The LD dataset containing all available data for pairwise LD
calculations is loaded in with pandas and an empty dataframe is created
for the filtered data. The pair of SNP lists are then used to index the
LD dataset dataframe for all rows with pairs of SNPs relevant to the
user's search query which are added to the LD results dataframe using
pandas concat.]{.c2}

[]{#t.258f382ba68c7d1d3a17e1bbd7a0ff9175b6a7fa}[]{#t.13}

+-----------------------------------------------------------------------+
| [\# Load LD dataset and create empty dataframe for filtered           |
| results]{.c6}[\                                                       |
| LD_df = pd.read_table(LD_dataset_file)\                               |
| LD_results_df = pd.DataFrame(columns=\[]{.c1}[\'SNP_1\']{.c26}[,      |
| ]{.c1}[\'SNP_2\']{.c26}[, ]{.c1}[\'FIN_D\\\'\']{.c26}[,               |
| ]{.c1}[\'FIN_r2\']{.c26}[, ]{.c1}[\'TSI_D\\\'\']{.c26}[,              |
| ]{.c1}[\'TSI_r2\']{.c26}[, ]{.c1}[\'GBR_D\\\'\']{.c26}[,              |
| ]{.c1}[\'GBR_r2\']{.c26}[\])\                                         |
| ]{.c1}[\# Loop indexing LD dataset using each pair of SNPs]{.c6}[\    |
| ]{.c1}[for]{.c24}[ SNP_1,SNP_2                                        |
| ]{.c1}[in]{.c24}[ zip(SNP_1\_list,SNP_2\_list):\                      |
|    LD_row = LD_df.loc\[((LD_df\[]{.c1}[\'SNP_1\']{.c26}[\] == SNP_1)  |
| & (LD_df\[]{.c1}[\'SNP_2\']{.c26}[\] == SNP_2) \|\                    |
|                        (LD_df\[]{.c1}[\'SNP_1\']{.c26}[\] == SNP_2) & |
| (LD_df\[]{.c1}[\'SNP_2\']{.c26}[\] == SNP_1))\]\                      |
|    LD_results_df = pd.concat(\[LD_results_df, LD_row\])]{.c1}         |
+-----------------------------------------------------------------------+

[]{.c17}

------------------------------------------------------------------------

## []{.c41 .c39} {#h.tm8mndqz55x9 .c27}

## [LD heatmap plots:]{.c41 .c39} {#h.hebu2brlzmob .c31 .c37}

When a user searches by gene name or chromosomal coordinates, if
multiple SNPs are returned, a list of SNPs is also used to extract LD
values for all relevant pairwise SNP calculations to create a dataframe
used to create a heatmap plot of LD values.

[The LD dataset is loaded in with pandas and SNPs not present in the
dataset are removed from the list of SNPs passed from the user query.
The SNP list is then used to create two lists containing the first and
second element of each tuple using the SNP_pair_lists() function defined
earlier.]{.c2}

[]{#t.37287ca283631a102efe72ff61cf4610e2d4e853}[]{#t.14}

+-----------------------------------------------------------------------+
| [\# load LD dataset]{.c6}[\                                           |
| LD_df = pd.read_table(]{.c1}[\'LD_T1DM_Chr6.tsv\']{.c26}[)\           |
| ]{.c1}[\# checks for SNPs in subset which are not in LD               |
| dataset]{.c6}[\                                                       |
| SNP_list = remove_invalid_SNPs(SNP_list)]{.c1 .c39}                   |
|                                                                       |
| [\# create a pair of lists containing the 1st and 2nd SNP of each     |
| combination]{.c6}[\                                                   |
| SNP_1\_list, SNP_2\_list = SNP_pair_lists(SNP_list)]{.c1 .c39}        |
+-----------------------------------------------------------------------+

[]{.c17}

[An empty dataframe is created to be filled with LD values used to
create the LD plot. The pair of SNP lists are then used to index the LD
dataset dataframe and extract the LD value for all possible pairwise LD
calculations from the SNP list. A row of LD values is created for each
SNP where each column corresponds with the pairwise LD calculation with
one of the SNPs from the list. Each row is added to the empty dataframe
using pandas concat.]{.c2}

[]{#t.f562ae5cedba9ec0d08c9ebb9c8653d95d6fa722}[]{#t.15}

+-----------------------------------------------------------------------+
| [LD_matrix_df = pd.DataFrame(columns=\[SNP_list\]) ]{.c1}[\# One      |
| column per SNP in list (Since a list object is passed, could just     |
| pass the SNP list]{.c6}[\                                             |
| ]{.c1}[for]{.c24}[ SNP_1 ]{.c1}[in]{.c24}[ SNP_list:\                 |
|    ]{.c1}[\# Create empty list]{.c6}[\                                |
|    LD_value_list = \[\]\                                              |
|    ]{.c1}[\# Sub-loop - Loops to create list of datapoints]{.c6}[\    |
|    ]{.c1}[for]{.c24}[ SNP_2 ]{.c1}[in]{.c24}[ SNP_list:\              |
|        ]{.c1}[if]{.c24}[ SNP_1 == SNP_2:\                             |
|            SNP_Datapoint = ]{.c1}[1]{.c7}[\                           |
|            LD_value_list.append(SNP_Datapoint)\                       |
|        ]{.c1}[else]{.c24}[:\                                          |
|            ]{.c1}[#try:]{.c6}[\                                       |
|            ]{.c1}[\# Search for specific row containing value]{.c6}[\ |
|            LD_row = LD_df.loc\[((LD_df\[]{.c1}[\'SNP_1\']{.c26}[\] == |
| SNP_1) & (LD_df\[]{.c1}[\'SNP_2\']{.c26}[\] == SNP_2) \|\             |
|                                (LD_df\[]{.c1}[\'SNP_1\']{.c26}[\] ==  |
| SNP_2) & (LD_df\[]{.c1}[\'SNP_2\']{.c26}[\] == SNP_1))\]\             |
|            ]{.c1}[\# Extract value and add to list]{.c6}[\            |
|            SNP_Datapoint =                                            |
| LD_row\[]{.c1}[\'GBR_r2\']{.c26}[\].tolist()\[]{.c1}[0]{.c7}[\]       |
| ]{.c1}[\# currently using Finnish data]{.c6}[\                        |
|            LD_value_list.append(SNP_Datapoint)\                       |
|            ]{.c1}[#except:]{.c6}[\                                    |
|                                                                       |
|  ]{.c1}[#invalid_list.append((SNP_main,SNP_second))]{.c6}[\           |
|    ]{.c1}[\# Convert into dataframe row and transpose]{.c6}[\         |
|    row = pd.DataFrame(LD_value_list).T\                               |
|    row.columns = LD_matrix_df.columns\                                |
|    LD_matrix_df = pd.concat(\[LD_matrix_df, row\])]{.c1}              |
+-----------------------------------------------------------------------+

[]{.c17}

[The LD matrix dataframe is passed to the ld_plot function. The number
of rows (n) is used to create a mask which will hide half of the heatmap
to create a triangular plot. A coordinate matrix is also created to
rotate the heatmap plot. The SNP list is used to create the axis labels
located at the bottom of the plot. The function's title parameter passes
a string which is used to determine the plot title.]{.c2}

[]{#t.29a54725cd80635d2188dacbe57f49bc64d7b5b3}[]{#t.16}

+-----------------------------------------------------------------------+
| [def]{.c24}[ ]{.c1}[ld_plot]{.c40}[(ld, labels, title):\              |
|    n = ld.shape\[]{.c1}[0]{.c7}[\]\                                   |
| \                                                                     |
|    figure = plt.figure()\                                             |
| \                                                                     |
|    ]{.c1}[\# mask triangle matrix]{.c6}[\                             |
|    mask = np.tri(n, k=]{.c1}[0]{.c7}[)\                               |
|    ld_masked = np.ma.array(ld, mask=mask)\                            |
| \                                                                     |
|    ]{.c1}[\# create rotation/scaling matrix]{.c6}[\                   |
|    t = np.array(\[\[]{.c1}[1]{.c7}[, ]{.c1}[0.5]{.c7}[\],             |
| \[]{.c1}[-1]{.c7}[, ]{.c1}[0.5]{.c7}[\]\])\                           |
|    ]{.c1}[\# create coordinate matrix and transform it]{.c6}[\        |
|    coordinate_matrix = np.dot(np.array(\[(i\[]{.c1}[1]{.c7}[\],       |
| i\[]{.c1}[0]{.c7}[\])\                                                |
|                                         ]{.c1}[for]{.c24}[ i          |
| ]{.c1}[in]{.c24}[ itertools.product(range(n, ]{.c1}[-1]{.c7}[,        |
| ]{.c1}[-1]{.c7}[), range(]{.c1}[0]{.c7}[, n + ]{.c1}[1]{.c7}[,        |
| ]{.c1}[1]{.c7}[))\]), t)\                                             |
|    ]{.c1}[\# plot]{.c6}[\                                             |
|    ax = figure.add_subplot(]{.c1}[1]{.c7}[, ]{.c1}[1]{.c7}[,          |
| ]{.c1}[1]{.c7}[)\                                                     |
|                                                                       |
|  ax.spines\                                                           |
| []{.c1}[\'bottom\']{.c26}[\].set_position(]{.c1}[\'center\']{.c26}[)\ |
|                                                                       |
|  a                                                                    |
| x.spines\[]{.c1}[\'top\']{.c26}[\].set_visible(]{.c1}[False]{.c24}[)\ |
|                                                                       |
|  ax.                                                                  |
| spines\[]{.c1}[\'right\']{.c26}[\].set_visible(]{.c1}[False]{.c24}[)\ |
|                                                                       |
|  ax                                                                   |
| .spines\[]{.c1}[\'left\']{.c26}[\].set_visible(]{.c1}[False]{.c24}[)\ |
|    ax.get_yaxis().set_visible(]{.c1}[False]{.c24}[)\                  |
|    plt.tick_params(axis=]{.c1}[\'x\']{.c26}[,                         |
| which=]{.c1}[\'both\']{.c26}[, top=]{.c1}[False]{.c24}[)\             |
|    plt.pcolor(coordinate_matrix\[:, ]{.c1}[1]{.c7}[\].reshape(n +     |
| ]{.c1}[1]{.c7}[, n + ]{.c1}[1]{.c7}[),\                               |
|               coordinate_matrix\[:, ]{.c1}[0]{.c7}[\].reshape(n +     |
| ]{.c1}[1]{.c7}[, n + ]{.c1}[1]{.c7}[),\                               |
|               np.flipud(ld_masked), edgecolors =                      |
| ]{.c1}[\"white\"]{.c26}[,\                                            |
|               linewidth = ]{.c1}[1.5]{.c7}[, cmap =                   |
| ]{.c1}[\'OrRd\']{.c26}[)\                                             |
|    plt.xticks(ticks=np.arange(len(labels)) + ]{.c1}[0.5]{.c7}[,       |
| labels=labels, rotation=]{.c1}[\'vertical\']{.c26}[,                  |
| fontsize=]{.c1}[8]{.c7}[)\                                            |
|    plt.colorbar()\                                                    |
| \                                                                     |
|    ]{.c1}[\# add title]{.c6}[\                                        |
|    plt.title(]{.c1}[f\"{title}\"]{.c26}[, loc =                       |
| ]{.c1}[\"center\"]{.c26}[)\                                           |
|  \                                                                    |
|    ]{.c1}[return]{.c24}[ figure\                                      |
| \                                                                     |
| LD_heatmap_plot = ld_plot(LD_matrix_df, SNP_list, ]{.c1}[\"LD plot    |
| title\"]{.c26}[)]{.c1 .c39}                                           |
+-----------------------------------------------------------------------+

[]{.c17}

[]{.c2}

[]{.c2}

## [Manhattan Plot:]{.c10} {#h.5zfnv0ig9q0m .c8}

# [Flask:]{.c30} {#h.hwsiupgp3f8i .c9 .c12 .c31}

[]{.c2}

# [Navigation:]{.c30} {#h.147jjkfr6rv5 .c9 .c12 .c31}

[]{.c2}

# [Citation:]{.c30} {#h.fysf9tqgmmsh .c9 .c12 .c31}

[]{.c2}

[]{.c2}

## []{.c10} {#h.nrbww7njcv3p .c8 .c32}

[]{.c2}

[]{.c2}

[]{.c2}

# []{.c49} {#h.1yu3kvn20cvs .c12 .c31 .c46}
