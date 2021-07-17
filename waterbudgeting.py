import os
import pandas as pd
import water_budgeting_modules.Rainfall.total_rainfall as tr
import field_worker_input as field
import water_budgeting_modules.Domestic_requirement.domestic_req as dom
import water_budgeting_modules.Crop_water_requirement.crop_call_CWR as crop
import water_budgeting_modules.Water_structures.artifical_recharge as art
import water_budgeting_modules.ET_nonAgri.indices as ind
#import water_budgeting_modules.ET_nonAgri.landsattest as ind
import water_budgeting_modules.Runoff.Total_runoff as run
import Advisories_modules.Demand.advisories_demand as adv
import Advisories_modules.Demand.advisories_area_red as areared
import Advisories_modules.Supply.supply_side as supply
import water_budgeting_modules.Canal_water.canal_call as canal
import matplotlib.pyplot as plt
import psycopg2
import mysql.connector
import re
mydb = mysql.connector.connect(
    host = "localhost",
    database = "boondv1",
    user = "root",
    password = "root"
)
fw_id = 'M0001'
mycursor = mydb.cursor()
mycursor.execute("select district_name,tehsil_name,village_name, code from village_details where fw_id ='"+fw_id+"'")
parent_dir="C:/Users/Rishabh/waterbudgeting/"
def main():
    a=input(("Press one for first time user and two for registered user"))
    if(int(a) ==1):
        field.enter_primary_Details()
    else:
        for d,t,v,vc in mycursor:
            district_name=d
            tehsil_name=t
            village_name="".join(re.split("[^a-zA-Z]*", v))
            village_code = vc
        show_water_budget(district_name,tehsil_name,village_name,village_code)

