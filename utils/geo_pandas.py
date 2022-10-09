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
import warnings

from shapely.errors import ShapelyDeprecationWarning

from constants import GEOMETRY_OSM_COLUMN, BOUNDING_BOX_OSM_KEY, SHAPE_TEMPLATES_FOLDER, OSM_LAND_SHAPEFILE, ROAD_OSM_KEY, BRIDGE_OSM_TAG, SERVICE_OSM_KEY, NOT_SHORE_WATER_OSM_KEY, WATER_OSM_KEY, NATURAL_OSM_KEY, OSM_TAGS, FOOTWAY_OSM_TAG, PATH_OSM_TAG, MAN_MADE_OSM_KEY, PIER_OSM_TAG, GOLF_OSM_KEY, FAIRWAY_OSM_TAG, EOL, CEND, TUNNEL_OSM_TAG, SEAMARK_TYPE_OSM_TAG, BUILDING_OSM_KEY, SHP_FILE_EXT, ELEMENT_TY_OSM_KEY, OSMID_OSM_KEY, RAILWAY_OSM_KEY, LANES_OSM_KEY, ONEWAY_OSM_KEY, ROAD_WITH_BORDERS, \
    ROAD_LANE_WIDTH, GEOCODE_OSM_FILE_PREFIX, PEDESTRIAN_ROAD_TYPE, FOOTWAY_ROAD_TYPE, SERVICE_ROAD_TYPE, LANDUSE_OSM_KEY, CONSTRUCTION_OSM_KEY, GDAL_LIB_PREFIX, FIONA_LIB_PREFIX, LAND_MASS_REPO, LAND_MASS_ARCHIVE, LEISURE_OSM_KEY
from utils import pr_bg_orange, install_python_lib, install_alternate_python_lib, install_shapefile_resource

try:
    import osgeo
except ModuleNotFoundError:
    install_alternate_python_lib(GDAL_LIB_PREFIX)

try:
    import networkx
except ModuleNotFoundError:
    install_python_lib('networkx')

try:
    import rtree
except ModuleNotFoundError:
    install_python_lib('rtree')

try:
    import matplotlib
except ModuleNotFoundError:
    install_python_lib('matplotLib')

try:
    import fiona
except ModuleNotFoundError:
    install_alternate_python_lib(FIONA_LIB_PREFIX)

try:
    import pandas as pd
except ModuleNotFoundError:
    install_python_lib('pandas')
    import pandas as pd

try:
    import geopandas as gpd
except ModuleNotFoundError:
    install_python_lib('geoPandas')
    import geopandas as gpd

try:
    import osmnx as ox
except ModuleNotFoundError:
    install_python_lib('osmnx')
    import osmnx as ox

try:
    import shapely
except ModuleNotFoundError:
    install_python_lib('shapely')
    import shapely

from osmnx.utils_geo import bbox_to_poly

from shapely.geometry import Polygon, JOIN_STYLE, CAP_STYLE, MultiPolygon, LineString, MultiPoint, Point
from shapely.ops import linemerge, unary_union, polygonize, nearest_points
from utils.progress_bar import ProgressBar
from utils.geometry import close_holes, extend_line


class EPSG:
    key = "epsg:"
    WGS84_degree_unit = 4326
    WGS84_meter_unit = 3857


class SHAPELY_TYPE:
    point = "Point"
    multiPoint = "MultiPoint"
    lineString = "LineString"
    multiLineString = "MultiLineString"
    polygon = "Polygon"
    multiPolygon = "MultiPolygon"
    none = "None"


class OSMID_TYPE:
    way = "way"
    relation = "relation"


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
    result[GEOMETRY_OSM_COLUMN] = result[GEOMETRY_OSM_COLUMN].apply(lambda p: close_holes(p))
    result = resize_gdf(result, 10)
    return result


def create_empty_gdf():
    return gpd.GeoDataFrame(columns=[GEOMETRY_OSM_COLUMN], geometry=GEOMETRY_OSM_COLUMN)


def create_bounding_box(coords):
    b = bbox_to_poly(coords[1], coords[0], coords[2], coords[3])
    return gpd.GeoDataFrame(pd.DataFrame([], index=[0]), crs=EPSG.key + str(EPSG.WGS84_degree_unit), geometry=[b]), b


