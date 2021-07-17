#Work pending
#Introduce the cwr of grapes 
#link the ET code with this code
#Create the data base for all the excel sheets

import calendar
import re
from numpy.lib.shape_base import apply_along_axis
import pandas as pd
import xlrd
import math
import datetime
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    database="boondv1",
    user = "root",
    password = "root",
)



def cropreq(crop, sowdates, area_crop,drip,drip_eff,et,d,t,season,vc):#crop_name, sow_date (crop,sow,area,drip,drip_eff,et,d,t,season,vc)
    tot_requirement=0
    monthly_list=[]
    total_list=[]
    crop_coefficient=[]
    for i in range(0,len(crop)):
        #df = pd.read_csv('days_crop.csv')
        name = crop[i]

        sowdate = sowdates[i]
        area = area_crop[i]
        drip_crop=drip[i]
        drip_eff_crop=drip_eff[i]
        monthly_water_req = [0.0 for i in range(0,12)]

        et_2002=et
        
        #The month days and month name is stored for printing purposes
        m=[[31,28,31,30,31,30,31,31,30,31,30,31], [31,29,31,30,31,30,31,31,30,31,30,31]]#write a code for leap year too
        m_name = ['January','February','March','April','May','June','July','August','September','October','November','December'] 
        year = int(sowdate[6:])

        df = pd.read_csv('C:/Users/Rishabh/waterbudgeting/Data/days_crop_max.csv')
        #df = pd.read_csv('C:/Users/Rishabh/waterbudgeting/Data/days_crop_min.csv')
        days_scrop = []#will contain the growth stages of the crop

        for j in range(0,len(df)):
            if df['crop'][j]==name:
            #if name in df['crop'][j]:
                days_scrop.append(df['initial_stage'][j])
                days_scrop.append(df['dev_stage'][j])
                days_scrop.append(df['mid_stage'][j])
                days_scrop.append(df['late_stage'][j])
        print(df['crop'])
        crop_grow_old=days_scrop# extract dynamically from the database, this is the growth stage of the crop
        #print('Duration before calibration',crop_grow_old)
        
        crop_grow=growthStages_calibrate(d,crop_grow_old,name)
        #print('Duration after calibration',crop_grow)
        kc_scrop = []
        df = pd.read_csv('C:/Users/Rishabh/waterbudgeting/Data/kc_val_temp.csv')
        #df = pd.read_csv('C:/Users/Rishabh/waterbudgeting/Data/kc_val.csv')
        for j in range(0,len(df)):
            if df['crop'][j]==crop[i]:
            #if crop[i] in df['crop'][j]:
                kc_scrop.append(df['initial_stage'][j])
                kc_scrop.append(df['dev_stage'][j])
                kc_scrop.append(df['mid_stage'][j])
                kc_scrop.append(df['late_stage'][j])
        kc_crop=kc_scrop#[0.45,0.75,1.15,0.8]# extract dynamically from the database, this is the kc value of the crop
        #print('Kc before calibaration',kc_crop)
        
        [kc_calibrate,monthly_water_req]=computations(sowdate,area,drip_crop,drip_eff_crop,monthly_water_req,m,m_name,year,crop_grow_old,kc_crop,et_2002)
        #print('Hello', sum(monthly_water_req))
        if(area!=0):
            kc_crop=cropCoefficient_calibrate(d,t,kc_crop,name,((sum(monthly_water_req)/area)*100))
        #print('Kc after calibaration',kc_crop)
        [kc_calibrate,monthly_water_req]=computations(sowdate,area,drip_crop,drip_eff_crop,monthly_water_req,m,m_name,year,crop_grow,kc_crop,et_2002)
        crop_coefficient.append(kc_calibrate)
        print('Total water required for', name,'in', area,'hectares of land','is', ((sum(monthly_water_req))), 'TCM')
        monthly_list.append(monthly_water_req)
        tot_requirement=tot_requirement+(sum(monthly_water_req))
        total_list.append(sum(monthly_water_req))

        db_monthly = monthly_water_req
        db_crop_name = name
        db_area = area
        db_drip = drip_crop

        mycursor = mydb.cursor()
        mycursor.execute("select * from cwr_"+season+" where village_code="+str(vc)+" and "+"db_crop_name='"+name+"';")
        res=mycursor.fetchall()
        if res:
            # print("update cwr_"+season+" set db_area="+str(db_area)+",db_drip="+str(db_drip)+",jan="+str(db_monthly[0])+",feb="+str(db_monthly[1])+",mar="+str(db_monthly[2])+",apr="+str(db_monthly[3])+",may="+str(db_monthly[4])+",jun="+str(db_monthly[5])+",jul="+str(db_monthly[6])+",aug="+str(db_monthly[7])+",sep="+str(db_monthly[8])+",oct="+str(db_monthly[9])+",nov="+str(db_monthly[10])+",december="+str(db_monthly[11])+",db_total_list="+str(total_list[0])+" where village_code="+str(vc)+" and db_crop_name='"+db_crop_name+"';")
            mycursor.execute("update cwr_"+season+" set db_area="+str(db_area)+",db_drip="+str(db_drip)+",jan="+str(db_monthly[0])+",feb="+str(db_monthly[1])+",mar="+str(db_monthly[2])+",apr="+str(db_monthly[3])+",may="+str(db_monthly[4])+",jun="+str(db_monthly[5])+",jul="+str(db_monthly[6])+",aug="+str(db_monthly[7])+",sep="+str(db_monthly[8])+",oct="+str(db_monthly[9])+",nov="+str(db_monthly[10])+",december="+str(db_monthly[11])+",db_total_list="+str(total_list[0])+" where village_code="+str(vc)+" and db_crop_name='"+db_crop_name+"';")
        else:
            mycursor.execute("insert into cwr_"+season+" values("+str(vc)+",'"+name+"',"+str(db_area)+","+str(db_drip)+","+str(db_monthly[0])+","+str(db_monthly[1])+","+str(db_monthly[2])+","+str(db_monthly[3])+","+str(db_monthly[4])+","+str(db_monthly[5])+","+str(db_monthly[6])+","+str(db_monthly[7])+","+str(db_monthly[8])+","+str(db_monthly[9])+","+str(db_monthly[10])+","+str(db_monthly[11])+","+str(total_list[0])+");")
        mydb.commit()
        #end of the main for loop
    return tot_requirement,monthly_list,total_list,crop_coefficient
    #end of function
