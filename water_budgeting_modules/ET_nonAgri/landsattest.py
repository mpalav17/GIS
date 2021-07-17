import ee
import geemap
import numpy as np
import rasterio as r
import copy
import pandas as pd
import matplotlib.pyplot as plt


def toImage(lats,lons,data):
 
    # get the unique coordinates
    uniqueLats = np.unique(lats)
    uniqueLons = np.unique(lons)
 
    # get number of columns and rows from coordinates
    ncols = len(uniqueLons)
    nrows = len(uniqueLats)
 
    # determine pixelsizes
    ys = uniqueLats[1] - uniqueLats[0]
    xs = uniqueLons[1] - uniqueLons[0]
 
    # create an array with dimensions of image
    arr = np.zeros([nrows, ncols], np.float32) #-9999
 
    # fill the array with values
    counter =0
    for y in range(0,len(arr),1):
        for x in range(0,len(arr[0]),1):
            if lats[counter] == uniqueLats[y] and lons[counter] == uniqueLons[x] and counter < len(lats)-1:
                counter+=1
                arr[len(uniqueLats)-1-y,x] = data[counter] # we start from lower left corner
    return arr


def anyFunction(img):
    ndvi = ee.Image(img.normalizedDifference(['B8', 'B4'])).rename(["ndvi"])
    return ndvi
def waterFunction(img):
    ndwi_image = img.normalizedDifference(['B3', 'B8'])
    water_image = ee.Image(ndwi_image.gt(0.001)).rename(["ndwi"])
    return water_image
def LatLonImg(img,shapefile):
    img = img.addBands(ee.Image.pixelLonLat())
 
    img = img.reduceRegion(reducer=ee.Reducer.toList(),
                                        geometry=shapefile,
                                        maxPixels=1e13,
                                        scale=10)
 
    data = np.array((ee.Array(img.get("result")).getInfo()))
    lats = np.array((ee.Array(img.get("latitude")).getInfo()))
    lons = np.array((ee.Array(img.get("longitude")).getInfo()))
    return lats, lons, data
