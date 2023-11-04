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
import logging
import os
import warnings
from shapely.errors import ShapelyDeprecationWarning

warnings.simplefilter(action="ignore", category=UserWarning, append=True)
warnings.simplefilter(action="ignore", category=FutureWarning, append=True)
warnings.simplefilter(action="ignore", category=DeprecationWarning, append=True)
warnings.simplefilter(action="ignore", category=RuntimeWarning, append=True)
warnings.simplefilter(action="ignore", category=ShapelyDeprecationWarning, append=True)

with warnings.catch_warnings():
    warnings.simplefilter(action="ignore", category=UserWarning, append=True)
    warnings.simplefilter(action="ignore", category=FutureWarning, append=True)
    warnings.simplefilter(action="ignore", category=DeprecationWarning, append=True)
    warnings.simplefilter(action="ignore", category=RuntimeWarning, append=True)
    warnings.simplefilter(action="ignore", category=ShapelyDeprecationWarning, append=True)

from constants import GEOMETRY_OSM_COLUMN, BOUNDING_BOX_OSM_KEY, SHAPE_TEMPLATES_FOLDER, OSM_LAND_SHAPEFILE, ROAD_OSM_KEY, BRIDGE_OSM_TAG, SERVICE_OSM_KEY, NOT_SHORE_WATER_OSM_KEY, WATER_OSM_KEY, NATURAL_OSM_KEY, OSM_TAGS, FOOTWAY_OSM_TAG, PATH_OSM_TAG, MAN_MADE_OSM_KEY, PIER_OSM_TAG, GOLF_OSM_KEY, FAIRWAY_OSM_TAG, EOL, CEND, TUNNEL_OSM_TAG, SEAMARK_TYPE_OSM_TAG, BUILDING_OSM_KEY, SHP_FILE_EXT, ELEMENT_TY_OSM_KEY, OSMID_OSM_KEY, RAILWAY_OSM_KEY, LANES_OSM_KEY, ONEWAY_OSM_KEY, ROAD_WITH_BORDERS, \
    ROAD_LANE_WIDTH, GEOCODE_OSM_FILE_PREFIX, PEDESTRIAN_ROAD_TYPE, FOOTWAY_ROAD_TYPE, SERVICE_ROAD_TYPE, LANDUSE_OSM_KEY, CONSTRUCTION_OSM_KEY, GDAL_LIB_PREFIX, FIONA_LIB_PREFIX, LAND_MASS_REPO, LAND_MASS_ARCHIVE, LEISURE_OSM_KEY, NETWORKX_LIB, RTREE_LIB, MATPLOTLIB_LIB, PANDAS_LIB, GEOPANDAS_LIB, OSMNX_LIB, SHAPELY_LIB, PATH_ROAD_TYPE, TRACK_ROAD_TYPE, AREA_OSM_TAG, NOT_EXCLUSION_BUILDING_OSM_KEY, WALL_OSM_KEY, WALL_OSM_TAG, CASTLE_WALL_OSM_TAG, CYCLEWAY_ROAD_TYPE, FULL_PREFIX, \
    ROAD_REMOVAL_LANDUSE_OSM_KEY, ROAD_REMOVAL_NATURAL_OSM_KEY, PROPOSED_OSM_TAG, LANDMARK_PREFIX, LON_OSM_KEY, LAT_OSM_KEY, FOREST_OSM_TAG, WOOD_OSM_TAG, SHAPELY_TYPE, OSMNX_LIB_VERSION, DEFAULT_OVERPASS_API_URI
from utils.colored_print import pr_bg_orange
from utils.install_lib import install_python_lib, install_alternate_python_lib, install_shapefile_resource

try:
    import osgeo
except ModuleNotFoundError:
    install_alternate_python_lib(GDAL_LIB_PREFIX)

try:
    import networkx
except ModuleNotFoundError:
    install_python_lib(NETWORKX_LIB)

try:
    import rtree
except ModuleNotFoundError:
    install_python_lib(RTREE_LIB)

try:
    import matplotlib
except ModuleNotFoundError:
    install_python_lib(MATPLOTLIB_LIB)

try:
    import fiona
except ModuleNotFoundError:
    install_alternate_python_lib(FIONA_LIB_PREFIX)

try:
    import shapely
except ModuleNotFoundError:
    install_python_lib(SHAPELY_LIB)
    import shapely

try:
    import pandas as pd
    # from pandas.errors import SettingWithCopyWarning
except ModuleNotFoundError:
    install_python_lib(PANDAS_LIB)
    import pandas as pd
    # from pandas.errors import SettingWithCopyWarning

try:
    import geopandas as gpd
except ModuleNotFoundError:
    install_python_lib(GEOPANDAS_LIB)
    import geopandas as gpd

try:
    import osmnx as ox
except ModuleNotFoundError:
    install_python_lib(OSMNX_LIB, OSMNX_LIB_VERSION)
    import osmnx as ox

from shapely.errors import ShapelyDeprecationWarning

from osmnx.utils_geo import bbox_to_poly

from shapely.geometry import Polygon, JOIN_STYLE, CAP_STYLE, MultiPolygon, LineString, MultiPoint, Point
from shapely.ops import linemerge, unary_union, polygonize, nearest_points
from utils.progress_bar import ProgressBar
from utils.geometry import close_holes, extend_line


class EPSG:
    key = "epsg:"
    WGS84_degree_unit = 4326
    WGS84_meter_unit = 3857


class OSMID_TYPE:
    way = "way"
    relation = "relation"
    node = "node"


class OVERLAY_OPERATOR:
    identity = "identity"
    union = "union"
    difference = "difference"
    symmetric_difference = "symmetric_difference"
    intersection = "intersection"


class PRESERVE_HOLES_METHOD:
    centroid_split = 1
    derivation_split = 2


def union_gdf(gdf1, gdf2):
    if gdf1.empty and not gdf2.empty:
        return gdf2.copy()

    if not gdf1.empty and not gdf2.empty:
        return gdf1.overlay(gdf2, how=OVERLAY_OPERATOR.union, keep_geom_type=True)

    return gdf1


def difference_gdf(gdf1, gdf2):
    if not gdf1.empty and not gdf2.empty:
        return gdf1.overlay(gdf2, how=OVERLAY_OPERATOR.difference, keep_geom_type=True)

    return gdf1


