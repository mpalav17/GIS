import os
import pandas as pd
import water_budgeting_modules.Canal_water.canal_water as canal
def canal_call(v,t,d,season,minor,canal_type): 
    print("Surface water from canal and recharge by it")
    parent_dir="C:/Users/Rishabh/waterbudgeting/Data/"
    home_dir=parent_dir+d+"/"+t+"/"+v+"/"
    df=pd.read_csv(home_dir+season+'_'+minor+"_canal.csv")
    sum_water_allot=0
    sum_recharge=0
    sum_surface_water=0
    water_alloted=[]
    recharge_list=[]
    surface_list=[]
    for i in range(0,len(df)):
        [water_allot,recharge,surface_water]=(canal.seepage_canal(canal_type,df['Minor'][i],df['Minor length'][i],df['Bed gradient'][i],df['Base width'][i],df['Design depth'][i],df['Water head'][i],df['Water mid'][i],df['Water tail'][i],df['Days'][i]))
        water_alloted.append(water_allot)
        sum_water_allot=sum_water_allot+sum(water_allot)
        recharge_list.append(recharge)
        sum_recharge=sum_recharge+sum(recharge)
        surface_list.append(surface_water)
        sum_surface_water=sum_surface_water+sum(surface_water)
    df['Water alloted']=water_alloted
    df['Recharge']=recharge_list
    df['Surface water']=surface_list
    df.to_csv(home_dir+season+'_'+minor+"_canal.csv",index=False)
    print(sum_water_allot)
    print(sum_recharge)
    print(sum_surface_water)
    return [sum_water_allot,sum_recharge,sum_surface_water]

#canal_call('Kanhur','Shirur','Pune','Kharif','12')