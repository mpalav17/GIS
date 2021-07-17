import geopandas as gpd

gdf = gpd.read_file("C:/Users/mihir/Downloads/nashik/nashik.shp")
print(len(gdf))
# list = []
# for i in range(0, len(gdf)):
#     if gdf['taluka_nam'][i] == "sinnar":
#         list.append(i)
# print(gdf['taluka_nam'][list[50]])