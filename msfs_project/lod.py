import os
import re

from constants import BIN_FILE_EXT, PNG_FILE_EXT, JPG_FILE_EXT


class MsfsLod:
    min_size: int
    model_file: str
    bin_file: str
    textures: list

    URI_TAG = "uri"
    BIN_FILE_PATTERN = "([a-zA-Z0-9\s_\\.\-\(\):])+" + BIN_FILE_EXT
    IMG_FILE_PATTERN = "([a-zA-Z0-9\s_\\.\-\(\):])+(" + PNG_FILE_EXT + "|" + JPG_FILE_EXT + ")"

    def __init__(self, min_size, model_file, folder):
        self.min_size = int(min_size)
        self.model_file = model_file
        self.__retrieve_gltf_resources(folder)

    def __retrieve_gltf_resources(self, folder):
        self.textures = []
        bin_pattern = re.compile(self.BIN_FILE_PATTERN)
        img_pattern = re.compile(self.IMG_FILE_PATTERN)
        for i, line in enumerate(open(os.path.join(folder, self.model_file))):
            if self.URI_TAG in line:
                for match in re.finditer(bin_pattern, line):
                    self.bin_file = match.group()
                for match in re.finditer(img_pattern, line):
                    self.textures.append(match.group())
