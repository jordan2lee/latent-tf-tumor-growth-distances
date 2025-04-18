#!/usr/bin/python

# # look up what is missing from kyle's distances
# ref[ref['tumor'].isin(['HCM-WCMC-0497-C18-01A', 'HCM-CSHL-1264-C25-01A'])]

# purpose save in the same format as reported for euclidean distances
import pandas as pd
import numpy as np
import scipy.stats as stats
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--dist", "-d", default="distance file")
parser.add_argument("--out", "-o", default="output file")
args = parser.parse_args()

# read in template (we will overwrite a column here with the updated distances)
ref = pd.read_excel('src/template_latent_reporting.xlsx')

# read in NEW latent distances
df = pd.read_csv(args.dist, sep=',', index_col=0)

# build new reporting of distance column
new_distance = []
for i in range(0, ref.shape[0]):
    model = ref['reference(model_OR_tcga)'][i]
    tumor = ref['tumor'][i]
    # Unique sample handling-'HCM-WCMC-0497-C18-01A' COADREAD, 'HCM-CSHL-1264-C25-01A' PAAD
    if tumor in ['HCM-WCMC-0497-C18-01A', 'HCM-CSHL-1264-C25-01A']:
        new_distance.append(np.nan)
    else:
        if isinstance(df.loc[tumor, model ], float):
            distance = [df.loc[tumor, model ]][0]
        else:
            dist_vect = [round(a,4) for a in list(df.loc[tumor, model ])]
            assert len(set(dist_vect))==1
            distance = list(set(df.loc[tumor, model ]))[0]
        new_distance.append(distance)
assert len(new_distance)==ref.shape[0]
ref = ref.drop('z-score_to_model_or_tcga', axis=1)
ref.insert(2, 'distance', new_distance)
# calculate z-scores to determine outlier sample-pairs
# z-scores are done on a per tissue cohort basis
# ex. take all BRCA samples and convert to z-score
uniq_cancers = set(ref['cohort'])
index2z = dict()
for cancer in uniq_cancers:
    s1 = ref[ref['cohort']==cancer]
    # calc z-score but if NA distance then remove from cohort
    nan_indices = list(s1.loc[pd.isna(s1['distance']), :].index)
    s1 = s1['distance'].dropna()
    # save row index for mapping back to original ref later
    index_order = list(s1.index) 
    darray =np.array(s1)
    z = stats.zscore(darray)
    # save
    for i_nan in nan_indices:
        index2z[i_nan]=np.nan
    for i in range(0, len(index_order)):
        index2z[index_order[i]]=z[i]
zscore = []
outlier =[]
for i in ref.index:
    z = index2z[i]
    zscore.append(z)
    if abs(z)>3:
        # print('outlier found {}'.format(i))
        outlier.append('TRUE')
    else:
        outlier.append(np.nan)

ref = ref.drop('outlier', axis=1)
ref.insert(3, 'outlier', outlier)
ref.insert(4, 'z_score', zscore)
ref = ref.sort_values(by=['cohort', 'tumor'])
ref.to_csv(args.out, sep='\t', index=False)
