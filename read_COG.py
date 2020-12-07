from osgeo import gdal
import numpy as np
import rasterio as rio
import matplotlib.pyplot as plt

# profile
with rio.open('USGS_13_n41w106_COG.tif') as src:
    print(src.profile)

# view
with rio.open('https://prod-is-usgs-sb-prod-publish.s3.amazonaws.com/5fc13d63d34e4b9faad7f403/test_dem_tile.tif') as src:
    oviews = src.overviews(1)

    oview = oviews[-1]
    print('Decimation factor= {}'.format(oview))
    thumbnail = src.read(1, out_shape=(1, int(src.height // oview), int(src.width // oview)))
    print('array type: ', type(thumbnail))

    print(thumbnail)

plt.imshow(thumbnail)
plt.colorbar()
plt.title('Overview - Band 4 {}'.format(thumbnail.shape))
plt.xlabel('Column #')
plt.ylabel('Row #')
plt.show()