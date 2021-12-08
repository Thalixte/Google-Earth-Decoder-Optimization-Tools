import json
import os
import shutil

from constants import BUFFERS_TAG, IMAGES_TAG, MIME_TYPE_TAG, URI_TAG, ASSET_TAG, GENERATOR_TAG
from msfs_project.binary import MsfsBinary
from msfs_project.texture import MsfsTexture
from utils import backup_file


class MsfsLod:
    optimized: bool
    lod_level: int
    min_size: int
    name: str
    model_file: str or None
    folder: str
    binaries: list
    textures: list

    TEXTURE_FOLDER = "texture"
    OPTIMIZATION_GENERATOR_TAG = "Scenery optimized"

    def __init__(self, lod_level, min_size, model_file, folder):
        self.lod_level = lod_level
        self.min_size = int(min_size)
        self.name = os.path.splitext(model_file)[0]
        self.model_file = model_file
        self.folder = folder
        self.optimized = self.__is_optimized()
        self.__retrieve_gltf_resources()

    def backup_files(self, backup_path, dry_mode=False, pbar=None):
        for binary in self.binaries:
            binary.backup_file(backup_path, dry_mode=dry_mode, pbar=pbar)
        for texture in self.textures:
            texture.backup_file(backup_path, dry_mode=dry_mode, pbar=pbar)
        self.backup_file(backup_path, dry_mode=dry_mode, pbar=pbar)

    def remove_files(self):
        for binary in self.binaries:
            binary.remove_file()
        for texture in self.textures:
            texture.remove_file()
        self.remove_file()

    def backup_file(self, backup_path, dry_mode=False, pbar=None):
        backup_file(backup_path, self.folder, self.model_file, dry_mode=dry_mode, pbar=pbar)

    def remove_file(self):
        file_path = os.path.join(self.folder, self.model_file)
        if os.path.isfile(file_path):
            os.remove(os.path.join(file_path))
            print(self.model_file, "removed")

    def create_optimization_folder(self, other_tiles=[]):
        optimization_folder_path = os.path.join(self.folder, self.name)
        os.makedirs(optimization_folder_path, exist_ok=True)
        self.move_resources(optimization_folder_path)
        for other_tile in other_tiles:
            for lod in other_tile.lods:
                if lod.lod_level == self.lod_level:
                    lod.move_resources(optimization_folder_path)

    def move_resources(self, dest_path):
        if not os.path.isfile(os.path.join(dest_path, self.model_file)): shutil.move(os.path.join(self.folder, self.model_file), dest_path)
        for binary in self.binaries:
            if not os.path.isfile(os.path.join(dest_path, binary.file)): shutil.move(os.path.join(binary.folder, binary.file), dest_path)
        for texture in self.textures:
            if not os.path.isfile(os.path.join(dest_path, texture.file)): shutil.move(os.path.join(texture.folder, texture.file), dest_path)

    def __retrieve_gltf_resources(self):
        self.binaries = []
        self.textures = []
        file_path = os.path.join(self.folder, self.model_file)
        if not os.path.isfile(file_path):
            return

        data = json.load(open(file_path))
        for buffer in data[BUFFERS_TAG]:
            self.binaries.append(MsfsBinary(file_path, self.folder, buffer[URI_TAG]))
        for idx, image in enumerate(data[IMAGES_TAG]):
            mime_type = str()
            if MIME_TYPE_TAG in image.keys():
                mime_type = image[MIME_TYPE_TAG]
            self.textures.append(MsfsTexture(idx, file_path, os.path.join(self.folder, self.TEXTURE_FOLDER), image[URI_TAG], mime_type))

    def __is_optimized(self):
        file_path = os.path.join(self.folder, self.model_file)
        if not os.path.isfile(file_path):
            return

        return self.OPTIMIZATION_GENERATOR_TAG in json.load(open(file_path))[ASSET_TAG][GENERATOR_TAG]
