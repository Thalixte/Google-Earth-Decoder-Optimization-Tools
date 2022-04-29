import geopandas as gpd
from shapely.geometry import MultiPolygon, Polygon


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
    