def show_water_budget(d,t,v,vc):
    print()
    
    village_area=getArea(v,t,d,vc)
    
    #Rainfall component/?
    rainfall_avail=tr.rainfall(village_area,v)
    print("The amount of water available from rainall is ",rainfall_avail," TCM")
    db_rainfall_avail = rainfall_avail
   
    #Runoff compononent/
    [tot_runoff,worthy_area]=run.runoff(v)
    print("Total runoff is ",tot_runoff," TCM")
    print('Worthy area',worthy_area)

    db_tot_runoff = tot_runoff
    db_worthy_area = worthy_area

    mycursor = mydb.cursor()
    mycursor.execute("select * from rain_runoff_res where village_code="+str(vc)+";")
    res=mycursor.fetchall()
    # print("update rain_runoff_res set tot_rainfall="+str(db_rainfall_avail)+",tot_runoff="+str(db_tot_runoff)+",worthy_area="+str(db_worthy_area)+"where village_code="+str(vc)+";")
    # print("insert into rain_runoff_res values("+str(vc)+","+str(db_rainfall_avail)+","+str(db_tot_runoff)+","+str(db_worthy_area)+");")
    if res:
        #print("hello")
        mycursor.execute("update rain_runoff_res set tot_rainfall="+str(db_rainfall_avail)+",tot_runoff="+str(db_tot_runoff)+",worthy_area="+str(db_worthy_area)+"where village_code="+str(vc)+";")
    else:
        mycursor.execute("insert into rain_runoff_res values("+str(vc)+","+str(db_rainfall_avail)+","+str(db_tot_runoff)+","+str(db_worthy_area)+");") 

    #Domestic component
    print()
    [sum_domreq,sum_domkharif]=dom.getDomestic(v,t,d,vc)
    
    db_sum_domreq = sum_domreq
    db_sum_domkharif = sum_domkharif

    #Crop water requirement component
    print()
    print('Kharif')
    total_cropreq_kharif=crop.crop_call(v,t,d,vc,'Kharif')
    db_total_cropreq_kharif = total_cropreq_kharif

    print('Annual')
    total_cropreq_annual=crop.crop_call(v,t,d,vc,'Annual')
    db_total_cropreq_annual = total_cropreq_annual

    print('Summer')
    total_cropreq_summer=crop.crop_call(v,t,d,vc,'Summer')
    db_total_cropreq_summer = total_cropreq_summer

    total_cropreq=(0.25*total_cropreq_annual)+total_cropreq_kharif
    #total_cropreq=total_cropreq+142.5
    #print('Crop water requirment for grape is in 60 hectares of land is 720TCM')
    #grape drip is considered at 100% for 48% effciency
    #total_cropreq=total_cropreq+375+142.5#considered fodders also for kharif, later change it in main 
    


    

    
    
    #WCS componenent
    print()
    print("Total amount of surface water impounded")
    [seepage_village,surface_water_kharif,total_seepage_nonmon,total_area_WCS]=art.recharge_structures(v,t,d,vc)

    db_seepage_village = seepage_village
    db_surface_water_kharif = surface_water_kharif
    db_total_seepage_nonmon = total_seepage_nonmon
    db_total_area_WCS = total_area_WCS

    print()
    [surface_water_kharif_linedponds,total_area_WCS_linedponds,surface_water_artificial_linedponds,surface_water_natural_linedponds]=art.farm_ponds(v,t,d,vc)
    
    db_surface_water_kharif_linedponds = surface_water_kharif_linedponds
    db_total_area_WCS_linedponds = total_area_WCS_linedponds
    db_surface_water_artificial_linedponds = surface_water_artificial_linedponds
    db_surface_water_natural_linedponds = surface_water_natural_linedponds

    print()
    [surface_water_kharif_unlined,total_seepage_unlined,total_seepage_nonmon_unlined,total_area_WCS_unlined]=art.farm_ponds_unlined(v,t,d,vc)

    db_surface_water_kharif_unlined = surface_water_kharif_unlined
    db_total_seepage_unlined = total_seepage_unlined
    db_total_seepage_nonmon_unlined = total_seepage_nonmon_unlined
    db_total_area_WCS_unlined = total_area_WCS_unlined
    
    total_seepage_village=seepage_village+total_seepage_unlined
    db_total_seepage_village = total_seepage_village

    total_seepage_nonmon_village=total_seepage_nonmon+total_seepage_nonmon_unlined
    db_total_seepage_nonmon_village = total_seepage_nonmon_village

    total_surface_water=surface_water_kharif+surface_water_kharif_linedponds+surface_water_kharif_unlined
    db_total_surface_water = total_surface_water

    total_area_WCS_village=total_area_WCS+total_area_WCS_linedponds+total_area_WCS_unlined
    db_total_area_WCS_village = total_area_WCS_village
    
    print("total nonmon", total_seepage_nonmon_village)
    #surface_water_kharif=surface_water_kharif-1501+500#this is temporary, just subtracting konambe dam surface water
    
    print("Total area of surface water", total_area_WCS_village)
    print("surface water before evaporation",total_surface_water)
    # total_surface_water=total_surface_water-((total_area_WCS_village*.934*0.6)/1000)#total evapo loss=(total_area_WCS_village*.934*0.6)/1000)
    
    #surface_water_kharif=surface_water_kharif-(surface_water_kharif*0.30)
    #et=0.3*rainfall_avail
    
    #ET componenent
    print()
    print("Evapotranspiration loses from non-agricultrual land")
    et=ind.Evapotranspiration()
    #et=ind.Evapotranspiration(v,t,d,vc)
    print("Total water lost in barren is ", et[0]/1000,'TCM') 
    #print("Total water lost in shrubs is ", (et[1]/1000),'TCM') 
    print("Total water lost in forest is ", et[2]/1000,'TCM')
    
    print()
    print("Total surface water available after kharif ",total_surface_water,'TCM')
    print("Total seepage in the village after kharif ",total_seepage_village,'TCM')
    print('Total kharif crop requirement is ',total_cropreq,'TCM')
    print('Total domestic requirement for the kharif is ',sum_domkharif,'TCM')
    print('Total loss from non agricultural land is ',(et[0]/1000)+(et[2]/1000)+(et[1]/1000),'TCM')
    print()
    sum_loss_non_agri_land = (et[0]/1000)+(et[2]/1000)+(et[1]/1000)


    #sum domreq
    mycursor = mydb.cursor()
    mycursor.execute("select * from total_cwr where village_code="+str(vc)+";")
    res=mycursor.fetchall()
    # print("update rain_runoff_res set tot_rainfall="+str(db_rainfall_avail)+",tot_runoff="+str(db_tot_runoff)+",worthy_area="+str(db_worthy_area)+"where village_code="+str(vc)+";")
    # print("insert into rain_runoff_res values("+str(vc)+","+str(db_rainfall_avail)+","+str(db_tot_runoff)+","+str(db_worthy_area)+");")
    if res:
        #print("hello")
        mycursor.execute("update total_cwr set village_code="+str(vc)+",sum_domreq="+str(db_sum_domreq)+",sum_domkharif="+str(db_sum_domkharif)+",total_cropreq="+str(total_cropreq)+",sum_loss_non_agri_land="+str(sum_loss_non_agri_land)+";")
    else:
        mycursor.execute("insert into total_cwr values("+str(vc)+","+str(db_sum_domreq)+","+str(db_sum_domkharif)+","+str(total_cropreq)+","+str(sum_loss_non_agri_land)+");") 




    mycursor.execute("select * from evapo_loss where village_code="+str(vc)+";")
    res = mycursor.fetchall()
    if res:
        mycursor.execute("update evapo_loss set barren_loss="+str(et[0]/1000)+", shrubs_loss="+str(et[1]/1000)+", forest_loss="+str(et[2]/1000)+"where village_code="+str(vc)+";")
    else:
        # print("insert into evapo_loss values("+str(et[0]/1000)+","+str(et[1]/1000)+","+str(et[2]/1000)+","+str(vc)+");")
        mycursor.execute("insert into evapo_loss values("+str(et[0]/1000)+","+str(et[1]/1000)+","+str(et[2]/1000)+","+str(vc)+");")

    mydb.commit()
    
    #Main equation
    water_kharif=rainfall_avail-tot_runoff+total_seepage_village+surface_water_kharif-total_cropreq-sum_domreq-(et[0]/1000)-(et[2]/1000)-(et[1]/1000)#-protect_irrigation
    print('The amount of water present for rabi is',water_kharif,' TCM')

    print()
    a=int(input("Press 1 to continue with rabi planning"))
    if(a==1):
        total_cropreq_rabi=crop.crop_call(v,t,d,vc,'Rabi')
        total_CWR_demand=total_cropreq_rabi+total_cropreq_summer+(0.75*total_cropreq_annual)
        print('Total CWR requirement for rabi is ',total_CWR_demand)




    #sum domreq
    mycursor = mydb.cursor()
    mycursor.execute("select * from planning where village_code="+str(vc)+";")
    res=mycursor.fetchall()
    # print("update rain_runoff_res set tot_rainfall="+str(db_rainfall_avail)+",tot_runoff="+str(db_tot_runoff)+",worthy_area="+str(db_worthy_area)+"where village_code="+str(vc)+";")
    # print("insert into rain_runoff_res values("+str(vc)+","+str(db_rainfall_avail)+","+str(db_tot_runoff)+","+str(db_worthy_area)+");")
    if res:
        #print("hello")
        mycursor.execute("update planning set village_code="+str(vc)+",water_kharif="+str(water_kharif)+",total_cropreq_rabi="+str(total_cropreq_rabi)+",total_cwr_demand="+str(total_CWR_demand)+";")
    else:
        mycursor.execute("insert into planning values("+str(vc)+","+str(water_kharif)+","+str(total_cropreq_rabi)+","+str(total_CWR_demand)+");") 




    #Changes to be done to the canal water 
    #canal_water=0
    canal_water=782#TCM
    water_allot2=0
    recharge2=0
    surface_cana_water2=0
    water_allot4=0
    recharge4=0
    surface_cana_water4=0

    [water_allot1,recharge1,surface_cana_water1]=canal.canal_call(v,t,d,'Rabi','12','unlined')
    #[water_allot2,recharge2,surface_cana_water2]=canal.canal_call(v,t,d,'Rabi','12','lined')
    [water_allot3,recharge3,surface_cana_water3]=canal.canal_call(v,t,d,'Summer','12','unlined')
    #[water_allot4,recharge4,surface_cana_water4]=canal.canal_call(v,t,d,'Summer','12','lined')
    #[water_allot3,recharge2,surface_cana_water2]=canal.canal_call(v,t,d,'Summer','12','lined')
    print('The amount of water through canal is',water_allot1+water_allot2+water_allot3+water_allot4,' TCM')
    print('The amount of surface water through canal is',surface_cana_water1+surface_cana_water2+surface_cana_water4+surface_cana_water3,' TCM')
    print('The amount of ground water seeped through canal is',recharge1+recharge2+recharge3+recharge4,' TCM')
    
    #Change-Net water balance computation
    #The net water balance
    net_water_balance=(water_kharif+canal_water)-total_CWR_demand
    print('The net water balance is',net_water_balance)


    annual_gross_draft=(.1*total_cropreq)+sum_domreq+total_CWR_demand-(total_surface_water+total_seepage_nonmon_village)-(.1*total_CWR_demand)
    print("Annual gross draft ",annual_gross_draft)
    groundwater=groundwater_avail(worthy_area,v,t,d)
    groundwater+=recharge1+recharge3
    print('Groundwater available in the village', groundwater)
    stage_of_development=(annual_gross_draft/groundwater)*100
    print('Stage of groundwater developement is ',stage_of_development,'%')



    #sum domreq
    mycursor = mydb.cursor()
    mycursor.execute("select * from gw_draft where village_code="+str(vc)+";")
    res=mycursor.fetchall()
    # print("update rain_runoff_res set tot_rainfall="+str(db_rainfall_avail)+",tot_runoff="+str(db_tot_runoff)+",worthy_area="+str(db_worthy_area)+"where village_code="+str(vc)+";")
    # print("insert into rain_runoff_res values("+str(vc)+","+str(db_rainfall_avail)+","+str(db_tot_runoff)+","+str(db_worthy_area)+");")
    if res:
        #print("hello")
        mycursor.execute("update gw_draft set village_code="+str(vc)+",water_kharif="+str(annual_gross_draft)+",total_cropreq_rabi="+str(groundwater)+",total_cwr_demand="+str(stage_of_development)+";")
    else:
        mycursor.execute("insert into gw_draft values("+str(vc)+","+str(annual_gross_draft)+","+str(groundwater)+","+str(stage_of_development)+");") 





    #Change-If statement added
    #Advisory
    if(net_water_balance<0):
        print('The drip irrigation advisory for the current water availability are as follows')
        area_drip=adv.demandsidedrip(v,t,d,total_CWR_demand,(water_kharif+canal_water))
        print(area_drip)
        print('The area reduction advisory for the current water availability are as follows')
        area_red=areared.demandsidearea(v,t,d,total_CWR_demand,(water_kharif+canal_water))
        print(area_red)
        #Impact of the advisory on Stage of developement
        annual_gross_draft_revised=annual_gross_draft+net_water_balance
        stage_of_development_revised=(annual_gross_draft_revised/groundwater)*100
        print('Stage of groundwater developement ater the intevention is ',stage_of_development_revised,'%')
        #Decrease in the gross annual draft
        percent_decrease=(abs(net_water_balance)/annual_gross_draft)*100
        print('Net decrease in the gross annual draft is ',percent_decrease,'%')
    
    #supply side advisory
    #Change-Supply side advisory added if not already present
    volume=supply.supply_advisories(v,t,d,tot_runoff,total_seepage_village,total_surface_water)#?
    if(volume>0):
        print('Volume of water expected to be recharged at 75 percent efficiency ',volume,'TCM')
        print('Artificial recharge structures are possible to be developed to arrest the surplus runoff.')
        #Impact of the supply side advisory on stage of develeopement
        groundwater_revised=groundwater+volume
        stage_of_development_revised=(annual_gross_draft/groundwater_revised)*100
        print('Stage of groundwater development after the intevention is ',stage_of_development_revised,'%')
        percent_increase=(volume/groundwater)*100
        print('Net increase in the groundwater recharge is ',percent_increase,'%') 
    else:
        print('Maximum runoff is arrested, no more artifical recharge structures can be built')
    
    #Change historical well water data added. All the function call corresponding to this needs to 
    #added that is historicalWater and linreg
    historicalWater(v,t,d)
    #
    
