import os
import pandas as pd
import water_budgeting_modules.Water_structures.structuresinvillage as strucvill
def recharge_structures(v,t,d):
    parent_dir="C:/Users/Rishabh/waterbudgeting/Data/"
    home_dir=parent_dir+d+"/"+t+"/"+v+"/"
    df=pd.read_csv(home_dir+"WCS_details.csv")
    surface_water_kharif=0
    
    tot_seepage=0#Total seepage done even during rabi
    total_seepage_nonmon=0
    seepage_village=0
    total_area_WCS=0
    surface_water=0
    seepage_nonmon=0
    
    for i in range(0,len(df)):
      
        if(df['Structure name'][i]=='K T weir'):
            [seepage,surface_water,seepage_nonmon]=strucvill.KT_weir(df['Storage capacity'][i],df['Area'][i])
            seepage=seepage*df['Number'][i]
            surface_water=surface_water*df['Number'][i]
            seepage_nonmon=seepage_nonmon*df['Number'][i]
            
            print("The seepage from ",df['Number'][i]," ", df['Structure name'][i]," during the monsoon is ",seepage,"TCM")
            print("The surface water in ",df['Number'][i]," ", df['Structure name'][i]," after the monsoon is ",surface_water,"TCM")
            total_area_WCS=total_area_WCS+(df['Number'][i]*df['Area'][i]*1000)
            print()
        elif(df['Structure name'][i]=='Konambe dam'):
            [seepage,surface_water,seepage_nonmon]=strucvill.dam(df['Storage capacity'][i],df['Area'][i])
            seepage=seepage*df['Number'][i]
            seepage_nonmon=seepage_nonmon*df['Number'][i]
            surface_water=surface_water*df['Number'][i]
            total_area_WCS=total_area_WCS+(df['Area'][i]*1000)
            #surface_water_kharif=surface_water_kharif+650#full 1501 tcm wont be available to be used for the village
            #print(seepage_nonmon)
            print("The seepage from ",df['Number'][i]," ", df['Structure name'][i]," during the monsoon is ",seepage,"TCM")
            print("The surface water in ",df['Number'][i]," ", df['Structure name'][i]," after the monsoon is ",surface_water,"TCM")
            #seepage=seepage+seepage_nonmon
            print()
        elif(df['Structure name'][i]=='CCT'):
            [seepage,soil_mois]=strucvill.CCT(df['Storage capacity'][i],df['Number'][i],df['Area'][i])
            print("The seepage from ", df['Structure name'][i]," during the monsoon is ",seepage,"TCM")
            print("The soilmois from ", df['Structure name'][i]," during the monsoon is ",soil_mois,"TCM")
            #infilteration=infilteration+soil_mois
            seepage=seepage+soil_mois
        elif(df['Structure name'][i]=='Recharge shaft'):
            seepage=strucvill.shaft(df['Storage capacity'][i])
            seepage=seepage*df['Number'][i]
            print("The seepage from ", df['Structure name'][i]," during the monsoon is ",seepage,"TCM")
        else:
            seepage=strucvill.WCS(df['Storage capacity'][i])
            seepage=seepage*df['Number'][i]
            print("The seepage from ",df['Number'][i]," ", df['Structure name'][i]," to the groundwater is",seepage,"TCM")
            if(df['Structure name'][i]=='Percolation tank forest' or df['Structure name'][i]=='Cement nala bund forest'):
                   seepage=0
            print()
        tot_seepage=tot_seepage+seepage
        surface_water_kharif=surface_water_kharif+surface_water
        total_seepage_nonmon=total_seepage_nonmon+seepage_nonmon
        
    seepage_village=seepage_village+tot_seepage
    return [seepage_village,surface_water_kharif,total_seepage_nonmon,total_area_WCS]

def farm_ponds(v,t,d):
    
    parent_dir="C:/Users/Rishabh/waterbudgeting/Data/"
    home_dir=parent_dir+d+"/"+t+"/"+v+"/"
    print("Total amount of surface water impounded by lined farm ponds")
    df=pd.read_csv(home_dir+"farmponds_lined.csv")
    surface_water_artificial=df['Capacity'][0]*df['Lined farm pond'][0]*0.7
    surface_water_natural=df['Capacity'][0]*df['Lined farm pond'][0]*0.3
    surface_water=surface_water_artificial+surface_water_natural
    #surface_water=surface_water-((df['Area'][0]*1900/1000)/1000)
    print("The surface water available in ",df['Lined farm pond'][0]," lined farm ponds after the monsoon is ",surface_water,"TCM")
    #print('u-lined',usable_water)
    surface_water_kharif_linedponds=surface_water
    total_area_WCS_linedponds=(df['Area'][0]*df['Lined farm pond'][0])
    return surface_water_kharif_linedponds,total_area_WCS_linedponds,surface_water_artificial,surface_water_natural

def farm_ponds_unlined(v,t,d):
    print("Total amount of surface water impounded by non lined farm ponds")
    parent_dir="C:/Users/Rishabh/waterbudgeting/Data/"
    home_dir=parent_dir+d+"/"+t+"/"+v+"/"
    df=pd.read_csv(home_dir+"farmponds.csv")
    [seepage,surface_water,seepage_nonmon]=strucvill.storage_tanks(df['Capacity'][0],df['Area'][0])
    print("The surface water available after seepage in ",df['Non Lined farm pond'][0]," Non lined farm ponds after the monsoon is ",(df['Non Lined farm pond'][0]*(surface_water)),"TCM")
    print("The seepage from ",df['Non Lined farm pond'][0]," Non lined farm ponds after the monsoon is ",(df['Non Lined farm pond'][0]*(seepage)),"TCM")
    #print('u-unlined',usable_water*df['Non Lined farm pond'][0])
    surface_water_kharif_unlined=(surface_water*df['Non Lined farm pond'][0])
    total_seepage_unlined=seepage*(df['Non Lined farm pond'][0])
    total_seepage_nonmon_unlined=(seepage_nonmon*df['Non Lined farm pond'][0])
    total_area_WCS_unlined=(df['Area'][0]*df['Non Lined farm pond'][0])
    return surface_water_kharif_unlined,total_seepage_unlined,total_seepage_nonmon_unlined,total_area_WCS_unlined