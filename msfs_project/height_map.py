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
from constants import HEIGHT_MAPS_DISPLAY_NAME
from msfs_project.position import MsfsPosition
from utils.octant import get_latlonbox_from_file_name


class MsfsHeightMapGroup:
    tag: str
    display_name: str
    group_index: int
    group_id: int
    group_generated: bool

    def __init__(self, group_id=None):
        self.tag = "Group"
        self.display_name = HEIGHT_MAPS_DISPLAY_NAME
        self.group_index = 1
        self.group_id = 1 if group_id is None else group_id
        self.group_generated = (group_id is not None)


class HeightMap:
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

    def __init__(self, tile=None, height_data=None, xml=None, width=None, altitude=None, grid_limit=None, group_id=None):
        if not tile is None and not height_data is None:
            self.__init_from_height_data(tile, height_data, width, altitude, grid_limit, group_id)

        if not xml is None:
            self.__init_from_xml(xml)

    def to_xml(self, xml):
        xml.add_height_map(self)

    def __init_from_height_data(self, tile, height_data, width, altitude, grid_limit, group_id):
        self.falloff = 100
        self.priority = 50000
        self.altitude = altitude
        self.pos = get_latlonbox_from_file_name(tile.name).bl_point
        self.pos2 = get_latlonbox_from_file_name(tile.name).tl_point
        self.mid = get_latlonbox_from_file_name(tile.name).mid_point
        self.size = grid_limit
        self.height_data = self.__serialize_height_data(height_data)
        self.width = width
        self.group = MsfsHeightMapGroup(group_id=group_id)

    def __init_from_xml(self, xml):
        rectangles = xml.find_rectangles()

        if not rectangles:
            return

        for rectangle in rectangles:
            self.falloff = rectangle.get(xml.FALLOFF_ATTR)
            self.priority = rectangle.get(xml.PRIORITY_ATTR)
            self.altitude = rectangle.get(xml.ALTITUDE_ATTR)
            self.pos = MsfsPosition(rectangle.get(xml.LATITUDE_ATTR), rectangle.get(xml.LONGITUDE2_ATTR), self.altitude)
            self.pos2 = MsfsPosition(rectangle.get(xml.LATITUDE2_ATTR), rectangle.get(xml.LONGITUDE2_ATTR), self.altitude)
            self.mid = MsfsPosition(rectangle.get(xml.LATITUDE_ATTR), rectangle.get(xml.LONGITUDE_ATTR), self.altitude)
            self.width = rectangle.get(xml.WIDTH_ATTR)

            height_maps = xml.find_height_maps(rectangle)

            for height_map in height_maps:
                self.size = height_map.get(xml.WIDTH_ATTR)
                self.height_data = height_map.get(xml.DATA_ATTR)

            self.group = MsfsHeightMapGroup(rectangle.get(xml.PARENT_GROUP_ID_ATTR))

    def __serialize_height_data(self, height_data):
        result = ""
        for i, x_data in enumerate(height_data.values()):
            if len(x_data) != self.size:
                continue

            x_data.reverse()
            result = (" ".join([str(h) for h in x_data])) + " " + result

        return result.strip()