def symmetric_difference_gdf(gdf1, gdf2):
    if not gdf1.empty and not gdf2.empty:
        return gdf1.overlay(gdf2, how=OVERLAY_OPERATOR.symmetric_difference, keep_geom_type=True)

    return gdf1


def intersect_gdf(gdf1, gdf2):
    if not gdf1.empty and not gdf2.empty:
        return gdf1.overlay(gdf2, how=OVERLAY_OPERATOR.intersection, keep_geom_type=True)

    return gdf1


def create_bounding_box_from_tiles(tiles):
    result = None
    valid_tiles = [tile for tile in list(tiles.values()) if tile.valid]
    for i, tile in enumerate(valid_tiles):
        if i <= 0:
            result = tile.bbox_gdf.copy()
        else:
            result = copy_geometry(tile.bbox_gdf, result, i)

    result = result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)
    result = result.explode()

    result[GEOMETRY_OSM_COLUMN] = result[GEOMETRY_OSM_COLUMN].apply(lambda p: close_holes(p))
    result = resize_gdf(result, 10)
    return result


def create_empty_gdf():
    return gpd.GeoDataFrame(columns=[GEOMETRY_OSM_COLUMN], geometry=GEOMETRY_OSM_COLUMN, crs=EPSG.key + str(EPSG.WGS84_degree_unit))


def create_bounding_box(coords):
    b = bbox_to_poly(coords[1], coords[0], coords[2], coords[3])
    return gpd.GeoDataFrame(pd.DataFrame([], index=[0]), crs=EPSG.key + str(EPSG.WGS84_degree_unit), geometry=[b]), b


def resize_gdf(gdf, resize_distance, single_sided=True, keep_points=False):
    if gdf is None:
        return None

    if gdf.empty:
        return gdf

    gdf = gdf.to_crs(EPSG.key + str(EPSG.WGS84_meter_unit))
    if keep_points:
        gdf[GEOMETRY_OSM_COLUMN] = gdf[GEOMETRY_OSM_COLUMN].buffer(resize_distance)
    else:
        gdf[GEOMETRY_OSM_COLUMN] = gdf[GEOMETRY_OSM_COLUMN].buffer(resize_distance, cap_style=CAP_STYLE.flat, join_style=JOIN_STYLE.mitre, single_sided=single_sided)
    return gdf.to_crs(EPSG.key + str(EPSG.WGS84_degree_unit))


