#!/usr/bin/bash

declare -a StringArray=('BLCA' 'BRCA' 'COADREAD' 'ESO' 'KIRCKICH' 'LGGGBM' 'LIHCCHOL' 'LUNG' 'OV' 'PAAD' 'SARC' 'SKCM' 'UCEC')
for tumor_cohort in ${StringArray[@]}; do
  echo $tumor_cohort
    mkdir -p data-raw/${tumor_cohort}_GEXP_Tumor ; ./gdc-client download -m src/gdc_download_ref/gdc_manifest.${tumor_cohort}_GEXP_Tumor.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data-raw/${tumor_cohort}_GEXP_Tumor
    mkdir -p data-raw/${tumor_cohort}_GEXP_Model ; ./gdc-client download -m src/gdc_download_ref/gdc_manifest.${tumor_cohort}_GEXP_Model.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data-raw/${tumor_cohort}_GEXP_Model
  done
  