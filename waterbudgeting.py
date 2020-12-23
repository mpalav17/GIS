import os
import pandas as pd
import water_budgeting_modules.Rainfall.total_rainfall as tr
import field_worker_input as field
import water_budgeting_modules.Domestic_requirement.domestic_req as dom
import water_budgeting_modules.Crop_water_requirement.crop_call_CWR as crop
import water_budgeting_modules.Water_structures.artifical_recharge as art
import water_budgeting_modules.ET_nonAgri.indices as ind
import water_budgeting_modules.Runoff.Total_runoff as run
import Advisories_modules.Demand.advisories_demand as adv
import Advisories_modules.Demand.advisories_area_red as areared
parent_dir="C:/Users/Rishabh/waterbudgeting/"
def main():
    a=input(("Press one for first time user and two for registered user"))
    if(int(a) ==1):
        field.enter_primary_Details()
    else:
        district_name=input("Enter the district name")
        tehsil_name=input("Enter the tehsii name")
        village_name=input("Enter the village name")
        show_water_budget(district_name,tehsil_name,village_name)

def show_water_budget(d,t,v):
    print()
    
    village_area=getArea(v,t,d)
    
    #Rainfall component
    rainfall_avail=tr.rainfall(village_area,v)
    print("The amount of water available from rainall is ",rainfall_avail," TCM")
   
    #Runoff compononent
    [tot_runoff,worthy_area]=run.runoff(v)
    print("Total runoff is ",tot_runoff," TCM")
    print('Worthy area',worthy_area)
    #Domestic component
    print()
    [sum_domreq,sum_domkharif]=dom.getDomestic(v,t,d)


    #Crop water requirement component
    print()
    print('Kharif')
    total_cropreq_kharif=crop.crop_call(v,t,d,'Kharif')
    print('Annual')
    total_cropreq_annual=crop.crop_call(v,t,d,'Annual')
    print('Summer')
    total_cropreq_summer=crop.crop_call(v,t,d,'Summer')

    total_cropreq=(0.25*total_cropreq_annual)+total_cropreq_kharif
    #total_cropreq=total_cropreq+142.5
    #print('Crop water requirment for grape is in 60 hectares of land is 720TCM')
    #grape drip is considered at 100% for 48% effciency
    #total_cropreq=total_cropreq+375+142.5#considered fodders also for kharif, later change it in main code
    
    
    #WCS componenent
    print()
    print("Total amount of surface water impounded")
    [seepage_village,surface_water_kharif,total_seepage_nonmon,total_area_WCS]=art.recharge_structures(v,t,d)
    print()
    [surface_water_kharif_linedponds,total_area_WCS_linedponds,surface_water_artificial_linedponds,surface_water_natural_linedponds]=art.farm_ponds(v,t,d)
    print()
    [surface_water_kharif_unlined,total_seepage_unlined,total_seepage_nonmon_unlined,total_area_WCS_unlined]=art.farm_ponds_unlined(v,t,d)
    
    total_seepage_village=seepage_village+total_seepage_unlined
    total_seepage_nonmon_village=total_seepage_nonmon+total_seepage_nonmon_unlined
    total_surface_water=surface_water_kharif+surface_water_kharif_linedponds+surface_water_kharif_unlined
    total_area_WCS_village=total_area_WCS+total_area_WCS_linedponds+total_area_WCS_unlined
    print("total nonmon", total_seepage_nonmon_village)
    #surface_water_kharif=surface_water_kharif-1501+500#this is temporary, just subtracting konambe dam surface water

    print("Total area of surface water", total_area_WCS_village)
    print("surface water before evaporation",total_surface_water)
    total_surface_water=total_surface_water-((total_area_WCS_village*.934*0.6)/1000)
    
    #surface_water_kharif=surface_water_kharif-(surface_water_kharif*0.30)
    #et=0.3*rainfall_avail
    
    #ET componenent
    print()
    print("Evapotranspiration loses from non-agricultrual land")
    et=ind.Evapotranspiration()
    print("Total water lost in barren is ", et[0]/1000,'TCM') 
    print("Total water lost in shrubs is ", (et[1]/1000),'TCM') 
    print("Total water lost in forest is ", et[2]/1000,'TCM')
    
    print()
    print("Total surface water available after kharif ",total_surface_water,'TCM')
    print("Total seepage in the village after kharif ",total_seepage_village,'TCM')
    print('Total kharif crop requirement is ',total_cropreq,'TCM')
    print('Total domestic requirement for the kharif is ',sum_domkharif,'TCM')
    print('Total loss from non agricultural land is ',(et[0]/1000)+(et[2]/1000)+(et[1]/1000),'TCM')
    print()
    
    #Main equation
    water_kharif=rainfall_avail-tot_runoff+total_seepage_village+surface_water_kharif-total_cropreq-sum_domreq-(et[0]/1000)-(et[2]/1000)-(et[1]/1000)#-protect_irrigation
    print('The amount of water present for rabi is',water_kharif,' TCM')

    print()
    a=int(input("Press 1 to continue with rabi planning"))
    if(a==1):
        total_cropreq_rabi=crop.crop_call(v,t,d,'Rabi')
        total_CWR_demand=total_cropreq_rabi+total_cropreq_summer+(0.75*total_cropreq_annual)
        print('Total CWR requirement for rabi is ',total_CWR_demand)
    annual_gross_draft=(.1*total_cropreq)+sum_domreq+total_CWR_demand-(total_surface_water+total_seepage_nonmon_village)-(.1*total_CWR_demand)
    print("Annual gross draft ",annual_gross_draft)
    groundwater=groundwater_avail(worthy_area)
    print('Groundwater available in the village', groundwater)
    stage_of_development=(annual_gross_draft/groundwater)*100
    print('Stage of groundwater developement is ',stage_of_development,'%')
    
    #Advisory
    print('The drip irrigation advisory for the current water availability are as follows')
    area_drip=adv.demandsidedrip(v,t,d,total_CWR_demand,water_kharif)
    print(area_drip)
    print('The drip irrigation advisory for the current water availability are as follows')
    area_red=areared.demandsidearea(v,t,d,total_CWR_demand,water_kharif)
    print(area_red)
    
#Ground water availabilty
def groundwater_avail(worthy_area):
    #pre_monlevel=8.7 # for village kanhur (Pabal area)
    #post_monlevel=4 #2 for village kanhur (Pabal area)
    #pre_monlevel=12#12 # for village konambe
    #post_monlevel=0#4# for village konambe
    #pre_monlevel=13.2#12.5 # for village Shastrinagar
    #post_monlevel=4#2.75 # for village Shastrinagar
    pre_monlevel=12.5 # for village Kirtangali
    post_monlevel=1# 4 for village Kirtangali
    specific_yield=0.02 
    print(worthy_area)
    groundwater=specific_yield*(pre_monlevel-post_monlevel)*worthy_area*10

    return groundwater
    #print(surface_water_kharif,' Surface water')
    #print(sum_domreq,' Domestic requirement')
def getArea(n,t,d):
    if(n == 'Konambe'):
        area=2022.1
    elif(n=='Kanhur'):
        area=2633
    elif(n=='Shastrinagar'):
        area=311
    elif(n=='Kirtangali'):
        area=607
    return area

main()
