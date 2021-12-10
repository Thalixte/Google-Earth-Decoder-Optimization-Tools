from constants import GENERATOR_TAG, IMAGES_TAG, URI_TAG, ASSET_TAG, MATERIALS_TAG, DOUBLESIDED_TAG, MIME_TYPE_TAG, \
    EXTENSIONS_TAG, ASOBO_TAGS_TAG, TAGS_TAG, ROAD_TAG, COLLISION_TAG, ENABLED_TAG, ASOBO_MATERIAL_DAY_NIGHT_SWITCH_TAG, \
    ASOBO_MATERIAL_FAKE_TERRAIN_TAG
from utils import load_json_file, save_json_file


class MsfsGltf:
    file_path: str
    data: str

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = load_json_file(self.file_path)

    def update_image(self, idx, uri, mime_type):
        if not self.data: return

        if not self.data[IMAGES_TAG][idx]: return

        image = self.data[IMAGES_TAG][idx]
        image[URI_TAG] = uri
        image[MIME_TYPE_TAG] = mime_type
        self.dump()

    def add_optimization_tag(self):
        if not self.data: return

        self.data[ASSET_TAG][GENERATOR_TAG] = "Scenery optimized Khronos glTF Blender I/O v1.2.75"

    def fix_texture_path(self):
        if not self.data: return

        for image in self.data[IMAGES_TAG]:
            image[URI_TAG] = image[URI_TAG].replace("texture/", "")

    def fix_doublesided(self):
        if not self.data: return

        for material in self.data[MATERIALS_TAG]:
            material[DOUBLESIDED_TAG] = False

    def add_asobo_extensions(self):
        if not self.data: return

        material_extensions_data = {
            ASOBO_TAGS_TAG: {
                TAGS_TAG: [ROAD_TAG, COLLISION_TAG]
            },
            ASOBO_MATERIAL_DAY_NIGHT_SWITCH_TAG: {
                ENABLED_TAG: True
            },
            ASOBO_MATERIAL_FAKE_TERRAIN_TAG: {
                ENABLED_TAG: True
            }
        }

        for material in self.data[MATERIALS_TAG]:
            material[EXTENSIONS_TAG] = material_extensions_data

    def dump(self):
        save_json_file(self.file_path, self.data)
