#!/usr/bin/env python

import argparse
import pandas as pd
import netvae



def log(*args):
    print(*args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("matrix")
    parser.add_argument("pathway")
    parser.add_argument("--out", "-o", default="model-tf")
    parser.add_argument("--gene-mask", default=None, type=str)
    parser.add_argument("--learning-rate", default=1e-4, type=float)
    parser.add_argument("--epochs", default=80, type=int)
    parser.add_argument("--batch-size", default=256, type=int)
    parser.add_argument("--tf-min-size", default=3, type=int)

    args = parser.parse_args()
    
    log("Loading Matrix")
    df = pd.read_csv(args.matrix, sep="\t", index_col=0)

    log("Loading pathways")
    pcDF = netvae.extract_pathway_interactions(args.pathway)

    vc = pcDF["from"].value_counts()
    vc = vc[vc >= args.tf_min_size].index

    pcSubDF = pcDF[ pcDF["from"].map(lambda x : x in vc ) ]
    geneSets = {}
    for _, r in pcSubDF[["from", "to"]].iterrows():
        if r["from"] in df.columns and r["to"] in df.columns:
            if r["from"] not in geneSets:
                geneSets[r["from"]] = [r["from"], r["to"]]
            else:
                geneSets[r["from"]].append(r["to"])

    """
    pathMember = {}
    for _, r in pcSubDF[["to", "from"]].iterrows():
        if r["to"] not in pathMember:
            pathMember[r["to"]] = [r["from"]]
        else:
            pathMember[r["to"]].append(r["from"])
    """

    x = set()
    for i in geneSets.values():
        x.update(i)
    genes = list(x)

    isect = df.columns.intersection(genes)

    normalDF = df[isect]

    set_index=list(geneSets.keys())

    log("Building model")
    nv = netvae.NetVae(list(normalDF.columns))
    nv.run_train(normalDF, set_index,
                 geneSets, batch_size=args.batch_size,
                 learning_rate=args.learning_rate,
                 epochs=args.epochs
                 )

    nv.save(args.out, normalDF)
