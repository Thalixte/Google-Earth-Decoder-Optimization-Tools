#  #
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 2
#   of the License, or (at your option) any later version.
#  #
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#  #
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#  #
#
#  <pep8 compliant>

import os
import shutil

import numpy as np

from constants import TORCH_LIB, SAMGEO_LIB
from utils import isolated_print
from utils.install_lib import install_python_lib
from PIL import Image, ImageSequence

try:
    import torch
except ModuleNotFoundError:
    install_python_lib(TORCH_LIB)

try:
    import samgeo
except ModuleNotFoundError:
    install_python_lib("numpy")
    install_python_lib("pycocotools-win")
    install_python_lib(SAMGEO_LIB)

from samgeo import tms_to_geotiff, split_raster, merge_rasters, get_basemaps, SamGeo
from samgeo.text_sam import LangSAM

import samgeo


def samgeo_sandbox(output_path, bbox=None, source_image=None):
    lbbox = [bbox[2], bbox[1], bbox[3], bbox[0]]
    zoom = 17
    isolated_print(get_basemaps().keys())

    sam = SamGeo(
        model_type="vit_h",
        sam_kwargs=None,
    )

    lbboxes = createZoneTable(2, westlimit=lbbox[0], southlimit=lbbox[1], eastlimit=lbbox[2], northlimit=lbbox[3])

    tiles_dir = os.path.join(output_path, "tiles")
    # masks_dir = os.path.join(output_path, "masks")

    try:
        shutil.rmtree(tiles_dir)
    except:
        pass

    os.makedirs(tiles_dir, exist_ok=True)

    for i, lbb in enumerate(lbboxes):
        image = 'satellite' + str(i) + '.tif'
        tms_to_geotiff(output=os.path.join(tiles_dir, image), bbox=lbb, zoom=zoom, source='Satellite', overwrite=True)

    if source_image is None:
        image = 'satellite.tif'
        merge_rasters(tiles_dir, os.path.join(output_path, image))

    im = Image.open(os.path.join(output_path, image))
    for i, page in enumerate(ImageSequence.Iterator(im)):
        output_png_path = os.path.join(output_path, image.replace(".tif", ".png"))
        fixTextureSizeForPackageCompilation(page)
        page.save(output_png_path)
    # else:
    #     image = source_image
    #
    # device = 'cuda' if torch.cuda.is_available() else 'cpu'
    # isolated_print(device, "selected")
    #
    # mask = "segments.tif"
    # sam.generate(
    #     os.path.join(output_path, image),
    #     os.path.join(output_path, mask),
    #     batch=True,
    #     foreground=True,
    #     erosion_kernel=(3, 3),
    #     mask_multiplier=255,
    #     device=device
    # )
    #
    # # Ensure to remove remaining cache folder
    # try:
    #     shutil.rmtree(tiles_dir)
    #     shutil.rmtree(masks_dir)
    # except:
    #     pass
    #
    # os.makedirs(masks_dir, exist_ok=True)
    #
    # # split_raster(os.path.join(output_path, image), out_dir=tiles_dir, tile_size=(1000, 1000), overlap=0)
    #
    # sam = LangSAM()
    #
    # text_prompt = "tree"
    #
    # # sam.predict_batch(
    # #     images=tiles_dir,
    # #     out_dir=masks_dir,
    # #     text_prompt=text_prompt,
    # #     box_threshold=0.26,
    # #     text_threshold=0.26,
    # #     mask_multiplier=255,
    # #     device=device,
    # #     dtype='uint8',
    # #     merge=True,
    # #     verbose=True,
    # # )
    #
    # # merge_rasters(masks_dir, os.path.join(output_path, "segment.tif"))
    #
    # shapefile = "segment.shp"
    # sam.raster_to_vector(os.path.join(output_path, "segment.tif"), os.path.join(output_path, shapefile))


def createZoneTable(zone_factor, westlimit, southlimit, eastlimit, northlimit):
    zone_table = list()
    longs = np.linspace(westlimit, eastlimit, zone_factor + 1)
    lats = np.linspace(southlimit, northlimit, zone_factor + 1)

    for i in range(0, len(longs) - 1):
        for j in range(0, len(lats) - 1):
            zone_table.append([longs[i], lats[j + 1], longs[i + 1], lats[j]])
    return zone_table


##################################################################
# fix texture final size for package compilation
##################################################################
def fixTextureSizeForPackageCompilation(image):
    new_img_width = image.size[0] + (4 - image.size[0] % 4)
    new_img_height = image.size[1] + (4 - image.size[1] % 4)
    isolated_print((new_img_width, new_img_height))
    image.resize((new_img_width, new_img_height))
