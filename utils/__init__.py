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

from .python_bin import *
from .install_lib import *

try:
    import numpy as np
except ModuleNotFoundError:
    install_python_lib("numpy", version=1.24)
    import numpy as np

try:
    import pygeodesy
except ModuleNotFoundError:
    install_python_lib("pygeodesy")
    import pygeodesy

try:
    import scipy
except ModuleNotFoundError:
    install_python_lib("scipy")
    import scipy

try:
    import shapely
except ModuleNotFoundError:
    install_python_lib("shapely")
    import shapely

from .colored_print import *
from .check_configuration import *
from .file_manip import *
from .msfs_sdk import *
from .octant import *
from .script_errors import *
from .settings import *
from .global_settings import *
from .xml import *
from .folders import *
from .backup import *
from .console import *
from .module import *
from .isolated_print import *
from .json import *
from .chunks import *
from .progress_bar import *
from .compressonator import *
from .script import *
from .geo_pandas import *
from .geometry import *
from .open_elevation import *
from .string import *
from .samgeo_utils import *
from .MapBoxDownloader import *
