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
from utils import isolated_print
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

    def __init__(self, tile, height_data, width, altitude, grid_limit, group_id=None):
        self.falloff = 100
        self.priority = 0
        self.pos = get_latlonbox_from_file_name(tile.name).bl_point
        self.pos2 = get_latlonbox_from_file_name(tile.name).tl_point
        self.mid = get_latlonbox_from_file_name(tile.name).mid_point
        self.size = grid_limit
        self.height_data = self.__serialize_height_data(height_data, grid_limit)
        self.width = width
        self.altitude = altitude
        self.group = MsfsHeightMapGroup(group_id=group_id)

    def to_xml(self, xml):
        xml.add_height_map(self)

    def __serialize_height_data(self, height_data, grid_limit):
        result = ""
        for i, x_data in enumerate(height_data.values()):
            if len(x_data) != self.size:
                continue

            x_data.reverse()
            result = (" ".join([str(h) for h in x_data])) + " " + result

        return result.strip()
