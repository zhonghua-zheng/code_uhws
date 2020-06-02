Urban Heat Waves Projection
===========================


<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [Introduction](#introduction)
- [Scripts and Data](#scripts-and-data)
  - [Prerequisite](#prerequisite)
  - [Scripts](#scripts)
  - [Data](#data)
- [Acknowledgments](#acknowledgments)

<!-- /code_chunk_output -->


## Introduction

This repository is a supplementary to the manuscript **"Large model parameter and structural uncertainties in global projections of urban heat waves"**.

The objectives of this project are:

- Use **[extreme gradient boosting (XGBoost or XGB)](https://xgboost.readthedocs.io/en/latest/)** to train the models (emulators) from the **[CESM-LENS](http://www.cesm.ucar.edu/projects/community-projects/LENS/)** (with [urban specific variable](https://www.earthsystemgrid.org/dataset/ucar.cgd.ccsm4.CESM_CAM5_BGC_LE.lnd.proc.daily_ave.html?df=true)) simulations
- Apply the models (emulators) to **[CMIP5](https://esgf-node.llnl.gov/search/cmip5/)** simulations to predict **Urban daily maximum of average 2-m temperature**, and project **Global Urban Heat Waves**
- Analysis the **uncertainties** in **global projections of urban heat waves**

## Scripts and Data

### Prerequisite

- If you do not have the **"[conda](https://docs.conda.io/en/latest/)"** system

```bash
# Download and install conda
$ wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
$ chmod +x Miniconda3-latest-Linux-x86_64.sh
$ ./Miniconda3-latest-Linux-x86_64.sh
# Edit .bash_profile or .bashrc
PATH=$PATH:$HOME/.local/bin:$HOME/bin:$HOME/miniconda3/bin
# Activate the conda system
$source .bash_profile
# OR source .bashrc
```

- Create and activate your own conda environment

```bash
# Create an environment "partmc" and install the necessary packages
conda env create -f environment.yml
# Activate the "partmc" environment
conda activate uhws
```

### Scripts

| Tasks             | Folders          | Fig or Tab in paper                | Fig or Tab in preprint |
| ----------------- | ---------------- | ---------------------------------- | ---------------------- |
| data preparation  | 1_data_prep      | Tab S1                             | Tab 1                  |
| model development | 2_model_dev      |                                    |                        |
| model validation  | 3_model_valid    | Fig S3                             | Fig 7                  |
| model application | 4_model_app      | Tab S1                             | Tab 1                  |
| data analysis     | 5_event_analysis | Fig 1 - Fig 4, and Fig S1 - Fig S2 | Fig 1 - Fig 6          |

### Data

| Folders                              | Comments                                    | Scripts in "5_event_analysis"              |
| ------------------------------------ | ------------------------------------------- | ------------------------------------------ |
| data/UHWs_CMIP                       | **urban** heat waves from **CMIP**          | _get_data_CMIP_2006_2061.ipynb             |
| data/RHWs_CMIP                       | background heat waves from CMIP             | _get_data_CMIP_2006_2061_gridcell.ipynb    |
| data/UHWs_CESM                       | **urban** heat waves from **CESM**          | _get_data_CESM-LE_2006_2061.ipynb          |
| data/HWs_CESM                        | background heat waves from CESM             | _get_data_CESM-LE_2006_2061_gridcell.ipynb |
| data/UHWs_CESM/model-validation      | model validation                            |                                            |
| data/UHWs_CESM/model-validation-diff | model validation in terms of the difference |                                            |

## Acknowledgments

- We would like to acknowledge high-performance computing support from Cheyenne (doi: 10.5065/D6RX99HX) provided by NCAR’s Computational and Information Systems Laboratory, sponsored by the National Science Foundation. 
- The CESM project is supported primarily by the National Science Foundation. 

- We thank AWS for providing AWS Cloud Credits for Research.