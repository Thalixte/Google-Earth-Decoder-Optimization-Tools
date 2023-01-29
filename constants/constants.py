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
CORANGEBG = "\033[6;30;43m"
OK = "OK"
KO = "KO"
EOL = "\n"
INI_FILE = "optimization_tools.ini"
MSFS_BUILD_EXE = "fspackagetool.exe"
EARTH_RADIUS = 6371010

ROAD_LANE_WIDTH = 3.0

PNG_TEXTURE_FORMAT = "png"
JPG_TEXTURE_FORMAT = "jpg"

ZIP_FILE_EXT = ".zip"
TXT_FILE_EXT = ".txt"
WHL_FILE_EXT = ".whl"
XML_FILE_EXT = ".xml"
GLTF_FILE_EXT = ".gltf"
BIN_FILE_EXT = ".bin"
DBF_FILE_EXT = ".dbf"
SHP_FILE_EXT = ".shp"
SHX_FILE_EXT = ".shx"
OSM_FILE_EXT = ".osm"
OBJ_FILE_EXT = ".obj"
POS_FILE_EXT = ".pos"
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
OBJ_FILE_PATTERN = "*" + OBJ_FILE_EXT

ENCODING = "utf-8"

XML_HEADER = '<?xml version="1.0"?>'

CLEAR_CONSOLE_CMD = "cls"

PYTHON_COMPIL_OPTION = "exec"

PILLOW_LIB = "Pillow"
OSMNX_LIB = "osmnx"
NETWORKX_LIB = "networkx"
RTREE_LIB = "rtree"
MATPLOTLIB_LIB = "matplotLib"
PANDAS_LIB = "pandas"
GEOPANDAS_LIB = "geopandas"
SHAPELY_LIB = "shapely"
PYGEODESY_LIB = "pygeodesy"
ALTERNATE_PYTHON_LIB_REPO = "https://download.lfd.uci.edu/pythonlibs/archived/"
GDAL_LIB_PREFIX = "GDAL-3.4.3"
FIONA_LIB_PREFIX = "Fiona-1.8.21"
WIN32_SUFFIX = "win32"
WIN64_SUFFIX = "win_amd64"

LAND_MASS_REPO = "https://osmdata.openstreetmap.de/download/"
LAND_MASS_ARCHIVE = "land-polygons-split-4326.zip"

CONSTANTS_FOLDER = "constants"
UTILS_FOLDER = "utils"
SCRIPT_FOLDER = "scripts"
UI_FOLDER = "UI"
TEXTURE_FOLDER = "texture"
CLEANUP_3D_DATA_BACKUP_FOLDER = "cleanup_3d_data"

SCRIPT_PREFIX = "_script"
COLLIDER_SUFFIX = "_collider"
GEOCODE_SUFFIX = "_geocode"
HEIGHT_MAP_PREFIX = "height_map_"

RESOURCE_FOLDER = "resource"
TEMPLATES_FOLDER = RESOURCE_FOLDER + "\\" + "templates"
THUMBNAIL_FOLDER = RESOURCE_FOLDER + "\\" + "thumbnail"
SHAPE_TEMPLATES_FOLDER = RESOURCE_FOLDER + "\\" + "shapes"
GEOIDS_DATASET_FOLDER = RESOURCE_FOLDER + "\\" + "geoids"

BUSINESS_JSON_TEMPLATE = "Business.json"
PACKAGE_DEFINITIONS_TEMPLATE = "package-definition" + XML_FILE_EXT
PROJECT_DEFINITION_TEMPLATE = "project-definition" + XML_FILE_EXT
THUMBNAIL_PICTURE_TEMPLATE = "Thumbnail" + JPG_FILE_EXT
OSM_LAND_SHAPEFILE = "land_polygons" + SHP_FILE_EXT
EGM2008_5_DATASET = "egm2008-5.pgm"

PROJECT_DEFINITION_TEMPLATE_PATH = TEMPLATES_FOLDER + "\\" + PROJECT_DEFINITION_TEMPLATE
BUSINESS_JSON_TEMPLATE_PATH = TEMPLATES_FOLDER + "\\" + BUSINESS_JSON_TEMPLATE
PACKAGE_DEFINITIONS_TEMPLATE_PATH = TEMPLATES_FOLDER + "\\" + PACKAGE_DEFINITIONS_TEMPLATE
THUMBNAIL_PICTURE_TEMPLATE_PATH = THUMBNAIL_FOLDER + "\\" + THUMBNAIL_PICTURE_TEMPLATE

LILY_TEXTURE_PACKER_ADDON = "LilyTexturePacker"

MAX_PHOTOGRAMMETRY_LOD = 23
LESS_DETAILED_LODS_LIMIT = 18

TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX = "target_min_size_value_"

