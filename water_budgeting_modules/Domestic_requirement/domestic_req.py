import os
import pandas as pd
import mysql.connector
import re
mydb = mysql.connector.connect(
    host = "localhost",
    database = "boondv1",
    user = "root",
    password = "root"
)
def getDomestic(village, taluka, district,village_code):
    print("Amount of water for domestic details")
    parent_dir="C:/Users/Rishabh/waterbudgeting/Data/"
    home_dir=parent_dir+district+"/"+taluka+"/"+village+"/"
    df=pd.read_csv(home_dir+village+"_primary.csv")

    mycursor = mydb.cursor()
    mycursor.execute("select human_popu, cattle_popu, sheep_popu, poultry_popu, human_req, cattle_req, sheep_req, poultry_req from domestic_details where village_code = '"+str(village_code)+"'")
    res = mycursor.fetchall()
    for hp,cp,sp,pp,hr,cr,sr,pr in res:
        hp = res[0][0]
        cp = res[0][1]
        sp = res[0][2]
        pp = res[0][3]
        hr = res[0][4]
        cr = res[0][5]
        sr = res[0][6]
        pr = res[0][7]

    # details=[df['Human pop'][0],df['cattle pop'][0],df['sheep pop'][0],df['poultry pop'][0]]    #?
    details=[hp,cp,sp,pp]
    requirement=[hr,cr,sr,pr]
    dom_req=getDomesticdetails(details,requirement)
    dom_req_kharif=getDomesticKharif(details,requirement)
    temp=['Human population','Cattle population','Sheep population','Poultry population']
    sum_domreq=0
    sum_domkharif=0
    for i in range(0,len(details)):
        print("The Total annual water requriement for ",details[i]," "+temp[i]+" is "+str(dom_req[i])+" TCM")
        sum_domreq=sum_domreq+dom_req[i]
        sum_domkharif=sum_domkharif+dom_req_kharif[i]
    mycursor = mydb.cursor()
    mycursor.execute("select * from domestic_details_res where village_code="+str(village_code)+";")
    res = mycursor.fetchall()
    if res:
        print("hello")
        mycursor.execute("update domestic_details_res set db_sum_domreq="+str(sum_domreq)+",db_sum_domkharif="+str(sum_domkharif)+",db_human_req="+str(dom_req[0])+",db_cattle_req="+str(dom_req[1])+",db_sheep_req="+str(dom_req[2])+",db_poultry_req="+str(dom_req[3])+" where village_code="+str(village_code)+";")
    else:
        #print("hello")
        mycursor.execute("insert into domestic_details_res values("+str(village_code)+","+str(sum_domreq)+","+str(sum_domkharif)+","+str(dom_req[0])+","+str(dom_req[1])+","+str(dom_req[2])+","+str(dom_req[3])+");")
    # print("update domestic_details_res set db_sum_domreq="+str(sum_domreq)+",db_sum_domkharif="+str(sum_domkharif)+",db_human_req="+str(dom_req[0])+",db_cattle_req="+str(dom_req[1])+",db_sheep_req="+str(dom_req[2])+",db_poultry_req="+str(dom_req[3])+" where village_code="+str(village_code)+";")
    
    #mycursor.execute("insert into domestic_details_res values("+str(village_code)+","+str(sum_domreq)+","+str(sum_domkharif)+","+str(dom_req[0])+","+str(dom_req[1])+","+str(dom_req[2])+","+str(dom_req[3])+");")
    mydb.commit()
    return [sum_domreq,sum_domkharif]


def getDomesticdetails(d,r):
    tot_Domestic=[]
    tot_Domestic.append(d[0]*r[0]*365/1000000)
    tot_Domestic.append(d[1]*r[1]*365/1000000)
    tot_Domestic.append(d[2]*r[2]*365/1000000)
    tot_Domestic.append(d[3]*r[3]*365/1000000)
    return tot_Domestic
def getDomesticKharif(d,r):
    tot_Domestic=[]
    tot_Domestic.append(d[0]*r[0]*122/1000000)
    tot_Domestic.append(d[1]*r[1]*122/1000000)
    tot_Domestic.append(d[2]*r[2]*122/1000000)
    tot_Domestic.append(d[3]*r[3]*122/1000000)
    return tot_Domestic
