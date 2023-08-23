# PolarbearGIS
A pipeline for GIS climate raster data. A script of scripts, using GCP.</br>




+ [Support PolarbearGIS](#support-polarbeargis)
+ [Screenshots](#screenshots)
+ [Usage on Debian](#usage-on-debian)
+ [Summary](#summary)
+ [Features](#features)
+ [Used Libraries](#used-libraries)
+ [TODO](#todo)
+ [GeoStreamable](#geostreamable)
+ [Polar Bears](#polar-bears)

### Support PolarbearGIS
* Polarbears are vulnerable!
* Star and fork it on GitLab
* Contribute bug reports or suggest features
* Translate it into a different language

### Screenshots
1. Temperature Correlated with nino34 Index
[![Temp](/polar_landing/images/temp_cor.png)](https://www.davidjleifer.com/pandamoniumGIS20210110_tmeanbuild/index.html)
2. Precipitation Correlated with nino34 Index
[![Temp](/polar_landing/images/ppt_cor.png)](https://www.davidjleifer.com/polarbearGIS/index.html)
3. Mean January Temperature and Precipitation Grouped by Oscillation
[![Temp](/polar_landing/images/Part2Section2.png)](https://www.davidjleifer.com/pandamoniumGIS_part2Section2_build-dist/index.html)
4. Difference between El Nino and Neutral years and La Nina and Neutral years
[![Temp](/polar_landing/images/difference-image.png)](https://www.davidjleifer.com/tha_difference-dist/index.html)
5. Twitter Sentiment Alongside Radar of the Polar Vortex 2019 Storm
[![Temp](/polar_landing/images/polar_radar.png)](https://www.davidjleifer.com/polar_radar/index.html)
6. The sixth app displays precipitation and CO2 correlation
[![Temp](/polar_landing/images/co2_cor_timeseries-dist.png)](https://www.davidjleifer.com/co2_cor_timeseries-dist/index.html)
7. The seventh app displays temperature and CO2 correlation
[![Temp](/polar_landing/images/co2_tmean_cor_timeseries.png)](https://www.davidjleifer.com/co2_tmean_cor_timeseries/index.html)

### Usage on Debian
1. Update `sudo apt update`
2. Install Git `sudo apt install git`
3. Clone Repository `sudo git clone https://gitlab.com/davleifer/polarbearGIS.git`
4. `cd polarbearGIS`
5. Make executable `sudo chmod u+x pipeline.sh`
6. Run the program `./pipeline.sh`

### Summary
PolarbearGIS is a simple data pipeline at the intersection of climatological, computer science, and geospatial technologies. The processing occurs on a Google Cloud Platform Debian instance and is orchestrated by a BASH script, installing libraries required for Python, R, NPM, and compiling GDAL from source to generate XYZ tile files. Data is downloaded through an R script and a module called Prism to examine the El Nino-Southern Oscillation (ENSO), which is said to control precipitation and temperature in the Pacific North West and Southeastern United States.




By manipulating such Python libraries as Rasterio, GDAL, Geopandas, SciPy, Numpy, and Seaborn, correlation between the nino34 index and climate rasters has been achieved for 34 years of data. Analysis of the Variance of the Means (ANOVA) and mean groupings for El Nino, La Nina, and Neutral years are further used to examine spatial and statistical patterns. Tweepy, geocoder, and NLTK are also utilized to create geojson files of twitter sentiment to be displayed overlaid radar data of a winter storm event dubbed the Polar Vortex of 2019. NPM installs OpenLayers packages and are choreographed to generate space-time visualizations for display across multiple browsers and platforms.




Some of the technical details are outlined in my blog, which can be found on my website and were generated using LibreOffice's save to HTML function. This is the most FOSS4G I could think of.

### Features
* Generation of a series of rasters from a csv index
* Correlation between two rasters
* Saving bils as geotifs
* Means of rasters grouped by a csv index
* ANOVA of rasters grouped by a csv index
* Splitting json by date and time and saving as geojson
* Performing point in polygon
* Building map applications
* Automated installation of libraries in the cloud
* Compiling GDAL from source
* HTTP/HTTPS load balancer
* Bears.

### Used Libraries
- Python
  * Rasterio: https://github.com/mapbox/rasterio
  * GDAL: https://github.com/OSGeo/gdal
  * GeoPandas: https://github.com/geopandas/geopandas
  * SciPy: https://github.com/scipy/scipy
  * NumPy: https://github.com/numpy/numpy
  * SeaBorn: https://github.com/mwaskom/seaborn
  * StreamHist: https://github.com/carsonfarmer/streamhist
  * Xarray: http://xarray.pydata.org/en/stable/
- R
  * Prism: https://github.com/ropensci/prism
- JavaScript
  * NPM: https://github.com/npm/cli
  * OpenLayers: https://github.com/openlayers/openlayers
  * ParcelBundler: https://github.com/parcel-bundler/parcel
  * OpenLayers-Ext: https://github.com/Viglino/ol-ext
  * jQuery: https://github.com/jquery/jquery
  * AngularJS Slider: https://github.com/angular-slider/angularjs-slider
- BASH
  * WGET: https://savannah.gnu.org/git/?group=wget
  * Git: https://github.com/git/git
  * R: https://www.r-project.org/
  * Build-Essential: https://packages.debian.org/sid/build-essential
  * LibCurl4: https://packages.debian.org/jessie/libcurl4-openssl-dev
  * Libssl-dev: https://packages.debian.org/jessie/libssl-dev
  * Pip: https://github.com/pypa/pip
  * Sqlite: https://github.com/sqlite/sqlite
  * GDAL: https://gdal.org/download.html

### TODO 
08/22/2021:</br>
- ~~use neural net regression for predictions (yay machine learning)~~
- ~~dockerize an app (yay devops)~~

### Polar Bears
![Polar Bears](/imgs/polar-bears.png?raw=true)




