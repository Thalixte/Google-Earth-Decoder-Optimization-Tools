import os
from pathlib import Path

from constants import GLTF_FILE_EXT
from msfs_project.object import MsfsObject
from msfs_project.position import MsfsPosition
from msfs_project.lod import MsfsLod


class MsfsSceneObject(MsfsObject):
    pos: MsfsPosition
    lods: list

    LOD_MODEL_FILES_SEARCH_PATTERN = "_LOD*.gltf"

    def __init__(self, path, name, definition_file):
        super().__init__(path, name, definition_file)
        self.pos = MsfsPosition(0, 0, 0)
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

    def __retrieve_lods(self):
        lods = []
        lods_definition = self.xml.find_scenery_lods()

        if not lods_definition:
            lods.append(MsfsLod(0, 0, self.name + GLTF_FILE_EXT, self.folder))

        for i, lod_definition in enumerate(lods_definition):
            lods.append(MsfsLod(i, lod_definition.get(self.xml.MIN_SIZE_TAG), lod_definition.get(self.xml.MODEL_FILE_TAG), self.folder))

        # check if other lod files exist
        for path in Path(os.path.dirname(self.folder)).rglob(self.name + self.LOD_MODEL_FILES_SEARCH_PATTERN):
            if not self.__model_file_exists(lods, path.name):
                lods.append(MsfsLod(int(path.stem[-2:]), 0, path.name, self.folder))

        return lods

    @staticmethod
    def __model_file_exists(lods, file_name):
        for lod in lods:
            if file_name == lod.model_file:
                return True

        return False
