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

| Tasks             | Folders            | Fig or Tab in paper                                          | Fig or Tab in preprint |
| ----------------- | ------------------ | ------------------------------------------------------------ | ---------------------- |
| data preparation  | 1_data_prep        | Tab S1, Fig S3 (extreme_range)                               | Tab 1                  |
| model development | 2_model_dev\*      |                                                              |                        |
| model validation  | 3_model_valid      | Fig S4 (figures_rmse)                                        | Fig 7                  |
| model application | 4_model_app        |                                                              |                        |
| data analysis     | 5_event_analysis\* | Fig 1 (urban_gridcell), Fig 2 (uhws), Fig 3 (uncertainty), Fig 4 (intensity), Fig S1 (SNR), Fig S2 (location), Fig S5 (warming), Fig S6 (uhws_min), Fig S7 (uncertainty_min), Fig S8 (intensity_min) | Fig 1 - Fig 6          |

### Data

- 1_data_prep

  | Num  | Folder                                                       | Comments                                                     | How to get it?                                               |
  | ---- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
  | 1.1  | CESM-LE-members-csv\*                                        | CESM large ensemble features and urban temperature           | **Raw CESM data** and scripts CESM_raw_nc_to_csv/\*.py       |
  | 1.2  | CESM-LE-members-urban-temp-extracted-csv\*/urban_heat_LE_*.csv | CESM large ensemble urban temperature only (for convenience) | Data 1.1 and scripts CESM_label_only_prep/\*.py              |
  | 1.3  | ensem_training_data\*/\*.csv                                 | training data                                                | Data 1.1, Raw CESM data (for 2051-2080 yrs training data), and scripts CESM_training_data/* |
  | 1.4  | CMIP5_tasmax_nc                                              | CMIP gridcell maximum temperature                            | **Download from website**                                    |
  | 1.5  | CMIP5_tasmax_csv                                             | CMIP urban gridcell only maximum temperature (for calculating urban heat) | Data 1.4 and scripts CMIP_gridcell_temp_prep/\*.ipynb        |
  | 1.6  | CMIP5-RCP85_nc                                               | CMIP features                                                | **Download from website**                                    |
  | 1.7  | CMIP5-RCP85_csv                                              | CMIP urban gridcell only features (for predicting urban temperatures) | Data 1.6 and scripts CMIP_feature_prep/\*.ipynb              |
  | 1.8  | feature_dist_95                                              | feature ranges of CMIP and CESM training data                | Data 1.7, Data 1.3, and script get_feature_extremes/get*.ipynb |
  | 1.9  | CESM-LE-members-gridcell-temp-extracted-csv/TREFHTMX_heat_LE_*.csv | CESM gridcell maximum temperature                            | **Raw CESM data** and scripts CESM_gridcell_temp_prep/\*.py  |

- 2_model_dev\*

  | Num  | Folder           | Comments                             | How to get it?                                               |
  | ---- | ---------------- | ------------------------------------ | ------------------------------------------------------------ |
  | 2.1  | lat_lon_dict.dat | lat and lon pairs                    | Data 1.1 and script get_lat_lon_dict_ls.ipynb                |
  | 2.2  | lat_ls.dat       | lat list (for distributing training) | Data 1.1 and script get_lat_lon_dict_ls.ipynb                |
  | 2.3  | ensem_model\*    | emulators from machine learning      | Data 1.3, Data 2.1, and Data 2.2, and scripts ens*.py and ens\*.sub |

- 3_model_valid\*

  | Num  | Folder                                                 | Comments                                            | How to get it?                                        |
  | ---- | ------------------------------------------------------ | --------------------------------------------------- | ----------------------------------------------------- |
  | 3.1  | CESM_validation\*                                      | CESM urban temperature predictions (for validation) | Data 1.1, Data 2.1, Data 2.3, and scripts pred/\*     |
  | 3.2  | model-validation\* (available at **data** folder)      | rmse and pcc of CESM predictions                    | Data 3.1 and script eval/model_evaluation.ipynb       |
  | 3.3  | model-validation-diff\* (available at **data** folder) | warming difference                                  | Data 3.1 and script  eval/model_diff_evaluation.ipynb |

- 4_model_app*

  | Num  | Folder       | Comments                           | How to get it?                            |
  | ---- | ------------ | ---------------------------------- | ----------------------------------------- |
  | 4.1  | CMIP5_pred\* | CMIP urban temperature predictions | Data 1.7, Data 2.1, Data 2.3, and scripts |

- 5_event_analysis*

  | Num  | Folders                                         | Comments                        | How to get it?                                               |
  | ---- | ----------------------------------------------- | ------------------------------- | ------------------------------------------------------------ |
  | 5.1  | uhws\*/UHWs_CMIP (available at **data** folder) | urban heat waves from CMIP      | Data 4.1 and script _get_data_CMIP_2006_2061.ipynb           |
  | 5.2  | uhws/HWs_CMIP (available at **data** folder)    | background heat waves from CMIP | Data 1.5 and script _get_data_CMIP_2006_2061_gridcell.ipynb  |
  | 5.3  | uhws\*/UHWs_CESM (available at **data** folder) | urban heat waves from CESM      | Data 1.2 and script _get_data_CESM-LE_2006_2061.ipynb        |
  | 5.4  | uhws/HWs_CESM (available at **data** folder)    | background heat waves from CESM | Data 1.9 and script _get_data_CESM-LE_2006_2061_gridcell.ipynb |

## Acknowledgments

- We would like to acknowledge high-performance computing support from Cheyenne ([doi:10.5065/D6RX99HX](https://doi.org/10.5065/D6RX99HX)) provided by NCAR's Computational and Information Systems Laboratory, sponsored by the National Science Foundation.
- The CESM project is supported primarily by the National Science Foundation (NSF).   
- This work is based upon material supported by the NCAR, which is a major facility sponsored by the NSF under Cooperative Agreement No. 1852977.   
- We thank AWS for providing AWS Cloud Credits for Research.   
- L.Z. acknowledges the financial support from the Start-up Grant from University of Illinois, Urbana-Champaign.
