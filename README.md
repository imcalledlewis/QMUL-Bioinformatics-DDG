# QMUL-Bioinformatics-DDG

 QMUL MSc Bioinformatics group project, team DuckDuckGo.

----

This web application prototype is designed to retrieve information on Single Nucleotide
Polymorphisms (SNPs) seen in Type 1 Diabetes Mellitus patients identified by Genome wide
association studies (GWAS). The database will use information from the GWAS catalogue,
along with population data from Ensembl, and the 1000 Genomes Project. Functional
information and Gene Ontology information are obtained through Ensembl’s VEP tool which
is all retrievable through a user-friendly interface through the input of an rsID, chromosome
position or a Gene name. The site also allows the user to calculate Linkage Disequilibrium
(LD) of SNPs selected for each population producing a text file containing the LD values and
plot these values as a LD heatmap. If the user inputs a region containing multiple SNPs, it
will return a Manhattan plot of p-values, which is interactive and can be saved as a png file.


[Documentation here](https://g-b-f.github.io/hosted/Documentation.pdf)