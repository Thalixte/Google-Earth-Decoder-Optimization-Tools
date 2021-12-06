import json
import os

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
    BUFFERS_TAG = "buffers"
    IMAGES_TAG = "images"
    MIME_TYPE_TAG = "mimeType"
    URI_TAG = "uri"

    def __init__(self, min_size, model_file, folder):
        self.min_size = int(min_size)
        self.model_file = model_file
        self.folder = folder
        self.__retrieve_gltf_resources(self.folder)

    def __retrieve_gltf_resources(self, folder):
        self.binaries = []
        self.textures = []
        if os.path.isfile(os.path.join(folder, self.model_file)):
            data = json.load(open(os.path.join(folder, self.model_file)))
            for buffer in data[self.BUFFERS_TAG]:
                self.binaries.append(MsfsBinary(self.folder, buffer[self.URI_TAG]))
            for image in data[self.IMAGES_TAG]:
                mime_type = str()
                if self.MIME_TYPE_TAG in image.keys():
                    mime_type = image[self.MIME_TYPE_TAG]
                self.textures.append(MsfsTexture(os.path.join(self.folder, self.TEXTURE_FOLDER), image[self.URI_TAG], mime_type))


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
