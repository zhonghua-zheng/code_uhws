# This script is used to store different members as csv
# The results are at "/glade/scratch/zhonghua/CESM_gridcell/"

import pandas as pd
import numpy as np
import xarray as xr
import datetime
import cftime
import time
import gc

def get_ts_masked_cam(start_date, end_date, var, member, CLM_lat, mask):
    print("Start to convert",var)
    count_time_start = time.time()
   
    # read raw data
    var_raw = xr.open_dataset("/glade/collections/cdg/data/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/" \
                              + var + "/b.e11.BRCP85C5CNBDRD.f09_g16."+member+".cam.h1." + var + ".20060101-20801231.nc")
    # select time period and reset coordinate index
    var_reg = var_raw[var].sel(time=slice(start_date, end_date)).assign_coords(lat = CLM_lat)
    # apply the mask 
    var_reg_mask = var_reg.where(mask)
    # plot the figure figure
    #var_reg_mask.loc[start_date[:4]+"-03-28"].plot()
    #Another way to plot
    #TREFMXAV_U["TREFMXAV_U"].sel(time=TREFMXAV_U.time[int(len(TREFMXAV_U["TREFMXAV_U"].time)*1/74)]).plot()
    #plt.show()
    # rename the DataArray
    var_final = var_reg_mask.rename(var)
    
    elapsed_time = time.time() - count_time_start
    print("It takes elapsed_time", elapsed_time, "to get the", var)
    print("\n")
    return var_final  

# Design the pipeline
def get_df(start_date, end_date, member):
    print("start_date:", start_date)
    print("end_date:", end_date) 
    print("member:", member)
    # load the urban maximal temperature
    TREFMXAV_U = xr.open_dataset("/glade/collections/cdg/data/cesmLE/CESM-CAM5-BGC-LE/lnd/proc/tseries/daily/TREFMXAV_U/b.e11.BRCP85C5CNBDRD.f09_g16."+member+".clm2.h1.TREFMXAV_U.20060101-20801231.nc")
    TREFMXAV_R = xr.open_dataset("/glade/collections/cdg/data/cesmLE/CESM-CAM5-BGC-LE/lnd/proc/tseries/daily/TREFMXAV_R/b.e11.BRCP85C5CNBDRD.f09_g16."+member+".clm2.h1.TREFMXAV_R.20060101-20801231.nc")
    # get the clm latitude
    CLM_lat = TREFMXAV_U.indexes['lat']
    # get the mask of clm
    mask = TREFMXAV_U["TREFMXAV_U"].loc["2006-01-02"].notnull().squeeze()
    # get the Urban maximal temperature
    U_max = TREFMXAV_U["TREFMXAV_U"].sel(time=slice(start_date, end_date))
    R_max = TREFMXAV_R["TREFMXAV_R"].where(mask)\
        .sel(time=slice(start_date, end_date))\
        .rename("TREFMXAV_R")
    
    # create a list to loop the variables
    temp = [U_max,R_max]


    var_list = ["TREFHTMX"]

    for var in var_list:
        df = get_ts_masked_cam(start_date, end_date, 
                               var, member, CLM_lat, mask)
        temp.append(df)
        del df
        gc.collect()

    # merge the list as a DataSet
    start_time = time.time()
    ds = xr.merge(temp)
    print("It took", time.time()-start_time,"to merge")

    # convert the DataSet to DataFrame
    start_time = time.time()
    df = ds.to_dataframe()
    print(df.shape)
    print("It took", time.time()-start_time,"to convert to DataFrame")

    # delete the NaN
    start_time = time.time()
    df_final = df[~np.isnan(df["TREFMXAV_U"])]
    print(df_final.shape)
    print("It took", time.time()-start_time,"to delete NaN")
    
    df_var = df_final[["TREFMXAV_U",
                       "TREFMXAV_R",
                       "TREFHTMX"]]
    
    print(df_var.shape)
    df_var.to_csv("/glade/scratch/zhonghua/CESM_gridcell/"+member+"_"+start_date[:4]+"_"+end_date[:4]+".csv")
    
    #return df_var
    
    
for i in range(2,34):
    member = (str(i).zfill(3))
    print(member)
    get_df(start_date="2006-01-02", end_date="2015-12-31", member=member)
    get_df(start_date="2061-01-01", end_date="2070-12-31", member=member)