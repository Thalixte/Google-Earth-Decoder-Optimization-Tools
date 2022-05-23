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

from shapely.geometry import Polygon, JOIN_STYLE, CAP_STYLE, MultiPolygon, LineString, MultiPoint, Point
from shapely.ops import linemerge, unary_union, polygonize, nearest_points

from constants import GEOMETRY_OSM_COLUMN, BOUNDING_BOX_OSM_KEY, SHAPE_TEMPLATES_FOLDER, OSM_LAND_SHAPEFILE
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


def create_tile_bounding_box(tile):
    b = bbox_to_poly(tile.coords[1], tile.coords[0], tile.coords[2], tile.coords[3])
    return gpd.GeoDataFrame(pd.DataFrame([], index=[0]), crs={"init": EPSG.key + str(EPSG.WGS84_degree_unit)}, geometry=[b]), b


def create_bounding_box_from_tiles(tiles, dest_folder):
    result = None
    pbar = ProgressBar(list(tiles.values()), title="CREATE BOUNDING BOX OSM FILES FOR EACH TILE")
    for i, tile in enumerate(tiles.values()):
        tile.create_bbox_osm_file(dest_folder)
        pbar.update("osm files created for %s tile" % tile.name)

        if i <= 0:
            result = tile.bbox_gdf.copy()
        else:
            result = copy_geometry(tile.bbox_gdf, result, i)

    result = result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)
    result[GEOMETRY_OSM_COLUMN] = result[GEOMETRY_OSM_COLUMN].apply(lambda p: close_holes(p))
    result = resize_gdf(result, 10)
    return result


def create_exclusion_masks_from_tiles(tiles, dest_folder, b, exclusion_mask):
    pbar = ProgressBar(list(tiles.values()), title="CREATE EXCLUSION MASKS OSM FILES")
    for i, tile in enumerate(tiles.values()):
        tile.create_exclusion_mask_osm_file(dest_folder, b, exclusion_mask)
        pbar.update("exclusion mask created for %s tile" % tile.name)


def resize_gdf(gdf, resize_distance):
    gdf = gdf.to_crs(EPSG.key + str(EPSG.WGS84_meter_unit))
    gdf[GEOMETRY_OSM_COLUMN] = gdf[GEOMETRY_OSM_COLUMN].buffer(resize_distance, cap_style=CAP_STYLE.flat, join_style=JOIN_STYLE.mitre, single_sided=True)
    return gdf.to_crs(EPSG.key + str(EPSG.WGS84_degree_unit))


def create_gdf_from_osm_data(coords, key, tags):
    result = ox.geometries_from_bbox(coords[0], coords[1], coords[2], coords[3], tags={key: tags})
    if not result.empty:
        result = result[[GEOMETRY_OSM_COLUMN, key]]
        result = result[(result.geom_type == SHAPELY_TYPE.polygon) | (result.geom_type == SHAPELY_TYPE.multiPolygon)]

    return result


def create_land_mass_gdf(bbox, b):
    result = gpd.read_file(os.path.join(SHAPE_TEMPLATES_FOLDER, OSM_LAND_SHAPEFILE), bbox=b).clip(bbox.geometry)
    return result[[GEOMETRY_OSM_COLUMN]].dissolve()


def create_sea_gdf(land_mass, bbox):
    # multicoords = [list(line.coords) for line in coastlines.geometry if line.geom_type != SHAPELY_TYPE.polygon]
    # # Making a flat list -> LineString
    # input_l = LineString([item for sublist in multicoords for item in sublist])
    #
    # keep_polys = []

    # for input_p in bbox.geometry:
    #     unioned = input_p.boundary.union(input_l)
    #     for poly in polygonize(unioned):
    #         if poly.representative_point().within(input_p):
    #             if globe.is_land(poly.centroid.y, poly.centroid.x):
    #                 keep_polys.append(poly)

    # remaining polygons are the split polys of original shape
    # bbox[GEOMETRY_OSM_COLUMN] = MultiPolygon(keep_polys)
    # osm_xml = OsmXml(self.osmfiles_folder, BOUNDING_BOX_OSM_FILE_PREFIX + OSM_FILE_EXT)
    # osm_xml.create_from_geodataframes([bbox], b)
    # bbox.to_file(os.path.join(self.osmfiles_folder, BOUNDING_BOX_OSM_FILE_PREFIX + SHP_FILE_EXT))

    result = land_mass.overlay(bbox, how=OVERLAY_OPERATOR.symmetric_difference).assign(boundary=BOUNDING_BOX_OSM_KEY)
    return result[[GEOMETRY_OSM_COLUMN]].dissolve()


def create_exclusion_gdf(landuse, leisure, natural, water, aeroway, sea):
    result = landuse.copy()

    if not leisure.empty:
        # slightly extend the leisure borders to remove bordering trees
        leisure = resize_gdf(leisure, 20)
        result = result.overlay(leisure, how=OVERLAY_OPERATOR.union)
    if not natural.empty:
        result = result.overlay(natural, how=OVERLAY_OPERATOR.union)
    if not water.empty:
        result = result.overlay(water, how=OVERLAY_OPERATOR.union)
    if not aeroway.empty:
        result = result.overlay(aeroway, how=OVERLAY_OPERATOR.union)
    if not sea.empty:
        result = result.overlay(sea, how=OVERLAY_OPERATOR.union)

    return result.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)


def create_scenery_shape_gdf(bbox, exclusion):
    bbox = resize_gdf(bbox, -100)
    return preserve_holes(bbox.overlay(exclusion, how=OVERLAY_OPERATOR.difference), split_method=PRESERVE_HOLES_METHOD.derivation_split)


def clip_gdf(gdf, clip):
    result = gdf
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
    result = gdf

    result_p = result.geometry.unary_union
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
        result = result.explode()

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
        proj_other_centroid_pts = [Point([pt.x, 0]) for pt in other_centroid_pts]

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
        for line in input_p.boundary:
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

