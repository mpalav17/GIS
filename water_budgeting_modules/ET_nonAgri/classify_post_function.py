# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:20:27 2020

@author: DELL
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 19:24:10 2020

@author: DELL
"""
def classify(village,rt,clipdata):
    import os
    #os.environ['PROJ_LIB'] = 'C:\\Users\\DELL\\Anaconda3\\Library\\share\\proj'
    import rasterio as r
    import rasterio.plot
    import numpy as np
    
    import rasterio.mask
    import fiona
    import copy
    from shapely.geometry import shape, Point
    import geopandas as gp
    from shapely.geometry import shape, Point
    import geojson
    from rasterio.features import shapes
    
    l=os.listdir(rt)
    print(l)
    b2=r.open(rt+'/'+l[0])
    b3=r.open(rt+'/'+l[1])
    b4=r.open(rt+'/'+l[2])
    b8=r.open(rt+'/'+l[3])
    b11=r.open(rt+'/'+l[4])
    #use reproject code and use output of reproject in the vect variable
    #check the projection of the shapefile. must be EPSG:32643
    
    
    
    vect=village
    #print(vect.crs)
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
    
    clipb2=clip(b2,clipdata+'/b2_clip.tif')
    clipb3=clip(b3,clipdata+'/b3_clip.tif')
    clipb4=clip(b4,clipdata+'/b4_clip.tif')
    clipb8=clip(b8,clipdata+'/b8_clip.tif')
    clipb11=clip(b11,clipdata+'/b11_clip.tif')
    
    #wter
    nb2=r.open(clipdata+'/b2_clip.tif')
    nb3=r.open(clipdata+'/b3_clip.tif')
    nb4=r.open(clipdata+'/b4_clip.tif')
    nb8=r.open(clipdata+'/b8_clip.tif' ) 
    nb11=r.open(clipdata+'/b11_clip.tif' )
    
    n2 = nb2.read(1,masked=True).astype('float32')
    n3 = nb3.read(1).astype('float32')
    n8 = nb8.read(1,masked=True).astype('float32')
    n11 = nb11.read(1,masked=True).astype('float32')
    
    w1 =np.ones_like(n11)
    w2 =np.zeros_like(n3)
    
    
    w=(np.logical_and(n11<0.1,n8<0.1,))
    water =np.where(w,w1,w2)
    #water_class=water.astype('int32')
    water_bodyImage = rasterio.open(clipdata+'/water_body_post_m.tif','w',driver='Gtiff',
                              width=nb3.width, 
                              height = nb3.height, 
                              count=1, crs=nb3.crs, 
                              transform=nb3.transform, 
                              dtype='float32')
    water_bodyImage.write(water,1)
    water_bodyImage.close()
    
    #urban
    urban=copy.copy(n2)
    urban[np.where(n2>0.055)] = 1
    urban[np.where(n2<=0.055)] = 0
    
    
    
    #After clipping(do not clip since you have clipped images. ust input them below.)
    
    
    
    
    
    
    red = nb4.read(1,masked=True).astype('float32')
    nir = nb8.read(1,masked=True).astype('float32')
    
    
    ndvi=(nir-red)/(nir+red)
    ndviImage = rasterio.open(clipdata+'/ndvi.tif','w',driver='Gtiff',
                              width=nb4.width, 
                              height = nb4.height, 
                              count=1, crs=nb4.crs, 
                              transform=nb4.transform, 
                              dtype='float32')
    ndviImage.write(ndvi,1)
    ndviImage.close()
    n=r.open(clipdata+'/ndvi.tif')
    #ndvi_clip=clip(n,'ndvi_clip.tif')
    
    ndvi_rc=copy.copy(ndvi)
    
    ndvi_rc[np.where((ndvi>0.5) & (ndvi<=0.8))] = 2
    ndvi_rc[np.where((ndvi>=-1)&(ndvi<=0.5))] = 1
    ndvi_rc[np.where(ndvi>0.8)] = 3
    ndvi_rc[np.where(water==1)] = 4
    ndvi_rc[np.where(ndvi<-1)]=0
    np.unique(ndvi_rc)
    
    
    u1 =np.ones_like(n3)
    u11=u1*5
    #Final classification
    classes=np.where(urban==1,u11,ndvi_rc)
    
    
    
    np.count_nonzero(classes==4)
    
    Classify = rasterio.open(clipdata+'/classify.tif','w',driver='Gtiff',
                              width=nb4.width, 
                              height = nb4.height, 
                              count=1, crs=nb4.crs, 
                              transform=nb4.transform, 
                              dtype='float32')
    Classify.write(classes,1)
    Classify.close()

#classify('D:/Boond/Data/Drainage/Nashik (2)/Kirtangali/kirtangali_pcs.shp','D:/Boond/Data/Drainage/Nashik (2)/Kirtangali/rt_kirtan','D:/Boond/Data/Drainage/Nashik (2)/Kirtangali/clip_kirtan')
classify('C:/Users/Rishabh/waterbudgeting/Konambe/Konambe_village.shp','C:/Users/Rishabh/waterbudgeting/Konambe','C:/Users/Rishabh/waterbudgeting/Konambe/')
