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

import itertools
import sys
from os.path import dirname, basename

import io
import shutil
import os
import subprocess

import bpy
from constants import *
from msfs_project.project_xml import MsfsProjectXml
from msfs_project.package_definitions_xml import MsfsPackageDefinitionsXml
from msfs_project.objects_xml import ObjectsXml
from msfs_project.scene_object import MsfsSceneObject
from msfs_project.collider import MsfsCollider
from msfs_project.tile import MsfsTile
from msfs_project.shape import MsfsShape
from utils import replace_in_file, is_octant, backup_file, install_python_lib, ScriptError, print_title, \
    get_backup_file_path, isolated_print, chunks
from pathlib import Path

from utils.compressonator import Compressonator
from utils.progress_bar import ProgressBar


class MsfsProject:
    parent_path: str
    project_name: str
    author_name: str
    project_folder: str
    package_definitions_folder: str
    package_sources_folder: str
    model_lib_folder: str
    texture_folder: str
    scene_folder: str
    business_json_folder: str
    content_info_folder: str
    project_definition_xml: str
    project_definition_xml_path: str
    package_definitions_xml: str
    package_definitions_xml_path: str
    scene_objects_xml_file_path: str
    business_json_path: str
    thumbnail_picture_path: str
    built_packages_folder: str
    built_project_package_folder: str
    model_lib_output_dir: str
    min_lod_level: int
    objects: dict
    tiles: dict
    shapes: dict
    colliders: dict
    objects_xml: ObjectsXml

    DUMMY_STRING = "dummy"
    AUTHOR_STRING = "author"
    BACKUP_FOLDER = "backup"
    PACKAGE_DEFINITIONS_FOLDER = "PackageDefinitions"
    PACKAGE_SOURCES_FOLDER = "PackageSources"
    BUILT_PACKAGES_FOLDER = "Packages"
    MODEL_LIB_FOLDER = "modelLib"
    SCENE_FOLDER = "scene"
    CONTENT_INFO_FOLDER = "ContentInfo"
    SCENE_OBJECTS_FILE = "objects" + XML_FILE_EXT
    COLLIDER_SUFFIX = "_collider"
    NB_PARALLEL_TASKS = 4

    def __init__(self, projects_path, project_name, author_name, sources_path, init_structure=False, fast_init=False):
        self.parent_path = projects_path
        self.project_name = project_name
        self.author_name = author_name
        self.project_folder = os.path.join(self.parent_path, self.project_name.capitalize())
        self.backup_folder = os.path.join(self.project_folder, self.BACKUP_FOLDER)
        self.package_definitions_folder = os.path.join(self.project_folder, self.PACKAGE_DEFINITIONS_FOLDER)
        self.package_sources_folder = os.path.join(self.project_folder, self.PACKAGE_SOURCES_FOLDER)

        if init_structure:
            self.model_lib_folder = os.path.join(self.package_sources_folder, self.MODEL_LIB_FOLDER)
        else:
            self.model_lib_folder = os.path.join(self.package_sources_folder, self.project_name.lower() + "-" + self.MODEL_LIB_FOLDER)
            # fix modellib folder name
            if not os.path.isdir(self.model_lib_folder) and os.path.isdir(os.path.join(self.package_sources_folder, self.MODEL_LIB_FOLDER)):
                os.rename(os.path.join(self.package_sources_folder, self.MODEL_LIB_FOLDER), self.model_lib_folder)

        self.scene_folder = os.path.join(self.package_sources_folder, self.SCENE_FOLDER)
        self.texture_folder = os.path.join(self.model_lib_folder, TEXTURE_FOLDER)
        self.scene_folder = os.path.join(self.package_sources_folder, self.SCENE_FOLDER)
        self.business_json_folder = os.path.join(self.package_definitions_folder, self.author_name.lower() + "-" + self.project_name.lower())
        self.content_info_folder = os.path.join(self.package_definitions_folder, self.business_json_folder, self.CONTENT_INFO_FOLDER)
        self.built_packages_folder = os.path.join(self.project_folder, self.BUILT_PACKAGES_FOLDER)
        self.built_project_package_folder = os.path.join(self.built_packages_folder, self.author_name.lower() + "-" + self.project_name.lower())
        self.scene_objects_xml_file_path = os.path.join(self.scene_folder, self.SCENE_OBJECTS_FILE)
        if os.path.isfile(self.scene_objects_xml_file_path):
            self.objects_xml = ObjectsXml(self.scene_folder, self.SCENE_OBJECTS_FILE)
        self.min_lod_level = 0

        self.__initialize(sources_path, init_structure, fast_init)

    def update_objects_position(self, settings):
        isolated_print(EOL)
        self.objects_xml.update_objects_position(self, settings)

    def backup(self, backup_subfolder, all_files=True):
        isolated_print(EOL)
        self.backup_files(backup_subfolder)
        if all_files:
            self.backup_tiles(backup_subfolder)
            self.backup_colliders(backup_subfolder)
        self.backup_scene_objects(backup_subfolder)
        self.backup_shapes(backup_subfolder)

    def clean(self):
        isolated_print(EOL)
        self.__clean_objects(self.tiles)
        self.__clean_objects(self.colliders)
        self.__clean_objects(self.objects)

    def optimize(self, settings):
        isolated_print(EOL)
        dest_format = settings.output_texture_format
        src_format = JPG_TEXTURE_FORMAT if dest_format == PNG_TEXTURE_FORMAT else PNG_TEXTURE_FORMAT
        lods = [lod for tile in self.tiles.values() for lod in tile.lods]
        self.__convert_tiles_textures(src_format, dest_format)
        self.update_min_size_values(settings)
        # some tile lods are not optimized
        if self.__optimization_needed():
            self.__create_optimization_folders()
            self.__optimize_tile_lods(self.__retrieve_lods_to_process())

        pbar = ProgressBar(list(lods), title="PREPARE THE TILES FOR MSFS")
        for lod in lods:
            lod.folder = os.path.dirname(lod.folder)
            lod.optimization_in_progress = False
            lod.prepare_for_msfs()
            pbar.update("%s prepared for msfs" % lod.name)

        self.objects_xml.update_objects_position(self, settings)

    def fix_tiles_lightning_issues(self, settings):
        isolated_print(EOL)
        lods = [lod for tile in self.tiles.values() for lod in tile.lods]
        pbar = ProgressBar(list(lods), title="FIX TILES LIGHTNING ISSUES")
        for lod in lods:
            lod.optimization_in_progress = False
            lod.prepare_for_msfs()
            pbar.update("%s lightning issues fixed" % lod.name)

    def backup_tiles(self, backup_subfolder):
        backup_path = os.path.join(self.backup_folder, backup_subfolder)
        self.__backup_objects(self.tiles, backup_path, "backup tiles")

    def backup_colliders(self, backup_subfolder):
        backup_path = os.path.join(self.backup_folder, backup_subfolder)
        self.__backup_objects(self.colliders, backup_path, "backup colliders")

    def backup_scene_objects(self, backup_subfolder):
        backup_path = os.path.join(self.backup_folder, backup_subfolder)
        self.__backup_objects(self.objects, backup_path, "backup scene objects")

    def backup_shapes(self, backup_subfolder):
        backup_path = os.path.join(self.backup_folder, backup_subfolder)
        self.__backup_objects(self.shapes, backup_path, "backup shapes")

    def backup_files(self, backup_subfolder):
        backup_path = os.path.join(self.backup_folder, backup_subfolder)
        if not os.path.isfile(get_backup_file_path(backup_path, self.scene_folder, self.SCENE_OBJECTS_FILE)):
            pbar = ProgressBar([self.SCENE_OBJECTS_FILE], title="backup " + self.SCENE_OBJECTS_FILE)
            backup_file(backup_path, self.scene_folder, self.SCENE_OBJECTS_FILE, pbar=pbar)

    def update_min_size_values(self, settings):
        pbar = ProgressBar(list())
        pbar.range = len(self.tiles) + len(self.colliders)
        pbar.display_title("Update lod values")
        for tile in self.tiles.values():
            tile.update_min_size_values(settings.target_min_size_values, pbar=pbar)
        for collider in self.colliders.values():
            collider.update_min_size_values(settings.target_min_size_values, pbar=pbar)

    def compress_built_package(self, settings):
        compressonator = Compressonator(settings.compressonator_exe_path, self.model_lib_output_folder)
        compressonator.compress_texture_files()

    def merge(self, project_to_merge):
        if self.objects_xml and project_to_merge.objects_xml:
            self.__merge_tiles(self.tiles, project_to_merge.project_name, project_to_merge.tiles, project_to_merge.objects_xml)
            self.__merge_colliders(self.colliders, project_to_merge.project_name, project_to_merge.colliders, project_to_merge.objects_xml)
            self.__merge_scene_objects(self.objects, project_to_merge.project_name, project_to_merge.objects, project_to_merge.objects_xml)
            self.objects_xml.save()
            self.__merge_shapes(self.shapes, project_to_merge.shapes)

    def split_tiles(self):
        self.__split_tiles(self.__retrieve_tiles_to_process())

    def __initialize(self, sources_path, init_structure, fast_init):
        self.__init_structure(sources_path, init_structure)

        if not fast_init:
            self.__init_components()
            self.__guess_min_lod_level()

    def __init_structure(self, sources_path, init_structure):
        self.project_definition_xml = self.project_name + XML_FILE_EXT
        if init_structure or not os.path.isfile(os.path.join(self.project_folder, self.project_definition_xml)):
            self.package_definitions_xml = self.author_name.lower() + "-" + self.project_definition_xml.lower()
        else:
            xml = MsfsProjectXml(self.project_folder, self.project_definition_xml)
            self.package_definitions_xml = basename(xml.definition_file)
        self.objects = dict()
        self.tiles = dict()
        self.shapes = dict()
        self.colliders = dict()

        if init_structure:
            try:
                # create the project folder if it does not exist
                os.makedirs(self.project_folder, exist_ok=True)
                # create the backup folder if it does not exist
                os.makedirs(self.backup_folder, exist_ok=True)
                # create the PackageSources folder if it does not exist
                os.makedirs(self.package_sources_folder, exist_ok=True)
                if not init_structure:
                    # create the modelLib folder if it does not exist
                    os.makedirs(self.model_lib_folder, exist_ok=True)
                    # create the scene folder if it does not exist
                    os.makedirs(self.scene_folder, exist_ok=True)
                    # create the texture folder if it does not exist
                    os.makedirs(self.texture_folder, exist_ok=True)
                # rename modelLib folder if it exists
                if os.path.isdir(os.path.join(self.package_sources_folder, self.MODEL_LIB_FOLDER)) and not os.path.isdir(self.model_lib_folder):
                    # change modelib folder to fix CTD issues (see
                    # https://flightsim.to/blog/creators-guide-fix-ctd-issues-on-your-scenery/)
                    os.rename(os.path.join(self.package_sources_folder, self.MODEL_LIB_FOLDER), self.model_lib_folder)
                # create the PackageDefinitions folder if it does not exist
                os.makedirs(self.package_definitions_folder, exist_ok=True)
                # create the business.json folder if it does not exist
                os.makedirs(self.business_json_folder, exist_ok=True)
                # create the content info folder if it does not exist
                os.makedirs(self.content_info_folder, exist_ok=True)
            except WindowsError:
                raise ScriptError("MSFS project folders creation is not possible")

        # rename project definition xml file folder if it exists
        old_project_definition_xml_path = os.path.join(self.project_folder, self.package_definitions_xml)
        self.project_definition_xml_path = os.path.join(self.project_folder, self.project_definition_xml)
        if os.path.isfile(old_project_definition_xml_path):
            os.rename(old_project_definition_xml_path, self.project_definition_xml_path)
        if init_structure: self.__create_project_file(sources_path, PROJECT_DEFINITION_TEMPLATE_PATH, self.project_definition_xml_path, True)

        # create package xml definition file if it does not exist
        self.package_definitions_xml_path = os.path.join(self.package_definitions_folder, self.package_definitions_xml)
        if init_structure: self.__create_project_file(sources_path, PACKAGE_DEFINITIONS_TEMPLATE_PATH, self.package_definitions_xml_path, True)

        # create business.json file if it does not exist
        self.business_json_path = os.path.join(self.business_json_folder, BUSINESS_JSON_TEMPLATE)
        if init_structure: self.__create_project_file(sources_path, BUSINESS_JSON_TEMPLATE_PATH, self.business_json_path, True)

        # create thumbnail file if it does not exist
        self.thumbnail_picture_path = os.path.join(self.content_info_folder, THUMBNAIL_PICTURE_TEMPLATE)
        if init_structure:  self.__create_project_file(sources_path, THUMBNAIL_PICTURE_TEMPLATE_PATH, self.thumbnail_picture_path)

        self.model_lib_output_folder = self.__get_model_lib_output_folder()

    def __init_components(self):
        self.__retrieve_objects()

    def __project_definition_xml_exists(self, project_definition_xml):
        alt_project_definition_xml = self.author_name.lower() + "-" + project_definition_xml.lower()

        return os.path.isfile(os.path.join(self.project_folder, project_definition_xml)) \
               or os.path.isfile(os.path.join(self.project_folder, alt_project_definition_xml))

    def __create_project_file(self, sources_path, src_file_relative_path, dest_file_path, replace_content=False):
        if not os.path.isfile(dest_file_path):
            src_file_path = os.path.join(sources_path, src_file_relative_path)

            try:
                shutil.copyfile(src_file_path, dest_file_path)
            except WindowsError:
                raise ScriptError("Impossible de copier le fichier " + sources_path + " vers " + dest_file_path)

        if replace_content:
            replace_in_file(dest_file_path, self.DUMMY_STRING.capitalize(), self.project_name)
            replace_in_file(dest_file_path, self.DUMMY_STRING, self.project_name.lower())
            replace_in_file(dest_file_path, self.AUTHOR_STRING.capitalize(), self.author_name)
            replace_in_file(dest_file_path, self.AUTHOR_STRING, self.author_name.lower())

    def __retrieve_objects(self):
        self.__retrieve_scene_objects()
        self.__retrieve_shapes()

    def __retrieve_scene_objects(self):
        pbar = ProgressBar(list(Path(self.model_lib_folder).rglob(XML_FILE_PATTERN)), title="Retrieve project infos")
        for i, path in enumerate(pbar.iterable):
            if not is_octant(path.stem):
                msfs_scene_object = MsfsSceneObject(self.model_lib_folder, path.stem, path.name)
                self.objects[msfs_scene_object.xml.guid] = msfs_scene_object
                pbar.update("%s" % path.name)
                continue

            if self.COLLIDER_SUFFIX in path.stem:
                msfs_collider = MsfsCollider(self.model_lib_folder, path.stem, path.name)
                self.colliders[msfs_collider.xml.guid] = msfs_collider
                pbar.update("%s" % path.name)
                continue

            msfs_tile = MsfsTile(self.model_lib_folder, path.stem, path.name)
            self.tiles[msfs_tile.xml.guid] = msfs_tile
            pbar.update("%s" % path.name)

    def __retrieve_shapes(self):
        pbar = ProgressBar(list(Path(self.scene_folder).rglob(DBF_FILE_PATTERN)), title="Retrieve shapes")
        for i, path in enumerate(pbar.iterable):
            self.shapes[path.stem] = MsfsShape(self.scene_folder, path.stem, path.stem + XML_FILE_EXT, path.name, path.stem + SHP_FILE_EXT, path.stem + SHX_FILE_EXT)
            pbar.update("%s" % path.name)

    def __backup_objects(self, objects: dict, backup_path, pbar_title="backup files"):
        pbar = ProgressBar(list())
        for guid, object in objects.items():
            object.backup_files(backup_path, dry_mode=True, pbar=pbar)
        if pbar.range > 0:
            pbar.display_title(pbar_title)
            for guid, object in objects.items():
                object.backup_files(backup_path, pbar=pbar)

    def __clean_objects(self, objects: dict):
        pop_objects = []
        for guid, object in objects.items():
            # first, check if the object is unused
            if not self.objects_xml.find_scenery_objects(guid) and not self.objects_xml.find_scenery_objects_in_group(guid):
                # unused object, so remove the files related to it
                object.remove_files()
                pop_objects.append(guid)
            else:
                object.clean_lods()

        for guid in pop_objects:
            objects.pop(guid)

    def __remove_object(self, object):
        guid = object.xml.guid

        found_scenery_objects_parents, found_scenery_objects = self.__find_scenery_objects_and_its_parents(self.objects_xml, guid)
        self.objects_xml.remove_tags(found_scenery_objects_parents, found_scenery_objects)

        self.objects_xml.save()

        if guid in self.tiles:
            self.tiles.pop(guid, None)

        if guid in self.colliders:
            self.colliders.pop(guid, None)

    def __retrieve_tiles_textures(self, extension):
        textures = []
        for guid, tile in self.tiles.items():
            for lod in tile.lods: textures.extend([texture for texture in lod.textures if extension in texture.file])
        return textures

    def __convert_tiles_textures(self, src_format, dest_format):
        textures = self.__retrieve_tiles_textures(src_format)

        if textures:
            isolated_print(src_format + " texture files detected in the tiles of the project! Try to install pip, then convert them")
            print_title("INSTALL PILLOW")
            install_python_lib("Pillow")

            pbar = ProgressBar(textures, title="CONVERT " + src_format.upper() + " TEXTURE FILES TO " + dest_format.upper())
            for texture in textures:
                file = texture.file
                if not texture.convert_format(src_format, dest_format):
                    raise ScriptError("An error was detected while converting texture files in " + self.texture_folder + " ! Please convert them to " + dest_format + " format prior to launch the script, or remove them")
                else:
                    pbar.update("%s converted to %s" % (file, dest_format))

    def __guess_min_lod_level(self):
        lod_stats = dict()
        for guid, tile in self.tiles.items():
            lod_level = len(tile.name)
            lod_stats[lod_level] = lod_stats[lod_level] + 1 if lod_level in lod_stats else 0

        if lod_stats:
            max_res = max(lod_stats.values())

            for lod_level, nb in lod_stats.items():
                if nb == max_res: self.min_lod_level = lod_level

    def __nb_lods(self):
        res = 0
        for tile in self.tiles.values():
            res += len(tile.lods)

        return res

    def __optimization_needed(self):
        for tile in self.tiles.values():
            for lod in tile.lods:
                if not lod.optimized: return True

        return False

    def __link_tiles_by_position(self):
        linked_tiles = {}
        tile_candidates = [tile for tile in self.tiles.values()]
        # maybe sorting in unnecessary, but as it can impact the optimization process, ensure that it is done
        sorted_tiles_by_name = sorted(sorted(tile_candidates, key=lambda tile: tile.name), key=lambda tile: len(tile.name))

        for tile in sorted_tiles_by_name[:]:
            if tile not in tile_candidates: continue
            linked_tiles[tile] = [tile]
            for tile_candidate in tile_candidates[:]:
                if tile_candidate.name == tile.name:
                    tile_candidates.remove(tile_candidate)
                    continue
                if tile.name != tile_candidate.name and tile.contains(tile_candidate):
                    linked_tiles[tile].append(tile_candidate)
                    tile_candidates.remove(tile_candidate)
                    sorted_tiles_by_name.remove(tile_candidate)
                    # remove tile candidate from the project
                    self.__remove_object(tile_candidate)

        return linked_tiles

    def __create_optimization_folders(self):
        pbar = ProgressBar(list())
        link_tiles_by_position = self.__link_tiles_by_position()
        for parent_tile, tiles in link_tiles_by_position.items():
            parent_tile.create_optimization_folders(tiles, dry_mode=True, pbar=pbar)
        if pbar.range > 0:
            pbar.display_title("Create optimization folders")
            for parent_tile, tiles in link_tiles_by_position.items():
                parent_tile.create_optimization_folders(tiles, dry_mode=False, pbar=pbar)

    def __get_model_lib_output_folder(self):
        if not os.path.isfile(os.path.join(self.package_definitions_folder, self.package_definitions_xml)):
            return str()
        xml = MsfsPackageDefinitionsXml(self.package_definitions_folder, self.package_definitions_xml)
        return os.path.join(self.built_project_package_folder, xml.find_model_lib_asset_group(self.project_name.lower() + "-" + self.MODEL_LIB_FOLDER))

    def __retrieve_lods_to_process(self):
        data = []
        for tile in self.tiles.values():
            for lod in tile.lods:
                if os.path.isdir(lod.folder) and lod.folder != self.model_lib_folder:
                    data.append({"name": lod.name, "params": ["--folder", str(lod.folder), "--model_file", str(lod.model_file)]})

        return chunks(data, self.NB_PARALLEL_TASKS)

    def __optimize_tile_lods(self, lods_data):
        self.__multithread_process_data(lods_data, "optimize_tile_lod.py", "OPTIMIZE THE TILES", "optimized")

    def __merge_tiles(self, tiles, project_to_merge_name, tiles_to_merge, objects_xml_to_merge):
        pbar = ProgressBar(tiles_to_merge.items(), title="MERGE THE TILES")
        self.__merge_objects(tiles, project_to_merge_name, objects_xml_to_merge, pbar)

    def __merge_colliders(self, colliders, project_to_merge_name, colliders_to_merge, objects_xml_to_merge):
        pbar = ProgressBar(colliders_to_merge.items(), title="MERGE THE COLLIDERS")
        self.__merge_objects(colliders, project_to_merge_name, objects_xml_to_merge, pbar)

    def __merge_scene_objects(self, scene_objects, project_to_merge_name, scene_objects_to_merge, objects_xml_to_merge):
        pbar = ProgressBar(scene_objects_to_merge.items(), title="MERGE THE OBJECTS")
        self.__merge_objects(scene_objects, project_to_merge_name, objects_xml_to_merge, pbar)

    def __merge_objects(self, objects, project_to_merge_name, objects_xml_to_merge, pbar):
        for guid, object in pbar.iterable:
            # copy or overwrite files
            add_guid = not os.path.isfile(os.path.join(self.model_lib_folder, object.definition_file))
            shutil.copyfile(os.path.join(object.folder, object.definition_file), os.path.join(self.model_lib_folder, object.definition_file))
            for lod in object.lods:
                shutil.copyfile(os.path.join(lod.folder, lod.model_file), os.path.join(self.model_lib_folder, lod.model_file))
                for binary in lod.binaries:
                    shutil.copyfile(os.path.join(binary.folder, binary.file), os.path.join(self.model_lib_folder, binary.file))
                for texture in lod.textures:
                    shutil.copyfile(os.path.join(texture.folder, texture.file), os.path.join(self.texture_folder, texture.file))

            # update objects.xml file
            if not add_guid:
                old_guid = self.__find_guid_with_definition_file(objects, object.definition_file)
                objects.pop(old_guid, None)
                scenery_objects_parents, scenery_objects = self.__find_scenery_objects_and_its_parents(self.objects_xml, old_guid)
                self.objects_xml.remove_tags(scenery_objects_parents, scenery_objects)

            # new guid to add
            new_scenery_objects_parents, new_scenery_objects = self.__find_scenery_objects_and_its_parents(objects_xml_to_merge, guid)
            for new_scenery_object in new_scenery_objects:
                new_scenery_object.set(self.objects_xml.DISPLAY_NAME_ATTR, project_to_merge_name + "_" + object.name)
                self.objects_xml.root.append(new_scenery_object)

            objects[guid] = object
            pbar.update("%s merged" % object.name)

    def __merge_shapes(self, shapes, shapes_to_merge):
        pbar = ProgressBar(shapes_to_merge.items())
        for name, shape in pbar.iterable:
            if not os.path.isfile(os.path.join(self.scene_folder, shape.definition_file)):
                pbar.display_title("MERGE THE SHAPES")
                shutil.copyfile(os.path.join(shape.folder, shape.definition_file), os.path.join(self.scene_folder, shape.definition_file))
                shutil.copyfile(os.path.join(shape.folder, shape.dbf_file_name), os.path.join(self.scene_folder, shape.dbf_file_name))
                shutil.copyfile(os.path.join(shape.folder, shape.shp_file_name), os.path.join(self.scene_folder, shape.shp_file_name))
                shutil.copyfile(os.path.join(shape.folder, shape.shx_file_name), os.path.join(self.scene_folder, shape.shx_file_name))
                shapes[name] = shape
                pbar.update("%s merged" % shape.name)

    def __retrieve_tiles_to_process(self):
        data = []
        for tile in self.tiles.values():
            if os.path.isdir(tile.folder):
                data.append({"name": tile.name, "params": ["--folder", str(tile.folder), "--name", str(tile.name), "--definition_file", str(tile.definition_file), "--objects_xml_folder", str(self.scene_folder), "--objects_xml_file", str(self.SCENE_OBJECTS_FILE)]})

        return chunks(data, 1)

    def __split_tiles(self, tiles_data):
        self.__multithread_process_data(tiles_data, "split_tile.py", "SPLIT THE TILES", "splitted")

    @staticmethod
    def __find_guid_with_definition_file(objects, definition_file):
        for key, object in objects.items():
            if object.definition_file == definition_file:
                return key

        return str()

    @staticmethod
    def __find_scenery_objects_and_its_parents(objects_xml, guid):
        if objects_xml.find_scenery_objects(guid):
            return objects_xml.find_scenery_objects_parents(guid), objects_xml.find_scenery_objects(guid)

        if objects_xml.find_scenery_objects_in_group(guid):
            return objects_xml.find_scenery_objects_in_group_parents(guid), objects_xml.find_scenery_objects_in_group(guid)

        return [], []

    @staticmethod
    def __multithread_process_data(processed_data, script_name, title, update_msg):
        ON_POSIX = 'posix' in sys.builtin_module_names

        processed_data, data = itertools.tee(processed_data)
        pbar = ProgressBar(list(data), title=title)

        try:
            for chunck in processed_data:
                # create a pipe to get data
                input_fd, output_fd = os.pipe()
                params = [str(bpy.app.binary_path), "--background", "--python", os.path.join(os.path.dirname(os.path.dirname(__file__)), script_name), "--"]

                for obj in chunck:
                    print("-------------------------------------------------------------------------------")
                    print("prepare command line: ", "\"" + str(bpy.app.binary_path) + "\" --background --python \"" + os.path.join(os.path.dirname(os.path.dirname(__file__)), script_name) + "\" -- " + str(" ").join(obj["params"]))

                si = subprocess.STARTUPINFO()
                si.dwFlags = subprocess.STARTF_USESTDHANDLES | subprocess.HIGH_PRIORITY_CLASS

                processes = [subprocess.Popen(params + obj["params"],
                                              stdout=output_fd, stderr=subprocess.DEVNULL, close_fds=ON_POSIX, startupinfo=si, encoding=ENCODING) for obj in chunck]

                os.close(output_fd)  # close unused end of the pipe

                # read output line by line as soon as it is available
                with io.open(input_fd, "r", buffering=1) as file:
                    for line in file:
                        print(line, end=str())

                for p in processes:
                    p.wait()

                pbar.update("%s %s" % (obj["name"], update_msg))
        except:
            pass
