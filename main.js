import 'ol/ol.css';
import Map from 'ol/Map';
import Stamen from 'ol/source/Stamen';
import TileLayer from 'ol/layer/Tile';
import TileWMS from 'ol/source/TileWMS';
import GeoJSON from 'ol/format/GeoJSON';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import Layer from 'ol/layer/Layer';
import View from 'ol/View';
import {getCenter} from 'ol/extent';
import {transformExtent} from 'ol/proj';
import {transform} from 'ol/proj';
import {Style, Fill, Stroke, Circle} from 'ol/style';
import 'regenerator-runtime/runtime';

const geojson = [
                  ".data/2019-01-29 18/30/00.geojson"
]
console.log(geojson)

//create extent and use it in the VectorLayer called all_ween
var extent = transformExtent([-89.30, 24.71, -64.70, 48.07], 'EPSG:4326', 'EPSG:3857');

//define make before adding to it
var map = new Map({
  target: 'map',
  view: new View({
    center: transform([-77.3765, 38.1667], 'EPSG:4326', 'EPSG:3857'),
    zoom: 5,
  }),
});

//define basemap and radar as a TileLayer
const basemap = new TileLayer({
  source: new Stamen({
    layer: 'terrain',
  }),
});
const radar = new TileLayer({
  extent: extent,
  source: new TileWMS({
    attributions: ['Iowa State University'],
    url: 'https://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r-t.cgi',
    params: {'LAYERS': 'nexrad-n0r-wmst'},
  }),
});

/* Add to map */
map.addLayer(basemap);
map.addLayer(radar);

//empty array for our dates and all_ween_array
var dates = [];
var all_ween_array = [];
//loop over each property of the geojson object and add it to the all_ween_array
for (const property in geojson) {
    const ween = new VectorSource({
      url: geojson[property],
      format: new GeoJSON(),
    });
    //create the layers for the point_changer function
    const all_ween = new VectorLayer({
      extent: extent,
      source: ween,
    });
    //push property (our datetime) to empty array called dates
    const property_t = property.replace(/\s/g, 'T')
    dates.push(property_t + ".000Z")
    //push layer to empty all_ween_array
    all_ween_array.push(all_ween)
    //console.log(`${property}: ${geojson[property]}`);
};

//event listener to change the layers, depends on the key
radar.addEventListener('change', point_changer, false);
function point_changer(){
  var el = document.getElementById('date_value').textContent;
  //console.log(el)
  Object.keys(all_ween_array).forEach(function(key){
    if (el == dates[key]){
      map.addLayer(all_ween_array[key]);
      //console.log(all_ween_array[key])
    }
    else {
      map.removeLayer(all_ween_array[key]);
    }
  });
};

//fill vars
var white = new Fill({color: 'white'});
var green = new Fill({color: 'green'});
var red = new Fill({color: 'red'});
//rgba opacity
var invis = new Fill({color: 'rgba(255, 0, 0, 0)'});

//create color style vars
var white_style = new Style({
      image: new Circle({
        radius: 7,
        fill: white,
        stroke: new Stroke({
          color: [255,255,255], width: 2
        })
      })
});
var green_style = new Style({
      image: new Circle({
        radius: 7,
        fill: green,
        stroke: new Stroke({
          color: [255,255,255], width: 2
        })
      })
});
var red_style = new Style({
      image: new Circle({
        radius: 7,
        fill: red,
        stroke: new Stroke({
          color: [255,255,255], width: 2
        })
      })
});
var invis_style = new Style({
      image: new Circle({
        radius: 0,
        fill: invis,
        stroke: new Stroke({
          color: [255,255,255,0], width: 0
        })
      })
});

//apply invis style so when the layer is loaded async the default style goes away
for (const l in all_ween_array) {
  all_ween_array[l].setStyle(invis_style);
};

//Proimise and await. who came up with that, its a(time)sync function
function resolveAfter2Seconds(x) {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve(x);
    }, 500);
    radar.addEventListener('change', style_points, false);
  });
};
async function style_points() {
  var x = await resolveAfter2Seconds(10);
  for (const k in all_ween_array) {
    all_ween_array[k].getSource().forEachFeature(function(feature){
      if ((feature.get('compound') === 0)) {
        feature.setStyle(white_style)
      }
      else if (feature.get('compound') > 0) {
        feature.setStyle(green_style)
      }
      else{
        feature.setStyle(red_style)
      }
    })
  }
};
style_points();

//define the slider and do some stuff
var sliderRange = document.getElementById("myRange");
sliderRange.max = dates.length-1;

var dateValue = document.getElementById("date_value");
dateValue.innerHTML = dates[sliderRange.value];
radar.getSource().updateParams({'TIME': dates[sliderRange.value]});

//split dates array object and put into two arrays date_date and time
var date_date = [];
var time = [];
for (var i in dates){
  var date_part = dates[i].substring(0, dates[i].indexOf("T"));
  var time_part_0 = dates[i].substring(dates[i].indexOf("T") + 1);
  var time_part = time_part_0.substring(0, time_part_0.indexOf(":00."));
  date_date.push(date_part)
  time.push(time_part)
}

//put into dateSub id
var dateSub = document.getElementById("date_sub");
dateSub.innerHTML = date_date[sliderRange.value];

//put into timeSub id
var time_sub = document.getElementById("time_sub");
time_sub.innerHTML = time[sliderRange.value];

// Update the current slider value (each time you drag the slider handle)
sliderRange.oninput = function() {
  dateValue.innerHTML = dates[this.value];
  dateSub.innerHTML = date_date[this.value];
  time_sub.innerHTML = time[this.value];
  radar.getSource().updateParams({'TIME': dates[this.value]});
};