LIGHT_WARM_GUID = "{DB0162E7-91A2-46E9-81B7-55A66CEC8839}"
LIGHT_COLD_GUID = "{8EF4C350-65F3-455B-AF52-64511D7F9510}"
LIGHT_WARM_DISPLAY_NAME = "Light warm"
LIGHT_COLD_DISPLAY_NAME = "Light cold"
LIGHT_HEADING = "-179.999995"

PITCH_TERRAFORM_POLYGONS_DISPLAY_NAME = "GEDOT_generated_pitch_terraform_polygons"
AMENITY_TERRAFORM_POLYGONS_DISPLAY_NAME = "GEDOT_generated_amenity_terraform_polygons"
CONSTRUCTION_TERRAFORM_POLYGONS_DISPLAY_NAME = "GEDOT_generated_construction_terraform_polygons"
INDUSTRIAL_TERRAFORM_POLYGONS_DISPLAY_NAME = "GEDOT_generated_industrial_terraform_polygons"
GOLF_TERRAFORM_POLYGONS_DISPLAY_NAME = "GEDOT_generated_golf_terraform_polygons"
EXCLUSION_BUILDING_POLYGONS_DISPLAY_NAME = "GEDOT_generated_exclusion_building_polygons"
EXCLUSION_VEGETATION_POLYGONS_DISPLAY_NAME = "GEDOT_generated_exclusion_vegetation_polygons"
HEIGHT_MAPS_DISPLAY_NAME = "GEDOT_generated_height_maps"
HEIGHT_MAP_DISPLAY_NAME = "GEDOT_generated_height_map"

PROJECT_INI_SECTION = "PROJECT"
MERGE_INI_SECTION = "MERGE"
TILE_INI_SECTION = "TILE"
LODS_INI_SECTION = "LODS"
OSM_INI_SECTION = "OPENSTREETMAP"
GEOCODE_INI_SECTION = "GEOCODE"
ALTITUDE_ADJUSTMENT_INI_SECTION = "ALTITUDE_ADJUSTMENT"
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

OSM_MATERIAL_NAME = "OSM_material"

WAY_OSM_PREFIX = "W"
RELATION_OSM_PREFIX = "R"
NODE_OSM_PREFIX = "N"

LANDUSE_OSM_KEY = "landuse"
LEISURE_OSM_KEY = "leisure"
NATURAL_OSM_KEY = "natural"
NATURAL_WATER_OSM_KEY = "natural_water"
WATER_OSM_KEY = "water"
WATERWAY_OSM_KEY = "waterway"
AEROWAY_OSM_KEY = "aeroway"
BOUNDARY_OSM_KEY = "boundary"
BOUNDING_BOX_OSM_KEY = "box"
RESIDENTIAL_OSM_KEY = "residential"
INDUSTRIAL_OSM_KEY = "industrial"
AMENITY_OSM_KEY = "amenity"
BUILDING_OSM_KEY = "building"
ROCKS_OSM_KEY = "rocks"
ROAD_OSM_KEY = "highway"
RAILWAY_OSM_KEY = "railway"
SERVICE_OSM_KEY = "service"
MAN_MADE_OSM_KEY = "man_made"
GROUND_OSM_KEY = "ground"
PITCH_OSM_KEY = "pitch"
CONSTRUCTION_OSM_KEY = "construction"
GRASS_OSM_KEY = "grass"
GOLF_OSM_KEY = "golf"
PARK_OSM_KEY = "park"
WALL_OSM_KEY = "wall"
NOT_SHORE_WATER_OSM_KEY = "not_shore",
NOT_EXCLUSION_BUILDING_OSM_KEY = "not_exclusion_building",
ROAD_REMOVAL_LANDUSE_OSM_KEY = "road_removal_landuse"
ROAD_REMOVAL_NATURAL_OSM_KEY = "road_removal_natural"
ELEMENT_TY_OSM_KEY = "element_ty"
OSMID_OSM_KEY = "osmid"
LANES_OSM_KEY = "lanes"
ONEWAY_OSM_KEY = "oneway"
BARRIER_OSM_KEY = "barrier"
LAT_OSM_KEY = "lat"
LON_OSM_KEY = "lon"

