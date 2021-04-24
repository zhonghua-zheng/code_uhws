import xarray as xr
import pandas as pd
import numpy as np
import xgboost as xgb
import time
import pickle
import sys

from xgboost import XGBRegressor

# load dataframe with maximal temp
def load_df_max_TREFHT(member, start_date, end_date):
    path = "/glade/scratch/zhonghua/CESM-LE-members-csv-min/"
    print("***************Start loading member",member,"***************")
    t0 = time.time()
    df = pd.read_csv(path+member+"_"+start_date+"_"+end_date+".csv")
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
    df["time"]=pd.to_datetime(df["time"],errors="coerce")
    #df = df.dropna(subset=['time'])
    months = ["Jan","Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
    month_to_months = dict(zip(range(1,13), months))
    df = pd.concat([df,pd.get_dummies(df["time"].dt.month.map(month_to_months).astype('category'))],axis=1)
    elapsed_time = time.time() - t2
    print("It takes elapsed_time", elapsed_time, "to finish the one hot encoding")
    return df

def XGB_test(df,year,lat,lon,member):
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
   

    XGBreg = pickle.load(open("/glade/scratch/zhonghua/ensem_model_min/"+year+"/"+"MX_"+lat+"_"+lon+".dat","rb"))
    df_temp[member]=XGBreg.predict(df_temp[vari_ls])
    
    #print("rmse:",np.sqrt(mean_squared_error(df_temp[member],df_temp[pred])))
    #print("mae:",mean_absolute_error(df_temp[member],df_temp[pred]))
    df_return=df_temp[["lat","lon","time",member,"TREFMNAV_U"]]
    df_return[["lat","lon"]]=df_return[["lat","lon"]].astype(np.float32)
    
    elapsed_time = time.time() - t_0
    print("It takes elapsed_time", elapsed_time, "to apply the model")
    
    return df_return.set_index(["lat","lon","time"])


#########################################################
lat_lon_dict=pickle.load(open("/glade/scratch/zhonghua/lat_lon_dict.dat","rb"))

member=sys.argv[1]
start_date=sys.argv[2]
end_date=sys.argv[3]

df = load_df_max_TREFHT(member, start_date, end_date)

i=1
df_final_ls=[]
for lat in lat_lon_dict:
    print(lat)
    for lon in lat_lon_dict[lat]:
        df_final_ls.append(XGB_test(df,start_date,lat,lon,member))
        i+=1
        if (i%10==0):
            print(i)
pd.concat(df_final_ls).to_csv("/glade/scratch/zhonghua/CESM_validation_min/"+start_date+"/"+member+"_ens.csv")
