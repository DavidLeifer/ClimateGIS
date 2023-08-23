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
from sklearn.linear_model import LinearRegression
import csv
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from mlxtend.evaluate import bias_variance_decomp
from sklearn.model_selection import train_test_split

'''
cd /Users/davidleifer/Documents/20170101-20190604/Geog531/Assignment3
python /Users/davidleifer/Documents/20170101-20190604/Geog531/Assignment3/read_ncx.py

http://xarray.pydata.org/en/stable/user-guide/indexing.html
https://www.earthdatascience.org/courses/use-data-open-source-python/hierarchical-data-formats-hdf/use-netcdf-in-python-xarray/
https://github.com/trentford/GEOG431-531/blob/master/GLEAM/ProcessGLEAM.m

#explore code
ds = the_x.open_dataset(ep_gleam)
df = ds.to_dataframe()
#make into nice columns
df2 = df.reset_index().rename(columns={'index':'TIMESTAMP'})
#make into nice date
df2['time'] = pd.to_datetime(df2['time'], format='%Y-%m-%d %H:%M:%S')
df_filtered = df2.loc[(df2['time'] < '2011-01-01 00:00:00') & (df2['time'] > '2003-01-01 00:00:00')]
print(df_filtered)
'''

cwd = os.getcwd()

# read in NCAR data, potential evaporation rate at daily resolution
nc_dir = "".join([cwd, '/data/NCAR/'])
folder_nc_list = glob(os.path.join(nc_dir, '*.nc'))
folder_nc_list.sort()
# make empty list and append ncar arrays to it
ncar_nc_dataset_list = []
for ncar_nc_path in folder_nc_list:
    # Open the data using a context manager
    with the_x.open_dataset(ncar_nc_path) as ncar_nc:
        ncar_nc.rio.set_crs(4269)
        ncar_nc_dataset = ncar_nc.rio.write_crs(ncar_nc.rio.crs, inplace=True)
    ncar_nc_dataset_list.append(ncar_nc_dataset)

# read in GLEAM data, potential evaporation rate at daily resolution
nc_dir = "".join([cwd, '/data/GLEAM/'])
folder_nc_list = glob(os.path.join(nc_dir, '*.nc'))
folder_nc_list.sort()
# make empty list and append gleam arrays to it
gleam_nc_dataset_list = []
for gleam_nc_path in folder_nc_list:
    # Open the data using a context manager
    with the_x.open_dataset(gleam_nc_path) as gleam_nc:
        gleam_nc.rio.set_crs(4269)
        gleam_nc_dataset = gleam_nc.rio.write_crs(gleam_nc.rio.crs, inplace=True)
    gleam_nc_dataset_list.append(gleam_nc_dataset)

# read in ASOS PET data (weather stations)
# Penman-Monteith method for potential evapotranspiration
csv_dir = "".join([cwd, '/data/Weather_Stations/'])
folder_csv_list = glob(os.path.join(csv_dir, '*.csv'))
folder_csv_list.sort()
# select the gleam dataset by each lat and lon for each weather station
#lat, lon
#Binghampton.csv, Columbia.csv, Dallas.csv, 
#Eau_Claire.csv, Evansville.csv, International_Falls.csv, 
#Lexington.csv, Memphis.csv, Pierre.csv
#y, x
point_array = [[42.099,-75.918],[34.001,-81.035],[32.755,-97.331],
[44.811,-91.499],[37.972,-87.571],[48.602,-93.404],
[38.041,-84.504],[35.149,-90.049],[44.368,-100.35]]
#put gleam points into a stacked array, each csv file being its own array
empty_array_gleam_list = []
for point in point_array:
    print(point)
    empty_array_gleam = []
    # get gleam points by lon and lat
    for gleam_nc_datar in gleam_nc_dataset_list:
        gleam_points = gleam_nc_datar["Ep"].sel(lon=point[1], lat=point[0], method="nearest")
        gleam_point_df = gleam_points.to_dataframe()
        #make list and extend into empty list
        gleam_point_list = gleam_point_df.values.tolist()
        empty_array_gleam.extend(gleam_point_list)
    empty_array_gleam_list.append(empty_array_gleam)

# put ncar into a stacked array, each csv file being its own array
empty_array_ncar_list = []
for point in point_array:
    empty_array_ncar = []
    # get ncar points by lon and lat
    for ncar_nc_datar in ncar_nc_dataset_list:
        ncar_points = ncar_nc_datar["pevpr"].sel(lon=(point[1] % 360), lat=point[0], method="nearest")
        ncar_point_df = ncar_points.to_dataframe()
        #make list and extend into empty list
        ncar_point_list = ncar_point_df.values.tolist()
        empty_array_ncar.extend(ncar_point_list)
    empty_array_ncar_list.append(empty_array_ncar)