def computations(sowdate,area,drip_crop,drip_eff_crop,monthly_water_req,m,m_name,year,crop_grow,kc_crop,et_2002):
    kc_calibrate=[0,0,0,0,0,0,0,0,0,0,0,0]
    y_t = 0
    if(calendar.isleap(year)):
        y_t=1
    else:
        y_t=0
        
        #loop intializations
    month=m[y_t]
    date=sowdate.split('-')
    start_month=int(date[1])
    start_date=int(date[0])-1
    month[start_month-1]=month[start_month-1]-start_date
    #print(month[start_month-1])
    i=0
    j=start_month-1
    c=start_month-1
    kc=0
    count=0
    flag=0
    #algorithm to calibrate the kc value per month
    #print('crop growth stages',crop_grow)
    while(i<len(crop_grow)):
        d=crop_grow[i]
        j=c
        #print(kc_crop[i])
        while(j<len(month)):
                
            if(d>=(month[j]-count)):

                kc=kc+((month[j]-count)*kc_crop[i])/month[j]
                    
                kc_calibrate[j]=kc
                kc=0
                flag=1
                d=d-(month[j]-count)
                count=0
                if(j==len(month)-1):
                    if(calendar.isleap(year+1)):
                        month=m[1]
                    else:
                        month=m[0]
                    j=0
                else:
                    j=j+1
            elif(d<(month[j]-count)):
                if(count!=0):
                    kc=kc+((d*kc_crop[i])/month[j])
                    count=count+d

                else:
                    count=d
                    kc=kc+((count*kc_crop[i])/month[j])
                        

                flag=0
                d=0
                c=j
                j=j+1
                break

        if((i==len(crop_grow)-1) and flag==0):
            kc_calibrate[c]=kc_crop[i]
        #print(c)
        i=i+1
    
    
    monthly_water_req=cropwaterequirement(kc_calibrate,area,et_2002,m,drip_eff_crop,drip_crop,y_t)
    
    #print('**************************************************************************************')
    
    
    
    return(kc_calibrate,monthly_water_req)
