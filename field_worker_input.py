import os
import pandas as pd
import waterbudgeting as wb
import xlrd
def enter_primary_Details():#field worker function
    print()
    parent_dir="C:/Users/Rishabh/waterbudgeting/Data"
    print("Basic village details")
    district_name=input("Enter the district name")
    directory=district_name
    path = parent_dir+directory
    os.mkdir(path)
    tehsil_name=input("Enter the tehsii name")
    directory=directory+"/"+tehsil_name
    path = parent_dir+directory
    os.mkdir(path)
    village_name=input("Enter the village name")
    directory=directory+"/"+village_name
    path = parent_dir+directory
    os.mkdir(path)
    station_name=input_station_name(parent_dir,district_name,tehsil_name,village_name)
    input_primary_details(directory,district_name,tehsil_name,village_name,station_name)
    input_gwlevel(directory,district_name,tehsil_name,village_name)
    input_cropdetails(directory,district_name,tehsil_name,village_name,'Kharif')
    input_cropdetails(directory,district_name,tehsil_name,village_name,'Rabi')
    input_cropdetails(directory,district_name,tehsil_name,village_name,'Annual')
    input_cropdetails(directory,district_name,tehsil_name,village_name,'Summer')
    input_structuredetails(directory,district_name,tehsil_name,village_name)
    input_farmponds(directory,district_name,tehsil_name,village_name,'Lined')
    input_farmponds(directory,district_name,tehsil_name,village_name,'Non Lined')

def input_station_name(parent_dir,district_name,tehsil_name,village_name):
    current_year='2019'
    print('Groundwater level trend station name')
    #Observation well station name
    loc=parent_dir+'/Groundwater_level_data'+'/'+current_year+'_groundwater_post.xls'
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(1)
    tehsil=tehsil_name.upper()
    for i in range(sheet.nrows):
        if(sheet.cell_value(i,3)==tehsil):
            print(sheet.cell_value(i,4))
    print('Choose a station nearby to the village')
    station_name=input("Enter the station name")
    return station_name
def input_primary_details(directory,district_name,tehsil_name,village_name,station_name):
    print()
    print("Enter the domestic details")
    human_pop=int(input("Enter the population of villagers"))
    cattle_pop=int(input("Enter the cattle population"))
    sheep_pop=int(input("Enter the sheep/goats population"))
    poultry_pop=int(input("Enter the poultry population"))
    dict_pop={'Human pop':human_pop,'cattle pop':cattle_pop,'sheep pop':sheep_pop,'poultry pop':poultry_pop,'Station name':station_name}
    df=pd.DataFrame(dict_pop,index=[0])
    df.to_csv(r'C:/Users/Rishabh/waterbudgeting/Data'+directory+'/'+village_name+'_primary.csv',index=False)
    print()
def input_gwlevel(directory,district_name,tehsil_name,village_name):
    print('Enter the groundwater level data for this year')
    pre_mon=float(input("Enter the premonsoon water level"))
    post_mon=float(input("Enter the postmonsoon water level"))
    dict_well_water={'post monsoon level':post_mon,'pre monsoon level':pre_mon}
    df=pd.DataFrame(dict_well_water,index=[0])
    df.to_csv(r'C:/Users/Rishabh/waterbudgeting/Data'+directory+'/'+village_name+'_well_water.csv',index=False)
def input_cropdetails(directory,district_name,tehsil_name,village_name,season): 
    print()
    print("Enter the cropping details")
    print("Enter crops detais ",season)
    crop_kharif=[]
    sow_kharif=[]
    area_kharif=[]
    drip=[]
    while(True):
        crop_kharif.append(input('Enter crop name : '))
        sow_kharif.append(input('Enter sow date : '))
        area_kharif.append(int(input('Enter area grown :')))
        drip.append(int(input('Enter area under drip for that crop :')))
        a=input("Enter 1 to continue")
        if(int(a)!=1):
            break
    dict_kharif={season+' crop':crop_kharif,'Sow date':sow_kharif,'Area':area_kharif,'drip':drip}
    df=pd.DataFrame(dict_kharif)
    df.to_csv(r'C:/Users/Rishabh/waterbudgeting/Data'+directory+'/'+season+'_crops.csv',index=False)
    print()
def input_structuredetails(directory,district_name,tehsil_name,village_name):
    print("Enter the water conservation structures details")
    i=0
    name=[]
    depth=[]
    area=[]
    storage_cap=[]
    number_struct=[]
    total_area=[]
    while(True):
        name.append(input("Enter the name of the water conservation structure"))
        if(name[i]=='CCT'):
            number_struct.append(int(input("Enter running meter of CCT")))
            total_area.append(int(input("Enter total area covered by CCT in hectares")))
            width=0.5#in m
            depth.append(fetch_depth(name[i]))
            storage_cap.append(width*depth[i]*number_struct[i])
            area.append(width*depth[i])
        else:
            number_struct.append(int(input("Enter number of structure")))
            #coordinates=fetch_loc(name[i])
            length=float(input('Enter the length in meters'))
            breadth=float(input('Enter the breadth in meters'))
            depthvalue=float(input('Enter the depth in meteres'))
            storage_cap.append(length*breadth*depthvalue)
            depth.append(depthvalue)
            area.append(length*breadth)#temporary function
        b1=input("Press 1 to continue")
        i=i+1
        if(int(b1)!=1):
            break
    dict_struct={'Structure name':name,'Area':area,'Storage capacity':storage_cap,'Number':number_struct,'Total area':total_area}
    df=pd.DataFrame(dict_struct)
    df.to_csv(r'C:/Users/Rishabh/waterbudgeting/Data'+directory+'/'+'WCS_details.csv',index=False)

def input_farmponds(directory,district_name,tehsil_name,village_name,typepond):
    print()
    print("Enter the village farm ponds details ",typepond)
    number_lined=int(input("Enter the number of  ponds in the village"))
    avg_area_lined=int(input("Enter the average area of the  ponds"))
    depth_farmpond=3#depth of the farm pond is considered to be 1m
    storage_farmpondlined=avg_area_lined*depth_farmpond/1000
    dict_farml={typepond+' farm pond':number_lined,'Area':avg_area_lined,'Capacity':storage_farmpondlined}
    df=pd.DataFrame(dict_farml,index=[0])
    df.to_csv(r'C:/Users/Rishabh/waterbudgeting/Data'+directory+'/'+'farmponds_'+typepond+'.csv',index=False)
    print()

def fetch_depth(name):
    n=['Earthen nala bund','K T weir','Cement nala bund','Cement nala bund forest','Percolation tank','Percolation tank forest','Gabion','Recharge shaft','CCT','Konambe dam']
    i=n.index(name)
    depth=[2,2,1,1,3,3,1,1,0.6,11.11]
    return depth[i]

def fetch_loc(name):
    lat=73.95
    lon=19.18
    return [lat, lon]
def getStorageTemp(name):
    n=['Earthen nala bund','K T weir','Cement nala bund','Cement nala bund forest','Percolation tank','Percolation tank forest','Gabion','Recharge shaft','Konambe dam']
    cap=[0.467,1.05,13.045,7.88,25.15,3.88,.345,1,1512]#in TCM,here for recharge shaft the avg tcm has been taken from doc given by deshpande sir+
    i=n.index(name)
    return cap[i]
'''
def getAreaTemp(name):
    n=['Earthen nala bund','K T weir','Cement nala bund','Percolation tank','Percolation tank new']
    area=[155.55,700,3487.5,12575,4800]#in m2
    
    i=n.index(name)
    return area[i]
'''
