#!/usr/bin/env python

import argparse
import pandas as pd
import netvae

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("samples")
    parser.add_argument("model")
    parser.add_argument("--out", "-o", default="samples.out.tsv")

    args = parser.parse_args()

    nv = netvae.Open(args.model)
    df = pd.read_csv(args.samples, sep="\t", index_col=0)[nv.features]

    latent = pd.DataFrame(nv.encoder.predict( df )[0], index=df.index, columns=nv.latent_index)
    latent.to_csv(args.out, sep="\t")