def load_gdf_from_geocode(geocode, overpass_api_uri, geocode_margin=5.0, preserve_roads=True, preserve_buildings=True, keep_data=False, coords=None, shpfiles_folder=None, display_warnings=True, by_osmid=False, check_geocode=False):
    warnings.simplefilter("ignore", UserWarning, append=True)
    import logging as lg
    ox.config(overpass_endpoint=overpass_api_uri, log_console=False, use_cache=False, log_level=lg.ERROR)

    try:
        warnings.simplefilter("ignore", FutureWarning, append=True)
        result = ox.geocode_to_gdf(geocode, by_osmid=by_osmid)
    except ValueError:
        result = create_empty_gdf()
        pass

    if check_geocode:
        return result

    if result.empty:
        try:
            warnings.simplefilter("ignore", FutureWarning, append=True)
            result = ox.geocode_to_gdf(geocode, by_osmid=True)
        except ValueError:
            result = create_empty_gdf()
            pass

    load_gdf_list = [None] * 8 if result.empty else [None] * 1

    if display_warnings:
        pbar = ProgressBar(load_gdf_list, title="RETRIEVE GEODATAFRAMES (THE FIRST TIME, MAY TAKE SOME TIME TO COMPLETE, BE PATIENT...)")
        pbar.update("retrieving buildings geodataframe...", stall=True)
    # load gdf twice to ensure to retrieve if from cache (to have osmid in a key, not in an index)
    load_gdf(coords, BUILDING_OSM_KEY, True, shp_file_path=os.path.join(shpfiles_folder, BUILDING_OSM_KEY + SHP_FILE_EXT))
    orig_building = load_gdf(coords, BUILDING_OSM_KEY, True, shp_file_path=os.path.join(shpfiles_folder, BUILDING_OSM_KEY + SHP_FILE_EXT), keep_geocode_data=True)

    if display_warnings:
        pbar.update("buildings geodataframe retrieved")

    if result.empty:
        if display_warnings:
            pbar.update("retrieving man made geodataframe...", stall=True)
        # load gdf twice to ensure to retrieve if from cache (to have osmid in a key, not in an index)
        load_gdf(coords, MAN_MADE_OSM_KEY, True, shp_file_path=os.path.join(shpfiles_folder, LANDMARK_PREFIX + MAN_MADE_OSM_KEY + SHP_FILE_EXT), keep_points=True)
        orig_man_made = load_gdf(coords, MAN_MADE_OSM_KEY, True, shp_file_path=os.path.join(shpfiles_folder, LANDMARK_PREFIX + MAN_MADE_OSM_KEY + SHP_FILE_EXT), keep_geocode_data=True, keep_points=True)
        if display_warnings:
            pbar.update("man made geodataframe retrieved")
            pbar.update("retrieving natural geodataframe...", stall=True)
        # load gdf twice to ensure to retrieve if from cache (to have osmid in a key, not in an index)
        load_gdf(coords, NATURAL_OSM_KEY, True, shp_file_path=os.path.join(shpfiles_folder, FULL_PREFIX + NATURAL_OSM_KEY + SHP_FILE_EXT))
        orig_natural = load_gdf(coords, NATURAL_OSM_KEY, True, shp_file_path=os.path.join(shpfiles_folder, FULL_PREFIX + NATURAL_OSM_KEY + SHP_FILE_EXT), keep_geocode_data=True)
        if display_warnings:
            pbar.update("natural geodataframe retrieved")
            pbar.update("retrieving landuse geodataframe...", stall=True)
        # load gdf twice to ensure to retrieve if from cache (to have osmid in a key, not in an index)
        load_gdf(coords, LANDUSE_OSM_KEY, True, shp_file_path=os.path.join(shpfiles_folder, FULL_PREFIX + LANDUSE_OSM_KEY + SHP_FILE_EXT))
        orig_landuse = load_gdf(coords, LANDUSE_OSM_KEY, True, shp_file_path=os.path.join(shpfiles_folder, FULL_PREFIX + LANDUSE_OSM_KEY + SHP_FILE_EXT), keep_geocode_data=True)
        if display_warnings:
            pbar.update("landuse geodataframe retrieved")
            pbar.update("retrieving leisures geodataframe...", stall=True)
        # load gdf twice to ensure to retrieve if from cache (to have osmid in a key, not in an index)
        load_gdf(coords, LEISURE_OSM_KEY, True, shp_file_path=os.path.join(shpfiles_folder, LEISURE_OSM_KEY + SHP_FILE_EXT))
        orig_leisure = load_gdf(coords, LEISURE_OSM_KEY, True, shp_file_path=os.path.join(shpfiles_folder, LEISURE_OSM_KEY + SHP_FILE_EXT), keep_geocode_data=True)
        if display_warnings:
            pbar.update("leisures geodataframe retrieved")
            pbar.update("retrieving constructions geodataframe...", stall=True)
        # load gdf twice to ensure to retrieve if from cache (to have osmid in a key, not in an index)
        load_gdf(coords, LANDUSE_OSM_KEY, OSM_TAGS[CONSTRUCTION_OSM_KEY], shp_file_path=os.path.join(shpfiles_folder, CONSTRUCTION_OSM_KEY + SHP_FILE_EXT))
        orig_construction = load_gdf(coords, LANDUSE_OSM_KEY, OSM_TAGS[CONSTRUCTION_OSM_KEY], shp_file_path=os.path.join(shpfiles_folder, CONSTRUCTION_OSM_KEY + SHP_FILE_EXT), keep_geocode_data=True)
        if display_warnings:
            pbar.update("constructions geodataframe retrieved")
            pbar.update("retrieving roads geodataframe...", stall=True)
        # load gdf twice to ensure to retrieve if from cache (to have osmid in a key, not in an index)
        load_gdf(coords, ROAD_OSM_KEY, True, shp_file_path=os.path.join(shpfiles_folder, ROAD_OSM_KEY + SHP_FILE_EXT), is_roads=True)
        orig_road = load_gdf(coords, ROAD_OSM_KEY, True, shp_file_path=os.path.join(shpfiles_folder, ROAD_OSM_KEY + SHP_FILE_EXT), is_roads=True, keep_geocode_data=True)
        if display_warnings:
            pbar.update("roads geodataframe retrieved")
            pbar.update("retrieving railways geodataframe...", stall=True)
        # load gdf twice to ensure to retrieve if from cache (to have osmid in a key, not in an index)
        load_gdf(coords, RAILWAY_OSM_KEY, True, shp_file_path=os.path.join(shpfiles_folder, RAILWAY_OSM_KEY + SHP_FILE_EXT), is_roads=True)
        orig_railway = load_gdf(coords, RAILWAY_OSM_KEY, True, shp_file_path=os.path.join(shpfiles_folder, RAILWAY_OSM_KEY + SHP_FILE_EXT), is_roads=True, keep_geocode_data=True)
        if display_warnings:
            pbar.update("railways geodataframe retrieved")
        road = prepare_roads_gdf(orig_road, orig_railway, bridge_only=False)
        try:
            if coords is not None and shpfiles_folder is not None:
                osmid = geocode
                if ELEMENT_TY_OSM_KEY in orig_building and OSMID_OSM_KEY in orig_building:
                    result = orig_building[((orig_building[ELEMENT_TY_OSM_KEY] == OSMID_TYPE.way) | (orig_building[ELEMENT_TY_OSM_KEY] == OSMID_TYPE.relation)) & (orig_building[OSMID_OSM_KEY] == int(osmid))]
                if result.empty and ELEMENT_TY_OSM_KEY in orig_man_made and OSMID_OSM_KEY in orig_man_made:
                    result = orig_man_made[((orig_man_made[ELEMENT_TY_OSM_KEY] == OSMID_TYPE.way) | (orig_man_made[ELEMENT_TY_OSM_KEY] == OSMID_TYPE.relation) | (orig_man_made[ELEMENT_TY_OSM_KEY] == OSMID_TYPE.node)) & (orig_man_made[OSMID_OSM_KEY] == int(osmid))]
                if result.empty and ELEMENT_TY_OSM_KEY in orig_natural and OSMID_OSM_KEY in orig_natural:
                    result = orig_natural[((orig_natural[ELEMENT_TY_OSM_KEY] == OSMID_TYPE.way) | (orig_natural[ELEMENT_TY_OSM_KEY] == OSMID_TYPE.relation)) & (orig_natural[OSMID_OSM_KEY] == int(osmid))]
                if result.empty and ELEMENT_TY_OSM_KEY in orig_landuse and OSMID_OSM_KEY in orig_landuse:
                    result = orig_landuse[((orig_landuse[ELEMENT_TY_OSM_KEY] == OSMID_TYPE.way) | (orig_landuse[ELEMENT_TY_OSM_KEY] == OSMID_TYPE.relation)) & (orig_landuse[OSMID_OSM_KEY] == int(osmid))]
                if result.empty and ELEMENT_TY_OSM_KEY in orig_leisure and OSMID_OSM_KEY in orig_leisure:
                    result = orig_leisure[((orig_leisure[ELEMENT_TY_OSM_KEY] == OSMID_TYPE.way) | (orig_leisure[ELEMENT_TY_OSM_KEY] == OSMID_TYPE.relation)) & (orig_leisure[OSMID_OSM_KEY] == int(osmid))]
                if result.empty and ELEMENT_TY_OSM_KEY in orig_construction and OSMID_OSM_KEY in orig_construction:
                    result = orig_construction[((orig_construction[ELEMENT_TY_OSM_KEY] == OSMID_TYPE.way) | (orig_construction[ELEMENT_TY_OSM_KEY] == OSMID_TYPE.relation)) & (orig_construction[OSMID_OSM_KEY] == int(osmid))]
                if result.empty and ELEMENT_TY_OSM_KEY in road and OSMID_OSM_KEY in road:
                    result = road[((road[ELEMENT_TY_OSM_KEY] == OSMID_TYPE.way) | (road[ELEMENT_TY_OSM_KEY] == OSMID_TYPE.relation)) & (road[OSMID_OSM_KEY] == int(osmid))]
        except ValueError:
            if display_warnings:
                pr_bg_orange("Osmid (" + geocode + ") not found in OSM data" + EOL + CEND)
            return create_empty_gdf()

    if result.empty:
        if display_warnings:
            pr_bg_orange(("Osmid" if geocode.isnumeric() else "Geocode") + " (" + geocode + ") not found in OSM data" + EOL + CEND)
        return create_empty_gdf()

    # warnings.simplefilter("ignore", SettingWithCopyWarning, append=True)
    result[LON_OSM_KEY] = result.centroid.iloc[0].x
    result[LAT_OSM_KEY] = result.centroid.iloc[0].y

    bounds_coords = result.bounds.iloc[0]
    result_coords = (bounds_coords["maxy"], bounds_coords["miny"], bounds_coords["maxx"], bounds_coords["minx"])
    result_bbox, b = create_bounding_box(result_coords)
    result_bbox = resize_gdf(result_bbox, 200)

    orig_building = orig_building.clip(result_bbox, keep_geom_type=True)
    building_mask = difference_gdf(orig_building, result)
    if not building_mask.empty:
        warnings.simplefilter("ignore", FutureWarning, append=True)
        warnings.simplefilter("ignore", UserWarning, append=True)
        building_mask.to_file(os.path.join(shpfiles_folder, GEOCODE_OSM_FILE_PREFIX + "_" + BUILDING_OSM_KEY + SHP_FILE_EXT))

    result = resize_gdf(result, geocode_margin)

    if keep_data:
        return result

    if not result.empty:
        result = result[[GEOMETRY_OSM_COLUMN]]

    if preserve_roads:
        orig_road = load_gdf(coords, ROAD_OSM_KEY, True, shp_file_path=os.path.join(shpfiles_folder, ROAD_OSM_KEY + SHP_FILE_EXT), is_roads=True)
        orig_railway = load_gdf(coords, RAILWAY_OSM_KEY, True, shp_file_path=os.path.join(shpfiles_folder, RAILWAY_OSM_KEY + SHP_FILE_EXT), is_roads=True)
        road = prepare_roads_gdf(orig_road, orig_railway, bridge_only=False)
        road = road.clip(result_bbox, keep_geom_type=True)
        # for debugging purpose, generate the shp file
        if not road.empty:
            warnings.simplefilter("ignore", FutureWarning, append=True)
            warnings.simplefilter("ignore", UserWarning, append=True)
            road = road.reset_index(drop=True)
            road.to_file(os.path.join(shpfiles_folder, GEOCODE_OSM_FILE_PREFIX + "_" + ROAD_OSM_KEY + SHP_FILE_EXT))
            road = clip_gdf(road, result)
            road = road[[GEOMETRY_OSM_COLUMN]]
            result = difference_gdf(result, road)

    if not building_mask.empty and preserve_buildings:
        building_mask = building_mask[[GEOMETRY_OSM_COLUMN]]
        result = difference_gdf(result, building_mask)

    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)


