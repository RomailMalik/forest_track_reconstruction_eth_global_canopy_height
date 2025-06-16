/**
 * ETH Global Canopy Height Export Script (Brandenburg, Germany)
 * Dataset: ETH GCH 2020 (10m resolution)
 * Source: Sentinel-2 + GEDI fusion
 * Platform: Google Earth Engine Code Editor
 * 
 * This script clips the GCH raster to a Brandenburg AOI,
 * visualizes it, and exports both raster and metadata to Google Drive.
 * Paste and run inside https://code.earthengine.google.com/
 */

// Initialize Earth Engine
print('Earth Engine Initialized!');

// Define the Area of Interest (AOI) - Brandenburg Polygon
var aoi = ee.Geometry.Polygon([
  [11.826946704195572, 52.38653948900606],
  [12.602273243781426, 51.44772577911472],
  [13.788796681281426, 51.31401416466567],
  [14.810525196906426, 51.49220953763709],
  [14.538293715079496, 53.29095098264212],
  [14.038415785391996, 53.61478693047816],
  [11.830163832266996, 53.37951483085859],
  [11.170984144766996, 53.12316160513924],
  [11.826946704195572, 52.38653948900606]
]);

// Load the ETH Global Canopy Height dataset
var canopyHeight = ee.Image('users/nlang/ETH_GlobalCanopyHeight_2020_10m_v1')
  .clip(aoi); // Clip to AOI

// Visualize the Canopy Height data
var visParams = {
  min: 0,
  max: 50, // Adjust based on expected canopy heights
  palette: ['blue', 'green', 'yellow', 'orange', 'red']
};
Map.centerObject(aoi, 8);
Map.addLayer(canopyHeight, visParams, 'Canopy Height 2020');

// Export the Canopy Height data as a GeoTIFF to Google Drive
Export.image.toDrive({
  image: canopyHeight,
  description: 'Canopy_Height_Brandenburg_2020',
  folder: 'EarthEngine_Exports',
  fileNamePrefix: 'canopy_height_brandenburg_2020',
  region: aoi,
  scale: 10, // Dataset resolution is 10 meters
  crs: 'EPSG:4326',
  maxPixels: 1e13
});

// Metadata for research documentation
var metadata = ee.Feature(null, {
  'Dataset': 'ETH Global Canopy Height 2020 (10m)',
  'Year': '2020',
  'Resolution': '10 meters',
  'Source': 'GEDI, Sentinel-2, ALOS, auxiliary variables',
  'Region': 'Brandenburg, Germany'
});

// Export metadata to Google Drive as CSV
Export.table.toDrive({
  collection: ee.FeatureCollection([metadata]),
  description: 'Canopy_Height_Metadata_Brandenburg',
  folder: 'EarthEngine_Exports',
  fileNamePrefix: 'canopy_height_metadata_brandenburg',
  fileFormat: 'CSV'
});

print('Export tasks initiated. Check Google Drive for the outputs.');

