#Pending work in the water extent function

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 20:15:10 2020

@author: DELL
"""

import rasterio as r
import rasterio.plot
import numpy as np
#import matplotlib.pyplot as plt
import os
from rasterio import plot
import rasterio.mask
import fiona
import copy

from rasterio.features import shapes
import geopandas as gpd
from geojson import FeatureCollection
#import geopandas.clip

#Required when I have the full image
l=os.listdir()
print(l)
b3=r.open(l[4])
b4=r.open(l[5])
b8=r.open(l[6])
b11=r.open(l[3])
#use reproject code and use output of reproject in the vect variable
#check the projection of the shapefile. must be EPSG:32643
#lat=input("Enter the latitude of the WCS")
#lon=input("Enter the longitude of the WCS")
shp=gpd.read_file('C:/Users/Rishabh/waterbudgeting/Data/Konambe/Konambe_village.shp')
vector1= fiona.open('C:/Users/Rishabh/waterbudgeting/Data/Konambe/Konambe_village.shp',mode='r')
vect=shp.to_crs({'init': 'epsg:32643'})
#vector1.to_file('C:/Users/risha/waterbudgeting/Konambe/Konambe_village_vector.shp')

#print(vector1.crs)
def clip(raster,out):
    

    img = raster
    vector= fiona.open(vect,mode='r')
    geom = [feature["geometry"] for feature in vector]
    oimg, otns = rasterio.mask.mask(img,geom, crop=True)
    ometa = img.meta
    ometa.update({"driver": "GTiff",
                 "height": oimg.shape[1],
                 "width": oimg.shape[2],
                 "transform": otns})
    with rasterio.open(out, "w", **ometa) as dest:
        dest.write(oimg)
    return(r.open(out))


#clipb3=clip(b3,'b3_clip.tif')
#clipb4=clip(b4,'b4_clip.tif')
#clipb8=clip(b8,'b8_clip.tif')
#clipb11=clip(b11,'b11_clip.tif')

#After clipping(do not clip since you have clipped images. ust input them below.)

def Evapotranspiration():

    
    clipb4=r.open('b4_clip.tif')
    clipb8=r.open('b8_clip.tif' )  





    red = clipb4.read(1).astype('float32')
    nir = clipb8.read(1).astype('float32')


    ndvi=(nir-red)/(nir+red)



    ndviImage = rasterio.open('C:/Users/Rishabh/waterbudgeting/Data/ndvi.tif','w',driver='Gtiff',
                              width=clipb4.width, 
                              height = clipb4.height, 
                              count=1, crs=clipb4.crs, 
                              transform=clipb4.transform, 
                              dtype='float32')
    ndviImage.write(ndvi,1)
    ndviImage.close()
    n=r.open('C:/Users/Rishabh/waterbudgeting/Data/ndvi.tif')
    #ndvi_clip=clip(n,'ndvi_clip.tif')

    ndvi_rc=copy.copy(ndvi)
    ndvi_rc[np.where((ndvi>0.1) & (ndvi<=0.75))] = 2
    ndvi_rc[np.where(ndvi<=0.1)] = 1


    ndvi_rc[np.where(ndvi>0.75)] = 3
    np.unique(ndvi_rc)
    barren=np.count_nonzero(ndvi_rc==1)
    #print('barren',barren*100)
    #barren_et=((barren*100)-5883000)*0.05
    #barren_et=3040000*0.1#kirtangali
    barren_et=4170000*0.1#kirtangali updated as per my code
    #barren_et=12598100*0.05#konambe
    #barren_et=2700000*0.05#kanhur
    #barren_et=400000*0.05#Shastrinagar
    shrubs=np.count_nonzero(ndvi_rc==2)
    #print('shrubs',shrubs*100)
    #shrubs_et=shrubs*100*0.2
    #shrubs_et=210000*0.4#kirthangali
    shrubs_et=500000*0.4#kirthangali updated as per my code
    #shrubs_et=4642200*0.4#0.2konambe and 0.4 for surplus year
    #shrubs_et=5200000*0.4#kanhur
    #shrubs_et=300000*0.4#Shastrinagar
    forest=np.count_nonzero(ndvi_rc==3)
    #forest_et=forest*100*0.8
    #forest_et=354500*0.8#Kirtangali
    forest_et=500000*0.8#Kirtangali updated as per my code
    #forest_et=295200*0.8#Konambe
    #forest_et=224000*0.8#Kanhur
    #forest_et=0*0.8#Shastrinagar
    #print('forest',forest*100)
    et=[barren_et,shrubs_et,forest_et] #et in m^3
    return et  



#Pending work
#Extract the geo-tagged structure list from JYS database
#Extract lat, long and capacity of these structure.
#Verify whether at these lat long water body is being detected.
#If yes then return the extent of water body area else return the capacity as
#obtained from JYS database
def extent_of_water_area(latcoordinate, longcoordinates):

    clipb3=r.open('b3_clip.tif')
    clipb8=r.open('b8_clip.tif' ) 
    clipb11=r.open('b11_clip.tif' )

    n3 = clipb3.read(1).astype('float32')
    n8 = clipb8.read(1).astype('float32')
    n11 = clipb11.read(1).astype('float32')


    #ndbi=(n11-n8)/(n11+n8)
    #ndwi=(n3-n8)/(n3+n8)

    #w1 =np.ones_like(ndbi)
    #w2 =np.zeros_like(ndbi)
    w1 =np.ones_like(n11)
    w2 =np.zeros_like(n11)


    w=(np.logical_and(n11<0.1,n8<0.1))

    #w=(np.logical_and(ndbi<0,ndwi>0))
    water =np.where(w,w1,w2)
    water_body=np.count_nonzero(water==1)
    water_area=water_body*100 #water area
    print(water_area)
    water_bodyImage = rasterio.open('C:/Users/Rishabh/waterbudgeting/Data/water_body.tif','w',driver='Gtiff',
                              width=clipb3.width, 
                              height = clipb3.height, 
                              count=1, crs=clipb3.crs, 
                              transform=clipb3.transform, 
                              dtype='float32')
    water_bodyImage.write(water,1)
    water_bodyImage.close()
    loc='C:/Users/Rishabh/waterbudgeting/Data/water_body.tif'
    import waterbodylocation as wbl
    water_area=wbl.pointArea(latcoordinate,longcoordinates,loc)
    
    return water_area


#et=Evapotranspiration()
#print("Total water lost in barren is ", et[0],'m3') 
#print("Total water lost in shrubs is ", et[1],'m3') 
#print("Total water lost in forest is ", et[2],'m3') 
#lat=386003
#lon=2186809
#area=extent_of_water_area(lat,lon)
#print(area)

#et=Evapotranspiration()













