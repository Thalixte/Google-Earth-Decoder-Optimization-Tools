import json
import os


class MsfsLod:
    min_size: int
    model_file: str
    bin_file: str
    textures: list

    BUFFERS_TAG = "buffers"
    IMAGES_TAG = "images"
    URI_TAG = "uri"

    def __init__(self, min_size, model_file, folder):
        self.bin_file = ""
        self.min_size = int(min_size)
        self.model_file = model_file
        self.__retrieve_gltf_resources(folder)

    def __retrieve_gltf_resources(self, folder):
        self.textures = []
        if not os.path.isfile(os.path.join(folder, self.model_file)):
            return

        data = json.load(open(os.path.join(folder, self.model_file)))
        for buffer in data[self.BUFFERS_TAG]:
            self.bin_file = buffer[self.URI_TAG]
        for image in data[self.IMAGES_TAG]:
            self.textures.append(image[self.URI_TAG])
