import numpy as np
import os
from glob import glob
import rasterio
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
warnings.filterwarnings('ignore')

'''
#mac stuff
https://machinelearningmastery.com/sarima-for-time-series-forecasting-in-python/
https://www.statsmodels.org/dev/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html
https://stackoverflow.com/questions/48221807/google-cloud-instance-terminate-after-close-browser
cd /Users/davidleifer/Documents/20170101-20190604/Geog531/Assignment2
python /Users/davidleifer/Documents/20170101-20190604/Geog531/Assignment2/polarbearGIS/gitLab/polarbearGIS/scripts/python/sarimax_for.py

#linux stuff
sudo apt-get install wget
sudo apt install python3-pip
sudo apt-get install unzip
sudo apt-get install screen

sudo pip3 install rasterio
sudo pip3 install pandas==1.2.0
sudo pip3 install -U scikit-learn
sudo pip3 install statsmodels

#https://drive.google.com/file/d/1OKHydzCk7oayMRs4wOdP2TO85bHm_7OI/view?usp=sharing

sudo wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1OKHydzCk7oayMRs4wOdP2TO85bHm_7OI' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1OKHydzCk7oayMRs4wOdP2TO85bHm_7OI" -O xyz-timeseries-data && rm -rf /tmp/cookies.txt

sudo unzip xyz-timeseries-data
sudo rm xyz-timeseries-data

sudo nano sarimax_for.py
sudo python3 -W ignore sarimax_for.py

/home/davleifer/ypred_training_arima.prj
/home/davleifer/ypred_training_arima.tif.aux.xml
/home/davleifer/ypred_training_arima.hdr
/home/davleifer/ypred_training_arima.tif
'''

#function to do the raster linear regression, accepts index and ppt/tmean
def raster_sarimax(ppt_stack):
    dates = np.asarray(pd.date_range('1/1/1981', periods=23, freq='AS-JAN'))
    #create some empty lists and an incremental variable
    increment2 = 0
    sarimax_raster = []
    for ppt_list in ppt_stack:
        #loop over list of index arrays and list of ppt arrays and list of tmean arrays
        sarimax_raster_staged = []
        for ppt in ppt_list:
            print(increment2)
            #SARIMAX
            numpy_full = np.full_like(ppt, 23)
            if numpy_full in ppt:
                sarimax_raster_staged.append(-9999)
                print(-9999)
            else:
                ppt_df = pd.DataFrame(ppt, index=dates, columns = {'A'})
                my_order = (1, 1, 1)
                my_seasonal_order = (1, 1, 1, 12)
                arima_model = SARIMAX(ppt_df.astype(float), order=my_order, seasonal_order=my_seasonal_order, enforce_stationarity=False)
                arima_model_fit = arima_model.fit(disp=0)
                output = arima_model_fit.forecast()
                sarimax_raster_staged.append(output)
            increment2 = increment2 + 1
            #if increment2 == 12:
                #break
        sarimax_raster.append(sarimax_raster_staged)
    #transpose the data into actionable insights
    npa_arima = np.asarray(sarimax_raster, dtype=np.float32)

    return npa_arima

#append all the numpy arrays into a list of numpy arrays for rasters
def read_dataset(bil_list, path_int, path_int2):
    raster_list_train = []
    raster_list_test = []
    year_list_train = []
    year_list_test = []
    for bil in bil_list:
        base = os.path.basename(bil)
        year = base[path_int:path_int2]
        #break the data into training set of 2/3 rasters
        if 1981 <= int(year) <= 2003:
            #load in precipitation raster bil
            width = 1405
            height = 621
            print(bil)
            with rasterio.open(bil, mode="r+") as src:
                raster = src.read(1, out_shape=(1, int(height), int(width)))
            raster_list_train.append(raster)
            year_list_train.append(str(year))
        #break the testing set into 1/3 rasters
        elif 2003 <= int(year) <= 2014:
            #load in raster bil
            width = 1405
            height = 621
            print(bil)
            with rasterio.open(bil, mode="r+") as src:
                raster_test = src.read(1, out_shape=(1, int(height), int(width)))
            raster_list_test.append(raster_test)
            year_list_test.append(str(year))

    raster_stacked_train = np.stack((raster_list_train), axis=-1)
    raster_stacked_testing = np.stack((raster_list_test), axis=-1)

    return raster_stacked_train, raster_stacked_testing, year_list_train, year_list_test

