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

import pandas as pd
import geopandas as gpd
import osmnx as ox
from osmnx.utils_geo import bbox_to_poly

from shapely.geometry import Polygon, JOIN_STYLE, CAP_STYLE, MultiPolygon, LineString, MultiPoint, Point, mapping
from shapely.ops import linemerge, unary_union, polygonize, nearest_points

from constants import GEOMETRY_OSM_COLUMN, BOUNDING_BOX_OSM_KEY, SHAPE_TEMPLATES_FOLDER, OSM_LAND_SHAPEFILE, ROADS_OSM_KEY, BRIDGE_OSM_TAG, SERVICE_OSM_KEY, SLIPWAY_OSM_TAG, NOT_SHORE_WATER_OSM_KEY, WATER_OSM_KEY, NATURAL_OSM_KEY, OSM_TAGS, FOOTWAY_OSM_TAG, PATH_OSM_TAG, PEDESTRIAN_OSM_TAG, MAN_MADE_OSM_KEY, PIER_OSM_TAG, GOLF_OSM_KEY, FAIRWAY_OSM_TAG, EOL, CEND, TUNNEL_OSM_TAG, SEAMARK_TYPE_OSM_TAG
from utils import pr_bg_orange
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


def create_bounding_box(coords):
    b = bbox_to_poly(coords[1], coords[0], coords[2], coords[3])
    return gpd.GeoDataFrame(pd.DataFrame([], index=[0]), crs=EPSG.key + str(EPSG.WGS84_degree_unit), geometry=[b]), b


def create_exclusion_masks_from_tiles(tiles, dest_folder, b, exclusion_mask, ground_exclusion_mask=None, rocks=None, keep_holes=True, file_prefix="", title="CREATE EXCLUSION MASKS OSM FILES"):
    valid_tiles = [tile for tile in list(tiles.values()) if tile.valid]
    pbar = ProgressBar(valid_tiles, title=title)
    exclusion = exclusion_mask.copy()

    for i, tile in enumerate(valid_tiles):
        tile.create_exclusion_mask_osm_file(dest_folder, b, exclusion, ground_exclusion_mask=ground_exclusion_mask, rocks=rocks, keep_holes=keep_holes, file_prefix=file_prefix)
        pbar.update("exclusion mask created for %s tile" % tile.name)


def resize_gdf(gdf, resize_distance, single_sided=True):
    if gdf.empty:
        return gdf

    gdf = gdf.to_crs(EPSG.key + str(EPSG.WGS84_meter_unit))
    gdf[GEOMETRY_OSM_COLUMN] = gdf[GEOMETRY_OSM_COLUMN].buffer(resize_distance, cap_style=CAP_STYLE.flat, join_style=JOIN_STYLE.mitre, single_sided=single_sided)
    return gdf.to_crs(EPSG.key + str(EPSG.WGS84_degree_unit))


def load_gdf_from_geocode(geocode, keep_data=False):
    try:
        result = ox.geocode_to_gdf(geocode)
    except ValueError:
        pr_bg_orange("Geocode (" + geocode + ") not found in OSM data" + EOL + CEND)
        return gpd.GeoDataFrame(columns=[GEOMETRY_OSM_COLUMN], geometry=GEOMETRY_OSM_COLUMN)

    if keep_data:
        return result

    result = resize_gdf(result, 5)

    if not result.empty:
        result = result[[GEOMETRY_OSM_COLUMN]]

    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)


def load_gdf(coords, key, tags, shp_file_path="", is_roads=False, is_buildings=False, is_sea=False, is_grass=False, land_mass=None, bbox=None):
    has_cache = os.path.isfile(shp_file_path)
    keys = [key]

    if has_cache:
        result = gpd.read_file(shp_file_path)
        result = result[~result[GEOMETRY_OSM_COLUMN].isna()]
    else:
        if is_sea and land_mass is not None and bbox is not None:
            result = symmetric_difference_gdf(land_mass, bbox).assign(boundary=BOUNDING_BOX_OSM_KEY)
        else:
            result = ox.geometries_from_bbox(coords[0], coords[1], coords[2], coords[3], tags={key: tags})
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

        result = result[keys]

        if not has_cache and shp_file_path != "":
            if not is_roads and not is_buildings:
                result = resize_gdf(result, 0.00001)

            try:
                result.to_file(shp_file_path)
            except:
                if os.path.isfile(shp_file_path):
                    os.remove(shp_file_path)
                pass
    else:
        for key in keys:
            result[key] = None

    return result


