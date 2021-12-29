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

    LOD_MODEL_FILES_SEARCH_PATTERN = "_LOD*.gltf"

    def __init__(self, path, name, definition_file):
        super().__init__(path, name, definition_file)
        self.pos = MsfsPosition(0, 0, 0)
        self.coords = ([0, 0, 0, 0])
        self.lods = self.__retrieve_lods()

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
        for i, lod in enumerate(self.lods):
            if not self.xml.find_scenery_lod_models(lod.model_file):
                lod.remove_files()
                pop_lods.append(i)
        self.lods.pop(i)

    def update_min_size_values(self, min_size_values, pbar=None):
        lods_definition = self.xml.find_scenery_lods()
        for i, lod_definition in enumerate(lods_definition):
            lod_definition.set(self.xml.MIN_SIZE_TAG, str(min_size_values[(len(lods_definition) - 1) - i]))

        self.xml.save()
        pbar.update("%s lod values updated" % self.name)

    def contains(self, tile):
        n1, s1, w1, e1 = self.coords
        n2, s2, w2, e2 = tile.coords

        return (n1 >= n2) and (s1 <= s2) and (w1 <= w2) and (e1 >= e2)

    def __retrieve_lods(self):
        lods = []
        lods_definition = self.xml.find_scenery_lods()

        if not lods_definition:
            lods.append(MsfsLod(0, 0, self.folder, self.name + GLTF_FILE_EXT))

        for i, lod_definition in enumerate(lods_definition):
            lods.append(MsfsLod(i, lod_definition.get(self.xml.MIN_SIZE_TAG), self.folder, lod_definition.get(self.xml.MODEL_FILE_TAG)))

        # check if other lod files exist
        for path in Path(os.path.dirname(self.folder)).rglob(self.name + self.LOD_MODEL_FILES_SEARCH_PATTERN):
            if not self.__model_file_exists(lods, path.name):
                lods.append(MsfsLod(int(path.stem[-2:]), 0, self.folder, path.name))

        return lods

    @staticmethod
    def __model_file_exists(lods, file_name):
        for lod in lods:
            if file_name == lod.model_file:
                return True

        return False