def landclassify(v,t,d):
    service_account = 'remote-sensing-midas@midas-water-accounting.iam.gserviceaccount.com'
    credentials = ee.ServiceAccountCredentials(service_account, 'privatekey.json')
    ee.Initialize(credentials)
    import_file = 'C:/Users/Rishabh/waterbudgeting/Data/'+d+'/'+t+'/'+v+'/shapefile/'+v+'.shp'
    shapefile = geemap.shp_to_ee(import_file)
    collection = (ee.ImageCollection('COPERNICUS/S2_SR') \
                        .filterBounds(shapefile) \
                        .filterDate(ee.Date('2020-11-01'), ee.Date('2020-11-30')) \
                        .select(['B2','B3','B4','B8','B11']))

    b2 = (collection.select('B2'))
    b3 = (collection.select('B3'))
    b4 = (collection.select('B4'))
    b8 = (collection.select('B8'))
    b11 =(collection.select('B11'))
    result2 = ee.Image(b2.median()).rename(['result'])
    result3 = ee.Image(b3.median()).rename(['result'])
    result4 = ee.Image(b4.median()).rename(['result'])
    result8 = ee.Image(b8.median()).rename(['result'])
    result11 = ee.Image(b11.median()).rename(['result'])
    lat, lon, data2 = LatLonImg(result2,shapefile)
    lat, lon, data3 = LatLonImg(result3,shapefile)
    lat, lon, data4 = LatLonImg(result4,shapefile)
    lat, lon, data8 = LatLonImg(result8,shapefile)
    lat, lon, data11 = LatLonImg(result11,shapefile)
    w1 =np.ones_like(data11)
    w2 =np.zeros_like(data3)
    #print('hello2',data2)
    #print('hello8',data8)
    #print('hello11',data11)
    w=(np.logical_and(data11<0.1,data8<0.1,))
    ndwi_collection=collection.map(waterFunction)
    result_ndwi=ee.Image(ndwi_collection.median()).rename(['result'])
    lat, lon, data_ndwi = LatLonImg(result_ndwi,shapefile)
    #print('ndwi',data_ndwi)
    #print('max ndwi',np.amax(data_ndwi))
    water =np.where(data_ndwi>0.5,w1,w2)
    #print('ndwi water',np.count_nonzero(water==1)*100)
    urban=copy.copy(data_ndwi)
    urban[np.where((data_ndwi>0) & (data_ndwi<=0.2))] = 1
    urban[np.where(data_ndwi>0.2)] = 0

    ndvicollection=collection.map(anyFunction)
    result_ndvi=ee.Image(ndvicollection.median()).rename(['result'])
    lat, lon, data_ndvi = LatLonImg(result_ndvi,shapefile)
    data_ndvi=data_ndvi
    #print('hellondvi',data_ndvi)
    #print('maxndvi',np.amax(data_ndvi))
    ndvi_rc=copy.copy(data_ndvi)

    ndvi_rc[np.where((data_ndvi>0.3) & (data_ndvi<=0.8))] = 2
    ndvi_rc[np.where((data_ndvi>0.055)&(data_ndvi<=0.3))] = 1
    ndvi_rc[np.where(data_ndvi>0.8)] = 3
    ndvi_rc[np.where((data_ndvi>=-1) & (data_ndvi<=0.055))]=5
    ndvi_rc[np.where(water==1)] = 4
    ndvi_rc[np.where(data_ndvi<-1)]=0
    np.unique(ndvi_rc)
    print(ndvi_rc)
    u1 =np.ones_like(data3)
    u11=u1*5
    image  = toImage(lat,lon,ndvi_rc)
    classes=ndvi_rc#np.where(urban==1,u11,ndvi_rc)
    np.count_nonzero(classes==4)
    habitation=np.count_nonzero(classes==5)*100
    barren=np.count_nonzero(classes==1)*100
    shrubs=np.count_nonzero(classes==2)*100
    dense_vegetation=np.count_nonzero(classes==3)*100
    water_bodies=np.count_nonzero(classes==4)*100
    #plt.imshow(image)
    #plt.show()
    #fig,ax = plt.subplots()
    #fig.savefig('LULC wadner.jpg',format='jpeg',dpi=100,bbox_inches='tight')
    color_map = {1: np.array([165, 42, 42]), # brown
             2: np.array([144, 238, 144]), # light green
             3: np.array([34, 139, 34]),# dark green
             4: np.array([0,0,255]),# blue
             5: np.array([255,0,0]),# red
             0: np.array([255,255,255])}# white 
    data=image
    data_3d = np.ndarray(shape=(data.shape[0], data.shape[1], 3), dtype=int)
    for i in range(0, data.shape[0]):
        for j in range(0, data.shape[1]):
            data_3d[i][j] = color_map[data[i][j]]
    fig, ax = plt.subplots(1,1)
    plt.imshow(data_3d)
    plt.show()
    '''
    import psycopg2
    conn_string = "host='localhost' dbname='postgis_30_sample' user='postgres' password='root'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    for i in range(0, len(ndvi_rc)):
        l1=lat[i]
        l2=lon[i]
        n=ndvi_rc[i]
        insertTable='INSERT into map values(%s,ST_SetSRID(ST_MakePoint(%s,%s),4326))'%(n,l1,l2)
        cursor.execute(insertTable)
    print(habitation,barren,shrubs,dense_vegetation,water_bodies)
    conn.commit()
    cursor.close()
    conn.close()
    '''
    return [barren+habitation,shrubs,dense_vegetation]

def Evapotranspiration(v,t,d):
    #print("Total crop water requirement of kharif crops")
    parent_dir="C:/Users/Rishabh/waterbudgeting/Data/"
    home_dir=parent_dir+d+"/"+t+"/"+v+"/"
    df=pd.read_csv(home_dir+"Rabi_crops.csv")
    area=[]
    for i in range(0,len(df)):
        area.append(df['Area'][i])
    sumation=sum(area)
    [barren,shrubs,dense_vegetation]=landclassify(v,t,d)
    print(barren,shrubs,dense_vegetation)
    shrubs=shrubs-(sumation*10000)
    barren_et=barren*0.05
    shrubs_et=shrubs*0.4
    dense_vegetation_et=dense_vegetation*0.8

    return[barren_et,shrubs_et,dense_vegetation_et]
#Evapotranspiration('Konambe','Sinnar','Nashik')