def historicalWater(v,t,d):
    parent_dir="C:/Users/Rishabh/waterbudgeting/Data/"
    home_dir=parent_dir+d+"/"+t+"/"+v+"/"
    df=pd.read_csv(home_dir+"Historical_well.csv")
    postmonsoon_level=[]
    year=[]
    rainfall=[]
    for i in range(0,len(df)):
        postmonsoon_level.append(df['Post-monsoon'][i])
        year.append(df['Year'][i])
        rainfall.append(df['Rainfall'][i])
    print(postmonsoon_level)
    fig,ax = plt.subplots()
    ax2=ax.twinx()
    ax.bar(year, rainfall, label = "Rainfall graph",color='blue') 
    # set x-axis label
    #ax.set_xticks(np.arange(0, len(year)+1, 2),minor=False)
    ax.set_xlabel("year",fontsize=14)
    
    # set y-axis label
    ax.set_ylabel("Rainfall",color="blue")
    ax2.plot(year, postmonsoon_level, label = "Postmonsoon level",color="red",marker='o')
    ax2.set_ylabel("Water level",color="red")
    #ax2.set_xticks(np.arange(0, len(year)+1, 1),minor=False)
    ax2.invert_yaxis()
    [a,b]=linreg(year,postmonsoon_level)
    print('y=',a,'x','+',b)
    
    y=[]
    for i in range(0,len(year)):
        y.append(a*year[i]+b)
    print(y)
    ax2.plot(year, y, label = "Postmonsoon trend",color="black",marker='x')

    #[m,b2] = np.polyfit(rainfall, postmonsoon_level, 1)
    #ax2.plot(year,m*)
    plt.show()
    # save the plot as a file
    fig.savefig('well water trend.jpg',format='jpeg',dpi=100,bbox_inches='tight')
    #ax2.set_ylabel('Y axis1')
    #ax.xlabel('Year')
    #ax.ylabel('Y axis2')
    #plt.title('Well water trend')
    #plt.legend() 
    #plt.show()  