def load_gdf(coords, key, tags, shp_file_path="", keep_geocode_data=False, is_roads=False, is_sea=False, is_waterway=False, is_grass=False, is_wall=False, land_mass=None, bbox=None, keep_points=False):
    result = create_empty_gdf()
    has_cache = os.path.isfile(shp_file_path)
    logging.getLogger('shapely.geos').setLevel(logging.CRITICAL)
    keys = [key]

    if has_cache:
        filesize = os.path.getsize(shp_file_path)
        if filesize > 0:
            result = gpd.read_file(shp_file_path)
            result = result[~result[GEOMETRY_OSM_COLUMN].isna()]
        else:
            return result
    else:
        if is_sea and land_mass is not None and bbox is not None:
            result = symmetric_difference_gdf(land_mass, bbox).assign(boundary=BOUNDING_BOX_OSM_KEY)
        elif coords is not None:
            warnings.simplefilter("ignore", DeprecationWarning, append=True)
            result = ox.geometries_from_bbox(coords[0], coords[1], coords[2], coords[3], tags={key: tags})

            # truncate index fields to avoid ogr2ogr warning logs
            if not result.empty:
                result.index.names = list(map(lambda x: x[:10], result.index.names))

            if not keep_points:
                # remove points to fix shapefile saving issues
                result = result[~(result.geom_type == SHAPELY_TYPE.point)]

    if not result.empty:
        keys.insert(0, GEOMETRY_OSM_COLUMN)

        if is_wall:
            if WALL_OSM_KEY in result:
                keys.append(WALL_OSM_KEY)

        if is_grass:
            if GOLF_OSM_KEY in result:
                keys.append(GOLF_OSM_KEY)

        if is_roads:
            if SEAMARK_TYPE_OSM_TAG in result:
                keys.append(SEAMARK_TYPE_OSM_TAG)
            if TUNNEL_OSM_TAG in result:
                keys.append(TUNNEL_OSM_TAG)
            if BRIDGE_OSM_TAG in result:
                keys.append(BRIDGE_OSM_TAG)
            if SERVICE_OSM_KEY in result:
                keys.append(SERVICE_OSM_KEY)
            if MAN_MADE_OSM_KEY in result:
                keys.append(MAN_MADE_OSM_KEY)
            if LANES_OSM_KEY in result:
                keys.append(LANES_OSM_KEY)
            if ONEWAY_OSM_KEY in result:
                keys.append(ONEWAY_OSM_KEY)
            if AREA_OSM_TAG in result:
                keys.append(AREA_OSM_TAG)

        if keep_geocode_data and has_cache:
            keys.append(ELEMENT_TY_OSM_KEY)
            keys.append(OSMID_OSM_KEY)

        result = result[keys]

        if not has_cache and shp_file_path != "":
            if (not is_roads and not is_waterway and not keep_geocode_data) or keep_points:
                result = resize_gdf(result, 0.00001, keep_points=keep_points)

            try:
                warnings.simplefilter("ignore", FutureWarning, append=True)
                warnings.simplefilter("ignore", UserWarning, append=True)
                result.to_file(shp_file_path)
            except:
                if os.path.isfile(shp_file_path):
                    os.remove(shp_file_path)
                pass
    else:
        for key in keys:
            result[key] = None
        # create empty shp file as cache
        open(shp_file_path, 'a').close()

    return result


def prepare_gdf(gdf, resize=0):
    if gdf is None:
        return None

    result = gdf.copy()

    if not result.empty:
        if resize != 0:
            result = resize_gdf(result, resize)

        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result