def create_exclusion_masks_from_tiles(tiles, dest_folder, b, exclusion_mask, keep_building_mask=None, airport_mask=None, ground_exclusion_mask=None, rocks=None, keep_holes=True, file_prefix="", title="CREATE EXCLUSION MASKS OSM FILES"):
    valid_tiles = [tile for tile in list(tiles.values()) if tile.valid]
    pbar = ProgressBar(valid_tiles, title=title)
    exclusion = exclusion_mask.copy()

    for i, tile in enumerate(valid_tiles):
        tile.create_exclusion_mask_osm_file(dest_folder, b, exclusion, keep_building_mask=keep_building_mask, airport_mask=airport_mask, ground_exclusion_mask=ground_exclusion_mask, rocks=rocks, keep_holes=keep_holes, file_prefix=file_prefix)
        pbar.update("exclusion mask created for %s tile" % tile.name)


def resize_gdf(gdf, resize_distance, single_sided=True):
    if gdf.empty:
        return gdf

    gdf = gdf.to_crs(EPSG.key + str(EPSG.WGS84_meter_unit))
    gdf[GEOMETRY_OSM_COLUMN] = gdf[GEOMETRY_OSM_COLUMN].buffer(resize_distance, cap_style=CAP_STYLE.flat, join_style=JOIN_STYLE.mitre, single_sided=single_sided)
    return gdf.to_crs(EPSG.key + str(EPSG.WGS84_degree_unit))


def load_gdf_from_geocode(geocode, geocode_margin=5.0, preserve_roads=True, preserve_buildings=True, keep_data=False, coords=None, shpfiles_folder=None, display_warnings=True, check_geocode=False):
    ox.config(use_cache=False)
    try:
        warnings.simplefilter("ignore", FutureWarning, append=True)
        result = ox.geocode_to_gdf(geocode)
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

    load_gdf_list = [None] * 5
    if display_warnings:
        pbar = ProgressBar(load_gdf_list, title="RETRIEVE GEODATAFRAMES (THE FIRST TIME, MAY TAKE SOME TIME TO COMPLETE, BE PATIENT...)")
        pbar.update("retrieving buildings geodataframe...", stall=True)
    # load gdf twice to ensure to retrieve if from cache (to have osmid in a key, not in an index)
    load_gdf(coords, BUILDING_OSM_KEY, True, shp_file_path=os.path.join(shpfiles_folder, BUILDING_OSM_KEY + SHP_FILE_EXT))
    orig_building = load_gdf(coords, BUILDING_OSM_KEY, True, shp_file_path=os.path.join(shpfiles_folder, BUILDING_OSM_KEY + SHP_FILE_EXT), keep_geocode_data=True)
    if display_warnings:
        pbar.update("buildings geodataframe retrieved")
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
    road = prepare_roads_gdf(orig_road, orig_railway, automatic_road_width_calculation=False)

    if result.empty:
        try:
            if coords is not None and shpfiles_folder is not None:
                osmid = geocode
                if ELEMENT_TY_OSM_KEY in orig_building and OSMID_OSM_KEY in orig_building:
                    result = orig_building[((orig_building[ELEMENT_TY_OSM_KEY] == OSMID_TYPE.way) | (orig_building[ELEMENT_TY_OSM_KEY] == OSMID_TYPE.relation)) & (orig_building[OSMID_OSM_KEY] == int(osmid))]
                if ELEMENT_TY_OSM_KEY in orig_leisure and OSMID_OSM_KEY in orig_leisure:
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
        road = prepare_roads_gdf(orig_road, orig_railway)
        road = road.clip(result_bbox, keep_geom_type=True)
        # for debugging purpose, generate the shp file
        if not road.empty:
            warnings.simplefilter("ignore", FutureWarning, append=True)
            warnings.simplefilter("ignore", UserWarning, append=True)
            road.to_file(os.path.join(shpfiles_folder, GEOCODE_OSM_FILE_PREFIX + "_" + ROAD_OSM_KEY + SHP_FILE_EXT))
            road = clip_gdf(road, result)
            road = road[[GEOMETRY_OSM_COLUMN]]
            result = difference_gdf(result, road)

    if not building_mask.empty and preserve_buildings:
        building_mask = building_mask[[GEOMETRY_OSM_COLUMN]]
        result = difference_gdf(result, building_mask)

    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)