#get current working dir
cwd = os.getcwd()

#read in ppt as list of file directories
ppt_dir = cwd + '/ppt/'
ppt_bil_list = glob(os.path.join(ppt_dir, '*.bil'))
ppt_bil_list.sort()

ppt_raster_stacked_train, ppt_raster_stacked_testing, year_list_train, year_list_test = read_dataset(ppt_bil_list, 23, 27)

#use the linear regression function
npa_sarimax = raster_sarimax(ppt_raster_stacked_train)

#read in example from nino34 tif
with rasterio.open(ppt_bil_list[0]) as src:
    naip_data = src.read()
    naip_meta = src.profile
# make any necessary changes to raster properties, e.g.:
naip_meta['dtype'] = "float32"

pred_output_path_arima = "".join([cwd, "/ypred_training_arima", ".tif"])
with rasterio.open(pred_output_path_arima, 'w', **naip_meta) as dst:
    dst.write(npa_sarimax, 1)

#test the linear model on the split testing data
increment2 = 0
arima_raster_list_test = []
#arima_rmse_raster_test = []
dates = np.asarray(pd.date_range('1/1/2003', periods=11, freq='AS-JAN'))
#loop over list of index arrays and list of ppt arrays
for ppt, arima in zip(ppt_raster_stacked_testing, npa_sarimax):
    arima_raster_test = []
    #arima_rmse_raster = []
    #loop over index pixel and ppt pixel, run linear regression for list of year at each pixel
    for ppt_pix, arima_pix in zip(ppt, arima):
        if -9999 in ppt_pix:
            arima_raster_test.append(-9999)
            #arima_rmse_raster.append(-9999)
        else:
            ppt_df = pd.DataFrame(ppt_pix, index=dates, columns = {'A'})
            my_order = (1, 1, 1)
            my_seasonal_order = (1, 1, 1, 12)
            arima_model = SARIMAX(ppt_df.astype(float), order=my_order, seasonal_order=my_seasonal_order, enforce_stationarity=False)
            arima_model_fit = arima_model.fit()
            output = arima_model_fit.forecast()
            arima_raster_test.append(output)
            #arima_rmse = mean_squared_error(output, arima_pix, squared=False)
            #arima_rmse_raster.append(arima_rmse)
    #append each list of year of each pixel to list
    arima_raster_list_test.append(arima_raster_test)
    #arima_rmse_raster_test.append(arima_rmse_raster)
    increment2 = increment2 + 1
#transpose the data into actionable insights
arima_pred_testing = np.asarray(arima_raster_list_test, dtype=np.float32)
#arima_rmse_testing = np.asarray(arima_rmse_raster_test, dtype=np.float32)

#read in example from nino34 tif
with rasterio.open(ppt_bil_list[0]) as src:
    naip_data = src.read()
    naip_meta = src.profile
# make any necessary changes to raster properties, e.g.:
naip_meta['dtype'] = "float32"

arima_pred_path = "".join([cwd, "/arima_pred", ".tif"])
with rasterio.open(arima_pred_path, 'w', **naip_meta) as dst:
    dst.write(arima_pred_testing, 1)
#arima_rmse_output = "".join([cwd, "/arima_rmse_testing", ".tif"])
#with rasterio.open(arima_rmse_output, 'w', **naip_meta) as dst:
    #dst.write(arima_rmse_testing, 1)
'''
#test to see if i did it right
test_array = []
increment = 0
for i in ppt_raster_stacked:
    increment = increment + 1
    for ii in i:
        test_array.append(ii[10])
npa = np.asarray(test_array, dtype=np.float32)
test_array_reshape = npa.reshape(621, 1405)

test_false_true = np.array_equal(test_array_reshape, ppt_raster_list[10])
print(test_false_true)'''
