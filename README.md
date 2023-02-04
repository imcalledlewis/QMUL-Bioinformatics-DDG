# QMUL-Bioinformatics-DDG

 QMUL MSc Bioinformatics group project, team DuckDuckGo.

----

## **Requirements:**

### 1. Input:

-    (rs value)
-    genomic coordinates (chromosome, start and end)
-    gene name

### 2. Output:

-   SNP name(s) (rs value)
-   genomic position(s) (its location)
-   p-value(s) from the association test
-   mapped gene(s), variant (allele) frequency in at least two different human populations of interest
-   at least one measure of functional impact and/or clinical relevance for each variant
-   at least one functional or ontology term associated with each mapped gene

### 3. For multiple SNPS:

If multiple SNPs are returned, the user should be able to select the SNPs of interest, calculate
measurements of linkage disequilibrium (LD) for each pair of SNPs, separately for each population,
and plot their values. The user will also be able to download a text file with the LD values.
Remember that results should be presented in a manner that will help answer biological questions.

### 4. Manhattan plot:

If genomic coordinates are provided in input and multiple SNPs are returned, a Manhattan plot of
p-values should be provided.
