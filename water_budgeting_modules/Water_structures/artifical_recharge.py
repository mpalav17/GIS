import os
import pandas as pd
import water_budgeting_modules.Water_structures.structuresinvillage as strucvill
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    database = "boondv1",
    user = "root",
    password = "root"
)

def recharge_structures(v,t,d,vc):
    parent_dir="C:/Users/Rishabh/waterbudgeting/Data/"
    home_dir=parent_dir+d+"/"+t+"/"+v+"/"
    ndf=pd.read_csv(home_dir+"WCS_details.csv")
    surface_water_kharif=0
    
    mycursor = mydb.cursor()
    mycursor.execute("select * from transact_vallidations where village_code="+str(551216)+";")
    res=mycursor.fetchall()
    Storage_capacity = []
    Structure_name = []
    Number=[]
    Area = []
    for i in range(0,len(res)):
        Storage_capacity.append(float(res[i][2])/1000)
        Structure_name.append(res[i][3])
        Number.append(1)
        Area.append(float(res[i][2])/1000)
    df=pd.DataFrame({"Storage capacity":Storage_capacity, "Structure name":Structure_name, "Number":Number, "Area":Area})
    print(df['Storage capacity'][0])

    tot_seepage=0#Total seepage done even during rabi
    total_seepage_nonmon=0
    seepage = 0
    seepage_village=0
    total_area_WCS=0
    surface_water=0
    seepage_nonmon=0
    
    for i in range(0,len(df)):
        mycursor=mydb.cursor()
        print("h")
        if(df['Structure name'][i]=='K T weir'):
            evaporation = 934/1000
            [seepage,surface_water,seepage_nonmon]=strucvill.KT_weir(df['Storage capacity'][i]*2,df['Area'][i])
            seepage=seepage*df['Number'][i]
            total_area_WCS=total_area_WCS+(df['Number'][i]*df['Area'][i]*1000)
            evapo_loss=evaporation*0.6*df['Area'][i]
            surface_water=surface_water*df['Number'][i]
            surface_water-=evapo_loss
            seepage_nonmon=seepage_nonmon*df['Number'][i]
            
            print("The seepage from ",df['Number'][i]," ", df['Structure name'][i]," during the monsoon is ",seepage,"TCM")
            print("The surface water in ",df['Number'][i]," ", df['Structure name'][i]," after the monsoon is ",surface_water,"TCM")
            
            
            print()

            count = df['Number'][i]
            mycursor = mydb.cursor()
            # mycursor.execute("select * from KTWeir where village_code="+str(vc)+";")#individual structures, data insert and access, evaporation
            # res = mycursor.fetchall()
            # if res:
            #     print("update KTWeir set count="+str(count)+",seepage="+str(seepage)+",surface_water="+str(surface_water)+",total_area="+str(total_area_WCS)+" where village_code="+str(vc)+";")
            #     mycursor.execute("update KTWeir set count="+str(count)+",seepage="+str(seepage)+",surface_water="+str(surface_water)+",total_area="+str(total_area_WCS)+" where village_code="+str(vc)+";")
            # else:
            #     print("Hello")
            mycursor.execute("insert into KTWeir values("+str(vc)+","+str(count)+","+str(seepage)+","+str(surface_water)+","+str(df['Area'][i])+");")
            mydb.commit()

        elif(df['Structure name'][i]=='Konambe dam'):#dam/river
            evaporation = 934/1000
            count = df['Number'][i]
            [seepage,surface_water,seepage_nonmon]=strucvill.dam(df['Storage capacity'][i]*11.11,df['Area'][i])
            seepage=seepage*df['Number'][i]
            seepage_nonmon=seepage_nonmon*df['Number'][i]
            surface_water=surface_water*df['Number'][i]
            total_area_WCS=total_area_WCS+(df['Area'][i]*1000)
            evapo_loss=evaporation*0.6*total_area_WCS
            surface_water-=evapo_loss
            #surface_water_kharif=surface_water_kharif+650#full 1501 tcm wont be available to be used for the village
            #print(seepage_nonmon)
            print("The seepage from ",df['Number'][i]," ", df['Structure name'][i]," during the monsoon is ",seepage,"TCM")
            print("The surface water in ",df['Number'][i]," ", df['Structure name'][i]," after the monsoon is ",surface_water,"TCM")#evapo loss
            #seepage=seepage+seepage_nonmon
            print()

            # mycursor.execute("select * from Dam where village_code="+str(vc)+";")
            # res = mycursor.fetchall()
            # if res:
            #     print("update Dam set count="+str(count)+",seepage="+str(seepage)+",seepage_nonmon="+str(seepage_nonmon)+",surface_water="+str(surface_water)+",total_area="+str(total_area_WCS)+" where village_code="+str(vc)+";")
            #     mycursor.execute("update Dam set count="+str(count)+",seepage="+str(seepage)+",seepage_nonmon="+str(seepage_nonmon)+",surface_water="+str(surface_water)+",total_area="+str(total_area_WCS)+" where village_code="+str(vc)+";")
            # else:
            #     print("Hello")
            mycursor.execute("insert into Dam values("+str(vc)+","+str(count)+","+str(seepage)+","+str(seepage_nonmon)+","+str(surface_water)+","+str(df['Area'][i])+");")
            mydb.commit()

        elif(df['Structure name'][i]=='CCT'):
            count = df['Number'][i]
            [seepage,soil_mois]=strucvill.CCT(df['Storage capacity'][i]*0.6,df['Number'][i],df['Area'][i])
            print("The seepage from ", df['Structure name'][i]," during the monsoon is ",seepage,"TCM")
            print("The soilmois from ", df['Structure name'][i]," during the monsoon is ",soil_mois,"TCM")
            #infilteration=infilteration+soil_mois
            seepage=seepage+soil_mois

            # mycursor.execute("select * from CCT where village_code="+str(vc)+";")
            # res = mycursor.fetchall()
            # if res:
            #     print("update CCT set count="+str(count)+",seepage="+str(seepage)+",soil_mois="+str(soil_mois)+" where village_code="+str(vc)+";")
            #     mycursor.execute("update CCT set count="+str(count)+",seepage="+str(seepage)+",soilmois="+str(soil_mois)+" where village_code="+str(vc)+";")
            # else:
            #     print("Hello")
            mycursor.execute("insert into CCT values("+str(vc)+","+str(count)+","+str(seepage)+","+str(soil_mois)+","+str(df['Area'][i]+");"))
            mydb.commit()

        elif(df['Structure name'][i]=='Recharge shaft'):
            count = df['Number'][i]
            seepage=strucvill.shaft(df['Storage capacity'][i])
            seepage=seepage*df['Number'][i]
            print("The seepage from ", df['Structure name'][i]," during the monsoon is ",seepage,"TCM")

            # mycursor.execute("select * from RechargeShaft where village_code="+str(vc)+";")
            # res = mycursor.fetchall()
            # if res:
            #     print("update RechargeShaft set count="+str(count)+",seepage="+str(seepage)+" where village_code="+str(vc)+";")
            #     mycursor.execute("update RechargeShaft set count="+str(count)+",seepage="+str(seepage)+" where village_code="+str(vc)+";")
            # else:
            #     print("Hello")
            mycursor.execute("insert into RechargeShaft values("+str(vc)+","+str(count)+","+str(seepage)+");")
            mydb.commit()

        else:#percolation tank and Nala
            if (df['Structure name'][i] == 'farm pond' or df['Structure name'][i] == 'Village pond'):
                pass
            else:
                count = df['Number'][i]
                capacity = float(df['Storage capacity'][i])*3
                seepage=strucvill.WCS(capacity)
                seepage=seepage*df['Number'][i]
                evaporation = seepage
                print("The seepage from ",df['Number'][i]," ", df['Structure name'][i]," to the groundwater is",seepage,"TCM")
                if(df['Structure name'][i]=='Percolation tank forest' or df['Structure name'][i]=='Cement nala bund forest'):
                    seepage=0
                print("Seepage is:",seepage)

                # mycursor.execute("select * from other_struct where village_code="+str(vc)+";")
                # res = mycursor.fetchall()
                # if res:
                #     print("update other_struct set count="+str(count)+",seepage="+str(seepage)+",name='"+str(df['Structure name'][i])+"' where village_code="+str(vc)+";")#name add,evapo

                #     mycursor.execute("update other_struct set count="+str(count)+",seepage="+str(seepage)+",name='"+str(df['Structure name'][i])+"' where village_code="+str(vc)+";")
                # else:
                #     print("Hello")
                print(df['Structure name'][i]+","+str(df['Area'][i]))
                print("insert into other_struct values("+str(vc)+","+str(count)+","+str(seepage)+",'"+str(df['Structure name'][i])+"',"+str(df['Area'][i])+");")
                mycursor.execute("insert into other_struct values("+str(vc)+","+str(count)+","+str(seepage)+",'"+df['Structure name'][i]+"',"+str(df['Area'][i])+");")
                mydb.commit()

        tot_seepage=tot_seepage+seepage
        surface_water_kharif=surface_water_kharif+surface_water
        total_seepage_nonmon=total_seepage_nonmon+seepage_nonmon
        
    seepage_village=seepage_village+tot_seepage
    return [seepage_village,surface_water_kharif,total_seepage_nonmon,total_area_WCS]