def prepare_roads_gdf(gdf, railway_gdf, bridge_only=True, automatic_road_width_calculation=True):
    result = gpd.GeoDataFrame(columns=[GEOMETRY_OSM_COLUMN], geometry=GEOMETRY_OSM_COLUMN, crs=EPSG.key + str(EPSG.WGS84_degree_unit))
    roads = gdf.copy()
    railways = railway_gdf.copy()
    warnings.simplefilter("ignore", FutureWarning, append=True)
    roads = roads._append(railways)
    has_bridge = False
    has_bridge_path = False
    has_seamark_bridge = False
    has_pier = False
    has_places = False
    bridge = None
    bridge_path = None
    seamark_bridge = None
    pier = None
    places = None

    if not roads.empty:
        roads = roads[~roads[GEOMETRY_OSM_COLUMN].isna()]

        # remove proposed roads
        roads = roads[~(roads[ROAD_OSM_KEY] == PROPOSED_OSM_TAG)]
        if PROPOSED_OSM_TAG in roads:
            roads = roads[roads[PROPOSED_OSM_TAG].isna()]

        if TUNNEL_OSM_TAG in roads:
            roads = roads[roads[TUNNEL_OSM_TAG].isna()]

        if bridge_only:
            # fix for bridge paths
            if BRIDGE_OSM_TAG in roads:
                bridge_path = roads[(roads[ROAD_OSM_KEY] == PATH_OSM_TAG) & ~(roads[BRIDGE_OSM_TAG].isna())]
                has_bridge_path = not bridge_path.empty

            if not has_bridge_path:
                roads = roads[~(roads[ROAD_OSM_KEY] == PATH_OSM_TAG)]

            if BRIDGE_OSM_TAG in roads:
                bridge = roads[~(roads[BRIDGE_OSM_TAG].isna())]
                has_bridge = True

            if SEAMARK_TYPE_OSM_TAG in roads:
                seamark_bridge = roads[(roads[SEAMARK_TYPE_OSM_TAG] == BRIDGE_OSM_TAG)]
                has_seamark_bridge = True

            if MAN_MADE_OSM_KEY in roads:
                pier = roads[(roads[ROAD_OSM_KEY] == FOOTWAY_OSM_TAG) & (roads[MAN_MADE_OSM_KEY] == PIER_OSM_TAG)]
                pier = pier._append(roads[(roads[ROAD_OSM_KEY] == FOOTWAY_OSM_TAG) & ~(roads[BRIDGE_OSM_TAG].isna())])
                pier = resize_gdf(pier, 12, single_sided=False)
                has_pier = not pier.empty

            if has_bridge:
                result = result._append(bridge)

            if has_bridge_path:
                result = result._append(bridge_path)

            if has_seamark_bridge:
                result = result._append(seamark_bridge)
        else:
            if TUNNEL_OSM_TAG in roads:
                roads = roads[roads[TUNNEL_OSM_TAG].isna()]

            if AREA_OSM_TAG in roads:
                places = roads[(roads[AREA_OSM_TAG] == "yes") & ~(roads[AREA_OSM_TAG].isna())]
                places = resize_gdf(places, 0.00001)
                places[GEOMETRY_OSM_COLUMN] = places[GEOMETRY_OSM_COLUMN].apply(lambda p: close_holes(p))
                has_places = not places.empty

            result = roads.copy()
            result = result[~(result[ROAD_OSM_KEY] == PEDESTRIAN_ROAD_TYPE) & ~(result[ROAD_OSM_KEY] == FOOTWAY_ROAD_TYPE) & ~(result[ROAD_OSM_KEY] == CYCLEWAY_ROAD_TYPE) & ~(result[ROAD_OSM_KEY] == SERVICE_ROAD_TYPE) & ~(result[ROAD_OSM_KEY] == PATH_ROAD_TYPE) & ~(result[ROAD_OSM_KEY] == TRACK_ROAD_TYPE)]

        result = result.reset_index(drop=True)
        result = result.to_crs(EPSG.key + str(EPSG.WGS84_meter_unit))
        result = result.explode()
        for index, row in result.iterrows():
            road_width = calculate_road_width(row) if automatic_road_width_calculation else 22
            result.loc[index, GEOMETRY_OSM_COLUMN] = row[GEOMETRY_OSM_COLUMN].buffer(road_width, resolution=32, cap_style=CAP_STYLE.square, join_style=JOIN_STYLE.mitre, mitre_limit=20.0, single_sided=False)
        result = result.to_crs(EPSG.key + str(EPSG.WGS84_degree_unit))

        if has_pier:
            result = result._append(pier)

        if has_places and not bridge_only:
            result = result._append(places)

        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]
        result[GEOMETRY_OSM_COLUMN] = result[GEOMETRY_OSM_COLUMN].buffer(0)

    return result


def prepare_wall_gdf(gdf):
    result = gpd.GeoDataFrame(columns=[GEOMETRY_OSM_COLUMN], geometry=GEOMETRY_OSM_COLUMN, crs=EPSG.key + str(EPSG.WGS84_degree_unit))
    warnings.simplefilter("ignore", FutureWarning, append=True)

    if not gdf.empty:
        result = gdf.copy()
        result = result[~result[GEOMETRY_OSM_COLUMN].isna()]
        if WALL_OSM_TAG in result:
            result = result[(result[WALL_OSM_TAG] == CASTLE_WALL_OSM_TAG)]
            result = resize_gdf(result, 5, single_sided=False)

        result = result.reset_index(drop=True)
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]
        result[GEOMETRY_OSM_COLUMN] = result[GEOMETRY_OSM_COLUMN].buffer(0)

    return result


def prepare_sea_gdf(gdf):
    result = gdf.copy()

    if not result.empty:
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result[[GEOMETRY_OSM_COLUMN]].dissolve()


def prepare_landuse_gdf(gdf):
    if gdf is None:
        return create_empty_gdf()

    result = gdf.copy()

    if not result.empty:
        if LANDUSE_OSM_KEY in result:
            # remove forests area
            result = result[~(result[LANDUSE_OSM_KEY] == FOREST_OSM_TAG)]
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result


def prepare_natural_gdf(gdf):
    if gdf is None:
        return create_empty_gdf()

    result = gdf.copy()

    if not result.empty:
        if NATURAL_OSM_KEY in result:
            # remove forests and woods area
            result = result[~(result[NATURAL_OSM_KEY] == FOREST_OSM_TAG)]
            result = result[~(result[NATURAL_OSM_KEY] == WOOD_OSM_TAG)]
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result


