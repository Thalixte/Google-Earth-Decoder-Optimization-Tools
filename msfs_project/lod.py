import json
import os

from constants import BUFFERS_TAG, IMAGES_TAG, MIME_TYPE_TAG, URI_TAG
from msfs_project.binary import MsfsBinary
from msfs_project.texture import MsfsTexture
from utils import backup_file


class MsfsLod:
    min_size: int
    model_file: str or None
    folder: str
    binaries: list
    textures: list

    TEXTURE_FOLDER = "texture"

    def __init__(self, min_size, model_file, folder):
        self.min_size = int(min_size)
        self.model_file = model_file
        self.folder = folder
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
