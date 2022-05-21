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

# constants
CEND = "\033[0m"
BOLD = "\033[01m"
CRED = "\033[31m"
CGREEN = "\033[32m"
CORANGE = "\033[38;5;214m"
CREDBG = "\033[41m"
CGREENBG = "\033[6;30;42m"
OK = "OK"
KO = "KO"
EOL = "\n"
INI_FILE = "optimization_tools.ini"
MSFS_BUILD_EXE="fspackagetool.exe"
EARTH_RADIUS = 6371010

PNG_TEXTURE_FORMAT = "png"
JPG_TEXTURE_FORMAT = "jpg"

XML_FILE_EXT = ".xml"
GLTF_FILE_EXT = ".gltf"
BIN_FILE_EXT = ".bin"
DBF_FILE_EXT = ".dbf"
SHP_FILE_EXT = ".shp"
SHX_FILE_EXT = ".shx"
OSM_FILE_EXT = ".osm"
PNG_FILE_EXT = "." + PNG_TEXTURE_FORMAT
JPG_FILE_EXT = "." + JPG_TEXTURE_FORMAT

XML_FILE_PATTERN = "*" + XML_FILE_EXT
GLTF_FILE_PATTERN = "*" + GLTF_FILE_EXT
BIN_FILE_PATTERN = "*" + BIN_FILE_EXT
DBF_FILE_PATTERN = "*" + DBF_FILE_EXT
SHP_FILE_PATTERN = "*" + SHP_FILE_EXT
SHX_FILE_PATTERN = "*" + SHX_FILE_EXT
OSM_FILE_PATTERN = "*" + OSM_FILE_EXT
JPG_FILE_PATTERN = "*" + JPG_FILE_EXT
PNG_FILE_PATTERN = "*" + PNG_FILE_EXT

ENCODING = "utf-8"

XML_HEADER = '<?xml version="1.0"?>'

CLEAR_CONSOLE_CMD = "cls"

PYTHON_COMPIL_OPTION = "exec"

CONSTANTS_FOLDER = "constants"
UTILS_FOLDER = "utils"
SCRIPT_FOLDER = "scripts"
UI_FOLDER = "UI"
TEXTURE_FOLDER = "texture"

SCRIPT_PREFIX = "_script"
COLLIDER_SUFFIX = "_collider"

RESOURCE_FOLDER = "resource"
TEMPLATES_FOLDER = RESOURCE_FOLDER + "\\" + "templates"
THUMBNAIL_FOLDER = RESOURCE_FOLDER + "\\" + "thumbnail"
SHAPE_TEMPLATES_FOLDER = RESOURCE_FOLDER + "\\" + "shapes"
GEOIDS_DATASET_FOLDER = RESOURCE_FOLDER + "\\" + "geoids"
GEOIDS_DATASET_FOLDER = "C:\\MSFS SDK\\Google-Earth-Decoder-optimisation-tools\\resource\geoids"

BUSINESS_JSON_TEMPLATE = "Business.json"
PACKAGE_DEFINITIONS_TEMPLATE = "package-definition" + XML_FILE_EXT
PROJECT_DEFINITION_TEMPLATE = "project-definition" + XML_FILE_EXT
THUMBNAIL_PICTURE_TEMPLATE = "Thumbnail" + JPG_FILE_EXT
OSM_LAND_SHAPEFILE = "land_polygons" + SHP_FILE_EXT
EGM96_5_DATASET = "egm96-5.pgm"
EGM2008_5_DATASET = "egm2008-5.pgm"
EGM2008_1_DATASET = "egm2008-1.pgm"

PROJECT_DEFINITION_TEMPLATE_PATH = TEMPLATES_FOLDER + "\\" + PROJECT_DEFINITION_TEMPLATE
BUSINESS_JSON_TEMPLATE_PATH = TEMPLATES_FOLDER + "\\" + BUSINESS_JSON_TEMPLATE
PACKAGE_DEFINITIONS_TEMPLATE_PATH = TEMPLATES_FOLDER + "\\" + PACKAGE_DEFINITIONS_TEMPLATE
THUMBNAIL_PICTURE_TEMPLATE_PATH = THUMBNAIL_FOLDER + "\\" + THUMBNAIL_PICTURE_TEMPLATE

LILY_TEXTURE_PACKER_ADDON = "LilyTexturePacker"

MAX_PHOTOGRAMMETRY_LOD = 23

TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX = "target_min_size_value_"

SHAPE_DISPLAY_NAME = "GEDOT_generated_shape"
HEIGHT_MAPS_DISPLAY_NAME = "GEDOT_generated_height_maps"