def prepare_golf_gdf(gdf):
    result = create_empty_gdf()

    if GOLF_OSM_KEY in gdf:
        result = gdf[(gdf[GOLF_OSM_KEY] == FAIRWAY_OSM_TAG)]

    if not result.empty:
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result[[GEOMETRY_OSM_COLUMN]].dissolve()


def prepare_forest_gdf(landuse_gdf, natural_gdf):
    result = create_empty_gdf()
    natural_forests = create_empty_gdf()

    if landuse_gdf is None and natural_gdf is None:
        return result

    if landuse_gdf is not None:
        landuse = landuse_gdf.copy()
        if LANDUSE_OSM_KEY in landuse_gdf:
            result = landuse[(landuse[LANDUSE_OSM_KEY] == FOREST_OSM_TAG)]

    if natural_gdf is not None:
        natural = natural_gdf.copy()
        if NATURAL_OSM_KEY in landuse_gdf:
            natural_forests = natural[(natural[NATURAL_OSM_KEY] == FOREST_OSM_TAG)]

    if not result.empty:
        if not natural_forests.empty:
            result = result._append(natural_forests)
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result


def prepare_wood_gdf(gdf):
    if gdf is None:
        return create_empty_gdf()

    result = gdf.copy()

    if not result.empty:
        if NATURAL_OSM_KEY in result:
            result = result[(result[NATURAL_OSM_KEY] == WOOD_OSM_TAG)]
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result


def prepare_park_gdf(gdf, bridges):
    if gdf is None:
        return create_empty_gdf()

    result = gdf.copy()

    if not result.empty:
        if not bridges.empty:
            result = difference_gdf(result, bridges)
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result


def prepare_amenity_gdf(gdf, water, natural_water, airport):
    if gdf is None:
        return create_empty_gdf()

    result = gdf.copy()

    if not result.empty:
        if not water.empty:
            result = difference_gdf(result, water)
        if not natural_water.empty:
            result = difference_gdf(result, natural_water)
        if not airport.empty:
            result = difference_gdf(result, airport)
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result


def prepare_residential_gdf(gdf, water, natural, natural_water, forests, woods, park, airport):
    if gdf is None:
        return create_empty_gdf()

    result = gdf.copy()

    if not result.empty:
        if not water.empty:
            result = difference_gdf(result, water)
        if not natural.empty:
            result = difference_gdf(result, natural)
        if not forests.empty:
            result = difference_gdf(result, forests)
        if not woods.empty:
            result = difference_gdf(result, woods)
        if not natural_water.empty:
            result = difference_gdf(result, natural_water)
        if not park.empty:
            result = difference_gdf(result, park)
        if not airport.empty:
            result = difference_gdf(result, airport)
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result


def prepare_bbox_gdf(bbox, land_mass, boundary):
    result = clip_gdf(bbox, land_mass)
    result = clip_gdf(result, boundary)
    return resize_gdf(result, 20)


def prepare_building_gdf(gdf, wall, man_made):
    result = gdf.copy()

    if not result.empty:
        result = resize_gdf(result, 10)
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    if not wall.empty:
        result = result._append(wall)

    if not man_made.empty:
        result = result._append(man_made)

    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)


def prepare_water_gdf(gdf, waterway):
    result = gdf.copy()

    if not result.empty:
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    if not waterway.empty:
        result = result._append(resize_gdf(waterway, 30))

    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)


def prepare_water_exclusion_gdf(gdf, building, bridges):
    result = gdf.copy()
    result = difference_gdf(resize_gdf(result, -5), building)
    result = difference_gdf(result, bridges)

    if not result.empty:
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)


def prepare_hidden_roads_gdf(landuse_gdf, natural_gdf):
    landuse_src = landuse_gdf.copy()
    natural_src = natural_gdf.copy()
    filter = create_empty_gdf()
    result = create_empty_gdf()

    if not landuse_src.empty:
        for tag in OSM_TAGS[ROAD_REMOVAL_LANDUSE_OSM_KEY]:
            if LANDUSE_OSM_KEY in landuse_src:
                filter = landuse_src[(landuse_src[LANDUSE_OSM_KEY] == tag)]

            if not filter.empty:
                result = result._append(filter)

    if not natural_src.empty:
        for tag in OSM_TAGS[ROAD_REMOVAL_NATURAL_OSM_KEY]:
            if NATURAL_OSM_KEY in natural_src:
                filter = natural_src[(natural_src[NATURAL_OSM_KEY] == tag)]

            if not filter.empty:
                result = result._append(filter)

    if not result.empty:
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)


def create_point_gdf(lat, lon, alt):
    data = {"x": [lon], "y": [lat], "z": [alt]}
    df = pd.DataFrame(data)
    return gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["x"], df["y"], df["z"]), crs=EPSG.key + str(EPSG.WGS84_degree_unit))


def create_land_mass_gdf(sources_path, bbox, b):
    land_mass_shapefile = os.path.join(sources_path, os.path.join(SHAPE_TEMPLATES_FOLDER, OSM_LAND_SHAPEFILE))
    if not os.path.isfile(land_mass_shapefile):
        install_shapefile_resource(LAND_MASS_REPO, LAND_MASS_ARCHIVE, os.path.join(sources_path, SHAPE_TEMPLATES_FOLDER))
    result = gpd.read_file(os.path.join(sources_path, land_mass_shapefile), bbox=b).clip(bbox.geometry)
    return result[[GEOMETRY_OSM_COLUMN]].dissolve()


def create_buildings_and_water_gdf(buildings, water):
    result = create_empty_gdf()

    result = union_gdf(result, resize_gdf(water, 5))
    result = union_gdf(result, buildings)
    result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)


def create_water_bridge_exclusion_gdf(natural_water, water, sea, roads):
    result = create_empty_gdf()
    result = union_gdf(result, intersect_gdf(water, roads))
    result = union_gdf(result, intersect_gdf(natural_water, roads))
    result = union_gdf(result, intersect_gdf(sea, roads))

    return result.dissolve().assign(building=BRIDGE_OSM_TAG)


def create_whole_water_gdf(natural_water, water, sea):
    result = create_empty_gdf()
    result = union_gdf(result, water)
    result = union_gdf(result, natural_water)
    result = union_gdf(result, sea)

    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)


