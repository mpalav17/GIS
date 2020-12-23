#work pending
#Extract the runoff coeff from the excel sheet

import os
import numpy as np
import copy
import elevation
import richdem as rd
import xlrd
def runoff(village_name):
    coeff1=0
    coeff2=0
    coeff3=0
    coeff=[]
    
    if(village_name=='Konambe'):
        dem_path=os.path.join('C:/Users/Rishabh/waterbudgeting/Data/Konambe_dem_clipped.tif')
        rainfall=780
        coeff=getCoeff(rainfall)
        coeff1=coeff[0]
        coeff2=coeff[2]
        coeff3=coeff[1]
    elif(village_name=='Shastrinagar'):
        return 299,240   #runoff considered earlier was 299, 674 when rainfall is 1031mm
    elif(village_name=='Watershed'):
        dem_path=os.path.join(os.getcwd(),'Watershed_dem_fill/dem_1.tif')
        coeff1=0.6543#1.0791
        coeff2=0.9814#1.6186
        coeff3=1.3086#2.1583
    elif(village_name=='Kanhur'):
        dem_path=os.path.join(os.getcwd(),'Kanhur_dem_fill/Kanhur_dem_fill.tif')
        rainfall=550
        coeff=getCoeff(rainfall)
        coeff1=coeff[0]
        coeff2=coeff[2]
        coeff3=coeff[1]
    elif(village_name=='Kirtangali'):
        dem_path=os.path.join(os.getcwd(),'Kirtangali_dem/Kirtangali_dem_fill.tif')
        rainfall=718
        coeff=getCoeff(rainfall)
        coeff1=coeff[0]
        coeff2=coeff[2]
        coeff3=coeff[1]
    
    village_dem=rd.LoadGDAL(dem_path,no_data=-9999)
    rd.FillDepressions(village_dem, epsilon=False, in_place=False)
    arr=rd.TerrainAttribute(village_dem,attrib='slope_percentage',zscale=1/111120)
    np.save('out.npy', arr)
    demnp=np.load('out.npy')
    dem=copy.copy(arr)
    dem[np.where((arr>0) & (arr<5))] = 1
    dem[np.where((arr>=5) & (arr<20))] = 2
    dem[np.where((arr>=20))] = 3

    c1=np.count_nonzero(dem==1)
    c2=np.count_nonzero(dem==2)
    c3=np.count_nonzero(dem==3)

    area_m2_1=c1*900
    area_m2_2=c2*900
    area_m2_3=c3*900
    area_ha1=area_m2_1*0.0001
    area_ha2=area_m2_2*0.0001
    area_ha3=area_m2_3*0.0001
    print('area',area_ha1+area_ha2+area_ha3)
    worthy_area=area_ha1+area_ha2
    runoff1=area_ha1*coeff1
    runoff2=area_ha2*coeff2
    runoff3=area_ha3*coeff3

    tot_runoff=runoff1+runoff2+runoff3
    print(tot_runoff)
    return tot_runoff,worthy_area


def getCoeff(rainfall):
    loc='C:/Users/Rishabh/waterbudgeting/Data/Stenges_Table.xlsx'#number of rainy
    wb = xlrd.open_workbook(loc)
    j=0
    coeff=[]
    while(j<3):
        sheet = wb.sheet_by_index(j)
        minimum=abs(rainfall-sheet.cell_value(4,1))
        i=4
        temp=i
        while(i<48):
            m=abs(rainfall-sheet.cell_value(i,1))
            if(m<=minimum):
                minimum=m
                temp=i
            i=i+1
        coeff.append(sheet.cell_value(temp,5))
        j=j+1
    return coeff

#runoff('Kirtangali')