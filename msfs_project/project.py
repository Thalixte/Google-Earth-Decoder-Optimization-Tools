import shutil
import os

from constants import *
from msfs_project.objects_xml import ObjectsXml
from msfs_project.scene_object import MsfsSceneObject
from msfs_project.collider import MsfsCollider
from msfs_project.tile import MsfsTile
from msfs_project.shape import MsfsShape
from utils import replace_in_file, is_octant, backup_file, install_python_lib, ScriptError, print_title, \
    get_backup_file_path, isolated_print, is_contained
from pathlib import Path

from utils.progress_bar import ProgressBar


class MsfsProject:
    parent_path: str
    project_name: str
    author_name: str
    project_folder: str
    package_definitions_folder: str
    package_sources_folder: str
    modelLib_folder: str
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
    MODEL_LIB_FOLDER = "modelLib"
    SCENE_FOLDER = "scene"
    TEXTURE_FOLDER = "texture"
    CONTENT_INFO_FOLDER = "ContentInfo"
    SCENE_OBJECTS_FILE = "objects" + XML_FILE_EXT
    COLLIDER_SUFFIX = "_collider"

    def __init__(self, projects_path, project_name, author_name, sources_path, init=False):
        isolated_print(EOL)
        self.parent_path = projects_path
        self.project_name = project_name
        self.author_name = author_name
        self.project_folder = os.path.join(self.parent_path, self.project_name.capitalize())
        self.backup_folder = os.path.join(self.project_folder, self.BACKUP_FOLDER)
        self.package_definitions_folder = os.path.join(self.project_folder, self.PACKAGE_DEFINITIONS_FOLDER)
        self.package_sources_folder = os.path.join(self.project_folder, self.PACKAGE_SOURCES_FOLDER)
        self.modelLib_folder = os.path.join(self.package_sources_folder, self.MODEL_LIB_FOLDER if init else self.project_name.lower() + "-" + self.MODEL_LIB_FOLDER)
        self.scene_folder = os.path.join(self.package_sources_folder, self.SCENE_FOLDER)
        self.texture_folder = os.path.join(self.modelLib_folder, self.TEXTURE_FOLDER)
        self.scene_folder = os.path.join(self.package_sources_folder, self.SCENE_FOLDER)
        self.business_json_folder = os.path.join(self.package_definitions_folder, self.author_name.lower() + "-" + self.project_name.lower())
        self.content_info_folder = os.path.join(self.package_definitions_folder, self.business_json_folder, self.CONTENT_INFO_FOLDER)
        self.scene_objects_xml_file_path = os.path.join(self.scene_folder, self.SCENE_OBJECTS_FILE)
        if os.path.isfile(self.scene_objects_xml_file_path):
            self.objects_xml = ObjectsXml(self.scene_folder, self.SCENE_OBJECTS_FILE)
        self.min_lod_level = 0

        self.__initialize(sources_path)

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
        self.__convert_tiles_textures(src_format, dest_format)
        self.__update_lod_values(settings)
        # some tile lods are not optimized
        if self.__optimization_needed():
            print_title("OPTIMIZE THE TILES")
            self.__create_optimization_folders()
            if settings.bake_textures_enabled:
                for tile in self.tiles.values():
                    for lod in tile.lods:
                        lod.optimize(settings.output_texture_format)

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

    def __initialize(self, sources_path):
        self.__init_structure(sources_path)
        self.__init_components()
        self.__guess_min_lod_level()

    def __init_structure(self, sources_path):
        self.project_definition_xml = self.project_name + XML_FILE_EXT
        self.package_definitions_xml = self.author_name.lower() + "-" + self.project_definition_xml.lower()
        self.objects = dict()
        self.tiles = dict()
        self.shapes = dict()
        self.colliders = dict()

        # create the project folder if it does not exist
        os.makedirs(self.project_folder, exist_ok=True)
        os.chdir(self.project_folder)
        # create the backup folder if it does not exist
        os.makedirs(self.backup_folder, exist_ok=True)
        # create the PackageSources folder if it does not exist
        os.makedirs(self.package_sources_folder, exist_ok=True)
        # rename modelLib folder if it exists
        if os.path.isdir(os.path.join(self.package_sources_folder, self.MODEL_LIB_FOLDER)):
            # change modelib folder to fix CTD issues (see
            # https://flightsim.to/blog/creators-guide-fix-ctd-issues-on-your-scenery/)
            os.rename(os.path.join(self.package_sources_folder, self.MODEL_LIB_FOLDER), self.modelLib_folder)
        # create the modelLib folder if it does not exist
        os.makedirs(self.modelLib_folder, exist_ok=True)
        # create the scene folder if it does not exist
        os.makedirs(self.scene_folder, exist_ok=True)
        # create the texture folder if it does not exist
        os.makedirs(self.texture_folder, exist_ok=True)
        # create the PackageDefinitions folder if it does not exist
        os.makedirs(self.package_definitions_folder, exist_ok=True)
        # create the business.json folder if it does not exist
        os.makedirs(self.business_json_folder, exist_ok=True)
        # create the content info folder if it does not exist
        os.makedirs(self.content_info_folder, exist_ok=True)

        # rename project definition xml file folder if it exists
        old_project_definition_xml_path = os.path.join(self.project_folder, self.package_definitions_xml)
        self.project_definition_xml_path = os.path.join(self.project_folder, self.project_definition_xml)
        if os.path.isfile(old_project_definition_xml_path):
            os.rename(old_project_definition_xml_path, self.project_definition_xml_path)
        self.__create_project_file(sources_path, PROJECT_DEFINITION_TEMPLATE_PATH, self.project_definition_xml_path, True)

        # create package xml definition file if it does not exist
        self.package_definitions_xml_path = os.path.join(self.package_definitions_folder, self.package_definitions_xml)
        self.__create_project_file(sources_path, PACKAGE_DEFINITIONS_TEMPLATE_PATH, self.package_definitions_xml_path, True)

        # create business.json file if it does not exist
        self.business_json_path = os.path.join(self.business_json_folder, BUSINESS_JSON_TEMPLATE)
        self.__create_project_file(sources_path, BUSINESS_JSON_TEMPLATE_PATH, self.business_json_path, True)

        # create thumbnail file if it does not exist
        self.thumbnail_picture_path = os.path.join(self.content_info_folder, THUMBNAIL_PICTURE_TEMPLATE)
        self.__create_project_file(sources_path, THUMBNAIL_PICTURE_TEMPLATE_PATH, self.thumbnail_picture_path)

    def __init_components(self):
        self.__retrieve_objects()

    def __project_definition_xml_exists(self, project_definition_xml):
        alt_project_definition_xml = self.author_name.lower() + "-" + project_definition_xml.lower()

        return os.path.isfile(os.path.join(self.project_folder, project_definition_xml)) \
               or os.path.isfile(os.path.join(self.project_folder, alt_project_definition_xml))

    def __create_project_file(self, sources_path, src_file_relative_path, dest_file_path, replace_content=False):
        if not os.path.isfile(dest_file_path):
            src_file_path = os.path.join(sources_path, src_file_relative_path)
            shutil.copyfile(src_file_path, dest_file_path)

        if replace_content:
            replace_in_file(dest_file_path, self.DUMMY_STRING.capitalize(), self.project_name)
            replace_in_file(dest_file_path, self.DUMMY_STRING, self.project_name.lower())
            replace_in_file(dest_file_path, self.AUTHOR_STRING.capitalize(), self.author_name)
            replace_in_file(dest_file_path, self.AUTHOR_STRING, self.author_name.lower())

    def __retrieve_objects(self):
        self.__retrieve_scene_objects()
        self.__retrieve_shapes()

    def __retrieve_scene_objects(self):
        pbar = ProgressBar(list(Path(self.modelLib_folder).rglob(XML_FILE_PATTERN)), title="Retrieve project infos")
        for i, path in enumerate(pbar.iterable):
            if not is_octant(path.stem):
                msfs_scene_object = MsfsSceneObject(self.modelLib_folder, path.stem, path.name)
                self.objects[msfs_scene_object.xml.guid] = msfs_scene_object
                pbar.update("%s" % path.name)
                continue

            if self.COLLIDER_SUFFIX in path.stem:
                msfs_collider = MsfsCollider(self.modelLib_folder, path.stem, path.name)
                self.colliders[msfs_collider.xml.guid] = msfs_collider
                pbar.update("%s" % path.name)
                continue

            msfs_tile = MsfsTile(self.modelLib_folder, path.stem, path.name)
            self.tiles[msfs_tile.xml.guid] = msfs_tile
            pbar.update("%s" % path.name)

    def __retrieve_shapes(self):
        pbar = ProgressBar(list(Path(self.scene_folder).rglob(DBF_FILE_PATTERN)), title="Retrieve shapes")
        for i, path in enumerate(pbar.iterable):
            self.shapes[path.stem] = MsfsShape(self.scene_folder, path.stem, path.stem + XML_FILE_EXT, path.name,
                                               path.stem + SHP_FILE_EXT, path.stem + SHX_FILE_EXT)
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
            if not self.objects_xml.find_scenery_objects(guid) and not self.objects_xml.find_scenery_objects_in_group(
                    guid):
                # unused object, so remove the files related to it
                object.remove_files()
                pop_objects.append(guid)
            else:
                object.clean_lods()

        for guid in pop_objects:
            objects.pop(guid)

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
                if not texture.convert(src_format, dest_format):
                    raise ScriptError(src_format + " texture files detected in " + self.texture_folder + " ! Please convert them to " + dest_format + " format prior to launch the script, or remove them")
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

    def __update_lod_values(self, settings):
        pbar = ProgressBar(list())
        pbar.range = len(self.tiles) + len(self.colliders)
        pbar.display_title("Update lod values")
        for tile in self.tiles.values():
            tile.update_lod_values(settings.target_lod_values, pbar=pbar)
        for collider in self.colliders.values():
            collider.update_lod_values(settings.target_lod_values, pbar=pbar)

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
                if tile.name != tile_candidate.name and ((tile_candidate.pos.lat, tile_candidate.pos.lon) == (tile.pos.lat, tile.pos.lon)) or is_contained(tile_candidate.coords, tile.coords):
                    linked_tiles[tile].append(tile_candidate)
                    tile_candidates.remove(tile_candidate)
                    sorted_tiles_by_name.remove(tile_candidate)

        return linked_tiles

    def __create_optimization_folders(self):
        pbar = ProgressBar(list())
        link_tiles_by_position = self.__link_tiles_by_position()
        for parent_tile, tiles in link_tiles_by_position.items():
            parent_tile.create_optimization_folders(tiles, dry_mode=True, pbar=pbar)
        if pbar.range > 0:
            isolated_print("Create optimization folders")
            for parent_tile, tiles in link_tiles_by_position.items():
                parent_tile.create_optimization_folders(tiles, dry_mode=False, pbar=pbar)

