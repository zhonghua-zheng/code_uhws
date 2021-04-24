# This script is used to extract the "TREFMNAV_U" from different members
# The results are at "/glade/scratch/zhonghua/CESM-LE-members-urban-temp-extracted-csv-min/"

import pandas as pd
import numpy as np
import time
import gc

############2006##########################
start_date="2006-01-02"; end_date="2015-12-31"; member="002"
time_point = time.time()
df = pd.read_csv("/glade/scratch/zhonghua/CESM-LE-members-csv-min/"+member+"_"+start_date[:4]+"_"+end_date[:4]+".csv")
print("It takes", time.time()-time_point, "to load csv")

df[member+"_min"] = df["TREFMNAV_U"]
df_temp = df[["lat","lon","time",member+"_min"]]
del df
gc.collect()

for i in range(3,34):
    member = (str(i).zfill(3))
    print("start to load member", member)
    t0 = time.time()
    df = pd.read_csv("/glade/scratch/zhonghua/CESM-LE-members-csv-min/"+member+"_"+start_date[:4]+"_"+end_date[:4]+".csv")
    df[member+"_min"] = df["TREFMNAV_U"]
    df_new = df[["lat","lon","time",member+"_min"]]
    print("It takes", time.time()-t0, "to load csv")
    
    print("start to merge member", member)
    t1 = time.time()
    df_temp = pd.merge(df_temp, 
                       df_new,
                       how='outer',
                       on=['lat', 'lon', 'time'])
    print(df_temp.shape)
    print("Merge time", time.time()-t1)
    print("\n")
    del df, df_new
    gc.collect()
    
df_temp.to_csv("/glade/scratch/zhonghua/CESM-LE-members-urban-temp-extracted-csv-min/urban_heat_LE_2006.csv",index=False)

del df_temp
gc.collect()

############2061##########################
start_date="2061-01-01"; end_date="2070-12-31"; member="002"
time_point = time.time()
df = pd.read_csv("/glade/scratch/zhonghua/CESM-LE-members-csv-min/"+member+"_"+start_date[:4]+"_"+end_date[:4]+".csv")
print("It takes", time.time()-time_point, "to load csv")

df[member+"_min"] = df["TREFMNAV_U"]
df_temp = df[["lat","lon","time",member+"_min"]]
del df
gc.collect()

for i in range(3,34):
    member = (str(i).zfill(3))
    print("start to load member", member)
    t0 = time.time()
    df = pd.read_csv("/glade/scratch/zhonghua/CESM-LE-members-csv-min/"+member+"_"+start_date[:4]+"_"+end_date[:4]+".csv")
    df[member+"_min"] = df["TREFMNAV_U"]
    df_new = df[["lat","lon","time",member+"_min"]]
    print("It takes", time.time()-t0, "to load csv")
    
    print("start to merge member", member)
    t1 = time.time()
    df_temp = pd.merge(df_temp, 
                       df_new,
                       how='outer',
                       on=['lat', 'lon', 'time'])
    print(df_temp.shape)
    print("Merge time", time.time()-t1)
    print("\n")
    del df, df_new
    gc.collect()
    
df_temp.to_csv("/glade/scratch/zhonghua/CESM-LE-members-urban-temp-extracted-csv-min/urban_heat_LE_2061.csv",index=False)