PROJECT_INI_SECTION = "PROJECT"
MERGE_INI_SECTION = "MERGE"
TILE_INI_SECTION = "TILE"
LODS_INI_SECTION = "LODS"
MSFS_SDK_INI_SECTION = "MSFS_SDK"
BUILD_INI_SECTION = "AUTOMATIC_BUILD"
COMPRESSONATOR_INI_SECTION = "COMPRESSONATOR"
BACKUP_INI_SECTION = "BACKUP"
PYTHON_INI_SECTION = "PYTHON"

NONE_ICON = "NONE"
FILE_FOLDER_ICON="FILE_FOLDER"
FILE_TICK_ICON = "FILE_TICK"
FILE_REFRESH_ICON = "FILE_REFRESH"
INFO_ICON = "INFO"
ADD_ICON = "ADD"
REMOVE_ICON = "REMOVE"

DUMMY_OBJECT = "dummy"

LANDUSE_OSM_KEY = "landuse"
LEISURE_OSM_KEY = "leisure"
NATURAL_OSM_KEY = "natural"
WATER_OSM_KEY = "water"
AEROWAY_OSM_KEY = "aeroway"
BOUNDARY_OSM_KEY = "boundary"
BOUNDING_BOX_OSM_KEY = "box"

FOREST_OSM_TAG = "forest"
NATURE_RESERVE_OSM_TAG = "nature_reserve"
FARMLAND_OSM_TAG = "farmland"
MEADOW_OSM_TAG = "meadow"
VINEYARD_OSM_TAG = "vineyard"
PARK_OSM_TAG = "park"
PLAYGROUND_OSM_TAG = "playground"
GRASS_OSM_TAG = "grass"
WOOD_OSM_TAG = "wood"
WATER_OSM_TAG = "water"
RIVER_OSM_TAG = "river"
STREAM_OSM_TAG = "stream"
SEA_OSM_TAG = "sea"
LAKE_TAG = "lake"
GRASSLAND_OSM_TAG = "grassland"
SCRUB_OSM_TAG = "scrub"
POND_OSM_TAG = "pond"
WASTEWATER_OSM_TAG = "wastewater"
CANAL_OSM_TAG = "canal"
BASIN_OSM_TAG = "basin"
ALLOTMENTS_OSM_TAG = "allotment"
HEATH_OSM_TAG = "heath"
WETLAND_OSM_TAG = "wetland"
BARE_ROCK_OSM_TAG = "bare_rock"
COASTLINE_OSM_TAG = "coastline"
GEOMETRY_OSM_COLUMN = "geometry"
MARITIME_OSM_KEY = "maritime"
NATIONAL_PARK_OSM_KEY = "national_park"
PROTECTED_AREA_OSM_KEY = "protected_area"
MARINA_OSM_TAG = "marina"
PIER_OSM_TAG = "pier"
RESIDENTIAL_OSM_TAG = "residential"
HEIGHT_OSM_TAG = "height"

EXCLUSION_OSM_FILE_PREFIX = "exclusion"
BOUNDING_BOX_OSM_FILE_PREFIX = "bbox"

FEET_TO_METER_RATIO = 0.3048

OSM_TAGS = {
    BOUNDARY_OSM_KEY: [
        FOREST_OSM_TAG,
        MARITIME_OSM_KEY,
        NATIONAL_PARK_OSM_KEY
    ],
    LANDUSE_OSM_KEY: [
        FOREST_OSM_TAG,
        NATURE_RESERVE_OSM_TAG,
        FARMLAND_OSM_TAG,
        MEADOW_OSM_TAG,
        VINEYARD_OSM_TAG,
        ALLOTMENTS_OSM_TAG,
        COASTLINE_OSM_TAG
    ],
    LEISURE_OSM_KEY: [
        PARK_OSM_TAG,
        PLAYGROUND_OSM_TAG,
        NATURE_RESERVE_OSM_TAG
    ],
    NATURAL_OSM_KEY: [
        WOOD_OSM_TAG,
        WATER_OSM_TAG,
        RIVER_OSM_TAG,
        STREAM_OSM_TAG,
        SEA_OSM_TAG,
        GRASSLAND_OSM_TAG,
        SCRUB_OSM_TAG,
        WETLAND_OSM_TAG,
        COASTLINE_OSM_TAG
    ],
    WATER_OSM_KEY: [
        RIVER_OSM_TAG,
        STREAM_OSM_TAG,
        SEA_OSM_TAG,
        LAKE_TAG,
        WATER_OSM_KEY,
        POND_OSM_TAG,
        WASTEWATER_OSM_TAG,
        CANAL_OSM_TAG,
        BASIN_OSM_TAG,
        MARINA_OSM_TAG,
        PIER_OSM_TAG
    ],
    AEROWAY_OSM_KEY: []
}

