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

from constants import TEXTURE_FOLDER
from utils import load_json_file, save_json_file


class MsfsGltf:
    file_path: str
    data: str

    NODES_TAG = "nodes"
    BUFFERS_TAG = "buffers"
    IMAGES_TAG = "images"
    MATERIALS_TAG = "materials"
    MIME_TYPE_TAG = "mimeType"
    URI_TAG = "uri"
    DOUBLESIDED_TAG = "doubleSided"
    ASSET_TAG = "asset"
    TAGS_TAG = "tags"
    GENERATOR_TAG = "generator"
    EXTENSIONS_TAG = "extensions"
    ASOBO_TAGS_TAG = "ASOBO_tags"
    ROAD_TAG = "Road"
    COLLISION_TAG = "Collision"
    ENABLED_TAG = "enabled"
    ASOBO_MATERIAL_DAY_NIGHT_SWITCH_TAG = "ASOBO_material_day_night_switch"
    ASOBO_MATERIAL_FAKE_TERRAIN_TAG = "ASOBO_material_fake_terrain"

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = load_json_file(self.file_path)

    def update_image(self, idx, uri, mime_type):
        if not self.data: return

        if not self.data[self.IMAGES_TAG][idx]: return

        image = self.data[self.IMAGES_TAG][idx]
        image[self.URI_TAG] = uri
        image[self.MIME_TYPE_TAG] = mime_type
        self.dump()

    def add_optimization_tag(self):
        if not self.data: return

        self.data[self.ASSET_TAG][self.GENERATOR_TAG] = "Scenery optimized Khronos glTF Blender I/O v1.2.75"

    def remove_texture_path(self):
        if not self.data: return
        if not self.IMAGES_TAG in self.data.keys(): return

        for image in self.data[self.IMAGES_TAG]:
            image[self.URI_TAG] = image[self.URI_TAG].replace(TEXTURE_FOLDER + "/", str())

    def add_texture_path(self):
        if not self.data: return
        if not self.IMAGES_TAG in self.data.keys(): return

        for image in self.data[self.IMAGES_TAG]:
            image[self.URI_TAG] = TEXTURE_FOLDER + "/" + image[self.URI_TAG]

    def fix_doublesided(self):
        if not self.data: return
        if not self.MATERIALS_TAG in self.data.keys(): return

        for material in self.data[self.MATERIALS_TAG]:
            material[self.DOUBLESIDED_TAG] = False

    def add_asobo_extensions(self):
        if not self.data: return

        material_extensions_data = {
            self.ASOBO_TAGS_TAG: {
                self.TAGS_TAG: [self.ROAD_TAG, self.COLLISION_TAG]
            },
            self.ASOBO_MATERIAL_DAY_NIGHT_SWITCH_TAG: {
                self.ENABLED_TAG: True
            },
            self.ASOBO_MATERIAL_FAKE_TERRAIN_TAG: {
                self.ENABLED_TAG: True
            }
        }

        for material in self.data[self.MATERIALS_TAG]:
            material[self.EXTENSIONS_TAG] = material_extensions_data

    def dump(self):
        save_json_file(self.file_path, self.data)
