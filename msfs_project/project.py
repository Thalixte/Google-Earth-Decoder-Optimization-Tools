import shutil
import os

from constants import *
from msfs_project.objects_xml import ObjectsXml
from msfs_project.scene_object import MsfsSceneObject
from msfs_project.collider import MsfsCollider
from msfs_project.tile import MsfsTile
from msfs_project.shape import MsfsShape
from utils import replace_in_file, is_octant
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

    def __init__(self, projects_path, project_name, author_name, sources_path):
        self.parent_path = projects_path
        self.project_name = project_name
        self.author_name = author_name
        self.project_folder = os.path.join(self.parent_path, self.project_name.capitalize())
        self.backup_folder = os.path.join(self.project_folder, self.BACKUP_FOLDER)
        self.package_definitions_folder = os.path.join(self.project_folder, self.PACKAGE_DEFINITIONS_FOLDER)
        self.package_sources_folder = os.path.join(self.project_folder, self.PACKAGE_SOURCES_FOLDER)
        self.modelLib_folder = os.path.join(self.package_sources_folder, self.project_name.lower() + "-" + self.MODEL_LIB_FOLDER)
        self.scene_folder = os.path.join(self.package_sources_folder, self.SCENE_FOLDER)
        self.texture_folder = os.path.join(self.modelLib_folder, self.TEXTURE_FOLDER)
        self.scene_folder = os.path.join(self.package_sources_folder, self.SCENE_FOLDER)
        self.business_json_folder = os.path.join(self.package_definitions_folder, self.author_name.lower() + "-" + self.project_name.lower())
        self.content_info_folder = os.path.join(self.package_definitions_folder, self.business_json_folder, self.CONTENT_INFO_FOLDER)
        self.scene_objects_xml_file_path = os.path.join(self.scene_folder, self.SCENE_OBJECTS_FILE)
        self.objects_xml = ObjectsXml(self.scene_folder, self.SCENE_OBJECTS_FILE)

        self.__initialize(sources_path)

    def update_objects_position(self, settings):
        print(self)
        self.objects_xml.update_objects_position(self, settings)

    def clean(self):
        print(self)

    def __initialize(self, sources_path):
        self.__init_structure(sources_path)
        self.__init_components()

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
        pbar = ProgressBar(list(Path(self.modelLib_folder).rglob(XML_FILE_PATTERN)), title="Retrieve scenery objects")
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
            self.shapes[path.stem] = MsfsShape(self.scene_folder, path.stem, path.stem + XML_FILE_EXT, path.name, path.stem + SHP_FILE_EXT, path.stem + SHX_FILE_EXT)
            pbar.update("%s" % path.name)
