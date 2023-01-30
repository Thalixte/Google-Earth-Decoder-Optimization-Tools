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

from constants import HEIGHT_MAPS_DISPLAY_NAME, HEIGHT_MAP_DISPLAY_NAME
from msfs_project.position import MsfsPosition
from utils import isolated_print
from utils.octant import get_latlonbox_from_file_name


class MsfsHeightMapGroup:
    tag: str
    display_name: str
    group_index: int
    group_id: int
    group_generated: bool

    def __init__(self, xml=None, elem=None, group_display_name=HEIGHT_MAPS_DISPLAY_NAME, group_id=None):
        self.tag = "Group"
        self.display_name = group_display_name
        self.group_index = 1
        self.group_id = 1 if group_id is None else group_id
        self.group_generated = (group_id is not None)

        if xml is not None and elem is not None:
            self.__init_from_xml(xml, elem)

    def __init_from_xml(self, xml, elem):
        parent_group_id = elem.get(xml.PARENT_GROUP_ID_ATTR)

        if parent_group_id is None:
            return

        groups = xml.root.findall(xml.PARENT_GROUP_SEARCH_PATTERN + elem.get(xml.PARENT_GROUP_ID_ATTR) + xml.PATTERN_SUFFIX)
        for group in groups:
            self.display_name = group.get(xml.DISPLAY_NAME_ATTR)
            group_index = elem.get(xml.GROUP_INDEX_ATTR)
            self.group_index = int(group_index) if group_index is not None else -1
            self.group_id = int(group.get(xml.GROUP_ID_ATTR))
            self.group_generated = bool(group.get(xml.GROUP_GENERATED_ATTR))


class MsfsHeightMap:
    display_name: str
    width: float
    size: int
    falloff: int
    surface = "{47D48287-3ADE-4FC5-8BEC-B6B36901E612}"
    priority: int
    height_data: str
    pos: MsfsPosition
    pos2: MsfsPosition
    mid: MsfsPosition
    altitude: str
    group: MsfsHeightMapGroup

    def __init__(self, tile=None, elem=None, height_data=None, xml=None, width=None, altitude=None, group_id=None):
        self.display_name = HEIGHT_MAP_DISPLAY_NAME

        if tile is not None and height_data is not None:
            self.__init_from_height_data(tile, height_data, width, altitude, group_id)

        if xml is not None and elem is not None:
            self.__init_from_xml(xml, elem)

    def to_xml(self, xml):
        xml.add_height_map(self)

    def __init_from_height_data(self, tile, height_data, width, altitude, group_id):
        lod = len(tile.name)
        lod_limit = lod - 1 if lod >= 19 else lod
        self.falloff = 100
        self.priority = 10
        self.altitude = altitude
        self.size = self.__guess_height_map_size(height_data)
        self.pos = get_latlonbox_from_file_name(tile.name).bl_point
        self.pos2 = get_latlonbox_from_file_name(tile.name[0:lod_limit]).tl_point
        self.mid = get_latlonbox_from_file_name(tile.name).mid_point
        self.height_data = self.__serialize_height_data(height_data)
        self.width = width
        self.group = MsfsHeightMapGroup(group_id=group_id)

    def __init_from_xml(self, xml, elem):
        self.display_name = elem.get(xml.DISPLAY_NAME_ATTR)
        self.falloff = elem.get(xml.FALLOFF_ATTR)
        self.priority = elem.get(xml.PRIORITY_ATTR)
        self.altitude = elem.get(xml.ALTITUDE_ATTR)
        self.pos = MsfsPosition(elem.get(xml.LATITUDE_ATTR), elem.get(xml.LONGITUDE2_ATTR), self.altitude)
        self.pos2 = MsfsPosition(elem.get(xml.LATITUDE2_ATTR), elem.get(xml.LONGITUDE2_ATTR), self.altitude)
        self.mid = MsfsPosition(elem.get(xml.LATITUDE_ATTR), elem.get(xml.LONGITUDE_ATTR), self.altitude)
        self.width = elem.get(xml.WIDTH_ATTR)

        height_maps = xml.find_rectangle_height_data(elem)

        for height_map in height_maps:
            self.size = height_map.get(xml.WIDTH_ATTR)
            self.height_data = height_map.get(xml.DATA_ATTR)

        self.group = MsfsHeightMapGroup(elem.get(xml.PARENT_GROUP_ID_ATTR))

    def __serialize_height_data(self, height_data):
        result = ""
        for i, x_data in enumerate(height_data.values()):
            if len(x_data) != self.size:
                continue

            x_data.reverse()
            result = (" ".join([str(h) for h in x_data])) + " " + result

        return result.strip()

    @staticmethod
    def __guess_height_map_size(height_data):
        x_size = [len(x_data) for x_data in list(height_data.values())]
        return max(x_size, key=x_size.count)


class MsfsHeightMaps:
    rectangles: list
    group: MsfsHeightMapGroup

    def __init__(self, xml, group_display_name=None):
        self.rectangles = []
        self.__init_from_xml(xml, group_display_name)

    def __init_from_xml(self, xml, group_name):
        rectangles = xml.find_rectangles() if group_name is None else xml.find_rectangles(group_name=group_name)

        if not rectangles:
            return

        for rectangle in rectangles:
            self.rectangles.append(MsfsHeightMap(xml=xml, elem=rectangle))

        if group_name is not None:
            self.group = MsfsHeightMapGroup(xml, rectangles[0])