def cropwaterequirement(kc_calibrate,area,et_2002,m,drip_eff_crop,drip_crop,y_t):
    monthly_water_req = [0.0 for i in range(0,12)]
    for i in range(0,12):
         if kc_calibrate[i] != 0:
             monthly_water_req[i] = ((area*10000)*(et_2002[i]/1000)*kc_calibrate[i]*m[y_t][i])/1000
             monthly_water_req[i]=monthly_water_req[i]-(monthly_water_req[i]*drip_eff_crop*drip_crop)
             #monthly_water_req[i] = ((area*10000)*(et_2002[i]/1000)*kc_calibrate[i])/1000
             #print('Water required for', name,'in', m_name[i], 'is', ((monthly_water_req[i])), 'TCM')
    return monthly_water_req
def growthStages_calibrate(d,crop_grow,name):
    district=d
    d='West part of Ahmadnagar'
    loc='C:/Users/Rishabh/waterbudgeting/Data/Agro_climatic_zone_CWR.xlsx'
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(1)
    i=0
    print(crop_grow)
    FAO_duration=sum(crop_grow)
    for row_num in range(sheet.nrows):
        row_value = sheet.row_values(row_num)
        #print(row_value[0])

        if row_value[0] == d:
            i=row_num
            break
    duration=''
    for col_num in range(sheet.ncols):
        col_value=sheet.col_values(col_num)
        #print(col_value)
        if(col_value[0]==name):
            duration=col_value[i]
            break
    if(duration=='' or duration=='NA'):
        duration=FAO_duration
    coeff=duration/FAO_duration
    for j in range(0,len(crop_grow)):
        crop_grow[j]=crop_grow[j]*coeff
    
    return crop_grow
def cropCoefficient_calibrate(d,t,kc_crop,name,cwr):
    #district=d
    district=agromap(t,d)
    #district='West part of Ahmadnagar'
    loc='C:/Users/Rishabh/waterbudgeting/Data/Agro_climatic_zone_CWR.xlsx'
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(1)
    i=0
    FAO_cwr=cwr
    for row_num in range(sheet.nrows):
        row_value = sheet.row_values(row_num)
        #print(row_value[0])

        if row_value[0] == district:
            i=row_num
            break
    requirement=''
    for col_num in range(sheet.ncols):
        col_value=sheet.col_values(col_num)
        #print(col_value)
        if(col_value[0]==name):
            col_value=sheet.col_values(col_num+1)
            requirement=col_value[i]
            #print(requirement)
            break
    if(requirement=='' or requirement=='NA'):
        requirement=FAO_cwr
    #print(FAO_cwr)
    coeff=requirement/FAO_cwr
    for j in range(0,len(kc_crop)):
        kc_crop[j]=kc_crop[j]*coeff
    
    return kc_crop
