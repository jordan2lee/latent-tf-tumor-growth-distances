#!/usr/bin/bash

mkdir -p data/src/BLCA_GEXP_Tumor ; ./gdc-client download -m src/gdc_manifest.BLCA_GEXP_Tumor.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data/src/BLCA_GEXP_Tumor
mkdir -p data/src/BLCA_GEXP_Model ; ./gdc-client download -m src/gdc_manifest.BLCA_GEXP_Model.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data/src/BLCA_GEXP_Model

mkdir -p data/src/COADREAD_GEXP_Tumor ; ./gdc-client download -m src/gdc_manifest.COADREAD_GEXP_Tumor.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data/src/COADREAD_GEXP_Tumor
mkdir -p data/src/COADREAD_GEXP_Model ; ./gdc-client download -m src/gdc_manifest.COADREAD_GEXP_Model.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data/src/COADREAD_GEXP_Model

mkdir -p data/src/ESO_GEXP_Tumor ; ./gdc-client download -m src/gdc_manifest.ESO_GEXP_Tumor.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data/src/ESO_GEXP_Tumor
mkdir -p data/src/ESO_GEXP_Model ; ./gdc-client download -m src/gdc_manifest.ESO_GEXP_Model.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data/src/ESO_GEXP_Model

mkdir -p data/src/KIRC_GEXP_Tumor ; ./gdc-client download -m src/gdc_manifest.KIRC_GEXP_Tumor.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data/src/KIRC_GEXP_Tumor
mkdir -p data/src/KIRC_GEXP_Model ; ./gdc-client download -m src/gdc_manifest.KIRC_GEXP_Model.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data/src/KIRC_GEXP_Model

mkdir -p data/src/LIHCCHOL_GEXP_Tumor ; ./gdc-client download -m src/gdc_manifest.LIHCCHOL_GEXP_Tumor.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data/src/LIHCCHOL_GEXP_Tumor
mkdir -p data/src/LIHCCHOL_GEXP_Model ; ./gdc-client download -m src/gdc_manifest.LIHCCHOL_GEXP_Model.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data/src/LIHCCHOL_GEXP_Model

mkdir -p data/src/OV_GEXP_Tumor ; ./gdc-client download -m src/gdc_manifest.OV_GEXP_Tumor.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data/src/OV_GEXP_Tumor
mkdir -p data/src/OV_GEXP_Model ; ./gdc-client download -m src/gdc_manifest.OV_GEXP_Model.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data/src/OV_GEXP_Model

mkdir -p data/src/PAAD_GEXP_Tumor ; ./gdc-client download -m src/gdc_manifest.PAAD_GEXP_Tumor.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data/src/PAAD_GEXP_Tumor
mkdir -p data/src/PAAD_GEXP_Model ; ./gdc-client download -m src/gdc_manifest.PAAD_GEXP_Model.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data/src/PAAD_GEXP_Model

mkdir -p data/src/SARC_GEXP_Tumor ; ./gdc-client download -m src/gdc_manifest.SARC_GEXP_Tumor.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data/src/SARC_GEXP_Tumor
mkdir -p data/src/SARC_GEXP_Model ; ./gdc-client download -m src/gdc_manifest.SARC_GEXP_Model.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data/src/SARC_GEXP_Model

mkdir -p data/src/SKCM_GEXP_Tumor ; ./gdc-client download -m src/gdc_manifest.SKCM_GEXP_Tumor.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data/src/SKCM_GEXP_Tumor
mkdir -p data/src/SKCM_GEXP_Model ; ./gdc-client download -m src/gdc_manifest.SKCM_GEXP_Model.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data/src/SKCM_GEXP_Model

mkdir -p data/src/UCEC_GEXP_Tumor ; ./gdc-client download -m src/gdc_manifest.UCEC_GEXP_Tumor.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data/src/UCEC_GEXP_Tumor
mkdir -p data/src/UCEC_GEXP_Model ; ./gdc-client download -m src/gdc_manifest.UCEC_GEXP_Model.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data/src/UCEC_GEXP_Model
