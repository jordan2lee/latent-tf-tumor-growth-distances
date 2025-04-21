<h1 align="center">Latent Transcription Factor Distance Method</h1>
<h4 align="center">Biological distance between tumors and their lab grown models</h4>


## Table of contents
- [Quickstart Guide](#quickstart-guide)
- [Download Data from Manifest File Using the GDC Client](#download-data-from-manifest-file-using-the-gdc-client)
- [Run Processing Pipeline](#run-processing-pipeline)
- [Calculate Euclidean Distances](#calculate-euclidean-distances)



## Quickstart Guide

### Setup

Install requirements - detailed instructions are found on the [Requirements page](doc/requirements.md):

1. Install Python 3+
2. Install GDC Data Transfer Tool Client
3. Install TensorFlow


Ensure that steps are completed on the [Requirements page](doc/requirements.md) - *(includes creating working environment, signining in, and manually downloading required data)*

## Download Data from Manifest File Using the GDC Client
Download Gene Expression Data - all cohorts need to be ran for downstream cohort analysis
```bash
bash scripts/gdc_download.sh
```

This will create subfolders in `data-raw/<CANCER>_GEXP_<TYPE>` and place GDC molecular matrices here.

## Run Processing Pipeline

```bash
bash scripts/process.sh data/prep
```

> Creates file `data/prep/<CANCER>_GEXP/<CANCER>_GEXP_prep2_<TYPE>.tsv` that is prepped for distance calculations

## Calculate Latent Transcription Factor Distances

Prep matrix
```bash
python scripts/matrix_prep.py \
    --maindir data/prep \
    --outfile data/distance_metric/hcmi.counts.tsv
```

Get the list of features intersecting with PathwayCommons
```bash
python scripts/matrix_intersect.py \
    -m data/distance_metric/hcmi.counts.tsv \
    -s src/PathwayCommons12.All.hgnc.sif.gz \
    --out data/distance_metric/features.txt
```

Normalize the matrix on the subset of represented features
```bash
python scripts/matrix_expmax_normalize.py \
    data/distance_metric/hcmi.counts.tsv \
    --features data/distance_metric/features.txt \
    --out data/distance_metric/hcmi.normalized.tsv \
    --precision 5
```

To get the model - this may take a while
```bash
python scripts/tf_net_train.py \
    data/distance_metric/hcmi.normalized.tsv src/PathwayCommons12.All.hgnc.sif.gz \
    --epochs 100 \
    -o data/distance_metric/model-tf-hcmi
```

To get the projection into latent space
```bash
python scripts/matrix_project.py \
    data/distance_metric/hcmi.normalized.tsv data/distance_metric/model-tf-hcmi \
    --out data/distance_metric/hcmi.latent.tsv
```

To get the all vs all distances
```bash
python scripts/matrix_distance.py \
    data/distance_metric/hcmi.latent.tsv \
    -m \
    -o data/distance_metric/hcmi.latent.dists.csv
```

Then reformat to report to larger group. Reports distances as euclidean distances and z-scores of euclidean distances (where z-scores are calculated ACROSS tissue cohorts)
```bash
python scripts/reformat_allvsall_lat.py \
    --dist data/distance_metric/hcmi.latent.dists.csv \
    --out data/distance_metric/main_results/latent_tf_dist_all_cohorts.tsv
```

> Final distances reported were z-scores from the file `data/distance_metric/main_results/latent_tf_dist_all_cohorts.tsv`