def agromap(t,d):
    if(t=='Chandgad' or t=='Radhanagari'or t=='Bavda'):
        return 'West part of Kolapur'
    elif(t=='Mahad' or t=='Poladpur'):
        return 'Raigad 1'
    elif(t=='Igatpuri' or t=='Trimbakeshwar'):
        return 'Extreme west part of nashik'
    elif(t=='Mahabaleshwar' or t=='Khandala'):
        return 'Hilly satara'
    elif(t=='Mawal' or t=='Mulshi' or t=='Velhe'):
        return 'Extreme west part of Pune'
    elif(d=='Ahmadnagar' and t=='Akola'):
        return 'West part of Ahmadnagar'
    elif(t=='Ajra' or t=='Bhudargad' or t=='Karvir' or t=='Panhala' or t=='Shahuwadi' or t=='Kagal' or t=='Gadhinglaj'):
        return 'Central part of Kolhapur'
    elif(t=='Hatkanangle' or t=='Shirol'):
        return 'North east part of Kolhapur'
    elif(t=='Paranda' or t=='Bhum' or t=='Washi'):
        return 'West part of Osmanabad'
    elif(t=='Akkalkot'):
        return 'East part of Solapur'
    elif(t=='Vaijapur' or t=='Gangapur'):
        return 'West part of Aurangabad'
    elif(t=='Ashti' or t=='Patoda' or t=='Shirur(Kasar)'):
        return 'West part of Beed'
    elif(t=='Sengaon'):
        return 'West part of Hingoli'
    elif(t=='Nanded' or t=='Ardhapur' or t=='Mudkhed' or t=='Umri' or t=='Dharmabad' or t=='Bhokar' or t=='Hadgaon' or t=='Himayatnagar' or t=='Kinwat' or t=='Mahoor'):
        return 'North and east part of Nanded'
    elif(t=='Warora' or t=='Bhadravati' or t=='Chandrapur' or t=='Ballarpur' or t=='Rajura' or t=='Jiwati' or t=='Korpana'):
        return 'West part of Chandrapur'
    else:
        return d
#et=[3.73, 4.74, 5.71, 6.5, 6.46, 5.27, 4.42, 4.06, 4.37, 4.77, 4.15, 3.78]
#cropreq(['Soybean'], ['10-02-2019'], [1],[0],[0],et,'Nashik')

'''
#function to extract ET
#cropreq(crop,sowdates,area_crop,'Kharif','Konambe')

def kc_correction(name,kc_scrop,days_scrop,sow_date):
    loc='C:/Users/Rishabh/waterbudgeting/Data/PadaliHMSfinal.xlsx'
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(1)
    #print('Hello',sheet.cell_value(5,1))
    crop_height={'Rice':0.8,'Maize-sweet':1.5,'Millet':1.5,'Soybean':0.6,'Groundnut':0.4,'Lentils':0.4}
    if(name in crop_height):
        height=crop_height[name]
    else:
        height=0
    date_1 = datetime.datetime.strptime(sow_date, "%d-%m-%y")
    start_date_mid = (date_1 + datetime.timedelta(days=(days_scrop[0]+days_scrop[1]))).timetuple().tm_yday
    start_date_end = (date_1 + datetime.timedelta(days=(days_scrop[0]+days_scrop[1]+days_scrop[2]))).timetuple().tm_yday
    humidity_mid=0
    windspeed_mid=0
    for i in range(start_date_mid+1,start_date_mid+1+(days_scrop[2]*2)):
        #print('excel',sheet.cell_value(i,1))
        windspeed_mid=windspeed_mid+sheet.cell_value(i,2)
        humidity_mid=humidity_mid+sheet.cell_value(i,1)
    humidity_mean_mid=humidity_mid/(days_scrop[2]*2)
    windspeed_mean_mid=windspeed_mid/(days_scrop[2]*2)

    humidity_end=0
    windspeed_end=0
    for i in range(start_date_end+1,start_date_end+1+(days_scrop[3]*2)):
        #print('excel',sheet.cell_value(i,1))
        windspeed_end=windspeed_end+sheet.cell_value(i,2)
        humidity_end=humidity_end+sheet.cell_value(i,1)
    humidity_mean_end=humidity_end/(days_scrop[2]*2)
    windspeed_mean_end=windspeed_end/(days_scrop[2]*2)
    kc_crop=[]
    for i in range(0, len(kc_scrop)):
        if(i==2):
            kc=kc_scrop[i]+(0.04*(windspeed_mean_mid-2)-0.004*(humidity_mean_mid-45))*math.pow(height/3,0.3)
            kc_crop.append(kc)
        elif(i==3):
            kc=kc_scrop[i]+(0.04*(windspeed_mean_end-2)-0.004*(humidity_mean_end-45))*math.pow(height/3,0.3)
            kc_crop.append(kc)
        else:
            kc_crop.append(kc_scrop[i])
    print(kc_crop)

    #print(start_date_mid)

#kc_correction('Maize-sweet',[0.4,0.8,1.15,1],[20,30,50,10],'10-06-20')
'''