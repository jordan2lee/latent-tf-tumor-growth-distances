#!/usr/bin/python

import pandas as pd
from glob import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--maindir", help='path to folder that contains the post processed files')
parser.add_argument("--outfile", help='name of output file')
args = parser.parse_args()

dfs = []
for g in glob(args.maindir+"/*_GEXP/*prep2*.tsv"):
    dfs.append(pd.read_csv(g, sep="\t", index_col=0))

isect = None
for i in dfs:
    if isect is None:
        isect = i.columns
    else:
        isect = isect.intersection(i.columns)

df = pd.concat( i[isect] for i in dfs )
hugo_map = dict( df.columns.map(lambda x: (x, x.split(":")[3])) )
out = df.rename(columns=hugo_map)
out = out[ ~out.index.duplicated(keep='first') ]
out.to_csv(args.outfile, sep="\t")
