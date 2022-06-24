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

from utils import Xml
import xml.etree.ElementTree as Et


class HeightMapXml(Xml):
    RECTANGLE_TAG = "Rectangle"
    HEIGHT_MAP_TAG = "Heightmap"
    LATITUDE_ATTR = "latitude"
    LATITUDE2_ATTR = "latitude2"
    LONGITUDE_ATTR = "longitude"
    LONGITUDE2_ATTR = "longitude2"
    PARENT_GROUP_ID_ATTR = "parentGroupID"
    GROUP_INDEX_ATTR = "groupIndex"
    ALTITUDE_ATTR = "altitude"
    ALTITUDE2_ATTR = "altitude2"
    VALUE_ATTR = "value"
    GROUP_ID_ATTR = "groupID"
    GROUP_GENERATED_ATTR = "groupGenerated"
    WIDTH_ATTR = "width"
    FALLOFF_ATTR = "falloff"
    SURFACE_ATTR = "surface"
    PRIORITY_ATTR = "priority"
    DATA_ATTR = "data"

    RECTANGLE_SEARCH_PATTERN = "./" + RECTANGLE_TAG
    HEIGHT_MAP_SEARCH_PATTERN = "./" + HEIGHT_MAP_TAG

    def __init__(self, file_folder, file_name):
        super().__init__(file_folder, file_name)

    def add_height_map(self, height_map):
        rectangle_elem = self.__add_height_map_rectangle(height_map)
        self.__add_height_map(rectangle_elem, height_map)
        self.save()

    def find_rectangles(self):
        return self.root.findall(self.RECTANGLE_SEARCH_PATTERN)

    def find_rectangle_height_data(self, root):
        return root.findall(self.HEIGHT_MAP_SEARCH_PATTERN)

    def __add_height_map_rectangle(self, height_map):
        return Et.SubElement(self.root, self.RECTANGLE_TAG, attrib={
            self.PARENT_GROUP_ID_ATTR: str(height_map.group.group_id),
            self.WIDTH_ATTR: str(height_map.width),
            self.FALLOFF_ATTR: str(height_map.falloff),
            self.SURFACE_ATTR: height_map.surface,
            self.PRIORITY_ATTR: str(height_map.priority),
            self.LATITUDE_ATTR: str(height_map.pos.lat),
            self.LONGITUDE_ATTR: str(height_map.mid.lon),
            self.ALTITUDE_ATTR: str(height_map.altitude),
            self.LATITUDE2_ATTR: str(height_map.pos2.lat),
            self.LONGITUDE2_ATTR: str(height_map.mid.lon),
            self.ALTITUDE2_ATTR: str(height_map.altitude)})

    def __add_height_map(self, rectangle, height_map):
        return Et.SubElement(rectangle, self.HEIGHT_MAP_TAG, attrib={
            self.WIDTH_ATTR: str(height_map.size),
            self.DATA_ATTR: str(height_map.height_data)})