def load_gdf(coords, key, tags, shp_file_path="", keep_geocode_data=False, is_roads=False, is_sea=False, is_grass=False, land_mass=None, bbox=None):
    has_cache = os.path.isfile(shp_file_path)
    filesize = os.path.getsize(shp_file_path)
    keys = [key]

    if has_cache:
        if filesize > 0:
            result = gpd.read_file(shp_file_path)
            result = result[~result[GEOMETRY_OSM_COLUMN].isna()]
        else:
            return create_empty_gdf()
    else:
        if is_sea and land_mass is not None and bbox is not None:
            result = symmetric_difference_gdf(land_mass, bbox).assign(boundary=BOUNDING_BOX_OSM_KEY)
        else:
            warnings.simplefilter("ignore", DeprecationWarning, append=True)
            result = ox.geometries_from_bbox(coords[0], coords[1], coords[2], coords[3], tags={key: tags})

            # truncate index fields to avoid ogr2ogr warning logs
            if not result.empty:
                result.index.names = list(map(lambda x: x[:10], result.index.names))

            # remove points to fix shapefile saving issues
            result = result[~(result.geom_type == SHAPELY_TYPE.point)]

    if not result.empty:
        keys.insert(0, GEOMETRY_OSM_COLUMN)

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

        if keep_geocode_data and has_cache:
            keys.append(ELEMENT_TY_OSM_KEY)
            keys.append(OSMID_OSM_KEY)

        result = result[keys]

        if not has_cache and shp_file_path != "":
            if not is_roads and not keep_geocode_data:
                result = resize_gdf(result, 0.00001)

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
    roads = roads.append(railways)
    has_bridge = False
    has_bridge_path = False
    has_seamark_bridge = False
    has_pier = False
    bridge = None
    bridge_path = None
    seamark_bridge = None
    pier = None

    if not roads.empty:
        roads = roads[~roads[GEOMETRY_OSM_COLUMN].isna()]

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
                pier = pier.append(roads[(roads[ROAD_OSM_KEY] == FOOTWAY_OSM_TAG) & ~(roads[BRIDGE_OSM_TAG].isna())])
                pier = resize_gdf(pier, 12, single_sided=False)
                has_pier = not pier.empty

            if has_bridge:
                result = result.append(bridge)

            if has_bridge_path:
                result = result.append(bridge_path)

            if has_seamark_bridge:
                result = result.append(seamark_bridge)
        else:
            if TUNNEL_OSM_TAG in roads:
                roads = roads[roads[TUNNEL_OSM_TAG].isna()]

            result = roads.copy()
            result = result[~(result[ROAD_OSM_KEY] == PEDESTRIAN_ROAD_TYPE) & ~(result[ROAD_OSM_KEY] == FOOTWAY_ROAD_TYPE) & ~(result[ROAD_OSM_KEY] == SERVICE_ROAD_TYPE)]

        result = result.reset_index(drop=True)
        result = result.to_crs(EPSG.key + str(EPSG.WGS84_meter_unit))
        for index, row in result.iterrows():
            road_width = calculate_road_width(row) if automatic_road_width_calculation else 22
            result.loc[index, GEOMETRY_OSM_COLUMN] = row[GEOMETRY_OSM_COLUMN].buffer(road_width, resolution=32, cap_style=CAP_STYLE.square, join_style=JOIN_STYLE.mitre, mitre_limit=20.0, single_sided=False)
        result = result.to_crs(EPSG.key + str(EPSG.WGS84_degree_unit))

        if has_pier:
            result = result.append(pier)

        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]
        result[GEOMETRY_OSM_COLUMN] = result[GEOMETRY_OSM_COLUMN].buffer(0)

    return result


def prepare_sea_gdf(gdf):
    result = gdf.copy()

    if not result.empty:
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result[[GEOMETRY_OSM_COLUMN]].dissolve()


def prepare_golf_gdf(gdf):
    result = create_empty_gdf()

    if GOLF_OSM_KEY in gdf:
        result = gdf[(gdf[GOLF_OSM_KEY] == FAIRWAY_OSM_TAG)]

    if not result.empty:
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result[[GEOMETRY_OSM_COLUMN]].dissolve()


def prepare_park_gdf(gdf, road):
    if gdf is None:
        return create_empty_gdf()

    result = gdf.copy()

    if not result.empty:
        if not road.empty:
            # road = road[road[ROAD_OSM_KEY] == "primary"]
            # road = resize_gdf(road, 28, single_sided=False)
            result = difference_gdf(result, road)
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result


def prepare_bbox_gdf(bbox, land_mass, boundary):
    result = clip_gdf(bbox, land_mass)
    result = clip_gdf(result, boundary)
    return resize_gdf(result, 20)


