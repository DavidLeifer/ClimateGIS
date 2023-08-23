import rasterio
from rasterio.mask import mask
from rasterio import Affine
import rasterio.features
from rasterio.transform import from_origin
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.plot import show
import fiona
import numpy as np
import pandas as pd
import pyproj
import seaborn as sns
import scipy.stats as stats
from glob import glob
from osgeo import ogr, gdal, osr, gdal_array
from osgeo.gdalnumeric import *
from osgeo.gdalconst import *
from scipy.stats.stats import pearsonr
import subprocess
import os
import sys
import math

'''
cd /Users/davidleifer/Documents/20170101-20190604/Geog531/Assignment2
/Applications/QGIS-LTR.app/Contents/MacOS/bin/python3 /Users/davidleifer/Documents/20170101-20190604/Geog531/Assignment2/polarbearGIS/gitLab/polarbearGIS/scripts/python/raster_correlation_main.py

'''

class raster_correlation:
    def __init__(self, raster, index, named_type, index_year, index_field, height, width):
        self.raster = raster
        self.index = index
        self.named_type = named_type
        self.index_year = index_year
        self.index_field = index_field
        self.height = height
        self.width = width

    def read_raster_dir(self):
        cwd = os.getcwd()
        #create a list of bil paths from each sub folder
        folder_bil = "/".join([cwd, "data", self.raster])
        folder_bil_list = glob(os.path.join(folder_bil, '*.bil'))
        folder_bil_list.sort()
        return folder_bil_list

    def read_index_dir(self):
        cwd = os.getcwd()
        df = "/data/".join([cwd, self.index])
        df_index = pd.read_csv(df)
        return df_index

    def make_directories(self):
        cwd = os.getcwd()
        #make the dir to hold the bil data
        bil2tif_resize = 'data/bil2tif_resize_'
        bil_dir_no_name = os.path.join(cwd, bil2tif_resize)
        output_bil_dir = "".join([bil_dir_no_name, self.named_type])
        print(output_bil_dir)
        os.mkdir(output_bil_dir)
        #make the dir to hold the index square data
        cor_mask = 'data/output_mask_'
        cor_mask_no_name = os.path.join(cwd, cor_mask)
        output_msk_dir = "".join([cor_mask_no_name, self.named_type])
        print(output_msk_dir)
        os.mkdir(output_msk_dir)
        #make the dir to hold the clipped index data
        clipped_output = 'data/clipped_output_'
        clipped_output_path = os.path.join(cwd, clipped_output)
        clipped_output_dir = "".join([clipped_output_path, self.named_type])
        print(clipped_output_dir)
        os.mkdir(clipped_output_dir)
        cor_actually_no_name = os.path.join(cwd, "data/")
        cor_actually_dst_filename = "".join([cor_actually_no_name, "pearson_final_", self.named_type])
        print(cor_actually_dst_filename)
        os.mkdir(cor_actually_dst_filename)

    def tif_and_clipped_index(self, folder_bil_list, df_index):
        cwd = os.getcwd()
        #print(folder_bil_list)
        for file in folder_bil_list:
            base = os.path.basename(file)
            year = base[-14:-10]
            print("this year " + year)
            #save resized bil to tif
            tif = ".tif"

            #make the path to hold the bil data
            data = 'data/'
            bil_dir_no_name = os.path.join(cwd, data)
            bil2tif_resize_name = "".join(["bil2tif_resize_", self.named_type])
            output_bil_path2tif = "".join([bil_dir_no_name, bil2tif_resize_name, "/", bil2tif_resize_name, "_", year, tif])
            print(output_bil_path2tif)
            #save bils as tifs
            with rasterio.open(file) as src:
                thumbnail = src.read(1, 
                    out_shape=(1, int(self.height), int(self.width)))
                print("OG bil = ")
                print(src.crs.wkt)
                print(year)
                with rasterio.Env():
                    profile = src.profile
                    profile.update(
                        dtype=rasterio.int32,
                        count=1,
                        compress='lzw',
                        height=self.height,
                        width=self.width,
                        crs=src.crs,
                        transform=src.transform,)
                    with rasterio.open(output_bil_path2tif, 'w', **profile,) as dst:
                        dst.write(thumbnail.astype(rasterio.int32), 1)
                        dst.close()

            with rasterio.Env():
                #create a np mask of the year's nino34.xlsx index and save as tif file
                df_index.loc[df_index[self.index_year] == int(year), self.index_field]
                yer_index = df_index.loc[df_index[self.index_year] == int(year), self.index_field].iloc[0]
                np_mask = (621,1405)
                yi_array = np.full(np_mask,yer_index)
                #write array with rasterio
                output_mask_no_name = os.path.join(cwd, data)
                output_mask_name = "".join(["output_mask_", self.named_type])
                output_mask_path2tif = "".join([output_mask_no_name, output_mask_name, "/", output_mask_name, "_", year, tif])

                new_dataset = rasterio.open(output_mask_path2tif, 'w', 
                                    driver='GTiff',
                                    height = self.height, 
                                    width = self.width,
                                    count=1,
                                    dtype=str(yi_array.dtype),
                                    crs=src.crs,
                                    transform=src.transform)

                new_dataset.write(yi_array, 1)
                print("square mask = ")
                print(year)
                new_dataset.close()

            #read in raster mask shapefile, for clipping the year's nino34.xlsx index array
            vectorize_output_reproj = "/".join([cwd, "/data/timeseries_contour_dissolve.shp"])
            with fiona.open(vectorize_output_reproj, "r") as shapefile_reproj:
                vectorize_output_shp_reproj = [feature["geometry"] for feature in shapefile_reproj]

            #read in dst_filename AKA a raster mask from index and clip it with the vectorize_output_shp from qgis
            with rasterio.open(output_mask_path2tif) as foo_fighter:
                out_image, out_transform = mask(foo_fighter, vectorize_output_shp_reproj, crop=False, nodata=-9999)
                out_meta = foo_fighter.meta
            out_meta.update({"driver": "GTiff",
                                 "height": self.height,
                                 "width": self.width,
                                 "transform": src.transform,
                                 "crs": src.crs,
                                 "nodata": -9999})
            #save and clip raster index mask as file
            pearson_no_name = os.path.join(cwd, data)
            pearson_output_path = "".join([pearson_no_name, "clipped_output_", self.named_type, "/", "clipped_output_", self.named_type, "_", year, tif])

            with rasterio.open(pearson_output_path, "w", **out_meta) as foo_fighter_dest:
                foo_fighter_dest.write(out_image)
                print("clipped index = ")
                print(foo_fighter_dest.crs.wkt)
                src.close()
                foo_fighter_dest.close()

    def cor_actually(self):
        def rolling_cov(array1, array2):
            i = 0
            i2 = 4
            rolling_corr1 = []
            for index in range(len(array1)):
                df_select1 = array1[i:i2]
                df_select2 = array2[i:i2]
                cov = np.cov(df_select1, df_select2)[0,0]
                print(cov)
                rolling_corr1.append(cov)
                i = i + 1
                i2 = i2 + 1
            return rolling_corr1

        #get current working dir
        cwd = os.getcwd()
        data = '/data/'
        #read in co2_bil2tif_resize as list of file directories
        co2_bil2tif_resize = "".join([cwd, data, "bil2tif_resize_", self.named_type])
        co2_bil2tif_resize_list = glob(os.path.join(co2_bil2tif_resize, '*.tif'))
        co2_bil2tif_resize_list.sort()

        #read in index files as list of file directories
        co2_pearson_output = "".join([cwd, data, "clipped_output_", self.named_type])
        co2_pearson_output_list = glob(os.path.join(co2_pearson_output, '*.tif'))
        co2_pearson_output_list.sort()

        for example_tif, index_tif in zip(co2_bil2tif_resize_list,co2_pearson_output_list):
            base = os.path.basename(example_tif)
            year = base[-8:-4]
            print("this year 2 " + year)
            base2 = os.path.basename(index_tif)
            #load in precipitation raster tif, output from co2_cor.py located in /data/co2_bil2tif_resize/
            with rasterio.open(example_tif, mode="r+") as src:
                co2_raster = src.read(1, out_shape=(1, int(self.height), int(self.width)))
            #load in 1981 index mask raster tif, output from co2_cor.py located in /data/co2_pearson_output/
            with rasterio.open(index_tif) as src:
                index_raster = src.read(1, out_shape=(1, int(self.height), int(self.width)))

            #create one big ol list of the two numppy arrays
            co2_raster = np.concatenate((co2_raster), dtype=float).ravel().tolist()
            index_raster = np.concatenate((index_raster), dtype=float).ravel().tolist()
            rolling_corr1 = rolling_cov(co2_raster, index_raster)

            npa = np.asarray(rolling_corr1, dtype=np.float32)
            #reshape
            newarr = npa.reshape(int(self.height), int(self.width))
            newarr2 = np.nan_to_num(x=newarr,nan=-9999,posinf=.00001,neginf=-.00001)
            newarr2[newarr2 == .00001] = -9999
            newarr2[newarr2 == -.00001] = -9999
            newarr2[newarr2 == 0] = -9999
            newarr2[newarr2 > 1] = -9999

            with rasterio.open(example_tif) as src:
                naip_data = src.read()
                naip_meta = src.profile
            # make any necessary changes to raster properties, e.g.:
            naip_meta['dtype'] = "float32"
            naip_meta['nodata'] = -9999

            tif = ".tif"
            cor_actually_no_name = "".join([cwd, data])
            cor_actually_dst_filename = "".join([cor_actually_no_name, "pearson_final_", self.named_type, "/", "pearson_final_", self.named_type, "_", year, tif])
            with rasterio.open(cor_actually_dst_filename, 'w', **naip_meta) as dst:
                dst.write(newarr2, 1)
        print("Finished cor_actually for " + self.named_type)

    def quantile_reclassify(self, folder):
        cwd = os.getcwd()
        self.folder = folder

        input_raster_folder = "".join([cwd, "/data/", self.folder, "_", self.named_type])

        #input_raster_folder = '/Users/davidleifer/Documents/20170101-20190604/Geog531/Assignment2/data/co2_pearson_final(backup)'
        input_raster_folder_list = glob(os.path.join(input_raster_folder, '*.tif'))
        input_raster_folder_list.sort()

        for input_raster in input_raster_folder_list:

            # open the dataset and retrieve raster data as an array
            dataset = gdal.Open(input_raster)
            band = dataset.GetRasterBand(1)
            array = band.ReadAsArray()

            nodata_val = band.GetNoDataValue()
            if nodata_val is not None:
                array = np.ma.masked_equal(array, nodata_val)
            #get only numbers (not nodata)
            array_ignored_nan = array[array >= array.min()]
            # create an array of zeros the same shape as the input array
            output = np.zeros_like(array).astype(np.uint8)

            # use the numpy percentile function to calculate percentile thresholds, gotta round for scientific notation
            try:
                percentile_80 = round(np.percentile(array_ignored_nan, 80), 5)
                percentile_60 = round(np.percentile(array_ignored_nan, 60), 5)
                percentile_40 = round(np.percentile(array_ignored_nan, 40), 5)
                percentile_20 = round(np.percentile(array_ignored_nan, 20), 5)
                percentile_0 = round(np.percentile(array_ignored_nan, 0), 5)

                print(percentile_0, percentile_20, percentile_40, percentile_60, percentile_80)

                txt_outname = "".join([(os.path.splitext(input_raster)[0]), "_reclassed.txt"])
                print(txt_outname)

                with open(txt_outname, "w") as text_file:
                    text_file.write(" ".join([str(percentile_0), str(percentile_20), str(percentile_40), str(percentile_60), str(percentile_80)]))

                output = np.where((array > percentile_0), 1, output)
                output = np.where((array > percentile_20), 2, output)
                output = np.where((array > percentile_40), 3, output)
                output = np.where((array > percentile_60), 4, output)
                output = np.where((array > percentile_80), 5, output)

                outname = os.path.splitext(input_raster)[0] + "_reclassed.tif"
                gdal_array.SaveArray(output, outname, "gtiff", prototype=dataset)

                print(outname)

            except:
                pass

        print("quantile_reclassify.py complete")

