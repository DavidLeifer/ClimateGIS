# ClimateGIS
A pipeline for GIS climate raster data. A script of scripts, using GCP.</br>




+ [Support ClimateGIS](#support-climategis)
+ [Screenshots](#screenshots)
+ [Usage on Debian](#usage-on-debian)
+ [Summary](#summary)
+ [Features](#features)
+ [Used Libraries](#used-libraries)
+ [TODO](#todo)

### Support ClimateGIS
* Star and fork it on GitHub
* Contribute bug reports or suggest features
* Translate it into a different language

### Screenshots
1. Temperature Correlated with nino34 Index
2. Precipitation Correlated with nino34 Index
3. Mean January Temperature and Precipitation Grouped by Category
4. Difference between El Nino and Neutral years and La Nina and Neutral years
5. Twitter Sentiment Alongside Radar of the Polar Vortex 2019 Storm
6. The sixth app displays precipitation and CO2 correlation
7. The seventh app displays temperature and CO2 correlation

### Usage on Debian
1. Update `apt update`
2. Install Git `apt install git`
3. Clone Repository `git clone`
4. `cd ClimateGIS`
5. Make executable
6. Run the program `./pipeline.sh`

### Summary
ClimateGIS is a simple data pipeline at the intersection of climatological, computer science, and geospatial technologies. The processing occurs on a Google Cloud Platform Debian instance and is orchestrated by a BASH script, installing libraries required for Python, R, NPM, and compiling GDAL from source to generate XYZ tile files. Data is downloaded through an R script and a module called Prism to examine the El Nino-Southern Oscillation (ENSO), which is said to control precipitation and temperature in the Pacific North West and Southeastern United States.




By manipulating such Python libraries as Rasterio, GDAL, Geopandas, SciPy, Numpy, and Seaborn, correlation between the nino34 index and climate rasters has been achieved for 34 years of data. Analysis of the Variance of the Means (ANOVA) and mean groupings for El Nino, La Nina, and Neutral years are further used to examine spatial and statistical patterns. Tweepy, geocoder, and NLTK are also utilized to create geojson files of twitter sentiment to be displayed overlaid radar data of a winter storm event dubbed the Polar Vortex of 2019. NPM installs OpenLayers packages and are choreographed to generate space-time visualizations for display across multiple browsers and platforms.





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
  * Xarray: https://xarray.pydata.org/en/stable/
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


