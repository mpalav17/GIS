import os
import pandas as pd
import water_budgeting_modules.Crop_water_requirement.crop_water_req as cwr
import water_budgeting_modules.Crop_water_requirement.et_calc as et_dyn
import mysql.connector
import re

mydb = mysql.connector.connect(
    host = "localhost",
    database = "boondv1",
    user = "root",
    password = "root"
)

def crop_call(v,t,d,vc,season): 
    print("Total crop water requirement of kharif crops")
    parent_dir="C:/Users/Rishabh/waterbudgeting/Data/"
    home_dir=parent_dir+d+"/"+t+"/"+v+"/"
    df=pd.read_csv(home_dir+season+"_crops.csv")
    mycursor = mydb.cursor()
    mycursor.execute("select Crop_name,Crop_area,Sow_date,Drip_area from crop_details_"+season+" where village_code ="+str(vc)+";")
    res = mycursor.fetchall()
    crop=[]
    sow=[]
    area=[]
    drip=[]
    for i in range(0,len(res)):
        crop.append(res[i][0])
        area.append(int(res[i][1]))
        sow.append(res[i][2])
        drip.append(int(res[i][3])/100)
    print(crop,area)
    drip_eff=[]
    et=getET(v)
    for i in range(0,len(df)):
        # crop.append(df[season+' crop'][i])
        # sow.append(df['Sow date'][i])
        # area.append(df['Area'][i])
        # drip.append(df['drip'][i])
        drip_eff.append(df['drip_eff'][i])
    [total_cropreq,monthly_list,total_list,crop_coefficient]=cwr.cropreq(crop,sow,area,drip,drip_eff,et,d,t,season,vc)
    #df['Monthly list']=monthly_list#?
    #df['Total_list']=total_list#?
    df.to_csv(home_dir+season+"_crops.csv",index=False)
    return total_cropreq
def getET(village):
    
    et_2002=et_dyn.evapotrans(village)
    #et_2002 = [3.73, 4.74, 5.71, 6.5, 6.46, 5.27, 4.42, 4.06, 4.37, 4.77, 4.15, 3.78]
    #et_2019 = [32, 27, 10.1, 10.5, 2.6, 55.7, 80.2, 81.4, 77.5, 77.4, 55, 34.5]
    return et_2002
