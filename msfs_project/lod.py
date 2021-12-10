import json
import os
import re
import shutil
from pathlib import Path

from blender import import_model_files, bake_texture_files, fix_object_bounding_box, export_to_optimized_gltf_files
from constants import BUFFERS_TAG, IMAGES_TAG, MIME_TYPE_TAG, URI_TAG, ASSET_TAG, GENERATOR_TAG, PNG_TEXTURE_FORMAT, \
    JPG_TEXTURE_FORMAT, GLTF_FILE_PATTERN, GLTF_FILE_EXT
from msfs_project.binary import MsfsBinary
from msfs_project.texture import MsfsTexture
from utils import backup_file, isolated_print, MsfsGltf
from utils.json import load_json_file


class MsfsLod:
    optimization_in_progress: bool
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
    ALT_OPTIMIZATION_GENERATOR_TAG = "FPS optimized"
    UNBAKED_TEXTURE_NAME_PATTERN = "([a-zA-Z0-9\s_\\.\-\(\):])(LOD)(\d+)(_)(\d+).(" + PNG_TEXTURE_FORMAT + "|" + JPG_TEXTURE_FORMAT + ")"

    def __init__(self, lod_level, min_size, model_file, folder):
        self.lod_level = lod_level
        self.min_size = int(min_size)
        self.name = os.path.splitext(model_file)[0]
        self.folder = folder
        self.optimization_in_progress = os.path.isdir(os.path.join(self.folder, self.name))
        self.folder = self.folder if not self.optimization_in_progress else os.path.join(self.folder, self.name)
        self.model_file = model_file
        self.optimized = self.__is_optimized(self.model_file)
        self.__retrieve_gltf_resources()

    def backup_files(self, backup_path, dry_mode=False, pbar=None):
        if self.optimization_in_progress:
            return

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
        if self.optimization_in_progress:
            return

        backup_file(backup_path, self.folder, self.model_file, dry_mode=dry_mode, pbar=pbar)

    def remove_file(self):
        file_path = os.path.join(self.folder, self.model_file)
        if os.path.isfile(file_path):
            os.remove(os.path.join(file_path))
            print(self.model_file, "removed")

    def create_optimization_folder(self, other_tiles=[]):
        if self.optimization_in_progress:
            return

        optimization_folder_path = os.path.join(self.folder, self.name)
        os.makedirs(optimization_folder_path, exist_ok=True)
        self.move_resources(optimization_folder_path)
        for other_tile in other_tiles:
            for lod in other_tile.lods:
                if lod.lod_level == self.lod_level:
                    lod.move_resources(optimization_folder_path)

            try:
                os.remove(os.path.join(other_tile.folder, other_tile.definition_file))
            except:
                pass

    def move_resources(self, dest_path):
        if not os.path.isfile(os.path.join(dest_path, self.model_file)): shutil.move(os.path.join(self.folder, self.model_file), dest_path)
        for binary in self.binaries:
            if not os.path.isfile(os.path.join(dest_path, binary.file)): shutil.move(os.path.join(binary.folder, binary.file), dest_path)
        for texture in self.textures:
            if not os.path.isfile(os.path.join(dest_path, texture.file)): shutil.move(os.path.join(texture.folder, texture.file), dest_path)
        self.folder = dest_path
        self.__retrieve_gltf_resources()

    def has_unbaked_textures(self):
        unbaked_texture_name_pattern = re.compile(self.UNBAKED_TEXTURE_NAME_PATTERN)
        for texture in self.textures:
            if re.search(unbaked_texture_name_pattern, texture.file):
                return True

        return False

    def optimize(self, output_texture_format):
        model_files = [model_file for model_file in Path(self.folder).glob(GLTF_FILE_PATTERN) if not self.__is_optimized(model_file)]
        if not model_files:
            return
        new_gltf = os.path.join(os.path.dirname(self.folder), Path(self.folder).name + GLTF_FILE_EXT)

        # Import the gltf files located in the object folder
        import_model_files(model_files)

        if self.has_unbaked_textures():
            isolated_print("bake textures for", self.name)
            bake_texture_files(self.folder, self.name + "." + output_texture_format)

        isolated_print("fix bounding box for", self.name)
        fix_object_bounding_box()
        export_to_optimized_gltf_files(new_gltf, self.TEXTURE_FOLDER)
        shutil.rmtree(self.folder)
        self.folder = os.path.dirname(self.folder)
        self.optimization_in_progress = False
        self.__retrieve_gltf_resources()


    def __load_model_file_json(self, model_file):
        file_path = os.path.join(self.folder, model_file)
        return file_path, load_json_file(file_path)

    def __retrieve_gltf_resources(self):
        self.binaries = []
        self.textures = []
        file_path = os.path.join(self.folder, self.model_file)
        model_file = MsfsGltf(file_path)
        if not model_file.data: return

        for buffer in model_file.data[BUFFERS_TAG]:
            self.binaries.append(MsfsBinary(file_path, self.folder, buffer[URI_TAG]))
        for idx, image in enumerate(model_file.data[IMAGES_TAG]):
            mime_type = str()
            if MIME_TYPE_TAG in image.keys():
                mime_type = image[MIME_TYPE_TAG]
            self.textures.append(MsfsTexture(idx, file_path, self.folder if self.optimization_in_progress else os.path.join(self.folder, self.TEXTURE_FOLDER), image[URI_TAG], mime_type))

    def __is_optimized(self, model_file):
        model_file = MsfsGltf(os.path.join(self.folder, model_file))
        if not model_file.data: return
        return self.OPTIMIZATION_GENERATOR_TAG in model_file.data[ASSET_TAG][GENERATOR_TAG] or self.ALT_OPTIMIZATION_GENERATOR_TAG in model_file.data[ASSET_TAG][GENERATOR_TAG]