def create_water_exclusion_gdf(natural_water, water, sea, roads):
    result = create_empty_gdf()
    result = union_gdf(result, difference_gdf(water, roads))
    result = union_gdf(result, difference_gdf(natural_water, roads))
    result = union_gdf(result, difference_gdf(sea, roads))

    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)


def create_ground_exclusion_gdf(landuse, forests, woods, nature_reserves, natural, aeroway, bridges, parks, airport, settings):
    result = create_empty_gdf()
    result = union_gdf(result, landuse)
    result = union_gdf(result, forests)
    result = union_gdf(result, woods)
    result = union_gdf(result, nature_reserves)
    result = union_gdf(result, natural)
    result = union_gdf(result, aeroway)
    result = union_gdf(result, airport)
    result = union_gdf(result, parks)
    result = resize_gdf(result, float(settings.ground_exclusion_margin))

    if not bridges.empty and BRIDGE_OSM_TAG in bridges:
        bridges = bridges[~(bridges[BRIDGE_OSM_TAG].isna())]
        result = difference_gdf(result, bridges)

    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)


def create_exclusion_water_gdf(orig_water, orig_natural_water, sea, bbox):
    water = orig_water.copy()
    for tag in OSM_TAGS[NOT_EXCLUSION_BUILDING_OSM_KEY]:
        if WATER_OSM_KEY in water:
            water = water[~(water[WATER_OSM_KEY] == tag)]
    water = clip_gdf(prepare_gdf(water), bbox)

    natural_water = orig_natural_water.copy()
    for tag in OSM_TAGS[NOT_EXCLUSION_BUILDING_OSM_KEY]:
        if NATURAL_OSM_KEY in natural_water:
            natural_water = natural_water[~(natural_water[NATURAL_OSM_KEY] == tag)]
    natural_water = clip_gdf(prepare_gdf(natural_water), bbox)

    result = create_whole_water_gdf(natural_water, water, sea)
    result = resize_gdf(result, 20)
    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)


def create_exclusion_vegetation_water_gdf(orig_water, orig_natural_water, sea, bbox):
    result = create_whole_water_gdf(orig_natural_water, orig_water, sea)
    result = resize_gdf(result, 20)
    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)


def create_shore_water_gdf(orig_water, orig_natural_water, sea, bbox):
    water = orig_water.copy()
    for tag in OSM_TAGS[NOT_SHORE_WATER_OSM_KEY]:
        if WATER_OSM_KEY in water:
            water = water[~(water[WATER_OSM_KEY] == tag)]
    water = clip_gdf(prepare_gdf(water), bbox)

    natural_water = orig_natural_water.copy()
    for tag in OSM_TAGS[NOT_SHORE_WATER_OSM_KEY]:
        if NATURAL_OSM_KEY in natural_water:
            natural_water = natural_water[~(natural_water[NATURAL_OSM_KEY] == tag)]
    natural_water = clip_gdf(prepare_gdf(natural_water), bbox)

    result = create_whole_water_gdf(natural_water, water, sea)
    result = resize_gdf(result, 20)
    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)


def create_terraform_polygons_gdf(gdf, exclusion):
    terraform_gdf = gdf.copy()
    terraform_gdf = difference_gdf(terraform_gdf, exclusion)
    terraform_gdf = terraform_gdf.dissolve()
    result = preserve_holes(resize_gdf(terraform_gdf, -10), split_method=PRESERVE_HOLES_METHOD.derivation_split)
    return result.dissolve()


def create_vegetation_polygons_gdf(gdf, exclusion):
    vegetation_gdf = gdf.copy()
    vegetation_gdf = difference_gdf(vegetation_gdf, exclusion)
    vegetation_gdf = vegetation_gdf.dissolve()
    result = preserve_holes(vegetation_gdf, split_method=PRESERVE_HOLES_METHOD.derivation_split)
    return result.dissolve()


def create_exclusion_building_polygons_gdf(bbox, exclusion, airport):
    boundary = bbox.copy()
    boundary = resize_gdf(boundary, -100)
    adjusted_exclusion = resize_gdf(exclusion, 20)
    adjusted_exclusion = union_gdf(boundary, adjusted_exclusion)
    airport = resize_gdf(airport, -50)
    adjusted_exclusion = difference_gdf(adjusted_exclusion, airport)
    adjusted_exclusion = adjusted_exclusion.dissolve()
    result = preserve_holes(adjusted_exclusion, split_method=PRESERVE_HOLES_METHOD.derivation_split)
    return result


def update_exclusion_building_polygons_gdf(exclusion_building, construction, amenity):
    result = exclusion_building.copy()
    construction = resize_gdf(construction, 30)
    amenity = resize_gdf(amenity, 30)

    if not construction.empty:
        result = difference_gdf(result, construction)

    if not amenity.empty:
        result = difference_gdf(result, amenity)

    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)


def create_exclusion_vegetation_polygons_gdf(exclusion):
    exclusion = exclusion.dissolve()
    result = preserve_holes(exclusion, split_method=PRESERVE_HOLES_METHOD.derivation_split)
    return result


def clip_gdf(gdf, clip):
    result = gdf.copy()

    if clip.empty:
        return result

    if not result.empty:
        result[GEOMETRY_OSM_COLUMN] = result[GEOMETRY_OSM_COLUMN].clip(clip)
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]
        result = result.dissolve()

    return result


def copy_geometry(source, dest, start_index=-1):
    source = source[source.geometry != SHAPELY_TYPE.none].explode()
    i = 1
    for index, row in source.iterrows():
        if isinstance(row.geometry, Polygon):
            dest.loc[index if start_index < 0 else start_index + i, GEOMETRY_OSM_COLUMN] = row.geometry
            i = i+1

    return dest


def preserve_holes(gdf, split_method=PRESERVE_HOLES_METHOD.centroid_split):
    keep_polys = []
    result_lp = []
    result = gdf.copy()
    result = resize_gdf(result, 1)
    result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    result_p = result.geometry.unary_union

    if result_p is None:
        return result

    if result_p.type == SHAPELY_TYPE.polygon:
        result_lp = [result_p]
    elif result_p.type == SHAPELY_TYPE.multiPolygon:
        for polygon in result_p.geoms:
            result_lp.append(polygon)

    warnings.simplefilter("ignore", ShapelyDeprecationWarning, append=True)
    for input_p in result_lp:
        if input_p.interiors:
            if split_method == PRESERVE_HOLES_METHOD.centroid_split:
                keep_polys = centroid_split_method(input_p, keep_polys)
            if split_method == PRESERVE_HOLES_METHOD.derivation_split:
                keep_polys = derivation_split_method(input_p, keep_polys)
        else:
            keep_polys.append(input_p)

    if keep_polys:
        result[GEOMETRY_OSM_COLUMN] = MultiPolygon(keep_polys)
        result = result.explode(index_parts=False)

    return result


