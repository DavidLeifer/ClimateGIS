import sys
sys.path.append("/scripts/python_refactor/")
from raster_correlation import raster_correlation

'''
cd /Users/davidleifer/Documents/20170101-20190604/Geog531/Assignment2
/Applications/QGIS-LTR.app/Contents/MacOS/bin/python3 /Users/davidleifer/Documents/20170101-20190604/Geog531/Assignment2/polarbearGIS/gitLab/polarbearGIS/scripts/python/raster_correlation_main.py

'''

'''#ppt vs co2
#name of raster directory
raster_dir = 'ppt'
#path to csv index
index_dir = 'mole_fraction_of_carbon_dioxide_in_air_input4MIPs_GHGConcentrations_CMIP_UoM-CMIP-1-1-0_gr3-GMNHSH_0000-2014.csv'
#folder name to be quantiled
folder = "pearson_final"

#raster_correlation accepts seven arguments: the raster directory, index directory, string name, string index year, string index field
p1 = raster_correlation(raster_dir, index_dir, "ppt_co2", "year", "data_mean_global", 621, 1405)
p1.make_directories()
p1.tif_and_clipped_index(p1.read_raster_dir(), p1.read_index_dir())
p1.cor_actually()
p1.quantile_reclassify(folder)

#tmean vs co2
#name of raster directory
raster_dir = 'tmean'
#path to csv index
index_dir = 'mole_fraction_of_carbon_dioxide_in_air_input4MIPs_GHGConcentrations_CMIP_UoM-CMIP-1-1-0_gr3-GMNHSH_0000-2014.csv'
#folder name to be quantiled
folder = "pearson_final"

#raster_correlation accepts seven arguments: the raster directory, index directory, string name, string index year, string index field
p1 = raster_correlation(raster_dir, index_dir, "tmean_co2", "year", "data_mean_global", 621, 1405)
p1.make_directories()
p1.tif_and_clipped_index(p1.read_raster_dir(), p1.read_index_dir())
p1.cor_actually()
p1.quantile_reclassify(folder)'''

#ppt vs nino34
#name of raster directory
raster_dir = 'ppt'
#path to csv index
index_dir = 'nino34.csv'
#folder name to be quantiled
folder = "pearson_final"

#raster_correlation accepts seven arguments: the raster directory, index directory, string name, string index year, string index field
p1 = raster_correlation(raster_dir, index_dir, "ppt_nino", "Year", "Index", 621, 1405)
p1.make_directories()
p1.tif_and_clipped_index(p1.read_raster_dir(), p1.read_index_dir())
#p1.cor_actually()
#p1.quantile_reclassify(folder)

'''#tmean vs nino34
#name of raster directory
raster_dir = 'tmean'
#path to csv index
index_dir = 'nino34.csv'
#folder name to be quantiled
folder = "pearson_final"

#raster_correlation accepts seven arguments: the raster directory, index directory, string name, string index year, string index field
p1 = raster_correlation(raster_dir, index_dir, "tmean_nino", "Year", "Index", 621, 1405)
p1.make_directories()
p1.tif_and_clipped_index(p1.read_raster_dir(), p1.read_index_dir())
p1.cor_actually()
p1.quantile_reclassify(folder)

#raster classify for tmean bil resize
#name of raster directory
raster_dir = 'bil2tif_resize_tmean_nino'
#path to csv index
index_dir = 'nino34.csv'
#folder name to be quantiled
folder = "bil2tif_resize"

#raster_correlation accepts seven arguments: the raster directory, index directory, string name, string index year, string index field
p1 = raster_correlation(raster_dir, index_dir, "tmean_nino", "Year", "Index", 621, 1405)
p1.quantile_reclassify(folder)

#raster classify for tmean bil resize
#name of raster directory
raster_dir = 'bil2tif_resize_tmean_nino'
#path to csv index
index_dir = 'nino34.csv'
#folder name to be quantiled
folder = "bil2tif_resize"

#raster_correlation accepts seven arguments: the raster directory, index directory, string name, string index year, string index field
p1 = raster_correlation(raster_dir, index_dir, "ppt_nino", "Year", "Index", 621, 1405)
p1.quantile_reclassify(folder)'''

