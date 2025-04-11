#!/usr/bin/bash
set -e

cancer=${1}
outdir=${2}

# extract info from STAR counts file (tumor)
echo 'Extracting tumor'
mkdir -p ${outdir}/${1}_GEXP
cp src/distance_metric/gdc_sample_sheet.${1}_GEXP_Tumor.tsv src/gdc_sample_sheet.${1}_GEXP.tsv
python scripts/extract_gdc_info.py --run ${1}_GEXP --dir data/distance_metric/src/${1}_GEXP_Tumor --outdir ${outdir}
mv src/index2file.${1}_GEXP.tsv src/distance_metric/index2file.${1}_GEXP_Tumor.tsv
mv ${outdir}/${1}_GEXP/${1}_GEXP.tsv ${outdir}/${1}_GEXP/${1}_GEXP_Tumor.tsv
rm src/gdc_sample_sheet.${1}_GEXP.tsv

# extract info from STAR counts file (model)
echo 'Extracting model'
cp src/distance_metric/gdc_sample_sheet.${1}_GEXP_Model.tsv src/gdc_sample_sheet.${1}_GEXP.tsv
python scripts/extract_gdc_info.py --run ${1}_GEXP --dir data/distance_metric/src/${1}_GEXP_Model --outdir ${outdir}
mv src/index2file.${1}_GEXP.tsv src/distance_metric/index2file.${1}_GEXP_Model.tsv
mv ${outdir}/${1}_GEXP/${1}_GEXP.tsv ${outdir}/${1}_GEXP/${1}_GEXP_Model.tsv
rm src/gdc_sample_sheet.${1}_GEXP.tsv

# convert to TMP nomenclature (entrez ids, then conversion)
echo 'Convert to Entrez ID'
Rscript scripts/gene_converter.R -i ${outdir}/${1}_GEXP/${1}_GEXP_Tumor.tsv -o ${outdir}/${1}_GEXP/${1}_GEXP_prep_Tumor.tsv
Rscript scripts/gene_converter.R -i ${outdir}/${1}_GEXP/${1}_GEXP_Model.tsv -o ${outdir}/${1}_GEXP/${1}_GEXP_prep_Model.tsv

echo 'Convert nomenclature'
cd gdan-tmp-models
# usual runs where multiple mappings
if [[ ${1} == 'LUNG' || ${1} == 'ESO' || ${1} == 'KID' ]]; then
  if [[ ${1} == 'LUNG' ]]; then
    modifed_1='LUAD'
    modifed_2='LUSC'
  fi
  if [[ ${1} == 'ESO' ]]; then
    modifed_1='GEA'
    modifed_2='ESCC'
  fi
  if [[ ${1} == 'KID' ]]; then
    modifed_1='KIRCKICH'
    modifed_2='KIRP'
  fi
  echo 'using TMP referene file' ${modifed_1}
  python tools/convert.py --data ../${outdir}/${1}_GEXP/${1}_GEXP_prep_Tumor.tsv --out ../${outdir}/${1}_GEXP/${modifed_1}_GEXP_prep2_Tumor.tsv --cancer ${modifed_1} --conversion_file tools/ft_name_convert/entrez2tmp_${modifed_1}_GEXP.json
  python tools/convert.py --data ../${outdir}/${1}_GEXP/${1}_GEXP_prep_Model.tsv --out ../${outdir}/${1}_GEXP/${modifed_1}_GEXP_prep2_Model.tsv --cancer ${modifed_1} --conversion_file tools/ft_name_convert/entrez2tmp_${modifed_1}_GEXP.json
  echo 'using TMP referene file' ${modifed_2}
  python tools/convert.py --data ../${outdir}/${1}_GEXP/${1}_GEXP_prep_Tumor.tsv --out ../${outdir}/${1}_GEXP/${modifed_2}_GEXP_prep2_Tumor.tsv --cancer ${modifed_2} --conversion_file tools/ft_name_convert/entrez2tmp_${modifed_2}_GEXP.json
  python tools/convert.py --data ../${outdir}/${1}_GEXP/${1}_GEXP_prep_Model.tsv --out ../${outdir}/${1}_GEXP/${modifed_2}_GEXP_prep2_Model.tsv --cancer ${modifed_2} --conversion_file tools/ft_name_convert/entrez2tmp_${modifed_2}_GEXP.json
# normal runs
else
  python tools/convert.py --data ../${outdir}/${1}_GEXP/${1}_GEXP_prep_Tumor.tsv --out ../${outdir}/${1}_GEXP/${1}_GEXP_prep2_Tumor.tsv --cancer ${1} --conversion_file tools/ft_name_convert/entrez2tmp_${1}_GEXP.json
  python tools/convert.py --data ../${outdir}/${1}_GEXP/${1}_GEXP_prep_Model.tsv --out ../${outdir}/${1}_GEXP/${1}_GEXP_prep2_Model.tsv --cancer ${1} --conversion_file tools/ft_name_convert/entrez2tmp_${1}_GEXP.json
fi
cd ..
echo 'Complete'
