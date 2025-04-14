# Requirements

## 1. Required Applications

+ Install [Python 3+](https://www.python.org/downloads/)
+ Install [Docker Desktop](https://docs.docker.com/get-started/get-docker/) (or Docker)
+ Install [GDC Data Transfer Tool Client](https://gdc.cancer.gov/access-data/gdc-data-transfer-tool)

    Get app to download GDC data, download the GDC Data Transfer Tool Client for your system at the above link. Below is an example for Ubuntu.
    ```bash
    curl -O https://gdc.cancer.gov/files/public/file/gdc-client_v1.6.1_Ubuntu_x64.zip
    unzip gdc-client_v1.6.1_Ubuntu_x64.zip
    ```
+ Install TensorFlow
    If you are running on Apple Silicon, see 1.1 section below

## 1.1 Install TensorFlow on Applice Silicon
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

## 2. Sign into Applications
Docker Sign In (if not already)

```bash
docker login
```

## 3. GDC Client Token
Token setup. Go to https://portal.awg.gdc.cancer.gov/ get token under profile and save as `secrets/gdc-awg.token`

## 4. Fetch Classifier Submodule
Intialize and fetch the submodule *gdan-tmp-models.*

```bash
 git submodule init; git submodule update
```

Make sure to complete each step on the [submodule requirements page](https://github.com/NCICCGPO/gdan-tmp-models/blob/main/doc/requirements.md)

## 5. Download Required Data

Download these files and place in:

+ `src/key_samples.csv`
+ `src/gdc_download_ref/gdc_manifest.<CANCER>_GEXP_Model.txt`
+ `src/gdc_download_ref/gdc_manifest.<CANCER>_GEXP_Tumor.txt`
+ `src/gdc_download_ref/gdc_sample_sheet.<CANCER>_GEXP_Model.tsv`
+ `src/gdc_download_ref/gdc_sample_sheet.<CANCER>_GEXP_Tumor.tsv`
+ `src/distance_metric/HCMI_AWG_Model-Tumor-Normal_Linkage_v2.0_2.20.2024.txt`