gleam_and_csv_list = []
#loop over csvs and gleam point array and merge them together and append to list
for csv_path, gleam_points in zip(folder_csv_list, empty_array_gleam_list):
    #read in each csv
    base = os.path.basename(csv_path)
    csv_df = pd.read_csv(csv_path, header=None)
    #concatenate the year month day columns and convert to datetime
    csv_df['time'] = csv_df[0].astype('str') + "-" + csv_df[1].astype('str') + "-" + csv_df[2].astype('str')
    csv_df['time'] = pd.to_datetime(csv_df['time'], format="%Y-%m-%d")
    csv_df_sorted = csv_df.sort_values(by=['time'])
    #put gleam in df
    gleam_points_df = pd.DataFrame(gleam_points)
    gleam_and_csv = pd.merge(csv_df_sorted, gleam_points_df, left_index=True, right_index=True)
    gleam_and_csv_list.append(gleam_and_csv)

gleam_csv_ncar_list = []
for gleam_csv, ncar_array in zip(gleam_and_csv_list, empty_array_ncar_list):
    #put ncar in df
    ncar_df = pd.DataFrame(ncar_array)
    #merge gleam_csv and ncar_array and append to list
    gleam_csv_ncar_merge = pd.merge(gleam_csv, ncar_df, left_index=True, right_index=True)
    gleam_csv_ncar_merge = gleam_csv_ncar_merge.drop(columns=['0_x', '1_x', '2_x', '0_y', '1_y', '2_y', 0, 1, 2])
    gleam_csv_ncar_merge = gleam_csv_ncar_merge.rename(columns={8: 'lat', 9: 'lon', 3: 'NCAR_PET', '3_y': 'GLEAM_PET', '3_x': 'avg_temp', 4: 'wind_speed', 5: 'AR_humid', 6: 'solar_radiation', 7: 'station_PET'})
    gleam_csv_ncar_list.append(gleam_csv_ncar_merge)

csv_names = ["Binghampton", "Columbia", "Dallas", 
"Eau_Claire", "Evansville", "International_Falls", 
"Lexington", "Memphis", "Pierre"]

mean_std_array = ["csv_name", "station_regression_mean", "station_regression_std", "NCAR_PET_mean", "NCAR_PET_std", "GLEAM_PET_mean", "GLEAM_PET_std", "station_PET_mean", "station_PET_std", "\n"]
#loop over all the pets and get mean and std, write to table
for pet,csv_base in zip(gleam_csv_ncar_list,csv_names):
    #x = lndependent
    #y = depdendent
    the_x_df = pet
    the_x_life = the_x_df.fillna(the_x_df.mean(numeric_only=True))
    x = the_x_life[['avg_temp', 'wind_speed', 'AR_humid', 'solar_radiation']]
    the_y_df = pet
    the_y = the_y_df.fillna(the_y_df.mean(numeric_only=True))
    y = the_y['station_PET']
    #create linear regression variable, fit the data, predict
    linear_regression = LinearRegression()
    linear_regression.fit(x,y)
    y_pred = linear_regression.predict(x)
    #add array into pandas column
    the_x_df['station_regression']=pd.Series(y_pred)
    print(csv_base)
    #calculate mean and std
    #'station_PET'
    y = (y - y.min()) / (y.max() - y.min())
    station_regression_mean = y.mean()
    station_regression_std = y.std()
    #'NCAR_PET'
    NCAR_PET_mean_std = the_x_life['NCAR_PET']
    NCAR_PET_mean_std = (NCAR_PET_mean_std - NCAR_PET_mean_std.min()) / (NCAR_PET_mean_std.max() - NCAR_PET_mean_std.min())
    NCAR_PET_mean = NCAR_PET_mean_std.mean()
    NCAR_PET_std = NCAR_PET_mean_std.std()
    #'NCAR_PET'
    GLEAM_PET_mean_std = the_x_life['GLEAM_PET']
    GLEAM_PET_mean_std = (GLEAM_PET_mean_std - GLEAM_PET_mean_std.min()) / (GLEAM_PET_mean_std.max() - GLEAM_PET_mean_std.min())
    GLEAM_PET_mean = GLEAM_PET_mean_std.mean()
    GLEAM_PET_std = GLEAM_PET_mean_std.std()
    #'station_PET'
    station_PET_mean_std = the_x_life['station_PET']
    station_PET_mean_std = (station_PET_mean_std - station_PET_mean_std.min()) / (station_PET_mean_std.max() - station_PET_mean_std.min())
    station_PET_mean = station_PET_mean_std.mean()
    station_PET_std = station_PET_mean_std.std()
    #RMSE
    ncar_rmse = mean_squared_error(station_PET_mean_std, NCAR_PET_mean_std, squared=False)
    gleam_rmse = mean_squared_error(station_PET_mean_std, GLEAM_PET_mean_std, squared=False)
    predicted_rmse = mean_squared_error(station_PET_mean_std, y_pred, squared=False)
    print("rmse")
    print(ncar_rmse)
    print(gleam_rmse)
    print(predicted_rmse)
    print("stop rmse")
    ncar_mae = mean_absolute_error(station_PET_mean_std, NCAR_PET_mean_std)
    gleam_mae = mean_absolute_error(station_PET_mean_std, GLEAM_PET_mean_std)
    predicted_mae = mean_absolute_error(station_PET_mean_std, y_pred)
    print("MAE")
    print(ncar_mae)
    print(gleam_mae)
    print(predicted_mae)
    print("stop MAE")
    model_lr = LinearRegression()
    # concatenate station and ncar, station and gleam
    station_ncar = pd.merge(station_PET_mean_std, NCAR_PET_mean_std, left_index=True, right_index=True)
    station_gleam = pd.merge(station_PET_mean_std, GLEAM_PET_mean_std, left_index=True, right_index=True)
    X_train, X_test, y_train, y_test = train_test_split(station_ncar.values, station_gleam.values, test_size=0.33, random_state=1)
    mse, bias, var = bias_variance_decomp(model_lr, X_train, y_train[:,0], X_test, y_test[:,0], loss='mse', num_rounds=200, random_seed=123)
    print("NCAR_PET_mean_std: mse, bias, var")
    print(mse)
    print(bias)
    print(var)

    mean_std_array.append(csv_base)
    mean_std_array.append(station_regression_mean)
    mean_std_array.append(station_regression_std)
    mean_std_array.append(NCAR_PET_mean)
    mean_std_array.append(NCAR_PET_std)
    mean_std_array.append(GLEAM_PET_mean)
    mean_std_array.append(GLEAM_PET_std)
    mean_std_array.append(station_PET_mean)
    mean_std_array.append(station_PET_std)
    mean_std_array.append('\n')

