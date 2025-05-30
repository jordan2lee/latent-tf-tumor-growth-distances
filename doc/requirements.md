# Requirements

## 1. Required Applications

+ Install [Python 3+](https://www.python.org/downloads/)
+ Install [GDC Data Transfer Tool Client](https://gdc.cancer.gov/access-data/gdc-data-transfer-tool)

    Get app to download GDC data, download the GDC Data Transfer Tool Client for your system at the above link. Below is an example for Ubuntu.
    ```bash
    curl -O https://gdc.cancer.gov/files/public/file/gdc-client_v1.6.1_Ubuntu_x64.zip
    unzip gdc-client_v1.6.1_Ubuntu_x64.zip
    ```
+ Install TensorFlow
    If you are running on Apple Silicon, see 1.1 section below

## 1.1 Install TensorFlow on Apple Silicon
Create conda environment
```bash
conda env create -n venv-ltf -f tf-arm64.yaml
```

Check the base architecture, if it returned osx-arm64 then create a conda environment otherwise follow this alternative instructions
```bash
conda config --show subdir
```

Activate environment
```bash
conda activate venv-ltf
```

> *Optional - Register the kernel with Jupyter.* This kernel can be selected within jupyter notebooks 
    > ```bash
    > python -m ipykernel install --user --name=venv-ltf
    > ```

## 2. GDC Client Token
Token setup. Go to https://portal.awg.gdc.cancer.gov/ get token under profile and save as `secrets/gdc-awg.token`

## 3. Fetch Classifier Submodule
Intialize and fetch the submodule *gdan-tmp-models.*

```bash
 git submodule init; git submodule update
```

Make sure to complete each step on the [submodule requirements page](https://github.com/NCICCGPO/gdan-tmp-models/blob/main/doc/requirements.md)

**Next**, download required data for submodule under [Download Required Data](https://github.com/NCICCGPO/gdan-tmp-models/blob/main/doc/requirements.md#4-download-required-data)

## 4. Download Required Data

Download these files from the publication page and place in:

+ `src/gdc_download_ref.tar.gz` then `cd src; tar -xf gdc_download_ref.tar.gz`
+ `src/key_samples.csv`
+ `src/distance_metric/HCMI_AWG_Model-Tumor-Normal_Linkage_v2.0_2.20.2024.txt`
+ `src/template_latent_reporting.xlsx`

And run
```bash
curl -o src/PathwayCommons12.All.hgnc.sif.gz https://download.baderlab.org/PathwayCommons/PC2/v12/PathwayCommons12.All.hgnc.sif.gz
```

