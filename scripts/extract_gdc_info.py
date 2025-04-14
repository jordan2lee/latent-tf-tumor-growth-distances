#!/usr/bin/env python

# ------
# Purpose: relabel features as per TMP nomenclature. quantile normalize data
#
# Note we are pulling the STAR Counts output for unstranded data (aka using the col right after "protein_coding")
#
# Description:
# input files:
# 1. all GDC GEXP count data in specified-dir/*/*.tsv
# output files:
# 1. index2file_CANCER_PLATFORM.tsv (sample to GDC case file)
# 2. CANCER_PLATFORM.tsv (reformatted GEXP data)
# ------

import pandas as pd
from glob import glob
import json
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--run", help='description of args.run; ex. COADREAD_GEXP')
parser.add_argument("--dir", help='path where the GDC files are saved')
parser.add_argument("--stype", help='sample type of "Tumor" or "Model" ')
parser.add_argument("--outdir", help='out dir path')
args = parser.parse_args()

# Open sample sheet - filter for useful cols
sample_df = pd.read_csv('src/gdc_download_ref/gdc_sample_sheet.{}_{}.tsv'.format(args.run, args.stype), sep='\t')
sample_df = sample_df[['File ID', 'File Name', 'Sample ID', 'Sample Type']]

# open sample id conversion
data = {}
index = 0
with open('src/distance_metric/index2file.{}_{}.tsv'.format(args.run, args.stype), 'w') as conversion:
    # Pull measured data (gene expression data) from all files in directory
    for file in glob('{}/*/*.tsv'.format(args.dir), recursive = True):
        with open(file, 'r') as fh:
            # Grab last dir and file name
            file_id, file_name = file.strip().split('/')[-2:]
            # Find SampleID based on fileid/name
            s1 = sample_df[sample_df['File ID']==file_id].reset_index(drop=True)
            assert s1['File Name'][0]== file_name
            sample= s1['Sample ID'][0]
            # Create conversion file
            # if 'e925c7f7-d9a2-46a5-9f78-77f9245ff2e1.rna_seq.augmented_star_gene_counts.tsv' in file:
            #     print(file)
            conversion.write(sample)
            conversion.write('\t')
            conversion.write(file)
            conversion.write('\n')

            # Results: add sample name as key
            assert sample not in data, 'ERROR This sample has already been seen'
            data[sample]={}
            # Parse file
            for line in fh:
                line = line.strip().split()
                # Only consider measured data lines (ex gene expression)
                if line[0].startswith('ENSG'):
                    # only protein coding
                    if line[2]== 'protein_coding':
                        gene = line[0]
                        # remove gene version
                        gene = gene.split('.')[0]
                        measured_data = line[3]
                        # Results: add measured data (ex gene expression)
                        data[sample][gene]=measured_data
            index+=1

# save row:cols genes:samples
out = '{}/{}/{}_{}.tsv'.format(args.outdir, args.run,args.run, args.stype)
pd.DataFrame.from_dict(data).to_csv(out, sep='\t')