#Ground water availabilty
def linreg(X, Y):
    """
    return a,b in solution to y = ax + b such that root mean square distance between trend line and original points is minimized
    """
    N = len(X)
    Sx = Sy = Sxx = Syy = Sxy = 0.0
    for x, y in zip(X, Y):
        Sx = Sx + x
        Sy = Sy + y
        Sxx = Sxx + x*x
        Syy = Syy + y*y
        Sxy = Sxy + x*y
    det = Sxx * N - Sx * Sx
    return (Sxy * N - Sy * Sx)/det, (Sxx * Sy - Sx * Sxy)/det

# #waterkharif - waterdemand #?
# #Advisory
# print('The drip irrigation advisory for the current water availability are as follows')
# area_drip=adv.demandsidedrip(v,t,d,total_CWR_demand,water_kharif)
# print(area_drip)
# print('The drip irrigation advisory for the current water availability are as follows')
# area_red=areared.demandsidearea(v,t,d,total_CWR_demand,water_kharif)
# print(area_red)
    
#Ground water availabilty
def groundwater_avail(worthy_area,v,t,d):
    parent_dir="C:/Users/Rishabh/waterbudgeting/Data/"
    home_dir=parent_dir+d+"/"+t+"/"+v+"/"
    df=pd.read_csv(home_dir+'''+v'''+'Wadner'+"_well_water.csv")
    post_monlevel=df['post monsoon level'][0]
    pre_monlevel=df['pre monsoon level'][0]
    #pre_monlevel=8.7 # for village kanhur (Pabal area)
    #post_monlevel=4 #2 for village kanhur (Pabal area)
    #pre_monlevel=12#12 # for village konambe
    #post_monlevel=0#4# for village konambe
    #pre_monlevel=13.2#12.5 # for village Shastrinagar
    #post_monlevel=4#2.75 # for village Shastrinagar
    #pre_monlevel=12.5 # for village Kirtangali
    #post_monlevel=1# 4 for village Kirtangali

    specific_yield=0.02 
    print(worthy_area)
    groundwater=specific_yield*(pre_monlevel-post_monlevel)*worthy_area*10

    return groundwater
    #print(surface_water_kharif,' Surface water')
    #print(sum_domreq,' Domestic requirement')
def getArea(n,t,d,vc):
    # if(n == 'Konambe'):
    #     area=2022.1
    # elif(n=='Kanhur'):
    #     area=2633
    # elif(n=='Shastrinagar'):
    #     area=311
    # elif(n=='Kirtangali'):
    #     area=607
    # return area
    print(vc)
    mycursor1 = mydb.cursor()
    mycursor1.execute("select village_area from village_details where code = '"+str(vc)+"'")
    res = mycursor1.fetchall()
    for a in res:
        area = a[0]
    return area

main()
