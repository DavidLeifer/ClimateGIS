import rasterio
import rasterio.plot
from rasterio.plot import show
import numpy as np
import pandas as pd
import pyproj
import scipy.stats as stats
from glob import glob
import os
import gdal
from osgeo import osr

cwd = os.getcwd()
#nino index
df = pd.read_csv(cwd + '/data/nino34.csv')
#el nino
elnino = df[df['Index'] > .5]
#la nina
lanina = df[df['Index'] < -0.5]
#neither el nino or la nina
less = df['Index'] < .5
great = df['Index'] > -0.5
neither = df[less & great]

#/Applications/QGIS-LTR.app/Contents/MacOS/bin/python3 /Users/davidleifer/Documents/20170101-20190604/Geog531/Assignment2/polarbearGIS/gitLab/polarbearGIS/scripts/python/tmean_LaElNeu_diff.py
#create list of el nino files based on year from elnino varible
data_dir = cwd + '/data/tmean/*'
data_dir_list = glob(data_dir)

#create a list of bil paths from each sub folder
folder_bil_list = []
for i in data_dir_list:
    folder_bil = glob(os.path.join(i, '*.bil'))
    folder_bil_list.append(folder_bil)

#see if year is in folder_bil_list
df2 = pd.DataFrame(folder_bil_list)
elnino_list = elnino['Year'].tolist()
df4 = []
for nin in elnino_list:
    df3 = df2[df2[0].str.contains(str(nin))]
    df4.append(df3)
df5 = pd.concat(df4)
elninolist2 = df5[0].tolist()

#calculate average of el nino arrays
#https://gis.stackexchange.com/questions/244376/computing-mean-of-all-rasters-in-a-directory-using-python
def read_file(file):
    with rasterio.open(file) as src:
        return(src.read(1))
# Read all data as a list of numpy arrays 
array_list = [read_file(x) for x in elninolist2]
# Perform averaging
elnino_array_out = np.mean(array_list, axis=0)
elnino_array_out[elnino_array_out == -9999] = -19998

#create list of neither files based on year from neither varible
neither_list = neither['Year'].tolist()
neutral_df4 = []
for nei in neither_list:
    netural_df3 = df2[df2[0].str.contains(str(nei)+ "01_bil")]
    neutral_df4.append(netural_df3)
neutral_df5 = pd.concat(neutral_df4)
neither_list2 = neutral_df5[0].tolist()
#calculate average of netural arrays
# Read all data as a list of numpy arrays 
netural_array_list = [read_file(x) for x in neither_list2]
# Perform averaging
neutral_array_out = np.mean(netural_array_list, axis=0)
#perform tha difference
elnino_minus_neutral = elnino_array_out - neutral_array_out

#create gdal variable example map to get transformation and projection from
example_tif = cwd + "/data/tmean/PRISM_tmean_stable_4kmM3_201001_bil/PRISM_tmean_stable_4kmM3_201001_bil.bil"
data0 = gdal.Open(example_tif)
#https://gis.stackexchange.com/questions/37238/writing-numpy-array-to-raster-file
#write array with gdal
dst_filename = cwd + '/data/tmean_elnino_minus_neutral/tmean_elnino_minus_neutral.tif'
x_pixels = 1405  # number of pixels in x
y_pixels = 621  # number of pixels in y
driver = gdal.GetDriverByName('GTiff')
dataset = driver.Create(dst_filename,x_pixels, y_pixels, 1,gdal.GDT_Float32)
dataset.GetRasterBand(1).WriteArray(elnino_minus_neutral)
# follow code is adding GeoTranform and Projection
geotrans=data0.GetGeoTransform()  #get GeoTranform from existed 'data0'
proj=data0.GetProjection() #you can get from a exsited tif or import 
dataset.SetGeoTransform(geotrans)
dataset.SetProjection(proj)
dataset.FlushCache()
band = dataset.GetRasterBand(1)
band.SetNoDataValue(-9999)
band=None
dataset=None

#create list of la nina files based on year from lanina varible
lanina_df2 = pd.DataFrame(folder_bil_list)
lanina_list = lanina['Year'].tolist()
lanina_df4 = []
for lan in lanina_list:
    lanina_df3 = lanina_df2[lanina_df2[0].str.contains(str(lan)+ "01_bil")]
    lanina_df4.append(lanina_df3)
lanina_df5 = pd.concat(df4)
lanina_list2 = lanina_df5[0].tolist()
#calculate average of la nina arrays
# Read all data as a list of numpy arrays 
lanina_array_list = [read_file(x) for x in lanina_list2]
# Perform averaging
lanina_array_out = np.mean(lanina_array_list, axis=0)
lanina_array_out[lanina_array_out == -9999] = -19998
#perform tha difference
lanina_minus_neutral = lanina_array_out - neutral_array_out

#write array with gdal
dst_filename = cwd + '/data/tmean_lanina_minus_neutral/tmean_lanina_minus_neutral.tif'
x_pixels = 1405  # number of pixels in x
y_pixels = 621  # number of pixels in y
driver = gdal.GetDriverByName('GTiff')
dataset = driver.Create(dst_filename,x_pixels, y_pixels, 1,gdal.GDT_Float32)
dataset.GetRasterBand(1).WriteArray(lanina_minus_neutral)
# follow code is adding GeoTranform and Projection
geotrans=data0.GetGeoTransform()  #get GeoTranform from existed 'data0'
proj=data0.GetProjection() #you can get from a exsited tif or import 
dataset.SetGeoTransform(geotrans)
dataset.SetProjection(proj)
dataset.FlushCache()
band = dataset.GetRasterBand(1)
band.SetNoDataValue(-9999)
band=None
dataset=None

print("finished tmean_LaElNeu_diff.py")
