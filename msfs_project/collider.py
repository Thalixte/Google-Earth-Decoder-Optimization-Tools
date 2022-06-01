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

from msfs_project.position import MsfsPosition
from msfs_project.scene_object import MsfsSceneObject
from utils import get_coords_from_file_name, get_position_from_file_name


class MsfsCollider(MsfsSceneObject):
    associated_tile: str

    def __init__(self, folder, name, definition_file, objects_xml=None):
        super().__init__(folder, name, definition_file, True)
        self.associated_tile = name.split("_")[0]
        self.coords = get_coords_from_file_name(self.associated_tile)
        altitude = 0.0
        if not objects_xml is None:
            altitude = float(objects_xml.get_object_altitude(self.xml.guid))
        pos = get_position_from_file_name(self.associated_tile)
        self.pos = MsfsPosition(pos[0], pos[1], altitude)

    def remove_files(self):
        for lod in self.lods:
            lod.remove_file()
        self.remove_file()