def farm_ponds(v,t,d,vc):#farmpond,forloop
    evaporation = 934/1000
    mycursor=mydb.cursor()
    parent_dir="C:/Users/Rishabh/waterbudgeting/Data/"
    home_dir=parent_dir+d+"/"+t+"/"+v+"/"
    print("Total amount of surface water impounded by lined farm ponds")

    mycursor = mydb.cursor()
    mycursor.execute("select * from transact_vallidations where village_code="+str(551216)+";")
    res=mycursor.fetchall()
    Storage_capacity = []
    Structure_name = []
    Number=[]
    Area=[]
    for i in range(0,len(res)):
        Storage_capacity.append(float(res[i][2])/1000)
        Structure_name.append(res[i][3])
        Number.append(1)
        Area.append(float(res[i][2])/1000)
    df=pd.DataFrame({"Storage capacity":Storage_capacity, "Structure name":Structure_name, "Number":Number, "Area":Area})

    surface_water_kharif_linedponds = 0
    total_area_WCS_linedponds = 0
    total_surface_water_artificial = 0
    total_surface_water_natural = 0
    for i in range(0,len(df)):
        if df['Structure name'][i] == "farm pond":
            #df=pd.read_csv(home_dir+"farmponds_Lined.csv")
            surface_water_artificial=df['Storage capacity'][i]*2*df['Number'][i]*0.7
            surface_water_natural=df['Storage capacity'][i]*2*df['Number'][i]*0.3
            surface_water=surface_water_artificial+surface_water_natural
            total_surface_water_artificial+=surface_water_artificial
            total_surface_water_natural += surface_water_natural

            #surface_water=surface_water-((df['Area'][0]*1900/1000)/1000)
            print("The surface water available in ",df['Number'][i]," lined farm ponds after the monsoon is ",surface_water,"TCM")
            count=df['Number'][i]
            #print('u-lined',usable_water)
            
            total_area_WCS_linedponds+=(df['Area'][i]*1000*df['Number'][i])
            evapo_loss=evaporation*0.6*df['Area'][i]
            surface_water-=evapo_loss
            surface_water_kharif_linedponds+=surface_water 

            # mycursor.execute("select * from Farm_ponds_lined where village_code="+str(vc)+";")
            # res = mycursor.fetchall()
            # if res:#only surface_water required
            #     print("update Farm_ponds_lined set count="+str(count)+",surface_water_art="+str(surface_water_artificial)+",surface_water_nat="+str(surface_water_natural)+",total_area="+str(total_area_WCS_linedponds)+" where village_code="+str(vc)+";")
            #     mycursor.execute("update Farm_ponds_lined set count="+str(count)+",surface_water_art="+str(surface_water_artificial)+",surface_water_nat="+str(surface_water_natural)+",total_area="+str(total_area_WCS_linedponds)+" where village_code="+str(vc)+";")
            # else:
            #     print("Hello")
            mycursor.execute("insert into Farm_ponds_lined values("+str(vc)+","+str(count)+","+str(surface_water_artificial)+","+str(surface_water_natural)+","+str(df['Area'][i])+");")
            mydb.commit()

    return surface_water_kharif_linedponds,total_area_WCS_linedponds,surface_water_artificial,surface_water_natural