def prepare_building_gdf(gdf):
    result = gdf.copy()

    if not result.empty:
        result = resize_gdf(result, 5)
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY).assign(boundary=BOUNDING_BOX_OSM_KEY)


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


def create_ground_exclusion_gdf(landuse, nature_reserve, natural, aeroway, road, park, airport):
    result = create_empty_gdf()
    result = union_gdf(result, landuse)
    result = union_gdf(result, nature_reserve)
    result = union_gdf(result, natural)
    result = union_gdf(result, aeroway)
    result = union_gdf(result, airport)
    result = union_gdf(result, park)
    result = resize_gdf(result, 10)

    if not road.empty and BRIDGE_OSM_TAG in road:
        bridges = road[~(road[BRIDGE_OSM_TAG].isna())]
        result = difference_gdf(result, bridges)

    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)


def create_shore_water_gdf(orig_water, orig_natural_water, sea, bbox):
    water = orig_water.copy()
    for tag in OSM_TAGS[NOT_SHORE_WATER_OSM_KEY]:
        water = water[~(water[WATER_OSM_KEY] == tag)]
    water = clip_gdf(prepare_gdf(water), bbox)

    natural_water = orig_natural_water.copy()
    for tag in OSM_TAGS[NOT_SHORE_WATER_OSM_KEY]:
        natural_water = natural_water[~(natural_water[NATURAL_OSM_KEY] == tag)]
    natural_water = clip_gdf(prepare_gdf(natural_water), bbox)

    result = create_whole_water_gdf(natural_water, water, sea)
    result = resize_gdf(result, 20)
    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)


def create_terraform_polygons_gdf(gdf, ground_exclusion):
    terraform_gdf = gdf.copy()
    terraform_gdf = difference_gdf(terraform_gdf, ground_exclusion)
    terraform_gdf = terraform_gdf.dissolve()
    result = preserve_holes(resize_gdf(terraform_gdf, -10), split_method=PRESERVE_HOLES_METHOD.derivation_split)
    return result.dissolve()


def create_exclusion_building_polygons_gdf(bbox, exclusion, airport):
    adjusted_exclusion = resize_gdf(exclusion, 20)
    adjusted_exclusion = union_gdf(bbox, adjusted_exclusion)
    adjusted_exclusion = difference_gdf(adjusted_exclusion, airport)
    adjusted_exclusion = resize_gdf(adjusted_exclusion, -50)
    adjusted_exclusion = adjusted_exclusion.dissolve()
    result = preserve_holes(adjusted_exclusion, split_method=PRESERVE_HOLES_METHOD.derivation_split)
    return result


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
    result = gdf.copy()
    result = resize_gdf(result, 1)
    result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    result_p = result.geometry.unary_union

    if result_p is None:
        return result

    if result_p.type == SHAPELY_TYPE.polygon:
        result_p = [result_p]

    warnings.simplefilter("ignore", ShapelyDeprecationWarning, append=True)
    for input_p in result_p:
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
            for pt in other_centroid_pts:
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
    result = []
    n = 0

    data = {"x": [], "y": []}
    for y, heights in hmatrix.items():
        if n % 2 == 0:
            for x, h in heights.items():
                data["x"].append(x)
                data["y"].append(y)

        n = n + 1

    df = pd.DataFrame(data)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["x"], df["y"]), crs=EPSG.key + str(EPSG.WGS84_meter_unit))

    gdf = gdf.to_crs(EPSG.key + str(EPSG.WGS84_degree_unit))

    for point in gdf[GEOMETRY_OSM_COLUMN]:
        co = list(point.coords)
        result.append((lat + co[0][0], lon + co[0][1]))

    gdf[GEOMETRY_OSM_COLUMN] = result

    return gdf


def calculate_road_width(row):
    road_type = row[ROAD_OSM_KEY]
    lanes = row[LANES_OSM_KEY]
    oneway = row[ONEWAY_OSM_KEY]
    is_oneway = oneway == "yes"
    is_railway = not pd.isna(row[RAILWAY_OSM_KEY])
    if is_railway or pd.isna(row[LANES_OSM_KEY]) or row[LANES_OSM_KEY] is None:
        lanes = 1 if is_oneway else 2

    lanes = float(lanes)
    road_width = lanes * ROAD_LANE_WIDTH
    if road_type in ROAD_WITH_BORDERS or is_railway:
        road_width += (lanes * 2)

    return road_width
