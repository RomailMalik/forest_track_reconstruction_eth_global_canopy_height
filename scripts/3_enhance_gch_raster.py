# 3_enhance_canopy_raster.py
# Enhancing ETH Global Canopy Height Raster for CNN Training

import rasterio
from rasterio.windows import Window
from scipy.ndimage import sobel
import numpy as np
import os

# Input/output paths (adjust if needed)
raw_path = "data/canopy_height_10m_brandenburg.tif"
enhanced_path = "data/canopy_height_10m_brandenburg_enhanced.tif"

# Open input raster
with rasterio.open(raw_path) as src:
    profile = src.profile.copy()
    width, height = src.width, src.height

    # Update for 3-band float32 output
    profile.update({
        "count": 3,
        "dtype": "float32"
    })

    with rasterio.open(enhanced_path, "w", **profile) as dst:
        block_size = 1024
        for y in range(0, height, block_size):
            for x in range(0, width, block_size):
                w = min(block_size, width - x)
                h = min(block_size, height - y)
                window = Window(x, y, w, h)

                # Read and process tile
                canopy = src.read(1, window=window).astype("float32")

                dzdx = sobel(canopy, axis=1)
                dzdy = sobel(canopy, axis=0)
                sobel_mag = np.hypot(dzdx, dzdy)

                eps = 1e-6
                canopy_norm = (canopy - canopy.min()) / (canopy.max() - canopy.min() + eps)
                sobel_norm = (sobel_mag - sobel_mag.min()) / (sobel_mag.max() - sobel_mag.min() + eps)
                gradient_mag = sobel_norm.copy()

                stacked = np.stack([canopy_norm, sobel_norm, gradient_mag]).astype("float32")
                dst.write(stacked, window=window)

print("Enhanced raster saved successfully:", enhanced_path)
