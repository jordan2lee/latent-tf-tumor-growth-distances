#!/usr/bin/env python

import argparse
import pandas as pd
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("matrix")
    parser.add_argument("--out", "-o", default="matrix.dist.tsv")
    parser.add_argument("--save-matrix", "-m", action="store_true", default=False)

    args = parser.parse_args()

    df = pd.read_csv(args.matrix, sep="\t", index_col=0)

    dist = []
    for i in range(df.shape[0]):
        dist.append( list(np.linalg.norm(df.iloc[i]-df.iloc[j]) for j in range(df.shape[0])) )
    
    distDF = pd.DataFrame(dist, columns=df.index, index=df.index)

    if args.save_matrix:
        distDF.to_csv(args.out)
    else:
        with open(args.out, "wt") as handle:
            for i, row in distDF.iterrows():
                for j, v in enumerate(row):
                    handle.write("%s\t%s\t%f\n" % (i, df.index[j], v))