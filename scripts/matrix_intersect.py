#!/usr/bin/env python

import argparse
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--matrix", default=[], action="append")
    parser.add_argument("-s", "--sif", default=[], action="append")
    parser.add_argument("--out", "-o", default="features.txt")

    args = parser.parse_args()

    isect = None
    for m in args.matrix:
        df = pd.read_csv(m, sep="\t", index_col=0, nrows=10)
        if isect is None:
            isect = df.columns
        else:
            isect = isect.intersection(df.columns)
    
    for s in args.sif:
        pc = pd.read_csv(s, sep="\t", 
                     header=None, names=["from", "relation", "to"])
        sel = pc["relation"] == "controls-expression-of"
        vals = pd.concat( [pc[sel]["from"], pc[sel]["to"] ] )
        isect = isect.intersection(vals)

    if isect is not None:
        with open(args.out, "wt", encoding="ascii") as handle:
            handle.write("\n".join(isect))