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

import torch
from samgeo import tms_to_geotiff, SamGeo

from constants import TORCH_LIB, SAMGEO_LIB
from utils import isolated_print
from utils.install_lib import install_python_lib

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

import samgeo

def samgeo_sandbox(output_path, bbox=None, source_image=None):
    isolated_print(bbox)
    if source_image is None:
        image = 'satellite.tif'
        tms_to_geotiff(output=image, bbox=bbox, zoom=20, source='Satellite')
    else:
        image = source_image

    checkpoint = os.path.join(output_path, 'sam_vit_h_4b8939.pth')
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    sam = SamGeo(
        checkpoint=checkpoint,
        model_type='vit_h',
        device=device,
        erosion_kernel=(3, 3),
        mask_multiplier=255,
        sam_kwargs=None,
    )

    mask = 'segment.tif'
    sam.generate(image, mask)

    vector = 'segment.gpkg'
    sam.tiff_to_gpkg(mask, vector, simplify_tolerance=None)