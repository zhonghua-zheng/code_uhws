import xarray as xr
import pandas as pd
import numpy as np
import xgboost as xgb
import time
import pickle
from xgboost import XGBRegressor
import sys

# load dataframe with maximal temp
def load_df_CMIP(model_name, start_date):
    path = "/glade/scratch/zhonghua/CMIP5-RCP85_csv/"
    print("***************Start loading",model_name,"***************")
    t0 = time.time()
    df = pd.read_csv(path+model_name+"/"+start_date+".csv")
    elapsed_time = time.time() - t0
    print("It takes elapsed_time", elapsed_time, "to read csv")
    print("***************Start to convert lat/lon to string***************")
    t1=time.time()
    df[["lat","lon"]]=df[["lat","lon"]].round(4).astype(str)
    elapsed_time = time.time() - t1
    print("It takes elapsed_time", elapsed_time, "to convert lat/lon to string")
    print("***************Start One Hot Encoding***************")
    # https://stackoverflow.com/questions/44124436/python-datetime-to-season
    t2=time.time()
    df["time"]=pd.to_datetime(df["time"],errors="coerce")
    df = df.dropna(subset=['time'])
    months = ["Jan","Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
    month_to_months = dict(zip(range(1,13), months))
    df = pd.concat([df,pd.get_dummies(df["time"].dt.month.map(month_to_months).astype('category'))],axis=1)
    elapsed_time = time.time() - t2
    print("It takes elapsed_time", elapsed_time, "to finish the one hot encoding")
    return df

def XGB_apply(df,start_date,lat,lon,model_name):
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
    
    XGBreg = pickle.load(open("/glade/scratch/zhonghua/ensem_model/"+start_date+"/"+"MX_"+lat+"_"+lon+".dat","rb"))
    df_temp[model_name]=XGBreg.predict(df_temp[vari_ls])
    elapsed_time = time.time() - t_0
    print("It takes elapsed_time", elapsed_time, "to apply the model")
    
    df_return=df_temp[["lat","lon","time",model_name]]
    df_return[["lat","lon"]]=df_return[["lat","lon"]].astype(np.float32)
    
    return df_return.set_index(["lat","lon","time"])


#########################################################
lat_lon_dict=pickle.load(open("/glade/scratch/zhonghua/lat_lon_dict.dat","rb"))

model_name=sys.argv[1]
start_date=sys.argv[2]

df=load_df_CMIP(model_name, start_date)

i=1
df_final_ls=[]
for lat in lat_lon_dict:
    print(lat)
    for lon in lat_lon_dict[lat]:
        df_final_ls.append(XGB_apply(df,start_date,lat,lon,model_name))
        i+=1
        if (i%10==0):
            print(i)
pd.concat(df_final_ls).to_csv("/glade/scratch/zhonghua/CMIP5_pred/"+start_date+"/"+model_name+".csv")