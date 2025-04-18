#!/usr/bin/Rscript

# # For R v4.2.0+
# if (!require("BiocManager", quietly = TRUE))
#     install.packages("BiocManager")
# BiocManager::install(version = "3.16")
# BiocManager::install('biomaRt')
# install.packages('argparse', quiet=TRUE)
suppressWarnings(suppressPackageStartupMessages(library(argparse)))
suppressWarnings(suppressPackageStartupMessages(library(biomaRt)))
suppressWarnings(suppressPackageStartupMessages(library(dplyr)))
suppressWarnings(suppressPackageStartupMessages(library(data.table)))

# create parser object
parser <- ArgumentParser()
parser$add_argument("-i", "--input", type='character', help='input file to read in ')
parser$add_argument("-o", "--output", type='character', help='output file to read out ')
args <- parser$parse_args()

# First pull gene info from Biomart
t <- fread(args$input)

ensembl.genes <- t %>% pull(1) #genes in col 1
ensembl.genes <-gsub("\\..*","",ensembl.genes) #rm ensembl gene version (after .)

# Use for HCMI data/TCGA
# ENSEMBL - May get a timeout error, if so just rerun this until it works
mart <- useDataset("hsapiens_gene_ensembl", useMart("ensembl"))
genes <- getBM(
  filters="ensembl_gene_id",
  attributes=c("ensembl_gene_id", "entrezgene_id"),
  values=ensembl.genes,
  mart=mart)
# head(genes, 3)
# Second convert our input file to entrez gene ids
t <- fread(args$input)
# Ensembl to entrez
entrez <- c()
for (g in t$V1){
  entrezid = genes[genes$ensembl_gene_id == g,]$entrezgene_id
  # Priliminary results = pick first entrez id if multiple matches
  if (length(entrezid)>1){
    entrezid <- entrezid[1]
  } else if(length(entrezid)==0) {
    entrezid <- NA
  }
  entrez <- c(entrez, entrezid)
}

# Replace with entrez genes
t$V1 <- entrez
names(t)[1]='Entrez_Gene_Id'
t <- na.omit(t) # clear where no entrez found
row.names(t)<- as.vector(seq(1, dim(t)[1]))
write.table(t, file=args$output, sep='\t', col.names = TRUE,row.names = TRUE)
