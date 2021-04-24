Urban Heat Waves Projection
===========================
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.3872519-blue)](https://doi.org/10.5281/zenodo.3872519)

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

This repository is a supplementary to the manuscript **"Large model structural uncertainty in global projections of urban heat waves"**.

The objectives of this project are:

- Use **[extreme gradient boosting (XGBoost or XGB)](https://xgboost.readthedocs.io/en/latest/)** to train the models (emulators) from the **[CESM-LENS](http://www.cesm.ucar.edu/projects/community-projects/LENS/)** (with [urban specific variable](https://www.earthsystemgrid.org/dataset/ucar.cgd.ccsm4.CESM_CAM5_BGC_LE.lnd.proc.daily_ave.html?df=true)) simulations
- Apply the models (emulators) to **[CMIP5](https://esgf-node.llnl.gov/search/cmip5/)** simulations to predict **Urban daily maximum of average 2-m temperature**, and project **Global Urban Heat Waves (UHWs)**
- Analysis the **uncertainties** in **global projections of UHWs**

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
| data preparation  | 1_data_prep      | Tab S1, Fig S3 (extreme_range)     | Tab 1                  |
| model development | 2_model_dev*     |                                    |                        |
| model validation  | 3_model_valid    | Fig S3                             | Fig 7                  |
| model application | 4_model_app      | Tab S1                             | Tab 1                  |
| data analysis     | 5_event_analysis | Fig 1 - Fig 4, and Fig S1 - Fig S2 | Fig 1 - Fig 6          |

### Data

**For Analysis**

| Folders                              | Comments                                    | Scripts in "5_event_analysis"              |
| ------------------------------------ | ------------------------------------------- | ------------------------------------------ |
| data/UHWs_CMIP                       | **urban** heat waves from **CMIP**          | _get_data_CMIP_2006_2061.ipynb             |
| data/RHWs_CMIP                       | background heat waves from CMIP             | _get_data_CMIP_2006_2061_gridcell.ipynb    |
| data/UHWs_CESM                       | **urban** heat waves from **CESM**          | _get_data_CESM-LE_2006_2061.ipynb          |
| data/HWs_CESM                        | background heat waves from CESM             | _get_data_CESM-LE_2006_2061_gridcell.ipynb |
| data/UHWs_CESM/model-validation      | model validation                            |                                            |
| data/UHWs_CESM/model-validation-diff | model validation in terms of the difference |                                            |

**Raw and Intermediate Data**

- 1_data_prep

  | Num  | Folder                                                       | Comments                                                     | How to get it?                                               |
  | ---- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
  | 1.1  | CESM-LE-members-csv\*                                        | CESM large ensemble features and temperature                 | **Raw CESM data** and scripts CESM_raw_nc_to_csv/\*.py       |
  | 1.2  | CESM-LE-members-urban-temp-extracted-csv\*/urban_heat_LE_*.csv | CESM large ensemble temperature only (for validation convenience) | Data 1.1 and scripts CESM_label_only_prep/\*.py              |
  | 1.3  | ensem_training_data\*/\*.csv                                 | training data                                                | Data 1.1, Raw CESM data (for 2051-2080 yrs training data), and scripts CESM_training_data/* |
  | 1.4  | CMIP5_tasmax_nc                                              | CMIP gridcell maximum temperature                            | **Download from website**                                    |
  | 1.5  | CMIP5_tasmax_csv                                             | CMIP urban gridcell only maximum temperature (for calculating urban heat) | Data 1.4 and scripts CMIP_gridcell_temp_prep/\*.ipynb        |
  | 1.6  | CMIP5-RCP85_nc                                               | CMIP features                                                | **Download from website**                                    |
  | 1.7  | CMIP5-RCP85_csv                                              | CMIP urban gridcell only features (for predicting urban temperatures) | Data 1.6 and scripts CMIP_feature_prep/\*.ipynb              |
  | 1.8  | feature_dist_95                                              | feature ranges of CMIP and CESM training data                | Data 1.7, Data 1.3, and script get_feature_extremes/get*.ipynb |

- 2_model_dev*

  | Num  | Folder           | Comments                             | How to get it?                                               |
  | ---- | ---------------- | ------------------------------------ | ------------------------------------------------------------ |
  | 2.1  | lat_lon_dict.dat | lat and lon pairs                    | Data 1.1 and script get_lat_lon_dict_ls.ipynb                |
  | 2.2  | lat_ls.dat       | lat list (for distributing training) | Data 1.1 and script get_lat_lon_dict_ls.ipynb                |
  | 2.3  | ensem_model\*    | emulators from machine learning      | Data 1.3, Data 2.1, and Data 2.2, and scripts ens*.py and ens\*.sub |

- 

## Acknowledgments

- We would like to acknowledge high-performance computing support from Cheyenne ([doi:10.5065/D6RX99HX](https://doi.org/10.5065/D6RX99HX)) provided by NCAR's Computational and Information Systems Laboratory, sponsored by the National Science Foundation.
- The CESM project is supported primarily by the National Science Foundation (NSF). 

- We thank AWS for providing AWS Cloud Credits for Research.
