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

from utils.install_lib import install_python_lib

try:
    import geopandas as gpd
except ModuleNotFoundError:
    install_python_lib('geoPandas')
    import geopandas as gpd

from shapely.geometry import MultiPolygon, Polygon, LineString
from shapely.ops import linemerge, unary_union, polygonize


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


def extend_line(p1, p2, ratio):
    # Creates a line extrapoled in p1->p2 direction
    a = p1
    b = (p1[0]+ratio*(p2[0]-p1[0]), p1[1]+ratio*(p2[1]-p1[1]) )
    return LineString([a, b])