#print(mean_std_array)
mean_std_output = "".join([cwd, '/data/mean_std_output.csv'])
with open(mean_std_output, 'w') as csv_writer:
    # using csv.writer method from CSV package
    write = csv.writer(csv_writer, lineterminator='\n')
    write.writerow(mean_std_array)


'''
for csv_path in folder_csv_list:
    #read in each csv
    base = os.path.basename(csv_path)
    csv_df = pd.read_csv(csv_path, header=None)
    #concatenate the year month day columns and convert to datetime
    csv_df['time'] = csv_df[0].astype('str') + "-" + csv_df[1].astype('str') + "-" + csv_df[2].astype('str') + " " + "00:00:10"
    csv_df['time'] = pd.to_datetime(csv_df['time'], format="%Y-%m-%d %H:%M:%S")
    #get the PET lat and lon
    csv_lat_col = csv_df[8]
    csv_lon_col = csv_df[9]
    csv_lat = csv_lat_col.iloc[0]
    csv_lon = csv_lon_col.iloc[0]
    # get gleam points by lon and lat
    points = gleam_nc_datar["Ep"].sel(lon=csv_lon, lat=csv_lat, method="nearest")
    gleam_point_array = points.to_dataframe(name=base)
'''
#Binghampton.append(gleam_point_array)

#csv_and_gleam_point = pd.concat([csv_df, gleam_point_array], axis=1)
#print(csv_and_gleam_point)

#select each points datasets
'''
empty_point_array = []
for gleam in gleam_nc_dataset_list:
points = gleam["Ep"].sel(lon=csv_lon, lat=csv_lat, method="nearest")
point_array = points.to_dataframe(name=None)
print(point_array)
empty_point_array.append(point_array)
#point_time = points.loc["2003-01-01 00:00:00":"2010-12-31 00:00:00"]'''

#print(point_time)

#print(point_time['time'])

#print(point_time)
'''

# Create a spatial map of your selected location with cartopy
extent = [70, -70, 90, -90]
central_lon = np.mean(extent[:2])
central_lat = np.mean(extent[2:])
f, ax = plt.subplots(figsize=(12, 6),
                 subplot_kw={'projection': ccrs.AlbersEqualArea(central_lon, central_lat)})
ax.coastlines()
# Plot the selected location 
ax.plot(csv_lon-360, csv_lat, 
    'r*', 
    transform=ccrs.PlateCarree(),
   color="purple", markersize=10)
ax.set_extent(extent)
ax.set(title="Location of the Latitude / Longitude Being Used To to Slice Your netcdf Climate Data File")
# Adds continent boundaries to the map
ax.add_feature(cfeature.LAND, edgecolor='black')
ax.gridlines()
plt.show()
'''

'''
one_point = gleam_dataset["Ep"].sel(lat=csv_lat,
                                               lon=csv_lon)
print(one_point)
start_date = "2003-07-01"
end_date = "2004-07-01"

two_months_conus = gleam_dataset["Ep"].sel(
    time=slice(start_date, end_date))

# Quickly plot the data using xarray.plot()
two_months_conus.plot(x="lon",
                      y="lat",
                      col="time",
                      col_wrap=1)
plt.suptitle("Two Time Steps of Monthly Ep", y=1.03)
plt.show()
'''

