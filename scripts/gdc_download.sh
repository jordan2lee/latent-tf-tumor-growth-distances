#!/usr/bin/bash
set -e
cancer=${1}
# Run all cohorts
declare -a StringArray=('BLCA' 'BRCA' 'COADREAD' 'ESO' 'KIRCKICH' 'LGGGBM' 'LIHCCHOL' 'LUNG' 'OV' 'PAAD' 'SARC' 'SKCM' 'UCEC')
for cancer in ${StringArray[@]}; do
  echo 'Running: ' $cancer
  mkdir -p data-raw/${cancer}_GEXP_Tumor ; ./gdc-client download -m src/gdc_download_ref/gdc_manifest.${cancer}_GEXP_Tumor.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data-raw/${cancer}_GEXP_Tumor
  mkdir -p data-raw/${cancer}_GEXP_Model ; ./gdc-client download -m src/gdc_download_ref/gdc_manifest.${cancer}_GEXP_Model.txt -t secrets/gdc-user-token.txt --server  https://api.awg.gdc.cancer.gov --dir data-raw/${cancer}_GEXP_Model
  done

