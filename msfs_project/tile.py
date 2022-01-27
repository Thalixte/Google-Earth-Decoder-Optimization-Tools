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

import os
from pathlib import Path

from msfs_project.scene_object import MsfsSceneObject
from msfs_project.position import MsfsPosition
from msfs_project.objects_xml import ObjectsXml
from utils import get_coords_from_file_name, get_position_from_file_name
from utils.minidom_xml import add_scenery_object


class MsfsTile(MsfsSceneObject):
    new_tiles: dict

    def __init__(self, folder, name, definition_file):
        super().__init__(folder, name, definition_file)
        self.coords = get_coords_from_file_name(self.name)
        pos = get_position_from_file_name(self.name)
        self.pos = MsfsPosition(pos[0], pos[1], 0)
        self.new_tiles = {}

    def create_optimization_folders(self, linked_tiles, dry_mode=False, pbar=None):
        other_tiles = [tile for tile in linked_tiles if tile.name != self.name]
        for lod in self.lods:
            if lod.optimized: continue
            if not dry_mode:
                lod.create_optimization_folder(other_tiles)
            if not pbar is None:
                if dry_mode and not os.path.isdir(os.path.join(lod.folder, lod.name)):
                    pbar.range += 1
                else:
                    pbar.update("folder %s created" % lod.name)

    def split(self, settings, objects_xml_folder, objects_xml_file):
        for i, lod in enumerate(self.lods):
            lod.split(self.name, str(settings.target_min_size_values[(len(self.lods) - 1) - i]), self)

        for new_tile_path in self.new_tiles.values():
            path = Path(new_tile_path)
            new_tile = MsfsTile(self.folder, path.stem, path.name)
            self.__add_splitted_tile(objects_xml_folder, objects_xml_file, self.xml.guid, new_tile)

        self.remove_file()

    @staticmethod
    def __add_splitted_tile(objects_xml_folder, objects_xml_file, guid, new_tile):
        objects_xml = ObjectsXml(objects_xml_folder, objects_xml_file)
        for scenery_object in objects_xml.find_scenery_objects(guid):
            add_scenery_object(objects_xml.file_path, new_tile, scenery_object)

        for scenery_object in objects_xml.find_scenery_objects_in_group(guid):
            add_scenery_object(objects_xml.file_path, new_tile, scenery_object)
