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
from utils import install_python_lib
from constants import GEOIDS_DATASET_FOLDER, EGM2008_5_DATASET, PYGEODESY_LIB

try:
    import pygeodesy
except ModuleNotFoundError:
    install_python_lib(PYGEODESY_LIB)
    import pygeodesy

from pygeodesy.ellipsoidalKarney import LatLon


def get_geoid_height(lat, lon):
    interpolator = pygeodesy.GeoidKarney(os.path.join(GEOIDS_DATASET_FOLDER, EGM2008_5_DATASET))
    single_position = LatLon(lat, lon)
    h = interpolator(single_position)
    return h
