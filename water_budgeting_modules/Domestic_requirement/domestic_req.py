import os
import pandas as pd
def getDomestic(village, taluka, district):
    print("Amount of water for domestic details")
    parent_dir="C:/Users/Rishabh/waterbudgeting/Data/"
    home_dir=parent_dir+district+"/"+taluka+"/"+village+"/"
    df=pd.read_csv(home_dir+village+"_primary.csv")
    details=[df['Human pop'][0],df['cattle pop'][0],df['sheep pop'][0],df['poultry pop'][0]]
    dom_req=getDomesticdetails(details)
    dom_req_kharif=getDomesticKharif(details)
    temp=['Human population','Cattle population','Sheep population','Poultry population']
    sum_domreq=0
    sum_domkharif=0
    for i in range(0,len(details)):
        print("The Total annual water requriement for ",details[i]," "+temp[i]+" is "+str(dom_req[i])+" TCM")
        sum_domreq=sum_domreq+dom_req[i]
        sum_domkharif=sum_domkharif+dom_req_kharif[i]
    return [sum_domreq,sum_domkharif]


def getDomesticdetails(d):
    tot_Domestic=[]
    tot_Domestic.append(d[0]*55*365/1000000)
    tot_Domestic.append(d[1]*35*365/1000000)
    tot_Domestic.append(d[2]*5*365/1000000)
    tot_Domestic.append(d[3]*2*365/1000000)
    return tot_Domestic
def getDomesticKharif(d):
    tot_Domestic=[]
    tot_Domestic.append(d[0]*55*122/1000000)
    tot_Domestic.append(d[1]*35*122/1000000)
    tot_Domestic.append(d[2]*5*122/1000000)
    tot_Domestic.append(d[3]*2*122/1000000)
    return tot_Domestic