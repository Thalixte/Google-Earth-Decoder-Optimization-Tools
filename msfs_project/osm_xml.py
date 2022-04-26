#  #
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 2
#   of the License, or (at your option) any later version.
#  #
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more dEtails.
#  #
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin StreEt, Fifth Floor, Boston, MA 02110-1301, USA.
#  #
#
#  <pep8 compliant>

from constants import DUMMY_OBJECT
from utils import Xml
import xml.etree.ElementTree as Et


class OsmXml(Xml):
    POLYGON_TYPE = "Polygon"
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
    NAN = "nan"
    GEOMETRY_COL = "geometry"
    APP_NAME = "G.E.D.O.T."

    def __init__(self, file_folder, file_name):
        super().__init__(file_folder, file_name)

    def create_from_geodataframes(self, geopandas_data_frames, bbox_poly, additional_tags=[]):
        osm_root = Et.Element(self.OSM_TAG, attrib={
            self.VERSION_ATTR: self.GENERATOR_VERSION,
            self.GENERATOR_ATTR: self.APP_NAME
        })

        Et.SubElement(osm_root, self.BOUNDS_TAG, attrib={
            self.MIN_LAT_ATTR: str(bbox_poly.bounds[0]),
            self.MIN_LON_ATTR: str(bbox_poly.bounds[1]),
            self.MAX_LAT_ATTR: str(bbox_poly.bounds[2]),
            self.MAX_LON_ATTR: str(bbox_poly.bounds[3])})

        for geopandas_data_frame in geopandas_data_frames:
            for index, row in geopandas_data_frame.iterrows():
                if not row.geometry.geom_type is self.POLYGON_TYPE:
                    continue

                i = -1
                current_way = Et.SubElement(osm_root, self.WAY_TAG, attrib={
                    self.ID_ATTR: str(index[1]),
                    self.VISIBLE_ATTR: str(True),
                    self.VERSION_ATTR: "1",
                    self.UID_ATTR: str(index[1]),
                    self.CHANGES_ET_ATTR: str(False)})

                for point in row.geometry.exterior.coords:
                    i = i + 1
                    current_node = Et.SubElement(osm_root, self.NODE_TAG, attrib={
                        self.ID_ATTR: str(index[1]) + str(i),
                        self.VISIBLE_ATTR: str(True),
                        self.VERSION_ATTR: "1",
                        self.UID_ATTR: str(index[1]),
                        self.LAT_ATTR: str(point[1]),
                        self.LON_ATTR: str(point[0]),
                        self.CHANGES_ET_ATTR: str(False)})

                    Et.SubElement(current_way, self.ND_TAG, attrib={
                        self.REF_ATTR: str(index[1]) + str(i)})

                i = 0
                Et.SubElement(current_way, self.ND_TAG, attrib={
                    self.REF_ATTR: str(index[1]) + str(i)})

                for column in geopandas_data_frame.columns:
                    if column != self.GEOMETRY_COL and str(row[column]) != self.NAN:
                        self.__add_tag(current_node, column, DUMMY_OBJECT)
                        self.__add_tag(current_way, column, DUMMY_OBJECT)

                for additional_tag in additional_tags:
                    self.__add_tag(current_node, additional_tag[0], str(additional_tag[1]))
                    self.__add_tag(current_way, additional_tag[0], str(additional_tag[1]))

        self.tree = Et.ElementTree(element=osm_root)
        self.root = self.tree.getroot()
        self.save()

    def __add_tag(self, node, key, value):
        Et.SubElement(node, self.TAG_TAG, attrib={
            self.KEY_ATTR: key,
            self.VALUE_ATTR: value})