FOREST_OSM_TAG = "forest"
NATURE_RESERVE_OSM_TAG = "nature_reserve"
FARMLAND_OSM_TAG = "farmland"
MEADOW_OSM_TAG = "meadow"
VINEYARD_OSM_TAG = "vineyard"
PARK_OSM_TAG = "park"
PLAYGROUND_OSM_TAG = "playground"
PITCH_OSM_TAG = "pitch"
GRASS_OSM_TAG = "grass"
WOOD_OSM_TAG = "wood"
BAY_OSM_TAG = "bay"
WATER_OSM_TAG = "water"
RIVER_OSM_TAG = "river"
STREAM_OSM_TAG = "stream"
SEA_OSM_TAG = "sea"
LAKE_OSM_TAG = "lake"
BEACH_OSM_TAG = "beach"
GRASSLAND_OSM_TAG = "grassland"
SCRUB_OSM_TAG = "scrub"
POND_OSM_TAG = "pond"
WASTEWATER_OSM_TAG = "wastewater"
RESERVOIR_OSM_TAG = "reservoir"
CANAL_OSM_TAG = "canal"
BASIN_OSM_TAG = "basin"
ALLOTMENTS_OSM_TAG = "allotment"
HEATH_OSM_TAG = "heath"
WETLAND_OSM_TAG = "wetland"
BARE_ROCK_OSM_TAG = "bare_rock"
CLIFF_OSM_TAG = "cliff"
FELL_OSM_TAG = "fell"
COASTLINE_OSM_TAG = "coastline"
GEOMETRY_OSM_COLUMN = "geometry"
MARITIME_OSM_KEY = "maritime"
NATIONAL_PARK_OSM_KEY = "national_park"
PROTECTED_AREA_OSM_KEY = "protected_area"
MARINA_OSM_TAG = "marina"
PIER_OSM_TAG = "pier"
HEIGHT_OSM_TAG = "height"
TREE_TAG = "tree"
TREE_ROW_TAG = "tree_row"
ORCHARD_OSM_TAG = "orchard"
BRIDGE_OSM_TAG = "bridge"
TUNNEL_OSM_TAG = "tunnel"
SEAMARK_TYPE_OSM_TAG = "seamark:type"
SLIPWAY_OSM_TAG = "slipway"
PEDESTRIAN_OSM_TAG = "pedestrian"
FOOTWAY_OSM_TAG = "footway"
PATH_OSM_TAG = "path"
FAIRWAY_OSM_TAG = "fairway"
AREA_OSM_TAG = "area"
CONSTRUCTION_OSM_TAG = "construction"
RESIDENTIAL_OSM_TAG = "residential"
INDUSTRIAL_OSM_TAG = "industrial"
DISPLAY_NAME_OSM_TAG = "display_name"
NAME_OSM_TAG = "name"
WALL_OSM_TAG = "wall"
CASTLE_WALL_OSM_TAG = "castle_wall"
WATERMILL_OSM_TAG = "watermill"
TOWER_OSM_TAG = "tower"
MAST_OSM_TAG = "mast"
BREAKWATER_OSM_TAG = "breakwater"
STORAGE_TANK_OSM_TAG = "storage_tank"
WORKS_OSM_TAG = "works"
CHIMNEY_OSM_TAG = "chimney"
OBELISK_OSM_TAG = "obelisk"
SILO_OSM_TAG = "silo"
TELESCOPE_OSM_TAG = "telescope"
WATER_TOWER_OSM_TAG = "water_tower"
OBSERVATORY_OSM_TAG = "observatory"
PROPOSED_OSM_TAG = "proposed"

AIRPORT_GEOCODE = "airport"

EXCLUSION_OSM_FILE_PREFIX = "exclusion"
ISOLATION_OSM_FILE_PREFIX = "isolation"
BOUNDING_BOX_OSM_FILE_PREFIX = "bbox"
WHOLE_WATER_OSM_FILE_PREFIX = "whole_water"
BUILDING_OSM_FILE_PREFIX = "building"
GEOCODE_OSM_FILE_PREFIX = "geocode"
LANDMARK_LOCATION_OSM_FILE_NAME = GEOCODE_OSM_FILE_PREFIX + "_landmark_location"

GEOCODE_LIGHTS_PREFIX = GEOCODE_OSM_FILE_PREFIX + "_lights"

FEET_TO_METER_RATIO = 0.3048
TILE_THICKNESS = 0.5

MOTORWAY_ROAD_TYPE = "motorway"
TRUNK_ROAD_TYPE = "trunk"
MOTORWAY_LINK_ROAD_TYPE = "motorway_link"
PRIMARY_ROAD_TYPE = "primary"
SECONDARY_ROAD_TYPE = "secondary"
TERTIARY_ROAD_TYPE = "tertiary"
RESIDENTIAL_ROAD_TYPE = "residential"
PEDESTRIAN_ROAD_TYPE = "pedestrian"
FOOTWAY_ROAD_TYPE = "footway"
CYCLEWAY_ROAD_TYPE = "cycleway"
SERVICE_ROAD_TYPE = "service"
RAILWAY_ROAD_TYPE = "railway"
PATH_ROAD_TYPE = "path"
TRACK_ROAD_TYPE = "track"

FULL_PREFIX = "full_"

