#Tiling and Labeling with OSM Using Enhanced Raster
#Generate 256x256 training tiles from enhanced raster and OSM labels

import os
import numpy as np
import rasterio
from rasterio.features import rasterize
from shapely.geometry import box
import geopandas as gpd
from tqdm import tqdm

# === Paths ===
raster_path = "data/canopy_height_10m_brandenburg_enhanced.tif"
gpkg_path = "data/osm_tracks_full_aoi.gpkg"
tile_size = 256
buffer_m = 2.5

out_img_dir = "data/tiles_rgb_gch"
out_lbl_dir = "data/tiles_labels_gch"
os.makedirs(out_img_dir, exist_ok=True)
os.makedirs(out_lbl_dir, exist_ok=True)

# === Load GPKG tracks ===
tracks = gpd.read_file(gpkg_path).to_crs("EPSG:4326")

# === Load raster ===
with rasterio.open(raster_path) as src:
    data = src.read().astype("float32")
    profile = src.profile
    bounds = src.bounds
    transform = src.transform
    res_x, res_y = transform[0], -transform[4]
    width, height = src.width, src.height

# === Build spatial index ===
sindex = tracks.sindex

# === Calculate pixel buffer ===
buffer_pix = int(buffer_m / res_x)
tile_id = 0

# === Iterate over tiles with pre-filtered geometries ===
for y in tqdm(range(0, height, tile_size), desc="Tiling rows"):
    row_geoms = []
    top_px = y
    bottom_px = y + tile_size
    if bottom_px > height:
        continue

    # Compute row bounds in geographic coords
    _, top = transform * (0, top_px)
    _, bottom = transform * (0, bottom_px)

    row_bounds = box(bounds.left, bottom, bounds.right, top)
    possible_idxs = list(sindex.intersection(row_bounds.bounds))
    row_tracks = tracks.iloc[possible_idxs]

    for x in range(0, width, tile_size):
        right_px = x + tile_size
        if right_px > width:
            continue

        # Crop image tile
        tile = data[:, y:y+tile_size, x:x+tile_size]
        if tile.shape[1] != tile_size or tile.shape[2] != tile_size:
            continue

        # Compute tile bounds
        left, top = transform * (x, y)
        right, bottom = transform * (x + tile_size, y + tile_size)
        tile_geom = box(left, bottom, right, top).buffer(buffer_m)

        # Filter geometries once
        tile_tracks = row_tracks[row_tracks.intersects(tile_geom)]
        shapes = [(geom, 1) for geom in tile_tracks.geometry]

        # Skip if no tracks
        if len(shapes) == 0:
            continue

        # Rasterize label
        label = rasterize(
            shapes,
            out_shape=(tile_size, tile_size),
            transform=rasterio.transform.from_bounds(left, bottom, right, top, tile_size, tile_size),
            fill=0,
            dtype="uint8"
        )

        # Skip if label too sparse
        if label.sum() < tile_size * tile_size * 0.005:
            continue

        # Save both
        np.save(f"{out_img_dir}/tile_{tile_id:05}.npy", tile)
        np.save(f"{out_lbl_dir}/tile_{tile_id:05}.npy", label)
        tile_id += 1

print(f"Done. {tile_id} tiles saved to {out_img_dir} and {out_lbl_dir}")
