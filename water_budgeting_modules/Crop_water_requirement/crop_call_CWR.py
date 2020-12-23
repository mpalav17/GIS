import os
import pandas as pd
import water_budgeting_modules.Crop_water_requirement.crop_water_req as cwr
import water_budgeting_modules.Crop_water_requirement.et_calc as et_dyn
def crop_call(v,t,d,season): 
    print("Total crop water requirement of kharif crops")
    parent_dir="C:/Users/Rishabh/waterbudgeting/Data/"
    home_dir=parent_dir+d+"/"+t+"/"+v+"/"
    df=pd.read_csv(home_dir+season+"_crops.csv")
    crop=[]
    sow=[]
    area=[]
    drip=[]
    drip_eff=[]
    et=getET(v)
    for i in range(0,len(df)):
        crop.append(df[season+' crop'][i])
        sow.append(df['Sow date'][i])
        area.append(df['Area'][i])
        drip.append(df['drip'][i])
        drip_eff.append(df['drip_eff'][i])
    [total_cropreq,monthly_list,total_list]=cwr.cropreq(crop,sow,area,drip,drip_eff,et)
    df['Monthly list']=monthly_list
    df['Total_list']=total_list
    df.to_csv(home_dir+season+"_crops.csv",index=False)
    return total_cropreq
def getET(village):
    
    et_2002=et_dyn.evapotrans(village)
    #et_2002 = [3.73, 4.74, 5.71, 6.5, 6.46, 5.27, 4.42, 4.06, 4.37, 4.77, 4.15, 3.78]
    #et_2019 = [32, 27, 10.1, 10.5, 2.6, 55.7, 80.2, 81.4, 77.5, 77.4, 55, 34.5]
    return et_2002