POI_LANDMARK_FORMAT_TYPE = "POI"
CITY_LANDMARK_FORMAT_TYPE = "City"

STANDARD_EXCLUSION_MARGIN = 10.0

ROAD_WITH_BORDERS = [
    MOTORWAY_ROAD_TYPE,
    TRUNK_ROAD_TYPE,
    MOTORWAY_LINK_ROAD_TYPE,
    PRIMARY_ROAD_TYPE,
    SECONDARY_ROAD_TYPE,
    TERTIARY_ROAD_TYPE
]

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
        VINEYARD_OSM_TAG,
        ALLOTMENTS_OSM_TAG,
        ORCHARD_OSM_TAG,
        MEADOW_OSM_TAG
    ],
    LEISURE_OSM_KEY: [
        NATURE_RESERVE_OSM_TAG
    ],
    NATURAL_OSM_KEY: [
        FOREST_OSM_TAG,
        WOOD_OSM_TAG,
        GRASSLAND_OSM_TAG,
        SCRUB_OSM_TAG,
        FELL_OSM_TAG
    ],
    WATER_OSM_KEY: [
        RIVER_OSM_TAG,
        STREAM_OSM_TAG,
        SEA_OSM_TAG,
        LAKE_OSM_TAG,
        WATER_OSM_KEY,
        POND_OSM_TAG,
        WASTEWATER_OSM_TAG,
        CANAL_OSM_TAG,
        BASIN_OSM_TAG,
        MARINA_OSM_TAG,
        RESERVOIR_OSM_TAG
    ],
    NATURAL_WATER_OSM_KEY: [
        BAY_OSM_TAG,
        WATER_OSM_TAG,
        RIVER_OSM_TAG,
        STREAM_OSM_TAG,
        SEA_OSM_TAG,
        WETLAND_OSM_TAG,
        BEACH_OSM_TAG
    ],
    WATERWAY_OSM_KEY: [
        RIVER_OSM_TAG,
        CANAL_OSM_TAG
    ],
    AEROWAY_OSM_KEY: [],
    ROCKS_OSM_KEY: [
        BARE_ROCK_OSM_TAG,
        CLIFF_OSM_TAG
    ],
    PITCH_OSM_KEY: [
        PITCH_OSM_TAG
    ],
    CONSTRUCTION_OSM_KEY: [
        CONSTRUCTION_OSM_TAG
    ],
    RESIDENTIAL_OSM_KEY: [
        RESIDENTIAL_OSM_TAG
    ],
    INDUSTRIAL_OSM_KEY: [
        INDUSTRIAL_OSM_TAG
    ],
    GRASS_OSM_KEY: [
        GRASS_OSM_TAG
    ],
    GOLF_OSM_KEY: [
        FAIRWAY_OSM_TAG
    ],
    PARK_OSM_KEY: [
        PARK_OSM_TAG
    ],
    NOT_SHORE_WATER_OSM_KEY: [
        WATER_OSM_KEY,
        POND_OSM_TAG,
        WASTEWATER_OSM_TAG,
        CANAL_OSM_TAG,
        BASIN_OSM_TAG,
        RESERVOIR_OSM_TAG,
        WETLAND_OSM_TAG,
        RIVER_OSM_TAG,
        LAKE_OSM_TAG,
        STREAM_OSM_TAG
    ],
    NOT_EXCLUSION_BUILDING_OSM_KEY: [
        WATER_OSM_KEY,
        POND_OSM_TAG,
        WASTEWATER_OSM_TAG,
        CANAL_OSM_TAG,
        BASIN_OSM_TAG,
        RESERVOIR_OSM_TAG,
        WETLAND_OSM_TAG
    ],
    BARRIER_OSM_KEY: [
        WALL_OSM_TAG
    ],
    MAN_MADE_OSM_KEY: [
        WATERMILL_OSM_TAG,
        TOWER_OSM_TAG,
        MAST_OSM_TAG,
        BREAKWATER_OSM_TAG,
        STORAGE_TANK_OSM_TAG,
        WORKS_OSM_TAG,
        CHIMNEY_OSM_TAG,
        OBELISK_OSM_TAG,
        SILO_OSM_TAG,
        TELESCOPE_OSM_TAG,
        WATER_TOWER_OSM_TAG,
        OBSERVATORY_OSM_TAG,
        PIER_OSM_TAG,
        BRIDGE_OSM_TAG
    ],
    ROAD_REMOVAL_LANDUSE_OSM_KEY: [
        FOREST_OSM_TAG,
        NATURE_RESERVE_OSM_TAG
    ],
    ROAD_REMOVAL_NATURAL_OSM_KEY: [
        FOREST_OSM_TAG,
        WOOD_OSM_TAG
    ],
}

