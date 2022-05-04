import geopandas as gpd
from shapely.geometry import MultiPolygon, Polygon, MultiLineString
from shapely.ops import linemerge, unary_union, polygonize

from constants import GEOMETRY_OSM_COLUMN


def copy_geometry(source, dest, start_index=-1):
    source = source[source.geometry != None].explode()
    i = 1
    for index, row in source.iterrows():
        if isinstance(row.geometry, Polygon):
            dest.loc[index if start_index < 0 else start_index + i, GEOMETRY_OSM_COLUMN] = row.geometry
            i = i+1

    return dest


def remove_interiors(poly):
    if poly.interiors:
        return Polygon(list(poly.exterior.coords))
    else:
        return poly


def pop_largest(gs):
    geoms = [g.area for g in gs]
    return gs.pop(geoms.index(max(geoms)))


def close_holes(geom):
    if isinstance(geom, MultiPolygon):
        ser = gpd.GeoSeries([remove_interiors(g) for g in geom])
        big = pop_largest(ser)
        outers = ser.loc[~ser.within(big)].tolist()
        if outers:
            return MultiPolygon([big] + outers)
        return Polygon(big)
    if isinstance(geom, Polygon):
        return remove_interiors(geom)


def cut_polygon_by_line(polygon, line):
    lines_to_merge = [line]
    if polygon.boundary.geom_type == "MultiLineString":
        for l in polygon.boundary:
            lines_to_merge.append(l)
    else:
        lines_to_merge.append(polygon.boundary)
    merged = linemerge(lines_to_merge)
    borders = unary_union(merged)
    polygons = polygonize(borders)
    return list(polygons)


def convert_3D_2D(geometry):
    '''
    Takes a GeoSeries of 3D Multi/Polygons (has_z) and returns a list of 2D Multi/Polygons
    '''
    new_geo = []
    for p in geometry:
        if p.has_z:
            if p.geom_type == 'Polygon':
                lines = [xy[:2] for xy in list(p.exterior.coords)]
                new_p = Polygon(lines)
                new_geo.append(new_p)
            elif p.geom_type == 'MultiPolygon':
                new_multi_p = []
                for ap in p:
                    lines = [xy[:2] for xy in list(ap.exterior.coords)]
                    new_p = Polygon(lines)
                    new_multi_p.append(new_p)
                new_geo.append(MultiPolygon(new_multi_p))
    return new_geo

    