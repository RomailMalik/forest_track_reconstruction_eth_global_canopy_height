# Downloading OSM Tracks for Forest Path Detection using QGIS

This step involves extracting OpenStreetMap (OSM) track data within the Brandenburg AOI using QGIS and the QuickOSM plugin. The downloaded vector data serves as ground truth labels for CNN training.

---

## Target Features

The following OSM `highway` values were extracted:

- `track`
- `path`
- `footway`
- `cycleway`
- `bridleway`
- `service`
- `unclassified`

---

## Tools Used

- **QGIS** (version 3.28 or similar)
- **QuickOSM plugin** (free and open-source)

---

## Step-by-Step Instructions

1. Open QGIS and install the **QuickOSM** plugin.
   - Go to *Plugins → Manage and Install Plugins* and search for “QuickOSM”.

2. Load your AOI:
   - You can use the raster `canopy_height_10m_brandenburg.tif` or any Brandenburg boundary shapefile as a reference.

3. Open QuickOSM:
   - From the QGIS top menu: *Vector → QuickOSM → QuickOSM*

4. Fill the form:
   - **Key**: `highway`
   - **Value**: `track;path;footway;cycleway;bridleway;service;unclassified`
   - **In**: Canvas extent (or custom polygon for AOI)
   - Click **“Run Query”**

5. Save the output:
   - Save the result as:  
     `osm_tracks_brandenburg.gpkg`  
     This file will be used for label generation in the CNN training pipeline.

---

## Output

- A `.gpkg` file containing all forest-related linear paths from OSM clipped to Brandenburg.
- Used for:
  - Label rasterization
  - Ground truth masks for supervised learning

---
