import xlrd
import math
#Future work
#Monthly calculation of seepage and evaporation
def storage_tanks(storage,area):#village unlinedfarm ponds
    water_area=0.6*area
    days_monsoon=90
    days_nonmon=120
    #evaporation_monsoon=(water_area*1900/1000)/1000
    infilteration=(water_area*days_monsoon*1.44/1000)/1000#seepage during monsoon
    infilteration_nonmon=(water_area*days_nonmon*1.44/1000)/1000
    surface_water=storage-(infilteration)
    return infilteration,surface_water,infilteration_nonmon
def KT_weir(storage,area):# K T weir
    water_area=0.6*area
    days_monsoon=90
    days_nonmon=120
    infilteration=(water_area*days_monsoon*1.44/1000)#seepage during monsoon
    #evaporation_monsoon=(water_area*1900/1000)#evaporation during monsoon considered as 1.44mm/day
    infilteration_nonmon=(water_area*days_nonmon*1.44/1000)
    surface_water=storage-(infilteration)#surface water available after monsoon
    return infilteration,surface_water,infilteration_nonmon
def dam(storage,area):# minor irrigation project
    water_area=0.6*area*2
    days_monsoon=90
    days_nonmon=275
    infilteration=(water_area*days_monsoon*1.44/1000)#seepage during monsoon
    infilteration_nonmon=(water_area*days_nonmon*1.44/1000)#seepage during monsoon
    #evaporation_monsoon=(water_area*1900/1000)#evaporation during monsoon considered as 1.44mm/day
    average_land=1.34
    water_req=1#1000 mm
    people_entitled=43
    surface_water=average_land*water_req*people_entitled*10
    return infilteration,surface_water,infilteration_nonmon

def WCS(storage):#for ENB, CNB, percolation tanks, Gabion and Recharge shaft
    fillings=2
    infilteration=fillings*storage*.5
    return infilteration
def CCT(storage,length,area):
    loc='C:/Users/Rishabh/waterbudgeting/Data/Stenges_Table.xlsx'#number of rainy
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    rainfall=621#need to automate this
    area_cover=80#need to automate this as well
    minimum=abs(rainfall-sheet.cell_value(4,1))
    i=4
    temp=i
    while(i<48):
        m=abs(rainfall-sheet.cell_value(i,1))
        if(m<=minimum):
            minimum=m
            temp=i
        i=i+1
    coeff=sheet.cell_value(temp,5)
    runoff=coeff*rainfall*area_cover*10
    fillings=runoff/(area*length)
    infilteration=fillings*storage*0.1/1000
    soil_mois=fillings*storage*0.55/1000#10% seepage,35% evaporation rest soil moisture
    print('My fill',fillings)
    return infilteration,soil_mois
def shaft(storage):
    #fillings =70#number of rainy
    infilteration=storage*0.8
    return infilteration
    

#def farm_pondsstorage()
