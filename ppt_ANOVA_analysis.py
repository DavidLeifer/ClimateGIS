import rasterio
import rasterio.plot
from rasterio.plot import show
import numpy as np
import pandas as pd
import pyproj
import seaborn as sns
import scipy.stats as stats
import os
from glob import glob

#https://gis.stackexchange.com/questions/244376/computing-mean-of-all-rasters-in-a-directory-using-python
def read_file(file):
    with rasterio.open(file) as src:
        return(src.read(1))

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

#create list of el nino files based on year from elnino varible
data_dir = cwd + '/data/ppt/*'
data_dir_list = glob(data_dir)
#create a list of bil paths from each sub folder
folder_bil_list = []
for i in data_dir_list:
    folder_bil = glob(os.path.join(i, '*.bil'))
    folder_bil_list.append(folder_bil)
#create list of el nino files based on year from elnino varible
df2 = pd.DataFrame(folder_bil_list)
elnino_list = elnino['Year'].tolist()
df4 = []
for nin in elnino_list:
    df3 = df2[df2[0].str.contains(str(nin))]
    df4.append(df3)
df5 = pd.concat(df4)
elninolist2 = df5[0].tolist()

#create list of la nina files based on year from lanina varible
df2 = pd.DataFrame(folder_bil_list)
lanina_list = lanina['Year'].tolist()
df4 = []
for lan in lanina_list:
    df3 = df2[df2[0].str.contains(str(lan))]
    df4.append(df3)
df5 = pd.concat(df4)
lanina_list2 = df5[0].tolist()

#create list of neither files based on year from neither varible
df2 = pd.DataFrame(folder_bil_list)
neither_list = neither['Year'].tolist()
df4 = []
for nei in neither_list:
	df3 = df2[df2[0].str.contains(str(nei))]
	df4.append(df3)
df5 = pd.concat(df4)
neither_list2 = df5[0].tolist()

#el nino array list
elnino_array_list = [read_file(x) for x in elninolist2]
elnino_array_out = np.mean(elnino_array_list, axis=0)
#calculate average of neither arrays
# Read all data as a list of numpy arrays 
neutral_array_list = [read_file(x) for x in neither_list2]
# Perform averaging
neautral_array_out = np.mean(neutral_array_list, axis=0)
#calculate average of la nina arrays
# Read all data as a list of numpy arrays 
lanina_array_list = [read_file(x) for x in lanina_list2]
# Perform averaging
lanina_array_out = np.mean(lanina_array_list, axis=0)

#one way ANOVA for PPT (cm)
#remove nodata, in this case -9999.0, doesnt preserve but creates list
arr = lanina_array_out[lanina_array_out != -9999.0]
arr2 = neautral_array_out[neautral_array_out != -9999.0]
arr3 = elnino_array_out[elnino_array_out != -9999.0]
ppt_ANOVA = str(stats.f_oneway(arr, arr2, arr3))
#write anova to txt file
ppt_ANOVA_output = cwd + "/data/ppt_ANOVA_output.txt"
with open(ppt_ANOVA_output, 'w') as f:
    f.write(ppt_ANOVA)

