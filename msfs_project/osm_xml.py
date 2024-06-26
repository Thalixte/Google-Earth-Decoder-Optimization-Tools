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

from utils import install_python_lib
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

try:
    import pandas as pd
except ModuleNotFoundError:
    install_python_lib('pandas')
    import pandas as pd

try:
    import shapely
except ModuleNotFoundError:
    install_python_lib('shapely')
    import shapely

from pandas import isna
from shapely.geometry import Polygon, MultiPolygon, Point

from constants import DUMMY_OBJECT
from utils import Xml
import xml.etree.ElementTree as Et


class OsmXml(Xml):
    POLYGON_TYPE = "Polygon"
    LINESTRING_TYPE = "LineString"
    OSM_TAG = "osm"
    BOUNDS_TAG = "bounds"
    WAY_TAG = "way"
    NODE_TAG = "node"
    ND_TAG = "nd"
    TAG_TAG = "tag"
    VERSION_ATTR = "version"
    GENERATOR_ATTR = "generator"
    MIN_LAT_ATTR = "minlat"
    MIN_LON_ATTR = "minlon"
    MAX_LAT_ATTR = "maxlat"
    MAX_LON_ATTR = "maxlon"
    ID_ATTR = "id"
    VISIBLE_ATTR = "visible"
    UID_ATTR = "uid"
    CHANGES_ET_ATTR = "changesEt"
    LAT_ATTR = "lat"
    LON_ATTR = "lon"
    REF_ATTR = "ref"
    KEY_ATTR = "k"
    VALUE_ATTR = "v"
    GENERATOR_VERSION = "1.0"
    GEOMETRY_OSM_COLUMN = "geometry"
    APP_NAME = "G.E.D.O.T."
    EXTRUDE_TYPE = "building"

    def __init__(self, file_folder, file_name):
        super().__init__(file_folder, file_name)

    def create_from_geodataframes(self, geopandas_data_frames, bbox_poly, extrude=False, additional_tags=[], is_point=False):
        osm_root = Et.Element(self.OSM_TAG, attrib={
            self.VERSION_ATTR: self.GENERATOR_VERSION,
            self.GENERATOR_ATTR: self.APP_NAME
        })

        Et.SubElement(osm_root, self.BOUNDS_TAG, attrib={
            self.MIN_LON_ATTR: str(bbox_poly.bounds[0]),
            self.MIN_LAT_ATTR: str(bbox_poly.bounds[1]),
            self.MAX_LON_ATTR: str(bbox_poly.bounds[2]),
            self.MAX_LAT_ATTR: str(bbox_poly.bounds[3])})

        i = 0
        for geopandas_data_frame in geopandas_data_frames:
            for index, row in geopandas_data_frame.iterrows():
                if not is_point and not isinstance(row.geometry, Polygon) and not isinstance(row.geometry, MultiPolygon):
                    continue

                geometries = []

                if isinstance(row.geometry, Polygon):
                    geometries = [row.geometry]
                elif isinstance(row.geometry, MultiPolygon):
                    for polygon in row.geometry.geoms:
                        geometries.append(polygon)
                elif is_point and isinstance(row.geometry, Point):
                    geometries = [row.geometry]
                else:
                    geometries = row.geometry

                for geometry in geometries:
                    if is_point:
                        if len(geometry.coords) <= 0:
                            continue
                    elif len(geometry.exterior.coords) <= 0:
                        continue

                    current_way = Et.SubElement(osm_root, self.WAY_TAG, attrib={
                        self.ID_ATTR: str(i),
                        self.VISIBLE_ATTR: str(True),
                        self.VERSION_ATTR: "1",
                        self.UID_ATTR: str(i),
                        self.CHANGES_ET_ATTR: str(False)})

                    if is_point:
                        coords = geometry.coords
                    else:
                        coords = geometry.exterior.coords

                    for point in coords:
                        i = i + 1
                        current_node = Et.SubElement(osm_root, self.NODE_TAG, attrib={
                            self.ID_ATTR: str(i),
                            self.VISIBLE_ATTR: str(True),
                            self.VERSION_ATTR: "1",
                            self.UID_ATTR: str(i),
                            self.LAT_ATTR: str(point[1]),
                            self.LON_ATTR: str(point[0]),
                            self.CHANGES_ET_ATTR: str(False)})

                        Et.SubElement(current_way, self.ND_TAG, attrib={self.REF_ATTR: str(i)})

                    for column in geopandas_data_frame.columns:
                        if column != self.GEOMETRY_OSM_COLUMN and not isna(str(row[column])):
                            code = self.EXTRUDE_TYPE if extrude else column
                            self.__add_tag(current_node, code, DUMMY_OBJECT)
                            self.__add_tag(current_way, code, DUMMY_OBJECT)

                    for additional_tag in additional_tags:
                        self.__add_tag(current_node, additional_tag[0], str(additional_tag[1]))
                        self.__add_tag(current_way, additional_tag[0], str(additional_tag[1]))

                    i = i + 1

        self.tree = Et.ElementTree(element=osm_root)
        self.root = self.tree.getroot()
        self.save()

    def __add_tag(self, node, key, value):
        Et.SubElement(node, self.TAG_TAG, attrib={
            self.KEY_ATTR: key,
            self.VALUE_ATTR: value})