def prepare_gdf(gdf):
    if gdf is None:
        return None

    result = gdf.copy()

    if not result.empty:
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result


def prepare_roads_gdf(gdf):
    result = gpd.GeoDataFrame(columns=[GEOMETRY_OSM_COLUMN], geometry=GEOMETRY_OSM_COLUMN, crs=EPSG.key + str(EPSG.WGS84_degree_unit))
    roads = gdf.copy()
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

        # fix for bridge paths
        if BRIDGE_OSM_TAG in roads:
            bridge_path = roads[(roads[ROADS_OSM_KEY] == PATH_OSM_TAG) & (roads[BRIDGE_OSM_TAG] == "yes")]
            has_bridge_path = not bridge_path.empty

        if not has_bridge_path:
            roads = roads[~(roads[ROADS_OSM_KEY] == PATH_OSM_TAG)]

        if BRIDGE_OSM_TAG in roads:
            bridge = roads[~(roads[BRIDGE_OSM_TAG].isna())]
            has_bridge = True

        if SEAMARK_TYPE_OSM_TAG in roads:
            seamark_bridge = roads[(roads[SEAMARK_TYPE_OSM_TAG] == BRIDGE_OSM_TAG)]
            has_seamark_bridge = True

        if MAN_MADE_OSM_KEY in roads:
            pier = roads[(roads[ROADS_OSM_KEY] == FOOTWAY_OSM_TAG) & (roads[MAN_MADE_OSM_KEY] == PIER_OSM_TAG)]
            pier = pier.append(roads[(roads[ROADS_OSM_KEY] == FOOTWAY_OSM_TAG) & (roads[BRIDGE_OSM_TAG] == "yes")])
            pier = resize_gdf(pier, 12, single_sided=False)
            has_pier = not pier.empty

        if has_bridge:
            result = result.append(bridge)

        if has_bridge_path:
            result = result.append(bridge_path)

        if has_seamark_bridge:
            result = result.append(seamark_bridge)

        result = resize_gdf(result, 22, single_sided=False)

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
    result = gpd.GeoDataFrame(columns=[GEOMETRY_OSM_COLUMN], geometry=GEOMETRY_OSM_COLUMN)

    if GOLF_OSM_KEY in gdf:
        result = gdf[(gdf[GOLF_OSM_KEY] == FAIRWAY_OSM_TAG)]

    if not result.empty:
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result[[GEOMETRY_OSM_COLUMN]].dissolve()


def prepare_park_gdf(gdf):
    if gdf is None:
        return gpd.GeoDataFrame(columns=[GEOMETRY_OSM_COLUMN], geometry=GEOMETRY_OSM_COLUMN)

    result = gdf.copy()

    if not result.empty:
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result


def prepare_bbox_gdf(bbox, land_mass, boundary):
    result = clip_gdf(bbox, land_mass)
    result = clip_gdf(result, boundary)
    return resize_gdf(result, 20)


def prepare_buildings_gdf(gdf):
    result = gdf.copy()

    if not result.empty:
        result = resize_gdf(result, 5)
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result


def create_land_mass_gdf(sources_path, bbox, b):
    result = gpd.read_file(os.path.join(sources_path, os.path.join(SHAPE_TEMPLATES_FOLDER, OSM_LAND_SHAPEFILE)), bbox=b).clip(bbox.geometry)
    return result[[GEOMETRY_OSM_COLUMN]].dissolve()


