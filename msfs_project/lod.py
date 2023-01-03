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

import os
import re
import shutil
from pathlib import Path

from blender import import_model_files, bake_texture_files, fix_object_bounding_box, export_to_optimized_gltf_files, clean_scene, extract_splitted_tile, align_model_with_mask, process_3d_data, generate_model_height_data, reduce_number_of_vertices
from constants import PNG_TEXTURE_FORMAT, JPG_TEXTURE_FORMAT, GLTF_FILE_PATTERN, GLTF_FILE_EXT, XML_FILE_EXT, TEXTURE_FOLDER
from msfs_project.binary import MsfsBinary
from msfs_project.texture import MsfsTexture
from msfs_project.gltf import MsfsGltf
from utils import backup_file, isolated_print
from utils.minidom_xml import create_new_definition_file, add_new_lod


class PROCESS_TYPE:
    cleanup_3d_data = "cleanup_3d_data"
    isolate_3d_data = "isolate_3d_data"


class MsfsLod:
    optimization_in_progress: bool
    optimized: bool
    cleaned: bool
    valid: bool
    lod_level: int
    min_size: int
    name: str
    model_file: str or None
    folder: str
    binaries: list
    textures: list
    splitted_nodes: dict

    OPTIMIZATION_GENERATOR_TAG = "Scenery optimized"
    ALT_OPTIMIZATION_GENERATOR_TAG = "FPS optimized"
    CLEANED_OPTIMIZATION_GENERATOR_TAG = "Scenery optimized and cleaned"
    UNBAKED_TEXTURE_NAME_PATTERN = "([a-zA-Z0-9\s_\\.\-\(\):])(LOD)(\d+)(_)(\d+).(" + PNG_TEXTURE_FORMAT + "|" + JPG_TEXTURE_FORMAT + ")"
    LOD_SUFFIX = "_LOD"

    def __init__(self, lod_level, min_size, folder, model_file, optimization_in_progress=False):
        self.lod_level = lod_level
        self.min_size = int(min_size) if min_size else 0
        self.name = os.path.splitext(model_file)[0]
        self.folder = folder
        self.optimization_in_progress = optimization_in_progress or os.path.isdir(os.path.join(self.folder, self.name))
        if self.optimization_in_progress and os.path.isdir(os.path.join(self.folder, self.name)):
            self.folder = os.path.join(self.folder, self.name)
        self.model_file = model_file
        self.optimized = self.__is_optimized(self.model_file)
        self.cleaned = self.__is_cleaned(self.model_file)
        self.valid = self.__is_valid(self.model_file)
        self.splitted_nodes = {}
        self.__retrieve_gltf_resources()

    def backup_files(self, backup_path, dry_mode=False, pbar=None):
        if self.optimization_in_progress:
            return

        for binary in self.binaries:
            binary.backup_file(backup_path, dry_mode=dry_mode, pbar=pbar)
        for texture in self.textures:
            texture.backup_file(backup_path, dry_mode=dry_mode, pbar=pbar)
        self.backup_file(backup_path, dry_mode=dry_mode, pbar=pbar)

    def remove_files(self, remove_textures=True):
        for binary in self.binaries:
            binary.remove_file()
        if remove_textures:
            for texture in self.textures:
                texture.remove_file()
        #  ensure that all the files are removed
        for file_path in Path(os.path.dirname(self.folder)).rglob(self.name + ".*"):
            os.remove(file_path)
            print(self.model_file, "removed")
        self.remove_file()

    def backup_file(self, backup_path, dry_mode=False, pbar=None):
        if self.optimization_in_progress:
            return

        backup_file(backup_path, self.folder, self.model_file, dry_mode=dry_mode, pbar=pbar)

    def remove_file(self):
        file_path = os.path.join(self.folder, self.model_file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(self.model_file, "removed")

    def create_optimization_folder(self, other_tiles=[]):
        if self.optimization_in_progress:
            return

        if not self.binaries:
            return

        if not self.textures:
            return

        optimization_folder_path = os.path.join(self.folder, self.name)
        os.makedirs(optimization_folder_path, exist_ok=True)
        self.move_resources(optimization_folder_path)
        for other_tile in other_tiles:
            for lod in other_tile.lods:
                if lod.lod_level == self.lod_level:
                    lod.move_resources(optimization_folder_path)

            # remove unused definition files
            other_tile.remove_file()

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

    def optimize(self, bake_textures_enabled, output_texture_format):
        model_files = [model_file for model_file in Path(self.folder).glob(GLTF_FILE_PATTERN) if not self.__is_optimized(model_file)]
        if not model_files:
            return
        new_gltf = os.path.join(os.path.dirname(self.folder), Path(self.folder).name + GLTF_FILE_EXT)

        # Import the gltf files located in the object folder
        import_model_files(model_files)
        has_unbaked_textures = False
        textures = []

        for model_file in model_files:
            lod = MsfsLod(int(self.folder[-2:]), 0, self.folder, os.path.basename(model_file), optimization_in_progress=True)
            textures.extend(lod.textures)
            if lod.has_unbaked_textures():
                has_unbaked_textures = True

        if bake_textures_enabled and has_unbaked_textures:
            isolated_print("bake textures for", self.name)
            bake_texture_files(os.path.join(os.path.dirname(self.folder), TEXTURE_FOLDER), self.name + "." + output_texture_format)
        else:
            for texture in textures:
                shutil.copyfile(os.path.join(self.folder, texture.file), os.path.join(os.path.dirname(self.folder), TEXTURE_FOLDER, texture.file))

        isolated_print("fix bounding box for", self.name)
        fix_object_bounding_box()
        export_to_optimized_gltf_files(new_gltf, TEXTURE_FOLDER)

        if os.path.isfile(new_gltf):
            shutil.rmtree(self.folder)
            self.folder = os.path.dirname(self.folder)
            self.optimization_in_progress = False
            self.__retrieve_gltf_resources()

    def prepare_for_msfs(self, model_file_path=None):
        model_file = MsfsGltf(os.path.join(self.folder, self.model_file)) if model_file_path is None else MsfsGltf(model_file_path)
        model_file.fix_doublesided()
        model_file.add_asobo_extensions()
        model_file.remove_texture_path(self.name)
        model_file.fix_gltf_nodes()
        model_file.dump()

    def remove_road_and_collision_tags(self):
        model_file = MsfsGltf(os.path.join(self.folder, self.model_file))
        model_file.remove_asobo_tag(model_file.ROAD_TAG)
        model_file.remove_asobo_tag(model_file.COLLISION_TAG)
        model_file.dump()

    def create_collider(self, collider_model_file_name):
        if os.path.isfile(os.path.join(self.folder, self.model_file)):
            shutil.copyfile(os.path.join(self.folder, self.model_file), os.path.join(self.folder, collider_model_file_name))
            collider_model_file = MsfsGltf(os.path.join(self.folder, collider_model_file_name))
            collider_model_file.add_asobo_extensions()
            collider_model_file.remove_asobo_extension(collider_model_file.ASOBO_MATERIAL_FAKE_TERRAIN_TAG)
            collider_model_file.remove_asobo_extension(collider_model_file.ASOBO_MATERIAL_DAY_NIGHT_SWITCH_TAG)
            collider_model_file.add_extension_tag(collider_model_file.ASOBO_MATERIAL_INVISIBLE_TAG)
            collider_model_file.dump()

    def split(self, tile_name, min_size_value, tile):
        self.__retrieve_splitted_nodes(tile_name)
        if self.splitted_nodes:
            model_file = MsfsGltf(os.path.join(self.folder, self.model_file))
            model_file.add_texture_path()
            model_file.dump()
            self.__extract_splitted_tiles(min_size_value, tile)
            self.remove_files(remove_textures=False)
        else:
            for definition_file in tile.new_tiles.values():
                add_new_lod(definition_file, self.model_file, min_size_value)

        model_file = MsfsGltf(os.path.join(self.folder, self.model_file))
        model_file.remove_texture_path(self.name)
        model_file.dump()

    def reduce_number_of_vertices(self):
        # Import the gltf files located in the object folder
        model_file = MsfsGltf(os.path.join(self.folder, self.model_file))
        model_file.remove_texture_path(self.name)
        model_file.add_texture_path()
        model_file.dump()
        reduce_number_of_vertices(os.path.join(self.folder, self.model_file))
        export_to_optimized_gltf_files(os.path.join(self.folder, self.model_file), TEXTURE_FOLDER, use_selection=True, export_extras=False)
        clean_scene()
        model_file = MsfsGltf(os.path.join(self.folder, self.model_file))
        model_file.remove_texture_path(self.name)
        model_file.dump()

    def process_3d_data(self, positioning_file_path, mask_file_path, output_folder, output_name=None, process_type=PROCESS_TYPE.cleanup_3d_data, debug=False):
        # Import the gltf files located in the object folder
        isolated_print("align", self.name, "model with mask")
        model_file = MsfsGltf(os.path.join(self.folder, self.model_file))
        model_file.remove_texture_path(self.name)
        model_file.add_texture_path()
        model_file.dump()
        align_model_with_mask(os.path.join(self.folder, self.model_file), positioning_file_path, mask_file_path)

        if process_type == PROCESS_TYPE.cleanup_3d_data:
            process_3d_data(model_file_path=os.path.join(self.folder, self.model_file), intersect=False)

        if process_type == PROCESS_TYPE.isolate_3d_data:
            process_3d_data(model_file_path=os.path.join(self.folder, self.model_file), intersect=True)

        output_model_file = output_name + self.LOD_SUFFIX + str(self.lod_level).zfill(2) + GLTF_FILE_EXT if output_name else self.model_file
        export_to_optimized_gltf_files(os.path.join(output_folder, output_model_file), TEXTURE_FOLDER, use_selection=True, export_extras=False, apply_modifiers=True)
        model_file = MsfsGltf(os.path.join(output_folder, output_model_file))
        model_file.remove_texture_path(self.name)
        model_file.add_extension_tag(model_file.ASOBO_MATERIAL_INVISIBLE_TAG, only_last_material=True)
        model_file.add_cleaned_tag()
        model_file.dump()

        if not debug:
            clean_scene()

    def get_subtiles(self):
        result = []
        model_file = MsfsGltf(os.path.join(self.folder, self.model_file))

        if model_file:
            result = model_file.get_subtiles()

        return result

    def calculate_height_data(self, lat, lon, altitude, height_adjustment, inverted=False, positioning_file_path="", water_mask_file_path="", ground_mask_file_path="", debug=False):
        model_file = MsfsGltf(os.path.join(self.folder, self.model_file))
        model_file.remove_texture_path(self.name)
        model_file.add_texture_path()
        model_file.dump()
        result = generate_model_height_data(os.path.join(self.folder, self.model_file), lat, lon, altitude, height_adjustment, inverted=inverted, positioning_file_path=positioning_file_path, water_mask_file_path=water_mask_file_path, ground_mask_file_path=ground_mask_file_path, debug=debug)
        model_file = MsfsGltf(os.path.join(self.folder, self.model_file))
        model_file.remove_texture_path(self.name)
        model_file.dump()
        return result

    def fix_imported_texture_names(self):
        file_path = os.path.join(self.folder, self.model_file)
        model_file = MsfsGltf(file_path)

        for i, texture in enumerate(self.textures):
            file_suffix = "_" + str(i)
            new_texture_name = self.name + file_suffix + os.path.splitext(texture.file)[1]
            os.rename(os.path.join(texture.folder, texture.file), os.path.join(texture.folder, new_texture_name))
            # update gltf model file
            model_file.rename_texture(texture.file, new_texture_name)
            model_file.dump()
            texture.name = new_texture_name

    def adjust_texture_colors(self, settings):
        for i, texture in enumerate(self.textures):
            texture.adjust_colors(settings)

    def __retrieve_gltf_resources(self):
        self.binaries = []
        self.textures = []
        file_path = os.path.join(self.folder, self.model_file)
        model_file = MsfsGltf(file_path)

        if not model_file.data: return
        if not MsfsGltf.BUFFERS_TAG in model_file.data: return
        if not MsfsGltf.IMAGES_TAG in model_file.data: return

        for buffer in model_file.data[MsfsGltf.BUFFERS_TAG]:
            self.binaries.append(MsfsBinary(file_path, self.folder, buffer[MsfsGltf.URI_TAG]))

        for idx, image in enumerate(model_file.data[MsfsGltf.IMAGES_TAG]):
            mime_type = str()
            if MsfsGltf.MIME_TYPE_TAG in image.keys():
                mime_type = image[MsfsGltf.MIME_TYPE_TAG]

            texture_path = self.folder if self.optimization_in_progress else os.path.join(self.folder, TEXTURE_FOLDER)
            if os.path.isfile(os.path.join(texture_path, image[MsfsGltf.URI_TAG])):
                self.textures.append(MsfsTexture(idx, file_path, self.folder if self.optimization_in_progress else os.path.join(self.folder, TEXTURE_FOLDER), image[MsfsGltf.URI_TAG], mime_type))

    def __is_optimized(self, model_file):
        model_file = MsfsGltf(os.path.join(self.folder, model_file))
        if not model_file.data: return
        return self.CLEANED_OPTIMIZATION_GENERATOR_TAG in model_file.data[MsfsGltf.ASSET_TAG][MsfsGltf.GENERATOR_TAG] or self.OPTIMIZATION_GENERATOR_TAG in model_file.data[MsfsGltf.ASSET_TAG][MsfsGltf.GENERATOR_TAG] or self.ALT_OPTIMIZATION_GENERATOR_TAG in model_file.data[MsfsGltf.ASSET_TAG][MsfsGltf.GENERATOR_TAG]

    def __is_cleaned(self, model_file):
        model_file = MsfsGltf(os.path.join(self.folder, model_file))
        if not model_file.data: return
        return self.CLEANED_OPTIMIZATION_GENERATOR_TAG in model_file.data[MsfsGltf.ASSET_TAG][MsfsGltf.GENERATOR_TAG]

    def __is_valid(self, model_file):
        model_file = MsfsGltf(os.path.join(self.folder, model_file))
        if not model_file.data: return False
        return model_file.is_valid()

    def __retrieve_splitted_nodes(self, tile_name):
        file_path = os.path.join(self.folder, self.model_file)
        model_file = MsfsGltf(file_path)

        if not model_file.data: return
        if not MsfsGltf.NODES_TAG in model_file.data: return

        for node in model_file.data[MsfsGltf.NODES_TAG]:
            node_name = node["name"].split("_")[0]
            if len(node_name) > len(tile_name):
                key = node_name[0:(len(tile_name) + 1)] + self.LOD_SUFFIX + str(self.lod_level).zfill(2)
                if not key in self.splitted_nodes:
                    self.splitted_nodes[key] = []
                self.splitted_nodes[key].append(node["name"])

    def __extract_splitted_tiles(self, min_size_value, tile):
        for key, node in self.splitted_nodes.items():
            splitted_tile_name = key.split("_")[0]

            import_model_files([os.path.join(self.folder, self.model_file)])
            model_file_path = os.path.join(self.folder, key + GLTF_FILE_EXT)
            extract_splitted_tile(model_file_path, node, TEXTURE_FOLDER)
            self.prepare_for_msfs(model_file_path=model_file_path)

            if not os.path.isfile(os.path.join(self.folder, splitted_tile_name + XML_FILE_EXT)):
                new_guid = create_new_definition_file(os.path.join(self.folder, splitted_tile_name + XML_FILE_EXT))
                tile.new_tiles[new_guid] = os.path.join(self.folder, splitted_tile_name + XML_FILE_EXT)
            if self.lod_level < (len(tile.lods) - 1):
                add_new_lod(os.path.join(self.folder, splitted_tile_name + XML_FILE_EXT), key + GLTF_FILE_EXT, min_size_value)

        clean_scene()
