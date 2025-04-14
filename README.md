<h1 align="center">Latent Transcription Factor Distance Method</h1>
<h4 align="center">Biological distance between tumors and their lab grown models</h4>


## Table of contents
- [Quickstart Guide](#quickstart-guide)
- [Download Source Files](#download-source-files)
- [Download Data from Manifest File Using the GDC Client](#download-data-from-manifest-file-using-the-gdc-client)
- [Run Processing Pipeline](#run-processing-pipeline)
- [Calculate Euclidean Distances](#calculate-euclidean-distances)



## Quickstart Guide

### Setup

Install requirements - detailed instructions are found on the [Requirements page](doc/requirements.md):

1. Install Python 3+
2. Install Docker Desktop (or Docker)
3. Install GDC Data Transfer Tool Client
4. Install TensorFlow


Ensure that steps are completed on the [Requirements page](doc/requirements.md) - *(includes creating working environment, signining in, and manually downloading required data)*

## Download Source Files

This will show how to get the files to download files from the GDC data portal by using a manifest file

### Download Manifest Files

Download manifest files for all samples and place in `src/gdc_download_ref/`. TODO add location to download these files.

> Manifest names follow the pattern: `gdc_manifest.<CANCER>_<DATAPLATFORM>_<TYPE>.txt`

### Download Sample Sheets

Download manifest files for all samples and place in `src/gdc_download_ref/`. TODO add location to download these files.

> Sample sheet names follow the pattern: `gdc_sample_sheet.<CANCER>_<DATAPLATFORM>_<TYPE>.tsv`

## Download Data from Manifest File Using the GDC Client
Download Gene Expression Data
```bash
bash scripts/gdc_download.sh
```

This will create subfolders in `data-raw/<CANCER>_GEXP_<TYPE>` and place GDC molecular matrices here.

> *Note on the selection of Cancer Type: These HCMI selections of Cancer Type were made and grouped together for each corresponding TCGA cancer cohort:*
>
> + 'BLCA':['Bladder Cancer']
> + 'BRCA':['Breast Cancer','Intraductal Carcinoma']
> + 'COADREAD': ['Colorectal Cancer', 'Rare Cancer','Serrated Adenoma','Tubular Adenoma','Tubulovilluos Adenoma']
> + 'ESO': ['Esophageal Cancer','Stomach Cancer']
> + 'HNSC':['Head and Neck']
> + 'KID':['Kidney Cancer']
> + 'LGGGBM':['Glioblastoma']
> + 'LIHCCHOL':['Extrahepatic Cholangiocarcinoma','Ampulla of Vater','Hepatocellular carcinoma','Intrahepatic Cholangiocarcinoma']
> + 'LUNG':['Lung Cancer']
> + 'OV':['Ovarian Cancer']
> + 'PAAD': ['Pancreatic Cancer']
> + 'SARC': ['Bone Cancer','Clear Cell Sarcoma','Desmoid Tumors','Epithelial Sarcoma','Ewing Sarcoma','Intimal Sarcoma','Leiomyosarcoma','Rhabdomyosarcoma','Spindle Cell Sarcoma','Undifferentiated Pleomorphic Sarcoma']
> + 'SKCM':['Melanoma']
> + 'UCEC':['Endometrial Cancer'],


## Run Processing Pipeline
TODO update this output dir name to reflect that this is for GEXP data

Example shown for running PAAD cohort
```bash
bash scripts/process.sh PAAD data/prep
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
curl -o src/PathwayCommons12.All.hgnc.sif.gz https://download.baderlab.org/PathwayCommons/PC2/v12/PathwayCommons12.All.hgnc.sif.gz
```
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

