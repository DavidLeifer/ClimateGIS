import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as the_x
import rioxarray
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import seaborn as sns
import geopandas as gpd
import earthpy as et
from glob import glob
import rioxarray as rxr
import geopandas as gpd
from shapely.geometry import mapping
import rasterio
import skimage.transform as st

'''
cd /Users/davidleifer/Documents/20170101-20190604/Geog531/Assignment3
python /Users/davidleifer/Documents/20170101-20190604/Geog531/Assignment2/polarbearGIS/gitLab/polarbearGIS/scripts/python/nc_data_prep.py

'''

cwd = os.getcwd()

# read in NCAR data, potential evaporation rate at daily resolution
nc_dir = "".join([cwd, '/data/NCAR/'])
folder_nc_list = glob(os.path.join(nc_dir, '*.nc'))
folder_nc_list.sort()
#read in shape file to clip the NCAR global dataset with USA
usa_df = gpd.read_file('/Users/davidleifer/Documents/20170101-20190604/Geog531/Assignment2/data/timeseries_contour_dissolve.shp') 
increment = 1981
# make empty list and append ncar arrays to it
for ncar_nc_path in folder_nc_list:
    # Open the data using rasterio xarray
    ncar_nc_dataset = rxr.open_rasterio(ncar_nc_path, masked=True)
    #get the time slice
    start_date = "".join([str(increment), "-01-01"])
    end_date = "".join([str(increment), "-01-31"])
    ncar_01_15_sel = ncar_nc_dataset.sel(time=slice(start_date, end_date))
    #average the time slice
    ncar_01_15 = ncar_01_15_sel.mean(dim='time',keep_attrs=True)
    #squeeze the averaged time slice into 2d
    ncar_01_15_squeeze = ncar_01_15.squeeze()
    #switch coordinates from 0-360 to -180-180
    ncar_01_15_180 = ncar_01_15_squeeze.assign_coords(x=(((ncar_01_15_squeeze.x + 180) % 360) - 180)).sortby('x')
    ncar_01_15_180 = ncar_01_15_180.rio.write_crs("epsg:4269")
    #clip the ncar with the usa
    ncar_01_15_clipped = ncar_01_15_180.rio.clip(usa_df.geometry.apply(mapping), usa_df.crs, drop=True, invert=False)
    #plot if you want
    #ncar_01_15_re_array.plot()
    #plt.waitforbuttonpress()
    #save the clipped output
    clipped_ncar_output = "".join([cwd, "/data/NCAR_tifs/ncar_", str(increment), ".tif"])
    ncar_01_15_clipped.rio.to_raster(clipped_ncar_output)
    #read in example from clipped nino34 tif for out meta data
    with rasterio.open('/Users/davidleifer/Documents/20170101-20190604/Geog531/Assignment2/data/clipped_output_ppt_nino/clipped_output_ppt_nino_1981.tif') as src:
        naip_data = src.read()
        naip_meta = src.profile
        naip_meta['nodata'] = -9999
    # make any necessary changes to raster properties, e.g.:
    naip_meta['dtype'] = "float32"
    #use sklearn resize to resize the rasta
    with rasterio.open(clipped_ncar_output) as src:
        arr = src.read()
        arr  = arr[0,:,:]
        new_shape = (621,1405)
        newarr = st.resize(arr, new_shape, mode='constant')
    newarr = np.nan_to_num(x=newarr,nan=-9999)
    #write the resized rasta
    newarr_output = "".join([cwd, "/data/NCAR_resized_tifs/ncar_resized_", str(increment), ".tif"])
    with rasterio.open(newarr_output, 'w', **naip_meta) as dst:
        dst.write(newarr, 1)
    #stop the loop when we reach 2015
    print(increment)
    increment = increment + 1
    if increment == 2015:
        break
