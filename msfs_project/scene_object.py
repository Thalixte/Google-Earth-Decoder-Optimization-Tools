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

from constants import GLTF_FILE_EXT
from msfs_project.object import MsfsObject
from msfs_project.position import MsfsPosition
from msfs_project.lod import MsfsLod


class MsfsSceneObject(MsfsObject):
    pos: MsfsPosition
    coords: tuple
    lods: list
    valid: bool
    cleaned: bool

    LOD_MODEL_FILES_SEARCH_PATTERN = "_LOD*.gltf"

    def __init__(self, folder, name, definition_file, is_collider=False):
        super().__init__(folder, name, definition_file)
        self.pos = MsfsPosition(0, 0, 0)
        self.coords = ([0, 0, 0, 0])
        self.lods = self.__retrieve_lods(is_collider)
        self.valid = self.__is_valid()
        self.cleaned = self.__is_cleaned()

    def backup_files(self, backup_path, dry_mode=False, pbar=None):
        for lod in self.lods:
            lod.backup_files(backup_path, dry_mode=dry_mode, pbar=pbar)
        self.backup_file(backup_path, dry_mode=dry_mode, pbar=pbar)

    def remove_files(self):
        for lod in self.lods:
            lod.remove_files()
        self.remove_file()

    def clean_lods(self):
        pop_lods = []
        if not self.xml.find_scenery_lods(): return
        for i, lod in enumerate(self.lods):
            if not lod.valid or not self.xml.find_scenery_lod_models(lod.model_file):
                lod.remove_files()
                pop_lods.append(i)
        self.lods.pop(i)

    def update_min_size_values(self, min_size_values, pbar=None):
        lods_definition = self.xml.find_scenery_lods()
        for i, lod_definition in enumerate(lods_definition):
            lod_definition.set(self.xml.MIN_SIZE_ATTR, str(min_size_values[(len(lods_definition) - 1) - i]))

        self.xml.save()

        if pbar is not None:
            pbar.update("%s lod values updated" % self.name)

    def contains(self, coords):
        n1, s1, w1, e1 = self.coords
        n2, s2, w2, e2 = coords

        return (n1 >= n2) and (s1 <= s2) and (w1 <= w2) and (e1 >= e2)

    def to_xml(self, xml, guid):
        xml.add_scenery_object(self, guid)
        xml.save()

    def __retrieve_lods(self, is_collider=False):
        lods = []
        lods_definition = self.xml.find_scenery_lods()

        if not lods_definition and is_collider:
            lods.append(MsfsLod(0, 0, self.folder, self.name + GLTF_FILE_EXT))

        for i, lod_definition in enumerate(lods_definition):
            lods.append(MsfsLod(i, lod_definition.get(self.xml.MIN_SIZE_ATTR), self.folder, lod_definition.get(self.xml.MODEL_FILE_ATTR)))

        # check if other lod files exist
        for path in Path(os.path.dirname(self.folder)).rglob(self.name + self.LOD_MODEL_FILES_SEARCH_PATTERN):
            if not self.__model_file_exists(lods, path.name):
                lods.append(MsfsLod(int(path.stem[-2:]), 0, self.folder, path.name))

        return lods

    def __is_valid(self):
        for lod in self.lods:
            if lod.valid:
                return True

        return False

    def __is_cleaned(self):
        for lod in self.lods:
            if lod.cleaned:
                return True

        return False

    @staticmethod
    def __model_file_exists(lods, file_name):
        for lod in lods:
            if file_name == lod.model_file:
                return True

        return False