def centroid_split_method(input_p, keep_polys):
    lines = []
    result = keep_polys

    centroid_pts = [p.centroid for p in input_p.interiors]
    centroid_pt = centroid_pts[0]

    pts = nearest_points(input_p.exterior, centroid_pt)
    input_l = LineString(pts[0].coords[:] + pts[1].coords[:])
    lines.append(input_l)

    centroid_pts = [pt for pt in centroid_pts if pt != centroid_pt]

    while centroid_pts:
        other_centroid_pts = MultiPoint([pt for pt in centroid_pts if pt != centroid_pt])

        if not other_centroid_pts:
            break

        pts = nearest_points(centroid_pt, other_centroid_pts)
        next_centroid_pt = pts[1]

        proj_centroid_pt = Point([centroid_pt.x, 0])
        proj_other_centroid_pts = [Point([pt.x, 0]) for pt in other_centroid_pts.geoms]

        proj_pts = nearest_points(proj_centroid_pt, MultiPoint(proj_other_centroid_pts))
        warnings.simplefilter("ignore", ShapelyDeprecationWarning, append=True)
        next_proj_centroid_pt = proj_pts[1]

        if next_proj_centroid_pt.x > next_centroid_pt.x:
            for pt in other_centroid_pts.geoms:
                if pt.x == next_proj_centroid_pt.x:
                    next_centroid_pt = pt

        centroid_pts = [pt for pt in centroid_pts if pt != next_centroid_pt]
        input_l = LineString((centroid_pt, next_centroid_pt))

        lines.append(input_l)
        centroid_pt = next_centroid_pt

    pts = nearest_points(centroid_pt, input_p.exterior)
    input_l = LineString(pts[0].coords[:] + pts[1].coords[:])
    l_coords = list(input_l.coords)
    input_l = extend_line(*l_coords[-2:], 1.5)

    lines.append(input_l)

    if input_p.boundary.geom_type == SHAPELY_TYPE.multiLineString:
        for line in input_p.boundary.geoms:
            lines.append(line)
    else:
        lines.append(input_p.boundary)

    merged_lines = linemerge(lines)
    border_lines = unary_union(merged_lines)

    polys = [poly for poly in polygonize(border_lines) if poly.representative_point().within(input_p)]
    for p in polys:
        result.append(p)

    return result


def derivation_split_method(input_p, keep_polys):
    new_pol_pts = []
    DERIVATION_BIAS = 0.0000001
    result = keep_polys

    input_pts = other_pts = [p for p in input_p.exterior.coords]
    del input_pts[-1]

    for i, interior in enumerate(input_p.interiors):
        interior_pts = list(zip(*interior.xy))
        del interior_pts[-1]

        pts = nearest_points(MultiPoint(other_pts), MultiPoint(interior_pts))
        derivation_pt = pts[0].coords[:][0]
        first_interior_pt = pts[1].coords[:][0]
        last_interior_pt = (first_interior_pt[0] - DERIVATION_BIAS, first_interior_pt[1] - DERIVATION_BIAS)
        j_first = interior_pts.index(first_interior_pt)
        new_derivation_pt = (derivation_pt[0] + DERIVATION_BIAS, derivation_pt[1] + DERIVATION_BIAS)

        new_pol_pts = []

        for input_pt in input_pts:
            if input_pt != derivation_pt:
                new_pol_pts.append(input_pt)
            else:
                new_pol_pts.append(derivation_pt)

                new_pol_pts += [pt for j, pt in enumerate(interior_pts) if j >= j_first]
                new_pol_pts += [pt for j, pt in enumerate(interior_pts) if j < j_first]

                new_pol_pts.append(last_interior_pt)
                new_pol_pts.append(new_derivation_pt)

        # ensure to close the poly
        if new_pol_pts[0] != input_pts[0]:
            new_pol_pts.append(input_pts[0])
        input_pts = new_pol_pts

        other_pts = [pt for pt in input_pts if pt != derivation_pt and pt != new_derivation_pt]

    result.append(Polygon(new_pol_pts))

    return result


def create_grid_from_hmatrix(hmatrix, lat, lon):
    n = 0

    data = {"x": [], "y": [], "z": []}
    for y, heights in hmatrix.items():
        if n % 2 == 0:
            for x, h in heights.items():
                data["x"].append(x)
                data["y"].append(y)
                data["z"].append(0.0)

        n = n + 1

    return create_latlon_gdf_from_meter_data(data, lat, lon, 0.0)


def create_latlon_gdf_from_meter_data(data, lat, lon, alt):
    result = []
    df = pd.DataFrame(data)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["x"], df["y"], df["z"]), crs=EPSG.key + str(EPSG.WGS84_meter_unit))

    gdf = gdf.to_crs(EPSG.key + str(EPSG.WGS84_degree_unit))

    for point in gdf[GEOMETRY_OSM_COLUMN]:
        co = list(point.coords)
        result.append((lat + co[0][0], lon + co[0][1], alt + co[0][2]))

    gdf[GEOMETRY_OSM_COLUMN] = result

    return gdf


def calculate_road_width(row):
    is_railway = False
    is_oneway = False
    lanes = 0
    road_type = row[ROAD_OSM_KEY]
    if LANES_OSM_KEY in row:
        lanes = row[LANES_OSM_KEY]
    if ONEWAY_OSM_KEY in row:
        oneway = row[ONEWAY_OSM_KEY]
        is_oneway = oneway == "yes"

    if RAILWAY_OSM_KEY in row:
        is_railway = not pd.isna(row[RAILWAY_OSM_KEY])

    if LANES_OSM_KEY in row:
        if is_railway or pd.isna(row[LANES_OSM_KEY]) or row[LANES_OSM_KEY] is None:
            lanes = 1 if is_oneway else 2

    if ";" in str(lanes):
        lanes = lanes.split(";")[0]
    lanes = float(lanes)
    road_width = lanes * ROAD_LANE_WIDTH
    if road_type in ROAD_WITH_BORDERS or is_railway:
        road_width += (lanes * 2)

    return road_width
