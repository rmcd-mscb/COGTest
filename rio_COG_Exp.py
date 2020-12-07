from osgeo import gdal
import numpy as np
import rasterio as rio
import matplotlib.pyplot as plt
from rasterio.plot import show
from pynhd import NLDI
from rasterio.mask import mask
from shapely import geometry
import geopandas as gpd
import json

def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]

band_of_interest = 1 # DEM
with rio.open('Mads_1_COG.tif') as dataset:
    elev = dataset.read(1)

    basin = NLDI().getfeature_byid("comid", "13294318", basin=True).to_crs('epsg:4269')

    ax = plt.subplot(111)
    show(dataset, ax=ax)
    basin.plot(ax=ax, facecolor="none",
              edgecolor='black', lw=0.7)
    plt.show()

#Subset to bounding box of basin
demdata = rio.open('Mads_1.tif')
show((demdata,1),cmap='terrain')
print(demdata.crs, basin.crs)
# print(basin.boundary.to_json())
basin_coords = getFeatures(basin)
minx,miny,maxx,maxy = basin.total_bounds
p1 = geometry.Point(minx,miny)
p2 = geometry.Point(minx,maxy)
p3 = geometry.Point(maxx, maxy)
p4 = geometry.Point(maxx,miny)

pointlist = [p1,p2,p3,p4,p1]
clipBnd = geometry.Polygon(pointlist)
clip = gpd.GeoSeries(clipBnd)

out_img, out_transform = mask(dataset=demdata, shapes=clip, crop=True)
out_meta = demdata.meta
out_meta.update({"driver": "GTiff",
                 "height": out_img.shape[1],
                 "width": out_img.shape[2],
                 "transform": out_transform})
out_raster = rio.open('Mads_clip_1.tif', "w", **out_meta)
out_raster.write(out_img)

out_raster.close()
demdata_clip = rio.open('Mads_clip_1.tif')
with rio.open('Mads_clip_1.tif') as dataset1:
    elev1 = dataset1.read(1)
show(demdata_clip,cmap='terrain')

tmp = 0

