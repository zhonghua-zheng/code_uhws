import xarray as xr
import pandas as pd
import numpy as np
import xgboost as xgb
import time
import pickle
import sklearn

from xgboost import XGBRegressor

import matplotlib.pyplot as plt

# load dataframe with maximal temp
def load_df_max_TREFHT(member, start_date, end_date):
    print("***************Start loading data***************")
    t0 = time.time()
    df = pd.read_csv("/glade/scratch/zhonghua/ensem_training_data_min/"+start_date+".csv")
    elapsed_time = time.time() - t0
    print("It takes elapsed_time", elapsed_time, "to read csv")
    print("***************Start convert lat/lon to string***************")
    t1=time.time()
    df[["lat","lon"]]=df[["lat","lon"]].round(4).astype(str)
    elapsed_time = time.time() - t1
    print("It takes elapsed_time", elapsed_time, "to convert lat/lon to string")
    print("***************Start One Hot Encoding***************")
    # https://stackoverflow.com/questions/44124436/python-datetime-to-season
    t2=time.time()
    df["time"]=pd.to_datetime(df["time"])
    months = ["Jan","Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
    month_to_months = dict(zip(range(1,13), months))
    df = pd.concat([df,pd.get_dummies(df["time"].dt.month.map(month_to_months).astype('category'))],axis=1)
    elapsed_time = time.time() - t2
    print("It takes elapsed_time", elapsed_time, "to finish the one hot encoding")
    return df

# XGB model 
def XGB_train(df,year,lat,lon,member):
    
    t_0=time.time()
    #df_temp = df[(df["lat"]==lat) & (df["lon"]==lon)].reset_index()
    df_lat = df[df["lat"]==lat]
    df_temp = df_lat[df_lat["lon"]==lon]
    
    vari_ls = ["QBOT","UBOT","VBOT",
               "TREFHT",
               "FLNS","FSNS",
               "PRECT","PRSN",
               "Jan","Feb", "Mar", 
               "Apr", "May", "June", 
               "July", "Aug", "Sept", 
               "Oct", "Nov", "Dec"]
    
    pred="TREFMNAV_U"

    XGBreg = XGBRegressor(objective ='reg:squarederror',n_jobs=-1,
                          learning_rate=0.08796346103242554,
                          max_depth=6,
                          n_estimators=576,
                          seed=66)
    XGBreg.fit(df_temp[vari_ls], df_temp[pred])
    elapsed_time = time.time() - t_0
    
    print("It takes elapsed_time", elapsed_time, "to train the model")
    pickle.dump(XGBreg, open("/glade/scratch/zhonghua/ensem_model_min/"+year+"/"+"MX_"+lat+"_"+lon+".dat","wb"))
    
    return XGBreg

# load the dictionary
lat_lon_dict=pickle.load(open("/glade/scratch/zhonghua/lat_lon_dict.dat","rb"))
lat_ls_load=pickle.load(open("/glade/scratch/zhonghua/lat_ls.dat","rb"))

# start the ml
member = "002"; start_date = "2061"; end_date = "2070"
df_002 = load_df_max_TREFHT(member, start_date, end_date)

df=df_002;year="2061";member="002"

i=1
for lat in lat_ls_load[1::2]:
    print(lat)
    for lon in lat_lon_dict[lat]:
        XGB_train(df,year,lat,lon,member)
        i+=1
        if (i%10==0):
            print(i)