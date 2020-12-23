import pandas as pd
import os
def demandsidedrip(v,t,d,demand,avail):
    parent_dir="C:/Users/Rishabh/waterbudgeting/Data/"
    home_dir=parent_dir+d+"/"+t+"/"+v+"/"
    df = pd.read_csv(home_dir+'Rabi_crops.csv')
    df = df.sort_values(by='drip',ascending=False,ignore_index=True)
   
    water_area = []
    for i in range(0,len(df)):
        water_area.append(df['Total_list'][i]/df['Area'][i])
    df['water_intensity'] = water_area
    sum = df['water_intensity'].sum()
    weight = []
    for i in range(0,len(df)):
        weight.append(df['water_intensity'][i]/sum)
    df['weight'] = weight
    #print(weight)
    cwr = demand
    aval = avail
    old_drip = [0 for i in range(0,len(df))]
    for i in range(0,600):
        #print(i) 
        #print(cwr)
        for j in range(0,len(df)):
            if  cwr > aval :
                if old_drip[j] + df['weight'][j] < 100 :
                    cwr = cwr - df['Total_list'][j] * df['drip_eff'][j]/100 * (old_drip[j] + df['weight'][j])/100
                    old_drip[j] = old_drip[j] + df['weight'][j]
                    #print(df['weight'][j])
                    #print(df['Rabi crop'][j],'drip',old_drip[j])
            else:
                break
        df['drip'] = old_drip
    print(df['Rabi crop'])
    print(old_drip)
    return old_drip
    '''drip only on onion and pea for shastrinagar
    area reduction on wheat and onion'''
#demandsidedrip('Kanhur','Shirur','Pune',642,467)