def farm_ponds_unlined(v,t,d,vc):#villagepond
    evaporation = 934/1000
    mycursor=mydb.cursor()
    print("Total amount of surface water impounded by non lined farm ponds")
    parent_dir="C:/Users/Rishabh/waterbudgeting/Data/"
    home_dir=parent_dir+d+"/"+t+"/"+v+"/"

    mycursor = mydb.cursor()
    mycursor.execute("select * from transact_vallidations where village_code="+str(551216)+";")
    res=mycursor.fetchall()
    Storage_capacity = []
    Structure_name = []
    Number=[]
    Area=[]
    for i in range(0,len(res)):
        Storage_capacity.append(float(res[i][2])/1000)
        Structure_name.append(res[i][3])
        Number.append(1)
        Area.append(float(res[i][2])/1000)
    df=pd.DataFrame({"Storage capacity":Storage_capacity, "Structure name":Structure_name, "Number":Number, "Area":Area})

    surface_water_total = 0
    total_seepage_nonmon_unlined = 0
    total_seepage_unlined = 0
    total_area_WCS_unlined = 0
    for i in range(0,len(df)):
        if df['Structure name'][i] == "Village pond":
        # df=pd.read_csv(home_dir+"farmponds_Non Lined.csv")
            [seepage,surface_water,seepage_nonmon]=strucvill.storage_tanks(df['Storage capacity'][i]*3,df['Area'][i])
            print("The surface water available after seepage in ",df['Number'][i]," Non lined farm ponds after the monsoon is ",(df['Number'][i]*(surface_water)),"TCM")
            print("The seepage from ",df['Number'][i]," Non lined farm ponds after the monsoon is ",(df['Number'][i]*(seepage)),"TCM")
            #print('u-unlined',usable_water*df['Non Lined farm pond'][0])
            count=df['Number'][i]
            surface_water_kharif_unlined=(surface_water*df['Number'][i])
            total_seepage_unlined += seepage*(df['Number'][i])
            total_seepage_nonmon_unlined += (seepage_nonmon*df['Number'][i])
            total_area_WCS_unlined += (df['Area'][i]*1000*df['Number'][i])
            evapo_loss=evaporation*0.6*df['Area'][i]
            surface_water -= evapo_loss
            surface_water_total+=surface_water
            # mycursor.execute("select * from Farm_ponds_unlined where village_code="+str(vc)+";")
            # res = mycursor.fetchall()
            # if res:
            #     print("update Farm_ponds_unlined set count="+str(count)+",surface_water="+str(surface_water)+",seepage_unlined="+str(total_seepage_unlined)+",seepage_nonmon="+str(total_seepage_nonmon_unlined)+",total_area="+str(total_area_WCS_unlined)+" where village_code="+str(vc)+";")
            #     mycursor.execute("update Farm_ponds_unlined set count="+str(count)+",surface_water="+str(surface_water)+",seepage_unlined="+str(total_seepage_unlined)+",seepage_nonmon="+str(total_seepage_nonmon_unlined)+",total_area="+str(total_area_WCS_unlined)+" where village_code="+str(vc)+";")
            # else:
            #     print("Hello")
            mycursor.execute("insert into Farm_ponds_unlined values("+str(vc)+","+str(count)+","+str(surface_water_kharif_unlined)+","+str(seepage)+","+str(seepage_nonmon)+","+str(df['Area'][i])+");")
            mydb.commit()

    return surface_water_total,total_seepage_unlined,total_seepage_nonmon_unlined,total_area_WCS_unlined