#!/usr/bin/env python

import argparse
import pandas as pd
import numpy as np

def expMaxNorm(df):
    t = np.log2(df+1)
    return (t.transpose() / t.max(axis=1)).transpose()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("matrix", nargs="+")
    parser.add_argument("--out", "-o", default="out.tsv")
    parser.add_argument("--features", "-f", default=None)
    parser.add_argument("--precision", "-p", type=int, default=5)

    args = parser.parse_args()

    features = None
    if args.features is not None:
        features = []
        with open(args.features, encoding="ascii") as handle:
            features = list(line.rstrip() for line in handle)

    dfs = []
    for i in args.matrix:
        df = pd.read_csv(i, sep="\t", index_col=0)
        if features is not None:
            df = df[features]
        dfs.append(df)

    df = pd.concat( dfs )
    normDF = expMaxNorm(df)
    normDF.round(decimals=args.precision).to_csv(args.out, sep="\t")