def create_buildings_and_water_gdf(buildings, water):
    result = gpd.GeoDataFrame(columns=[GEOMETRY_OSM_COLUMN], geometry=GEOMETRY_OSM_COLUMN)

    result = union_gdf(result, resize_gdf(water, 5))
    result = union_gdf(result, buildings)
    result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)


def create_exclusion_gdf(landuse, leisure, natural, natural_water, water, sea, aeroway, roads):
    result = gpd.GeoDataFrame(columns=[GEOMETRY_OSM_COLUMN], geometry=GEOMETRY_OSM_COLUMN)
    result = union_gdf(result, landuse)
    result = union_gdf(result, resize_gdf(leisure, 20))
    result = union_gdf(result, natural)
    result = union_gdf(result, aeroway)
    result = union_gdf(result, difference_gdf(water, roads))
    result = union_gdf(result, difference_gdf(natural_water, roads))
    result = union_gdf(result, difference_gdf(sea, roads))

    if not roads.empty and BRIDGE_OSM_TAG in roads:
        bridges = roads[roads[BRIDGE_OSM_TAG] == "yes"]
        result = difference_gdf(result, bridges)

    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)


def create_water_bridge_exclusion_gdf(natural_water, water, sea, roads):
    result = gpd.GeoDataFrame(columns=[GEOMETRY_OSM_COLUMN], geometry=GEOMETRY_OSM_COLUMN)
    result = union_gdf(result, intersect_gdf(water, roads))
    result = union_gdf(result, intersect_gdf(natural_water, roads))
    result = union_gdf(result, intersect_gdf(sea, roads))

    return result.dissolve().assign(building=BRIDGE_OSM_TAG)


def create_whole_water_gdf(natural_water, water, sea):
    result = gpd.GeoDataFrame(columns=[GEOMETRY_OSM_COLUMN], geometry=GEOMETRY_OSM_COLUMN)
    result = union_gdf(result, water)
    result = union_gdf(result, natural_water)
    result = union_gdf(result, sea)

    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)


def create_water_exclusion_gdf(natural_water, water, sea, roads):
    result = gpd.GeoDataFrame(columns=[GEOMETRY_OSM_COLUMN], geometry=GEOMETRY_OSM_COLUMN)
    result = union_gdf(result, difference_gdf(water, roads))
    result = union_gdf(result, difference_gdf(natural_water, roads))
    result = union_gdf(result, difference_gdf(sea, roads))

    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)


def create_ground_exclusion_gdf(landuse, leisure, natural, aeroway, roads, park, airport):
    result = gpd.GeoDataFrame(columns=[GEOMETRY_OSM_COLUMN], geometry=GEOMETRY_OSM_COLUMN)
    result = union_gdf(result, landuse)
    result = union_gdf(result, leisure)
    result = union_gdf(result, natural)
    result = union_gdf(result, aeroway)
    result = union_gdf(result, park)
    result = union_gdf(result, airport)

    if not roads.empty and BRIDGE_OSM_TAG in roads:
        bridges = roads[~(roads[BRIDGE_OSM_TAG].isna())]
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
    result = preserve_holes(resize_gdf(terraform_gdf, -10), split_method=PRESERVE_HOLES_METHOD.derivation_split)
    return result.dissolve()


def create_exclusion_building_polygons_gdf(bbox, exclusion, park, airport):
    adjusted_exclusion = resize_gdf(exclusion, 20)
    adjusted_exclusion = union_gdf(bbox, adjusted_exclusion)
    adjusted_exclusion = difference_gdf(adjusted_exclusion, park)
    adjusted_exclusion = difference_gdf(adjusted_exclusion, airport)
    result = preserve_holes(adjusted_exclusion, split_method=PRESERVE_HOLES_METHOD.derivation_split)
    return result


def create_exclusion_vegetation_polygons_gdf(exclusion):
    result = preserve_holes(exclusion, split_method=PRESERVE_HOLES_METHOD.derivation_split)
    return result.dissolve()


def clip_gdf(gdf, clip):
    result = gdf.copy()

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
