import os
import pandas as pd
import waterbudgeting as wb
def enter_primary_Details():#field worker function
    print()
    parent_dir="C:/Users/Rishabh/waterbudgeting/"
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
    
    

    print()
    print("Enter the domestic details")
    human_pop=int(input("Enter the population of villagers"))
    cattle_pop=int(input("Enter the cattle population"))
    sheep_pop=int(input("Enter the sheep/goats population"))
    poultry_pop=int(input("Enter the poultry population"))
    dict_pop={'Human pop':human_pop,'cattle pop':cattle_pop,'sheep pop':sheep_pop,'poultry pop':poultry_pop}
    df=pd.DataFrame(dict_pop,index=[0])
    df.to_csv(r'C:/Users/Rishabh/waterbudgeting/'+directory+'/'+village_name+'_primary.csv',index=False)

    print()
    print("Enter the cropping details")
    print("Enter kharif crops detais")
    crop_kharif=[]
    sow_kharif=[]
    area_kharif=[]
    while(True):
        crop_kharif.append(input('Enter crop name : '))
        sow_kharif.append(input('Enter sow date : '))
        area_kharif.append(int(input('Enter area grown :')))
        a=input("Enter 1 to continue")
        if(int(a)!=1):
            break
    dict_kharif={'Kharif crop':crop_kharif,'Sow date':sow_kharif,'Area':area_kharif}
 
    df=pd.DataFrame(dict_kharif)
    df.to_csv(r'C:/Users/Rishabh/waterbudgeting/'+directory+'/'+'Kharif_crops.csv',index=False)
    print()
    print("Enter rabi crops detais")
    crop_rabi=[]
    sow_rabi=[]
    area_rabi=[]
    while(True):
        crop_rabi.append(input('Enter crop name : '))
        sow_rabi.append(input('Enter sow date : '))
        area_rabi.append(int(input('Enter area grown :')))
        a=input("Enter 1 to continue")
        if(int(a)!=1):
            break
    dict_rabi={'Rabi crop':crop_rabi,'Sow date':sow_rabi,'Area':area_rabi}
    df=pd.DataFrame(dict_rabi)
    df.to_csv(r'C:/Users/Rishabh/waterbudgeting/'+directory+'/'+'Rabi_crops.csv',index=False)

    print()
    
    print("Enter the water conservation structures details")
    i=0
    name=[]
    depth=[]
    area=[]
    storage_cap=[]
    number_struct=[]
    while(True):

        name.append(input("Enter the name of the water conservation structure"))
        if(name[i]=='CCT'):
            number_struct.append(int(input("Enter running meter of CCT")))
            width=0.5#in m
            depth.append(fetch_depth(name[i]))
            storage_cap.append(width*depth[i]*number_struct[i])
            area.append(width*depth[i])
        else:
            number_struct.append(int(input("Enter number of structure")))
            coordinates=fetch_loc(name[i])
            storage_cap.append(float(input("Enter the capacity")))
            depth.append(float(input("Enter the depth")))
            area.append(storage_cap[i]/depth[i])#temporary function
                
        #area.append(ind.extent_of_water_area(coordinates[0],coordinates[1]))
        #storage_cap.append(area[i]*depth[i]/1000)
        #print(area[i])
        #print("Storage of the single structure ", name[i], " is ",storage_cap[i],"TCM")
        b1=input("Press 1 to continue")
        i=i+1
        if(int(b1)!=1):
            break
    dict_struct={'Structure name':name,'Area':area,'Storage capacity':storage_cap,'Number':number_struct}
    df=pd.DataFrame(dict_struct)
    df.to_csv(r'C:/Users/Rishabh/waterbudgeting/'+directory+'/'+'WCS_details.csv',index=False)

    print()
    print("Enter the village farm ponds details")
    number_lined=int(input("Enter the number of lined farm ponds in the village"))
    avg_area_lined=int(input("Enter the average area of the lined farm ponds"))
    depth_farmpond=3#depth of the farm pond is considered to be 1m
    storage_farmpondlined=avg_area_lined*depth_farmpond/1000
    dict_farml={'Lined farm pond':number_lined,'Area':avg_area_lined,'Capacity':storage_farmpondlined}
    df=pd.DataFrame(dict_farml,index=[0])
    df.to_csv(r'C:/Users/Rishabh/waterbudgeting/'+directory+'/'+'farmponds_lined.csv',index=False)
    print()
    depth_farmpond_unlined=3#depth of the farm pond is considered to be 2 m
    number=int(input("Enter the number of non lined farm ponds in the village"))
    
    avg_area=int(input("Enter the average area of the non lined farm ponds"))
    storage_farmpond=avg_area*depth_farmpond_unlined/1000

    dict_farm={'Non Lined farm pond':number,'Area':avg_area,'Capacity':storage_farmpond}
    df=pd.DataFrame(dict_farm,index=[0])
    df.to_csv(r'C:/Users/Rishabh/waterbudgeting/'+directory+'/'+'farmponds.csv',index=False)

    print()
    c=input("Do you want to see the water budget")
    if(c=='y' or c=='Y'):
        wb.show_water_budget(district_name,tehsil_name,village_name)
    else:
        print("Thank you for entering in the details")

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
