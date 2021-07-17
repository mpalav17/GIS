import pandas as pd
import os
def demandsidearea(v,t,d,demand,avail):
    parent_dir="C:/Users/Rishabh/waterbudgeting/Data/"
    home_dir=parent_dir+d+"/"+t+"/"+v+"/"
    df = pd.read_csv(home_dir+'Rabi_crops.csv')
    df = df.sort_values(by='drip',ascending=False,ignore_index=True)
    water_ha = []
    area_reduction=[]
    for i in range(0,len(df)):
        water_ha.append(df['Total_list'][i]/df['Area'][i]) #more water intensive crop per hectare
    sum1 = sum(water_ha)
    #print(sum)
    final_red = {}
    water_int = []
    for i in range(0,len(df)):
        water_int.append(water_ha[i]/sum1)
    #print(water_int)
    for i in range(0,400):
        area_red = water_int
        #print(demand)
        #sum = 0
        for j in range(0,len(df)):
            if demand > avail :
                if area_red[j]*i < 100 :
                    demand -= df['Total_list'][j] * ((area_red[j])/100)
                    #area_red[j]+=0.1
                    #print('area reduce by',df['Rabi crop'][j],'by',area_red[j]*i)
                    #area_reduction.append(area_red[j]*i)
                    final_red[df['Rabi crop'][j]] = area_red[j]*i
            else :
                break
    #print(final_red) 
    return final_red
#demandsidearea('Kanhur','Shirur','Pune',4745,4566)
