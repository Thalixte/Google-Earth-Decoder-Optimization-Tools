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
import warnings
from os.path import basename

import io
import shutil
import os
import subprocess

from shapely.errors import ShapelyDeprecationWarning

from utils.install_lib import install_python_lib
from utils.string import remove_accents
from utils.geo_pandas import prepare_wall_gdf, create_exclusion_water_gdf, prepare_water_gdf, prepare_amenity_gdf, prepare_hidden_roads_gdf, prepare_water_exclusion_gdf, prepare_residential_gdf, create_point_gdf, prepare_forest_gdf, prepare_wood_gdf, prepare_natural_gdf, prepare_landuse_gdf, create_vegetation_polygons_gdf, create_exclusion_vegetation_water_gdf
from constants import *

try:
    import osmnx as ox
except ModuleNotFoundError:
    install_python_lib(OSMNX_LIB, OSMNX_LIB_VERSION)
    import osmnx as ox

import logging as lg
from osmnx.utils_geo import bbox_to_poly

import bpy
from msfs_project.project_settings import ProjectSettings
from msfs_project.landmark import MsfsLandmarks
from msfs_project.height_map_xml import HeightMapXml
from msfs_project.height_map import MsfsHeightMaps
from msfs_project.osm_xml import OsmXml
from msfs_project.project_xml import MsfsProjectXml
from msfs_project.package_definitions_xml import MsfsPackageDefinitionsXml
from msfs_project.objects_xml import ObjectsXml
from msfs_project.object_xml import MsfsObjectXml
from msfs_project.scene_object import MsfsSceneObject
from msfs_project.collider import MsfsCollider
from msfs_project.tile import MsfsTile
from msfs_project.shape import MsfsShapes
from utils import replace_in_file, is_octant, backup_file, ScriptError, print_title, \
    get_backup_file_path, isolated_print, chunks, create_bounding_box_from_tiles, clip_gdf, create_terraform_polygons_gdf, create_land_mass_gdf, preserve_holes, create_exclusion_building_polygons_gdf, create_whole_water_gdf, create_ground_exclusion_gdf, load_gdf, \
    prepare_sea_gdf, prepare_bbox_gdf, prepare_gdf, create_exclusion_vegetation_polygons_gdf, load_gdf_from_geocode, difference_gdf, create_shore_water_gdf, resize_gdf, pr_bg_orange, load_json_file, prepare_park_gdf, prepare_building_gdf, create_empty_gdf, union_gdf, prepare_roads_gdf
from pathlib import Path

from utils.compressonator import Compressonator
from utils.minidom_xml import add_scenery_object, create_new_definition_file, add_new_lod
from utils.progress_bar import ProgressBar

warnings.simplefilter(action="ignore", category=UserWarning, append=True)
warnings.simplefilter(action="ignore", category=FutureWarning, append=True)
warnings.simplefilter(action="ignore", category=DeprecationWarning, append=True)
warnings.simplefilter(action="ignore", category=ShapelyDeprecationWarning, append=True)


class MsfsProject:
    settings: ProjectSettings
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
    osmfiles_folder: str
    shpfiles_folder: str
    xmlfiles_folder: str
    tilefiles_folder: str
    sources_folder: str
    project_definition_xml: str
    project_definition_xml_path: str
    package_definitions_xml: str
    package_definitions_xml_path: str
    scene_objects_xml_file_path: str
    business_json_path: str
    thumbnail_picture_path: str
    light_models_path: str
    built_packages_folder: str
    built_project_package_folder: str
    model_lib_output_dir: str
    min_lod_level: int
    objects: dict
    tiles: dict
    shapes: dict
    height_maps: dict
    landmarks: MsfsLandmarks
    colliders: dict
    objects_xml: ObjectsXml | None
    coords: tuple
    nb_parallel_blender_tasks: float

    DUMMY_STRING = "dummy"
    AUTHOR_STRING = "author"
    BACKUP_FOLDER = "backup"
    PACKAGE_DEFINITIONS_FOLDER = "PackageDefinitions"
    PACKAGE_SOURCES_FOLDER = "PackageSources"
    BUILT_PACKAGES_FOLDER = "Packages"
    MODEL_LIB_FOLDER = "modelLib"
    SCENE_FOLDER = "scene"
    CACHE_FOLDER = "cache"
    OSMFILES_FOLDER = "osm"
    SHPFILES_FOLDER = "shp"
    XMLFILES_FOLDER = "xml"
    TILEFILES_FOLDER = "tiles"
    CONTENT_INFO_FOLDER = "ContentInfo"
    SCENE_OBJECTS_FILE = "objects" + XML_FILE_EXT

    def __init__(self, projects_path, project_name, definition_file, global_path, author_name, init_structure=False, fast_init=False):
        self.parent_path = projects_path
        self.project_name = project_name
        self.project_definition_xml = definition_file
        self.author_name = author_name
        self.project_folder = os.path.join(self.parent_path, self.project_name.capitalize())
        self.backup_folder = os.path.join(self.project_folder, self.BACKUP_FOLDER)
        self.osmfiles_folder = os.path.join(self.project_folder, self.OSMFILES_FOLDER)
        self.shpfiles_folder = os.path.join(self.project_folder, self.SHPFILES_FOLDER)
        self.xmlfiles_folder = os.path.join(self.project_folder, self.XMLFILES_FOLDER)
        self.tilefiles_folder = os.path.join(self.project_folder, self.TILEFILES_FOLDER)
        self.package_definitions_folder = os.path.join(self.project_folder, self.PACKAGE_DEFINITIONS_FOLDER)
        self.package_sources_folder = os.path.join(self.project_folder, self.PACKAGE_SOURCES_FOLDER)
        self.sources_folder = global_path
        self.objects_xml = None

        # Ensure to remove remaining cache folder
        try:
            shutil.rmtree(os.path.join(self.project_folder, self.CACHE_FOLDER))
        except:
            pass

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

        self.__initialize(global_path, init_structure, fast_init)
        self.settings = ProjectSettings(global_path, self.project_folder, self.project_name)

    def update_objects_position(self, settings):
        isolated_print(EOL)
        self.objects_xml.update_objects_position(self, settings)

    def backup(self, backup_subfolder, all_files=True, texture_only=False):
        isolated_print(EOL)
        self.backup_files(backup_subfolder)
        if texture_only:
            all_files = False
            self.backup_textures(backup_subfolder)
        if all_files:
            self.backup_tiles(backup_subfolder)
            self.backup_colliders(backup_subfolder)
            self.backup_scene_objects(backup_subfolder)

    def clean(self):
        isolated_print(EOL)
        self.__clean_objects(self.tiles)
        self.__clean_objects(self.colliders)
        self.__clean_objects(self.objects)

        if not self.colliders:
            lods = [lod for tile in self.tiles.values() for lod in tile.lods]
            pbar = ProgressBar(list(lods), title="PREPARE THE TILES FOR MSFS")
            for lod in lods:
                lod.optimization_in_progress = False
                lod.prepare_for_msfs()
                pbar.update("%s prepared for msfs" % lod.name)

        # from UI.prefs import get_prefs
        # prefs = get_prefs()
        # compressonator = Compressonator(prefs.compressonator_exe_path, package_sources_folder=os.path.join(self.package_sources_folder, os.path.basename(self.model_lib_folder)))
        # compressonator.compress_gltf_files()

    def optimize(self, settings):
        isolated_print(EOL)
        dest_format = self.settings.output_texture_format
        src_format = JPG_TEXTURE_FORMAT if dest_format == PNG_TEXTURE_FORMAT else PNG_TEXTURE_FORMAT
        self.__convert_tiles_textures(src_format, dest_format)
        self.update_min_size_values()
        self.objects_xml.update_objects_position(self, settings)

        # some tile lods are not optimized
        if self.__optimization_needed():
            self.__create_optimization_folders()
            self.__optimize_tile_lods(self.__retrieve_lods_to_optimize(settings.nb_parallel_blender_tasks))

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

    def backup_textures(self, backup_subfolder):
        backup_path = os.path.join(self.backup_folder, backup_subfolder)
        self.__backup_textures(self.tiles, backup_path, "backup textures")

    def backup_colliders(self, backup_subfolder):
        backup_path = os.path.join(self.backup_folder, backup_subfolder)
        self.__backup_objects(self.colliders, backup_path, "backup colliders")

    def backup_scene_objects(self, backup_subfolder):
        backup_path = os.path.join(self.backup_folder, backup_subfolder)
        self.__backup_objects(self.objects, backup_path, "backup scene objects")

    def backup_files(self, backup_subfolder):
        backup_path = os.path.join(self.backup_folder, backup_subfolder)
        if not os.path.isfile(get_backup_file_path(backup_path, self.scene_folder, self.SCENE_OBJECTS_FILE)):
            pbar = ProgressBar([self.SCENE_OBJECTS_FILE], title="backup " + self.SCENE_OBJECTS_FILE)
            backup_file(backup_path, self.scene_folder, self.SCENE_OBJECTS_FILE, pbar=pbar, overwrite=True)

    def update_min_size_values(self):
        pbar = ProgressBar(list())
        pbar.range = len(self.tiles) + len(self.colliders)
        pbar.display_title("Update lod values")
        for tile in self.tiles.values():
            tile.update_min_size_values(self.settings.target_min_size_values, pbar=pbar)
        for collider in self.colliders.values():
            collider.update_min_size_values(self.settings.target_min_size_values, pbar=pbar)

    def compress_built_package(self):
        from UI.prefs import get_prefs
        prefs = get_prefs()
        compressonator = Compressonator(prefs.compressonator_exe_path, model_lib_folder=self.model_lib_output_folder)
        compressonator.compress_texture_files()

    def merge(self, project_to_merge):
        if self.objects_xml and project_to_merge.objects_xml:
            self.__merge_tiles(self.tiles, project_to_merge.project_name, project_to_merge.tiles, project_to_merge.objects_xml, project_to_merge)
            self.__merge_colliders(self.colliders, project_to_merge.project_name, project_to_merge.colliders, project_to_merge.objects_xml, project_to_merge)
            self.__merge_scene_objects(self.objects, project_to_merge.project_name, project_to_merge.objects, project_to_merge.objects_xml, project_to_merge)
            self.objects_xml.save()

    def remove_colliders(self):
        # clean previous colliders
        self.__remove_colliders()

        lods = [lod for tile in self.tiles.values() for lod in tile.lods]
        pbar = ProgressBar(list(lods), title="ADD ROAD AND COLLISION TAGS IN THE TILE LODS")
        for lod in lods:
            lod.optimization_in_progress = False
            lod.prepare_for_msfs()
            pbar.update("road and collision tags added from %s" % lod.name)

    def add_tile_colliders(self, collider_as_lower_lod=False):
        # clean previous colliders
        self.__remove_colliders()

        lods = [lod for tile in self.tiles.values() for lod in tile.lods]
        pbar = ProgressBar(list(lods), title="REMOVE ROAD AND COLLISION TAGS IN THE TILE LODS")
        for lod in lods:
            lod.optimization_in_progress = False
            lod.remove_road_and_collision_tags()
            pbar.update("road and collision tags removed from %s" % lod.name)

        pbar = ProgressBar(list(self.tiles.values()), title="ADD TILE COLLIDERS")
        for tile in self.tiles.values():
            tile_guid = tile.xml.guid
            new_collider = tile.add_collider(collider_as_lower_lod=collider_as_lower_lod)
            if new_collider is not None:
                self.__add_object_in_objects_xml(tile_guid, new_collider)
            pbar.update("collider added for %s tile" % tile.name)

    def split_tiles(self, settings):
        self.__split_tiles(self.__retrieve_tiles_to_process(settings.nb_parallel_blender_tasks))
        previous_tiles = {guid: tile for guid, tile in self.tiles.items()}
        new_tiles = {}

        # reload the project to retrieve the new tiles
        self.__retrieve_scene_objects()

        # create the matching dictionary between the previous tiles and the corresponding splitted tiles
        for previous_guid, previous_tile in previous_tiles.items():
            new_tiles[previous_tile] = [tile for tile in self.tiles.values() if previous_tile.name in tile.name and previous_tile.name != tile.name]

        pbar = ProgressBar(new_tiles.items(), title="REPLACE THE OLD TILES BY THE NEW SPLITTED TILES IN THE SCENE DEFINITION FILE")
        for previous_tile, new_tiles in new_tiles.items():
            self.__replace_tiles_in_objects_xml(previous_tile, new_tiles)

            pbar.update("splitted tiles added, replacing the previous %s tile" % previous_tile.name)

    def prepare_3d_data(self, settings, generate_height_data=False, process_3d_data=False, create_polygons=True, process_all=False):

        if self.settings.force_osm_data_download:
            # ensure to clean the xml folder containing the shapefile data by removing it
            try:
                shutil.rmtree(self.shpfiles_folder)
            except:
                pass

            # create the xml folder if it does not exist
            os.makedirs(self.shpfiles_folder, exist_ok=True)

        self.__create_tiles_bounding_boxes(init_osm_folder=True)
        self.__prepare_3d_data(settings, generate_height_data=generate_height_data, process_3d_data=process_3d_data, create_polygons=create_polygons, process_all=process_all)

        if generate_height_data:
            # ensure to clean the xml folder containing the heightmaps data by removing it
            try:
                shutil.rmtree(self.xmlfiles_folder)
            except:
                pass

            # create the xml folder if it does not exist
            os.makedirs(self.xmlfiles_folder, exist_ok=True)

            self.__generate_height_map_data(settings)

        if process_3d_data:
            # self.__reduce_number_of_vertices(settings.nb_parallel_blender_tasks)
            self.__process_lods_3d_data(settings.nb_parallel_blender_tasks, process_all=process_all)

    def exclude_3d_data_from_geocode(self, settings):
        geocode = self.settings.geocode
        geocode_gdf = self.__create_geocode_osm_files(geocode, settings, self.settings.preserve_roads, self.settings.preserve_buildings, self.coords, self.shpfiles_folder)

        if geocode_gdf is None:
            return geocode_gdf

        if not geocode_gdf.empty:
            self.__create_tiles_bounding_boxes()
            self.__exclude_lods_3d_data_from_geocode(geocode, geocode_gdf, settings)
            # update the existing exclusion building gdf file
            # exclusion_building = osmnx.geometries_from_xml(os.path.join(self.osmfiles_folder, "exclusion_building_polygons" + OSM_FILE_EXT))
            # construction = osmnx.geometries_from_xml(os.path.join(self.osmfiles_folder, "construction_terraform_polygons" + OSM_FILE_EXT))
            # amenity = osmnx.geometries_from_xml(os.path.join(self.osmfiles_folder, "amenity_terraform_polygons" + OSM_FILE_EXT))
            # update_exclusion_building_polygons_gdf(exclusion_building, construction, amenity)

    def isolate_3d_data_from_geocode(self, settings):
        geocode = self.settings.geocode
        geocode_gdf = self.__create_geocode_osm_files(geocode, settings, False, False, self.coords, self.shpfiles_folder)

        if geocode_gdf is None:
            return geocode_gdf

        if not geocode_gdf.empty:
            self.__create_tiles_bounding_boxes()
            self.__isolate_lods_3d_data_from_geocode(geocode, geocode_gdf, settings)

    def adjust_altitude(self, altitude_adjustment):
        self.__adjust_altitude(altitude_adjustment)

    def resize_textures(self, ratio):
        self.__resize_tiles_textures(ratio)

    def create_landmark_from_geocode(self, settings, lat, lon):
        geocode = self.settings.geocode
        self.__create_landmark_from_geocode(geocode, settings, self.coords)

    def add_lights_to_geocode(self, settings):
        geocode = self.settings.geocode
        geocode_gdf = self.__create_geocode_osm_files(geocode, settings, False, False, self.coords, self.shpfiles_folder)

        if geocode_gdf is None:
            return geocode_gdf

        if geocode_gdf.empty:
            return geocode_gdf

        lat = geocode_gdf.centroid.y.iloc[0]
        lon = geocode_gdf.centroid.x.iloc[0]

        point_gdf = create_point_gdf(lat, lon, 0.0)

        if not point_gdf.empty:
            # for debugging purpose, generate the osm file
            osm_xml = OsmXml(self.osmfiles_folder, LANDMARK_LOCATION_OSM_FILE_NAME + OSM_FILE_EXT)
            osm_xml.create_from_geodataframes([point_gdf], bbox_to_poly(self.coords[1], self.coords[0], self.coords[2], self.coords[3]), is_point=True)

        if not geocode_gdf.empty:
            self.__create_tiles_bounding_boxes()
            self.__add_lights_to_geocode(geocode, geocode_gdf, lat, lon, settings)

    def import_old_google_earth_decoder_tiles(self, settings):
        self.__import_old_google_earth_decoder_tiles(settings)

    def keep_common_tiles(self, project_to_compare):
        if self.objects_xml and project_to_compare.objects_xml:
            tiles_to_remove = self.__find_different_tiles(self.tiles, project_to_compare.tiles)
            for tile in tiles_to_remove:
                tile.remove_files()
            self.objects_xml.save()

    def __initialize(self, sources_path, init_structure, fast_init):
        self.__init_structure(sources_path, init_structure, fast_init)

        if not fast_init:
            self.__init_components()
            self.__guess_min_lod_level()
            self.__calculate_coords()

    def __init_structure(self, sources_path, init_structure, fast_init):
        if init_structure:
            self.project_definition_xml = self.project_name.capitalize() + XML_FILE_EXT
        if init_structure or not os.path.isfile(os.path.join(self.project_folder, self.project_definition_xml)):
            self.package_definitions_xml = self.author_name.lower() + "-" + self.project_definition_xml.lower()
        else:
            xml = MsfsProjectXml(self.project_folder, self.project_definition_xml)
            self.package_definitions_xml = basename(xml.definition_file)
        self.objects = dict()
        self.tiles = dict()
        self.shapes = dict()
        self.height_maps = dict()
        self.colliders = dict()
        self.light_models_path = os.path.join(sources_path, LIGHT_MODELS_FOLDER)

        if init_structure:
            try:
                # create the project folder if it does not exist
                os.makedirs(self.project_folder, exist_ok=True)
                # create the backup folder if it does not exist
                os.makedirs(self.backup_folder, exist_ok=True)
                # create the PackageSources folder if it does not exist
                os.makedirs(self.package_sources_folder, exist_ok=True)
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
            except:
                pass

        # rename project definition xml file folder if it exists
        old_project_definition_xml_path = os.path.join(self.project_folder, self.package_definitions_xml)
        self.project_definition_xml_path = os.path.join(self.project_folder, self.project_definition_xml)
        if os.path.isfile(old_project_definition_xml_path):
            os.rename(old_project_definition_xml_path, self.project_definition_xml_path)
        if init_structure:
            self.__create_project_file(sources_path, PROJECT_DEFINITION_TEMPLATE_PATH, self.project_definition_xml_path, True)

        # create package xml definition file if it does not exist
        self.package_definitions_xml_path = os.path.join(self.package_definitions_folder, self.package_definitions_xml)
        if init_structure:
            self.__create_project_file(sources_path, PACKAGE_DEFINITIONS_TEMPLATE_PATH, self.package_definitions_xml_path, True)

        # create business.json file if it does not exist
        self.business_json_path = os.path.join(self.business_json_folder, BUSINESS_JSON_TEMPLATE)
        if init_structure:
            self.__create_project_file(sources_path, BUSINESS_JSON_TEMPLATE_PATH, self.business_json_path, True)

        # create thumbnail file if it does not exist
        self.thumbnail_picture_path = os.path.join(self.content_info_folder, THUMBNAIL_PICTURE_TEMPLATE)
        if init_structure:
            self.__create_project_file(sources_path, THUMBNAIL_PICTURE_TEMPLATE_PATH, self.thumbnail_picture_path)

        self.model_lib_output_folder = self.__get_model_lib_output_folder()

        if not fast_init:
            try:
                # create the osm folder if it does not exist
                os.makedirs(self.osmfiles_folder, exist_ok=True)

                # create the shp folder if it does not exist
                os.makedirs(self.shpfiles_folder, exist_ok=True)

                # create the xml folder if it does not exist
                os.makedirs(self.xmlfiles_folder, exist_ok=True)

                # create the tiles folder if it does not exist
                os.makedirs(self.tilefiles_folder, exist_ok=True)
            except WindowsError:
                raise ScriptError("MSFS project folders creation is not possible")
            except:
                pass

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
                raise ScriptError("File copy not possible from " + sources_path + " to " + dest_file_path)

        if replace_content:
            replace_in_file(dest_file_path, self.DUMMY_STRING.capitalize(), self.project_name)
            replace_in_file(dest_file_path, self.DUMMY_STRING, self.project_name.lower())
            replace_in_file(dest_file_path, self.AUTHOR_STRING.capitalize(), self.author_name)
            replace_in_file(dest_file_path, self.AUTHOR_STRING, self.author_name.lower())

    def __retrieve_objects(self):
        self.__retrieve_scene_objects()
        self.__retrieve_shapes()
        self.__retrieve_height_maps()
        self.__retrieve_landmarks()

    def __retrieve_scene_objects(self):
        pbar = ProgressBar(list(Path(self.model_lib_folder).rglob(XML_FILE_PATTERN)), title="Retrieve project infos")
        for i, path in enumerate(pbar.iterable):
            if not is_octant(path.stem):
                msfs_scene_object = MsfsSceneObject(self.model_lib_folder, path.stem, path.name)
                if not self.objects_xml.find_scenery_objects(msfs_scene_object.xml.guid) and not self.objects_xml.find_scenery_objects_in_group(msfs_scene_object.xml.guid):
                    msfs_scene_object.remove_files()
                    pbar.update("%s" % path.name)
                    continue
                self.objects[msfs_scene_object.xml.guid] = msfs_scene_object
                pbar.update("%s" % path.name)
                continue

            if COLLIDER_SUFFIX in path.stem:
                msfs_collider = MsfsCollider(self.model_lib_folder, path.stem, path.name, self.objects_xml)
                if not self.objects_xml.find_scenery_objects(msfs_collider.xml.guid) and not self.objects_xml.find_scenery_objects_in_group(msfs_collider.xml.guid):
                    msfs_collider.remove_files()
                    pbar.update("%s" % path.name)
                    continue
                self.colliders[msfs_collider.xml.guid] = msfs_collider
                pbar.update("%s" % path.name)
                continue

            msfs_tile = MsfsTile(self.model_lib_folder, path.stem, path.name, self.objects_xml)
            if not self.objects_xml.find_scenery_objects(msfs_tile.xml.guid) and not self.objects_xml.find_scenery_objects_in_group(msfs_tile.xml.guid):
                msfs_tile.remove_files()
                pbar.update("%s" % path.name)
                continue
            if not msfs_tile.lods:
                msfs_tile.remove_files()
            else:
                self.tiles[msfs_tile.xml.guid] = msfs_tile
            pbar.update("%s" % path.name)

    def __retrieve_shapes(self):
        if self.objects_xml:
            self.shapes = {PITCH_TERRAFORM_POLYGONS_GROUP_DISPLAY_NAME: MsfsShapes(xml=self.objects_xml, group_display_name=PITCH_TERRAFORM_POLYGONS_GROUP_DISPLAY_NAME),
                           CONSTRUCTION_TERRAFORM_POLYGONS_GROUP_DISPLAY_NAME: MsfsShapes(xml=self.objects_xml, group_display_name=CONSTRUCTION_TERRAFORM_POLYGONS_GROUP_DISPLAY_NAME),
                           AMENITY_TERRAFORM_POLYGONS_GROUP_DISPLAY_NAME: MsfsShapes(xml=self.objects_xml, group_display_name=AMENITY_TERRAFORM_POLYGONS_GROUP_DISPLAY_NAME),
                           # GOLF_TERRAFORM_POLYGONS_DISPLAY_NAME: MsfsShapes(xml=self.objects_xml, group_display_name=GOLF_TERRAFORM_POLYGONS_DISPLAY_NAME),
                           EXCLUSION_BUILDING_POLYGONS_GROUP_DISPLAY_NAME: MsfsShapes(xml=self.objects_xml, group_display_name=EXCLUSION_BUILDING_POLYGONS_GROUP_DISPLAY_NAME),
                           EXCLUSION_VEGETATION_POLYGONS_GROUP_DISPLAY_NAME: MsfsShapes(xml=self.objects_xml, group_display_name=EXCLUSION_VEGETATION_POLYGONS_GROUP_DISPLAY_NAME)}

    def __retrieve_landmarks(self):
        if self.objects_xml:
            self.landmarks = MsfsLandmarks(xml=self.objects_xml)

    def __retrieve_height_maps(self):
        if self.objects_xml:
            self.height_maps = {HEIGHT_MAPS_GROUP_DISPLAY_NAME: MsfsHeightMaps(xml=self.objects_xml, group_display_name=HEIGHT_MAPS_GROUP_DISPLAY_NAME)}

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

    def __convert_tiles_textures(self, src_format, dest_format):
        textures = self.__retrieve_tiles_textures(src_format)

        if textures is None:
            return

        isolated_print(src_format.capitalize() + " texture files detected in the tiles of the project! Try to install Pillow lib, then convert them")
        install_python_lib("Pillow")

        pbar = ProgressBar(textures, title="CONVERT " + src_format.upper() + " TEXTURE FILES TO " + dest_format.upper())
        for texture in textures:
            file = texture.file
            if not texture.convert_format(src_format, dest_format):
                raise ScriptError("An error was detected while converting texture files in " + self.texture_folder + " ! Please convert them to " + dest_format + " format prior to launch the script, or remove them")
            else:
                pbar.update("%s converted to %s" % (file, dest_format))

    def __resize_tiles_textures(self, ratio):
        textures = []
        # when the original tiles are available in the backup, use them, otherwise use the current modified tiles (which give less accurate results than the original ones)
        backup_path = os.path.join(self.__find_backup_path(RESIZE_SCENERY_TEXTURES_BACKUP_FOLDER), TEXTURE_FOLDER)

        for tile in self.tiles.values():
            if not os.path.isdir(tile.folder):
                continue

            for lod in tile.lods:
                if not os.path.isdir(lod.folder):
                    continue

                for texture in lod.textures:
                    textures.append(texture)

        install_python_lib("Pillow")

        pbar = ProgressBar(textures, title="RESIZE TEXTURE FILES BY " + str(int(ratio*100)) + "%")
        for texture in textures:
            file = texture.file
            if not texture.resize(ratio, orig_folder=backup_path):
                raise ScriptError("An error was detected while resizing texture files in " + self.texture_folder)
            else:
                pbar.update("{} resized by {}%".format(file, int(ratio*100)))

    def __retrieve_tiles_textures(self, extension):
        textures = []
        for guid, tile in self.tiles.items():
            for lod in tile.lods: textures.extend([texture for texture in lod.textures if extension in texture.file])
        return textures

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

    def __calculate_coords(self):
        self.coords = tuple([0, 0, 0, 0])

        for tile in self.tiles.values():
            self.coords = tile.define_max_coords(self.coords)

        return self.coords

    def __optimization_needed(self):
        for tile in self.tiles.values():
            for lod in tile.lods:
                if not lod.optimized:
                    return True

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
                if tile.name != tile_candidate.name and tile.contains(tile_candidate.coords):
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

    def __retrieve_lods_to_optimize(self, nb_parallel_blender_tasks):
        data = []
        for tile in self.tiles.values():
            for lod in tile.lods:
                if not os.path.isdir(lod.folder):
                    continue

                if not lod.valid:
                    continue

                if lod.folder != self.model_lib_folder:
                    data.append({"name": lod.name, "params": ["--folder", str(lod.folder), "--model_file", str(lod.model_file), "--output_texture_format", str(self.settings.output_texture_format)]})

        return chunks(data, nb_parallel_blender_tasks)

    def __retrieve_tiles_to_calculate_height_map(self, nb_parallel_blender_tasks, new_group_id=-1, parallel=True, height_adjustment=0.0, high_precision=False):
        data = []

        for guid, tile in self.tiles.items():
            if not os.path.isdir(tile.folder):
                continue

            if not tile.valid:
                continue

            # if tile.name != "30604050607051455" and tile.name != "30604160614140752" and tile.name != "30604160614140773" and tile.name != "30604160614140770" and tile.name != "30604160614140650" and tile.name != "30604160614140453" and tile.name != "30604143504360660" and tile.name != "30604050607051672" and tile.name != "21615350715260724":
            #     continue

            ground_mask_file_path = os.path.join(self.osmfiles_folder, GROUND_OSM_KEY + "_" + EXCLUSION_OSM_FILE_PREFIX + "_" + tile.name + OSM_FILE_EXT)
            building_mask_file_path = os.path.join(self.osmfiles_folder, BUILDING_OSM_KEY + "_" + EXCLUSION_OSM_FILE_PREFIX + "_" + tile.name + OSM_FILE_EXT)
            rocks_mask_file_path = os.path.join(self.osmfiles_folder, ROCKS_OSM_KEY + "_" + EXCLUSION_OSM_FILE_PREFIX + "_" + tile.name + OSM_FILE_EXT)
            water_mask_file_path = os.path.join(self.osmfiles_folder, WATER_OSM_KEY + "_" + EXCLUSION_OSM_FILE_PREFIX + "_" + tile.name + OSM_FILE_EXT)
            has_mask_file = os.path.isfile(ground_mask_file_path) or os.path.isfile(rocks_mask_file_path) or os.path.isfile(water_mask_file_path)

            # when the original tiles are available in the backup, use them, otherwise use the current modified tiles (which give less accurate results than the original ones)
            backup_path = self.__find_backup_path(CLEANUP_3D_DATA_BACKUP_FOLDER)
            tile_folder = backup_path if os.path.isdir(backup_path) else tile.folder

            if not os.path.isdir(tile_folder):
                continue

            params = ["--folder", str(tile_folder), "--name", str(tile.name), "--definition_file", str(tile.definition_file),
                      "--height_map_xml_folder", str(self.xmlfiles_folder), "--group_id", str(new_group_id), "--altitude", str(tile.pos.alt), "--height_adjustment", str(height_adjustment)]

            if has_mask_file:
                params.extend(["--positioning_file_path", str(os.path.join(self.osmfiles_folder, BOUNDING_BOX_OSM_FILE_PREFIX + "_" + tile.name + OSM_FILE_EXT))])

            if os.path.isfile(ground_mask_file_path):
                params.extend(["--ground_mask_file_path", str(ground_mask_file_path)])

            if os.path.isfile(building_mask_file_path):
                params.extend(["--building_mask_file_path", str(building_mask_file_path)])

            if os.path.isfile(rocks_mask_file_path):
                params.extend(["--rocks_mask_file_path", str(rocks_mask_file_path)])

            if os.path.isfile(water_mask_file_path):
                params.extend(["--water_mask_file_path", str(water_mask_file_path)])

            params.extend(["--high_precision", str(high_precision)])
            data.append({"name": tile.name, "params": params})

        return chunks(data, nb_parallel_blender_tasks if parallel else 1)

    def __retrieve_lods_to_decimate(self, nb_parallel_blender_tasks):
        data = []
        for tile in self.tiles.values():
            for lod in tile.lods:
                if not os.path.isdir(lod.folder):
                    continue

                if not lod.valid:
                    continue

                data.append({"name": lod.name, "params": ["--folder", str(lod.folder), "--model_file", str(lod.model_file)]})

        return chunks(data, nb_parallel_blender_tasks)

    def __retrieve_lods_to_process(self, nb_parallel_blender_tasks, force_cleanup=False):
        data = []
        tiles = []

        # when the original tiles are available in the backup, use them, otherwise use the current modified tiles (which give less accurate results than the original ones)
        backup_path = self.__find_backup_path(CLEANUP_3D_DATA_BACKUP_FOLDER)

        for tile in self.tiles.values():
            if not os.path.isdir(tile.folder):
                continue

            if not tile.valid:
                continue

            mask_file_path = os.path.join(self.osmfiles_folder, EXCLUSION_OSM_FILE_PREFIX + "_" + tile.name + OSM_FILE_EXT)
            copy_lods = (not os.path.isfile(mask_file_path))
            has_mask_file = os.path.isfile(mask_file_path)

            collider = self.__get_tile_collider(tile.name)
            has_collider = (collider is not None)

            if has_collider:
                self.__remove_tile_collider(tile.name)
                tiles.append(tile)

            for lod in tile.lods:
                if not os.path.isdir(lod.folder):
                    continue

                if not lod.valid:
                    continue

                lod_folder = backup_path if os.path.isdir(backup_path) else lod.folder

                if not os.path.isdir(lod_folder):
                    continue

                if not lod.valid:
                    continue

                if lod.cleaned and not force_cleanup:
                    continue

                # if no mask file is present for this tile, this means that the tile will not be cleaned, so if it has been cleaned before,
                # we ensure to retrieve the previous one (i.e. the entire tile, if it exists in the backup path)
                if copy_lods:
                    shutil.copyfile(os.path.join(lod_folder, lod.model_file), os.path.join(lod.folder, lod.model_file))

                    for binary in lod.binaries:
                        shutil.copyfile(os.path.join(lod_folder, binary.file), os.path.join(binary.folder, binary.file))

                params = ["--folder", str(lod_folder), "--output_folder", str(lod.folder), "--model_file", str(lod.model_file),
                                                          "--positioning_file_path", str(os.path.join(self.osmfiles_folder, BOUNDING_BOX_OSM_FILE_PREFIX + "_" + tile.name + OSM_FILE_EXT))]

                if has_mask_file:
                    params.extend(["--mask_file_path", str(mask_file_path)])
                    data.append({"name": lod.name, "params": params})

        return tiles, chunks(data, nb_parallel_blender_tasks)

    def __retrieve_lods_to_exclude_3d_data_from_geocode(self, geocode, geocode_gdf, backup_subfolder, settings):
        data = []
        modified_tiles = []
        tiles_with_collider = []

        for tile in self.tiles.values():
            if not os.path.isdir(tile.folder):
                continue

            if not tile.valid:
                continue

            processed = clip_gdf(geocode_gdf, tile.bbox_gdf)
            if processed.empty:
                continue

            collider = self.__get_tile_collider(tile.name)
            has_collider = (collider is not None)

            if self.settings.backup_enabled:
                backup_path = os.path.join(os.path.join(self.backup_folder, backup_subfolder), geocode)
                tile.backup_files(backup_path)
                if has_collider:
                    collider.backup_files(backup_path)

            mask_file_path = os.path.join(self.osmfiles_folder, GEOCODE_OSM_FILE_PREFIX + "_" + EXCLUSION_OSM_FILE_PREFIX + OSM_FILE_EXT)

            if not os.path.isfile(mask_file_path):
                continue

            if has_collider:
                self.__remove_tile_collider(tile.name)
                tiles_with_collider.append(tile)

            for lod in tile.lods:
                if not os.path.isdir(lod.folder):
                    continue

                if not lod.valid:
                    continue

                params = ["--folder", str(lod.folder), "--output_folder", str(lod.folder), "--model_file", str(lod.model_file),
                                                          "--positioning_file_path", str(os.path.join(self.osmfiles_folder, BOUNDING_BOX_OSM_FILE_PREFIX + "_" + tile.name + OSM_FILE_EXT)),
                                                          "--mask_file_path", str(mask_file_path)]

                data.append({"name": lod.name, "params": params})
                modified_tiles.append(tile)

        if not data:
            pr_bg_orange("Geocode (" + geocode + ") found in OSM data, but not in the scenery" + EOL + CEND)

        return modified_tiles, tiles_with_collider, chunks(data, settings.nb_parallel_blender_tasks)

    def __retrieve_lods_to_isolate_3d_data_from_geocode(self, geocode, geocode_gdf, backup_subfolder, settings):
        data = []
        src_tiles = []

        for tile in self.tiles.values():
            if not os.path.isdir(tile.folder):
                continue

            if not tile.valid:
                continue

            processed = clip_gdf(geocode_gdf, tile.bbox_gdf)
            if processed.empty:
                continue

            if self.settings.backup_enabled:
                backup_path = os.path.join(os.path.join(self.backup_folder, backup_subfolder), geocode)
                tile.backup_files(backup_path)

            mask_file_path = os.path.join(self.osmfiles_folder, GEOCODE_OSM_FILE_PREFIX + "_" + EXCLUSION_OSM_FILE_PREFIX + OSM_FILE_EXT)

            if not os.path.isfile(mask_file_path):
                continue

            for lod in tile.lods:
                if not os.path.isdir(lod.folder):
                    continue

                if not lod.valid:
                    continue

                # when the original tiles are available in the backup, use them, otherwise use the current modified tiles (which give less accurate results than the original ones)
                backup_path = self.__find_backup_path(CLEANUP_3D_DATA_BACKUP_FOLDER)
                lod_folder = backup_path if os.path.isdir(backup_path) else lod.folder

                if not os.path.isdir(lod_folder):
                    continue

                params = ["--folder", str(lod_folder), "--output_folder", str(lod.folder), "--output_name", self.__get_geocode_file_prefix(geocode) + "_" + tile.name, "--model_file", str(lod.model_file),
                                                          "--positioning_file_path", str(os.path.join(self.osmfiles_folder, BOUNDING_BOX_OSM_FILE_PREFIX + "_" + tile.name + OSM_FILE_EXT)),
                                                          "--mask_file_path", str(mask_file_path)]

                data.append({"name": lod.name, "params": params})

            src_tiles.append(tile)

        if not data:
            pr_bg_orange("Geocode (" + geocode + ") found in OSM data, but not in the scenery" + EOL + CEND)

        return src_tiles, chunks(data, settings.nb_parallel_blender_tasks)

    def __retrieve_process_data_to_add_lights_to_geocode(self, geocode, geocode_gdf, lat, lon, settings):
        data = []
        positioning_files_paths = []
        model_files_paths = []
        alt = -9999.99
        mask_file_path = os.path.join(self.osmfiles_folder, GEOCODE_OSM_FILE_PREFIX + "_" + EXCLUSION_OSM_FILE_PREFIX + OSM_FILE_EXT)
        landmark_location_file_path = os.path.join(self.osmfiles_folder, LANDMARK_LOCATION_OSM_FILE_NAME + OSM_FILE_EXT)

        if not os.path.isfile(mask_file_path):
            return

        if not os.path.isfile(landmark_location_file_path):
            return

        for i, tile in enumerate(self.tiles.values()):
            if not os.path.isdir(tile.folder):
                continue

            if not tile.valid:
                continue

            processed = clip_gdf(geocode_gdf, tile.bbox_gdf)
            if processed.empty:
                continue

            if not tile.lods:
                continue

            lod_idx = 1
            if len(tile.lods) <= lod_idx:
                continue

            lod = tile.lods[lod_idx]

            if not os.path.isdir(lod.folder):
                continue

            if not lod.valid:
                continue

            # when the original tiles are available in the backup, use them, otherwise use the current modified tiles (which give less accurate results than the original ones)
            backup_path = self.__find_backup_path(CLEANUP_3D_DATA_BACKUP_FOLDER)
            lod_folder = backup_path if os.path.isdir(backup_path) else lod.folder

            if not os.path.isdir(lod_folder):
                continue

            alt = max(alt, tile.pos.alt)

            positioning_files_paths.append(str(os.path.join(self.osmfiles_folder, BOUNDING_BOX_OSM_FILE_PREFIX + "_" + tile.name + OSM_FILE_EXT)))
            model_files_paths.append(os.path.join(lod_folder, lod.model_file))

        prefix = geocode.split(",")

        if prefix:
            prefix = prefix[0]
            group_suffix = prefix.replace(" ", "_").replace("'", str())
        else:
            prefix = str()
            group_suffix = str()

        self.objects_xml.remove_lights(LIGHTS_GROUP_DISPLAY_NAME + "_" + group_suffix, True)
        new_group_id = self.objects_xml.get_new_group_id()

        params = ["--light_guid", self.settings.light_guid, "--positioning_files_paths", str('"') + "|".join(positioning_files_paths) + str('"'), "--model_files_paths", str('"') + "|".join(model_files_paths) + str('"'),
                  "--landmark_location_file_path", str('"') + landmark_location_file_path + str('"'), "--mask_file_path", str('"') + mask_file_path + str('"'), "--lat", str(lat), "--lon", str(lon), "--alt", str(alt),
                  "--geocode_prefix", str('"') + prefix + str('"'), "--scene_definition_file", str('"') + self.objects_xml.file_path + str('"'), "--group_id", str(new_group_id)]

        data.append({"name": "add_lights", "params": params})

        return chunks(data, settings.nb_parallel_blender_tasks)

    def __optimize_tile_lods(self, lods_data):
        self.__multithread_blender_process_data(lods_data, "optimize_tile_lod.py", "OPTIMIZE THE TILES", "optimized")

    def __merge_tiles(self, tiles, project_to_merge_name, tiles_to_merge, objects_xml_to_merge, project_to_merge):
        pbar = ProgressBar(tiles_to_merge.items(), title="MERGE THE TILES")
        self.__merge_objects(tiles, project_to_merge_name, objects_xml_to_merge, project_to_merge, pbar)

    def __merge_colliders(self, colliders, project_to_merge_name, colliders_to_merge, objects_xml_to_merge, project_to_merge):
        pbar = ProgressBar(colliders_to_merge.items(), title="MERGE THE COLLIDERS")
        self.__merge_objects(colliders, project_to_merge_name, objects_xml_to_merge, project_to_merge, pbar)

    def __merge_scene_objects(self, scene_objects, project_to_merge_name, scene_objects_to_merge, objects_xml_to_merge, project_to_merge):
        pbar = ProgressBar(scene_objects_to_merge.items(), title="MERGE THE OBJECTS")
        self.__merge_objects(scene_objects, project_to_merge_name, objects_xml_to_merge, project_to_merge, pbar)

    def __merge_objects(self, objects, project_to_merge_name, objects_xml_to_merge, project_to_merge, pbar):
        backup_objects_to_cleanup = False
        project_to_merge_backup_path = None
        project_to_merge_backup_texture_path = None
        backup_path = self.__find_backup_path(CLEANUP_3D_DATA_BACKUP_FOLDER)
        backup_texture_path = os.path.join(backup_path, TEXTURE_FOLDER)

        if os.path.isdir(backup_path) and project_to_merge is not None:
            backup_objects_to_cleanup = True
            project_to_merge_backup_path = project_to_merge.__find_backup_path()
            project_to_merge_backup_texture_path = os.path.join(project_to_merge_backup_path, TEXTURE_FOLDER)

        for guid, object in pbar.iterable:
            # copy or overwrite files
            add_guid = not os.path.isfile(os.path.join(self.model_lib_folder, object.definition_file))
            self.__copy_and_backup(object, object.definition_file, self.model_lib_folder, project_to_merge_backup_path, backup_path, backup_objects_to_cleanup, object.optimized, object.cleaned)

            for lod in object.lods:
                self.__copy_and_backup(lod, lod.model_file, self.model_lib_folder, project_to_merge_backup_path, backup_path, backup_objects_to_cleanup, object.optimized, object.cleaned)

                for binary in lod.binaries:
                    self.__copy_and_backup(binary, binary.file, self.model_lib_folder, project_to_merge_backup_path, backup_path, backup_objects_to_cleanup, object.optimized, object.cleaned)

                for texture in lod.textures:
                    self.__copy_and_backup(texture, texture.file, self.texture_folder, project_to_merge_backup_texture_path, backup_texture_path, backup_objects_to_cleanup, object.optimized, object.cleaned)

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

    def __retrieve_tiles_to_process(self, nb_parallel_blender_tasks, new_group_id=-1, parallel=True):
        data = []

        for tile in self.tiles.values():
            if os.path.isdir(tile.folder):
                data.append({"name": tile.name, "params": ["--folder", str(tile.folder), "--name", str(tile.name), "--definition_file", str(tile.definition_file), "--objects_xml_folder", str(self.scene_folder), "--objects_xml_file", str(self.SCENE_OBJECTS_FILE)]})

        return chunks(data, nb_parallel_blender_tasks)

    def __split_tiles(self, tiles_data):
        self.__multithread_blender_process_data(tiles_data, "split_tile.py", "SPLIT THE TILES", "splitted")

    def __replace_tiles_in_objects_xml(self, previous_tile, new_tiles):
        previous_guid = previous_tile.xml.guid

        for new_tile in new_tiles:
            self.__add_object_in_objects_xml(previous_guid, new_tile)

        # since we added the new tiles with minidom, we have to reload the xml file
        self.objects_xml = ObjectsXml(self.scene_folder, self.SCENE_OBJECTS_FILE)
        self.__remove_object(previous_tile)

    def __add_object_in_objects_xml(self, previous_guid, new_object):
        found_scenery_objects_parent, found_scenery_object = self.__find_scenery_objects_and_its_parents(self.objects_xml, previous_guid)
        add_scenery_object(self.objects_xml.file_path, new_object, found_scenery_object)

    def __remove_colliders(self):
        self.__remove_colliders_lod()
        pbar = ProgressBar(list(self.colliders.values()), title="REMOVE TILE COLLIDERS")
        for guid, collider in self.colliders.items():
            self.objects_xml.remove_object(guid)
            pbar.update("%s removed" % collider.name)
        self.__clean_objects(self.colliders)

    def __remove_tile_collider(self, tile_name):
        print_title("REMOVE " + tile_name + " COLLIDER")
        for guid, collider in self.colliders.items():
            if collider.name.replace(COLLIDER_SUFFIX, str()) == tile_name:
                self.objects_xml.remove_object(guid)
        self.__clean_objects(self.colliders)

    def __remove_colliders_lod(self):
        pbar = ProgressBar(list(self.tiles.values()), title="REMOVE COLLIDERS LODS")
        for guid, tile in self.tiles.items():
            tile.remove_collider_lod()
            pbar.update("%s removed" % tile.name)

    def __generate_height_map_data(self, settings):
        self.objects_xml.remove_height_maps(HEIGHT_MAPS_GROUP_DISPLAY_NAME, True)
        new_group_id = self.objects_xml.get_new_group_id()

        tiles_data = self.__retrieve_tiles_to_calculate_height_map(settings.nb_parallel_blender_tasks, new_group_id=new_group_id, parallel=True, height_adjustment=float(self.settings.height_adjustment), high_precision=self.settings.high_precision)
        self.__multithread_blender_process_data(tiles_data, "calculate_tile_height_data.py", "CALCULATE HEIGHT MAPS FOR EACH TILE", "height map calculated")
        self.__add_height_maps_to_objects_xml()

    def __add_height_maps_to_objects_xml(self):
        height_maps = None

        for tile in self.tiles.values():
            if os.path.isdir(tile.folder) and os.path.isfile(os.path.join(self.xmlfiles_folder, HEIGHT_MAP_PREFIX + tile.name + XML_FILE_EXT)):
                height_maps = MsfsHeightMaps(xml=HeightMapXml(self.xmlfiles_folder, HEIGHT_MAP_PREFIX + tile.name + XML_FILE_EXT))
                if height_maps:
                    self.objects_xml.add_height_map(height_maps.rectangles[0])

        if height_maps is not None:
            self.objects_xml.add_height_map_group(height_maps.rectangles[0])
        self.objects_xml.save()

    def __create_tiles_bounding_boxes(self, init_osm_folder=False):
        if init_osm_folder:
            # ensure to clean the xml folder containing the heightmaps data by removing it
            try:
                shutil.rmtree(self.osmfiles_folder)
            except:
                pass

            # create the osm folder if it does not exist
            os.makedirs(self.osmfiles_folder, exist_ok=True)

        valid_tiles = [tile for tile in list(self.tiles.values()) if tile.valid]
        pbar = ProgressBar(valid_tiles, title="CREATE BOUNDING BOX OSM FILES FOR EACH TILE")
        for i, tile in enumerate(valid_tiles):
            tile.create_bbox_osm_file(self.osmfiles_folder, self.min_lod_level)
            pbar.update("osm files created for %s tile" % tile.name)
            # gmd = MapBoxDownloader(tile.bbox_gdf.centroid.iloc[0].x, tile.bbox_gdf.centroid.iloc[0].y, self.min_lod_level)
            #
            # print("The tile coordinates are {}".format(gmd.get_xy()))
            # # Get the high resolution image
            # img = gmd.generate_image(target_folder=self.tilefiles_folder)
            #
            # # Save the image to disk
            # img.save(os.path.join(self.tilefiles_folder, tile.name + PNG_FILE_EXT))
            # print("The map has successfully been created")

    def __prepare_3d_data(self, settings, generate_height_data=False, process_3d_data=False, create_polygons=True, process_all=False):
        ox.config(overpass_endpoint=settings.overpass_api_uri, log_console=False, use_cache=False, log_level=lg.ERROR)

        # create bounding box data
        b = bbox_to_poly(self.coords[1], self.coords[0], self.coords[2], self.coords[3])
        orig_bbox = create_bounding_box_from_tiles(self.tiles)

        # retrieve_osm_data
        orig_water, orig_natural_water, bbox, roads, bridges, hidden_roads, sea, pitch, construction, airport, building, \
        water_without_bridges, water, exclusion, rocks, amenity, residential, industrial, forests, woods = self.__retrieve_osm_data(b, orig_bbox, settings)

        if create_polygons:
            self.__create_scenery_polygons(b, orig_bbox, orig_water, orig_natural_water, bbox, sea, pitch, amenity, construction, industrial, forests, woods, airport, exclusion, disable_terraform=self.settings.disable_terraform)

        if process_3d_data:
            if self.settings.isolate_3d_data:
                self.__create_exclusion_masks_from_tiles(b, orig_bbox.assign(building=BOUNDING_BOX_OSM_KEY), building_mask=resize_gdf(building, self.settings.building_margin), water_mask=water, construction_mask=construction if self.settings.keep_constructions else None, road_mask=roads if self.settings.keep_roads else None, bridges_mask=bridges if self.settings.keep_roads else None, hidden_roads=hidden_roads if self.settings.keep_roads else None, amenity_mask=amenity if self.settings.keep_roads else None, residential_mask=residential if self.settings.keep_residential_and_industrial else None, industrial_mask=industrial if self.settings.keep_residential_and_industrial else None, airport_mask=airport, rocks_mask=resize_gdf(rocks, self.settings.building_margin), file_prefix=EXCLUSION_OSM_FILE_PREFIX, title="CREATE EXCLUSION MASKS OSM FILES", process_all=process_all)
            else:
                self.__create_exclusion_masks_from_tiles(b, exclusion, building_mask=building, road_mask=roads if self.settings.keep_roads else None, bridges_mask=bridges if self.settings.keep_roads else None, hidden_roads=hidden_roads if self.settings.keep_roads else None, airport_mask=airport, rocks_mask=rocks, file_prefix=EXCLUSION_OSM_FILE_PREFIX, title="CREATE EXCLUSION MASKS OSM FILES", process_all=process_all)

        if generate_height_data:
            if self.settings.isolate_3d_data:
                self.__generate_isolated_height_data(b, construction, roads, bridges, hidden_roads, airport, building, water_without_bridges, orig_bbox.assign(building=BOUNDING_BOX_OSM_KEY), None, residential if self.settings.keep_residential_and_industrial else None, industrial if self.settings.keep_residential_and_industrial else None, rocks, keep_roads=self.settings.keep_roads, keep_residential_and_industrial=self.settings.keep_residential_and_industrial, keep_constructions=self.settings.keep_constructions, process_all=process_all)
            else:
                self.__generate_excluded_height_data(b, construction, roads, bridges, hidden_roads, airport, building, water_without_bridges, orig_bbox.assign(building=BOUNDING_BOX_OSM_KEY), resize_gdf(exclusion, self.settings.building_margin), rocks, keep_roads=self.settings.keep_roads, keep_constructions=self.settings.keep_constructions, process_all=process_all)

        # remove tiles that are completely in the water
        self.__remove_full_water_tiles(water)

    def __retrieve_osm_data(self, b, orig_bbox, settings):
        print_title("RETRIEVE OSM DATA")

        if not orig_bbox.empty:
            # for debugging purpose, generate the boundary osm file
            osm_xml = OsmXml(self.osmfiles_folder, BOUNDING_BOX_OSM_FILE_PREFIX + "_" + EXCLUSION_OSM_FILE_PREFIX + OSM_FILE_EXT)
            osm_xml.create_from_geodataframes([preserve_holes(orig_bbox.drop(labels=BOUNDARY_OSM_KEY, axis=1, errors='ignore'))], b)

        orig_land_mass, orig_boundary, orig_road, orig_railway, orig_sea, orig_landuse, orig_grass, orig_nature_reserve, \
        orig_natural, orig_natural_water, orig_water, orig_waterway, orig_aeroway, orig_pitch, orig_construction, orig_park, orig_building, \
        orig_wall, orig_man_made, orig_rocks, orig_amenity, orig_residential, orig_industrial, orig_airport = self.__load_geodataframes(settings, orig_bbox, b)

        bbox, roads, bridges, hidden_roads, sea, pitches, construction, airport, buildings, \
        water_without_bridges, water, exclusion, rocks, amenities, residentials, industrials, forests, woods = self.__prepare_geodataframes(orig_road, orig_railway, orig_sea, orig_bbox, orig_land_mass, orig_boundary,
                                                                                               orig_landuse, orig_natural, orig_natural_water, orig_water, orig_waterway, orig_aeroway,
                                                                                               orig_pitch, orig_construction, orig_airport, orig_building, orig_wall, orig_man_made,
                                                                                               orig_park, orig_nature_reserve, orig_rocks, orig_amenity, orig_residential, orig_industrial, settings)

        if not residentials.empty:
            print_title("CREATE RESIDENTIAL OSM FILE")
            # for debugging purpose, generate the residentials osm file
            osm_xml = OsmXml(self.osmfiles_folder, RESIDENTIAL_OSM_KEY + OSM_FILE_EXT)
            osm_xml.create_from_geodataframes([preserve_holes(residentials.drop(labels=BOUNDARY_OSM_KEY, axis=1, errors='ignore'))], b)

        if not industrials.empty:
            print_title("CREATE INDUSTRIAL OSM FILE")
            # for debugging purpose, generate the industrials osm file
            osm_xml = OsmXml(self.osmfiles_folder, INDUSTRIAL_OSM_KEY + OSM_FILE_EXT)
            osm_xml.create_from_geodataframes([preserve_holes(industrials.drop(labels=BOUNDARY_OSM_KEY, axis=1, errors='ignore'))], b)

        if not exclusion.empty:
            print_title("CREATE GLOBAL EXCLUSION OSM FILE")
            # for debugging purpose, generate the exclusion osm file
            osm_xml = OsmXml(self.osmfiles_folder, EXCLUSION_OSM_FILE_PREFIX + OSM_FILE_EXT)
            osm_xml.create_from_geodataframes([preserve_holes(exclusion.drop(labels=BOUNDARY_OSM_KEY, axis=1, errors='ignore'))], b, extrude=True, additional_tags=[(HEIGHT_OSM_TAG, 1000)])

        return orig_water, orig_natural_water, bbox, roads, bridges, hidden_roads, sea, pitches, construction, airport, buildings, \
               water_without_bridges, water, exclusion, rocks, amenities, residentials, industrials, forests, woods

    def __create_scenery_polygons(self, b, orig_bbox, orig_water, orig_natural_water, bbox, sea, pitch, amenity, construction, industrial, forests, woods, airport, exclusion, disable_terraform=False):
        forests_vegetation_polygons = create_empty_gdf()
        woods_vegetation_polygons = create_empty_gdf()

        print_title("CREATE PITCH TERRAFORM POLYGONS GEO DATAFRAMES...")
        pitch_terraform_polygons = create_terraform_polygons_gdf(pitch, exclusion)
        # for debugging purpose
        osm_xml = OsmXml(self.osmfiles_folder, "pitch_terraform_polygons" + OSM_FILE_EXT)
        osm_xml.create_from_geodataframes([pitch_terraform_polygons.drop(labels=BOUNDARY_OSM_KEY, axis=1, errors='ignore')], b)

        print_title("CREATE AMENITY TERRAFORM POLYGONS GEO DATAFRAMES...")
        amenity_terraform_polygons = create_terraform_polygons_gdf(amenity, exclusion)
        # for debugging purpose
        osm_xml = OsmXml(self.osmfiles_folder, "amenity_terraform_polygons" + OSM_FILE_EXT)
        osm_xml.create_from_geodataframes([amenity_terraform_polygons.drop(labels=BOUNDARY_OSM_KEY, axis=1, errors='ignore')], b)

        print_title("CREATE CONSTRUCTION TERRAFORM POLYGONS GEO DATAFRAMES...")
        construction_terraform_polygons = create_terraform_polygons_gdf(construction, exclusion)
        # for debugging purpose
        osm_xml = OsmXml(self.osmfiles_folder, "construction_terraform_polygons" + OSM_FILE_EXT)
        osm_xml.create_from_geodataframes([construction_terraform_polygons.drop(labels=BOUNDARY_OSM_KEY, axis=1, errors='ignore')], b)

        print_title("CREATE INDUSTRIAL TERRAFORM POLYGONS GEO DATAFRAMES...")
        industrial_terraform_polygons = create_terraform_polygons_gdf(industrial, exclusion)
        # for debugging purpose
        osm_xml = OsmXml(self.osmfiles_folder, "industrial_terraform_polygons" + OSM_FILE_EXT)
        osm_xml.create_from_geodataframes([industrial_terraform_polygons.drop(labels=BOUNDARY_OSM_KEY, axis=1, errors='ignore')], b)

        print_title("CREATE EXCLUSION BUILDINGS POLYGONS GEO DATAFRAMES...")
        exclusion_water = create_exclusion_water_gdf(orig_water, orig_natural_water, sea, bbox)
        exclusion_building_polygons = create_exclusion_building_polygons_gdf(orig_bbox, exclusion_water, airport)
        # for debugging purpose
        osm_xml = OsmXml(self.osmfiles_folder, "exclusion_building_polygons" + OSM_FILE_EXT)
        osm_xml.create_from_geodataframes([exclusion_building_polygons.drop(labels=BOUNDARY_OSM_KEY, axis=1, errors='ignore')], b)

        print_title("CREATE EXCLUSION VEGETATION POLYGONS GEO DATAFRAMES...")
        shore_water = create_shore_water_gdf(orig_water, orig_natural_water, sea, bbox)
        exclusion_vegetation_polygons = create_exclusion_vegetation_polygons_gdf(shore_water)
        # for debugging purpose
        osm_xml = OsmXml(self.osmfiles_folder, "exclusion_vegetation_polygons" + OSM_FILE_EXT)
        osm_xml.create_from_geodataframes([exclusion_vegetation_polygons.drop(labels=BOUNDARY_OSM_KEY, axis=1, errors='ignore')], b)

        if self.settings.create_forests_vegetation:
            print_title("CREATE FORESTS VEGETATION POLYGONS GEO DATAFRAMES...")
            exclusion_water = create_exclusion_vegetation_water_gdf(orig_water, orig_natural_water, sea, bbox)
            forests_vegetation_polygons = create_vegetation_polygons_gdf(forests, exclusion_water)
            # for debugging purpose
            osm_xml = OsmXml(self.osmfiles_folder, "forests_vegetation_polygons" + OSM_FILE_EXT)
            osm_xml.create_from_geodataframes([forests_vegetation_polygons.drop(labels=BOUNDARY_OSM_KEY, axis=1, errors='ignore')], b)

        if self.settings.create_woods_vegetation:
            print_title("CREATE WOODS VEGETATION POLYGONS GEO DATAFRAMES...")
            exclusion_water = create_exclusion_vegetation_water_gdf(orig_water, orig_natural_water, sea, bbox)
            woods_vegetation_polygons = create_vegetation_polygons_gdf(woods, exclusion_water)
            # for debugging purpose
            osm_xml = OsmXml(self.osmfiles_folder, "woods_vegetation_polygons" + OSM_FILE_EXT)
            osm_xml.create_from_geodataframes([woods_vegetation_polygons.drop(labels=BOUNDARY_OSM_KEY, axis=1, errors='ignore')], b)

        new_group_id = self.objects_xml.get_new_group_id()
        if not exclusion_building_polygons.empty:
            self.shapes[EXCLUSION_BUILDING_POLYGONS_GROUP_DISPLAY_NAME] = MsfsShapes(shape_gdf=exclusion_building_polygons, group_display_name=EXCLUSION_BUILDING_POLYGONS_GROUP_DISPLAY_NAME, group_id=new_group_id, name_prefix=EXCLUSION_BUILDING_POLYGON_NAME_PREFIX, exclude_buildings=True)
        if not exclusion_vegetation_polygons.empty:
            self.shapes[EXCLUSION_VEGETATION_POLYGONS_GROUP_DISPLAY_NAME] = MsfsShapes(shape_gdf=exclusion_vegetation_polygons, group_display_name=EXCLUSION_VEGETATION_POLYGONS_GROUP_DISPLAY_NAME, group_id=new_group_id + 1, name_prefix=EXCLUSION_VEGETATION_POLYGON_NAME_PREFIX, exclude_vegetation=True, exclude_buildings=True)
        if not pitch_terraform_polygons.empty:
            self.shapes[PITCH_TERRAFORM_POLYGONS_GROUP_DISPLAY_NAME] = MsfsShapes(shape_gdf=pitch_terraform_polygons, group_display_name=PITCH_TERRAFORM_POLYGONS_GROUP_DISPLAY_NAME, group_id=new_group_id + 2, name_prefix=PITCH_TERRAFORM_POLYGON_NAME_PREFIX, tiles=self.tiles, flatten=not disable_terraform)
        if not amenity_terraform_polygons.empty:
            self.shapes[AMENITY_TERRAFORM_POLYGONS_GROUP_DISPLAY_NAME] = MsfsShapes(shape_gdf=amenity_terraform_polygons, group_display_name=AMENITY_TERRAFORM_POLYGONS_GROUP_DISPLAY_NAME, group_id=new_group_id + 3, name_prefix=AMENITY_TERRAFORM_POLYGON_NAME_PREFIX, tiles=self.tiles, flatten=not disable_terraform)
        if not construction_terraform_polygons.empty:
            self.shapes[CONSTRUCTION_TERRAFORM_POLYGONS_GROUP_DISPLAY_NAME] = MsfsShapes(shape_gdf=construction_terraform_polygons, group_display_name=CONSTRUCTION_TERRAFORM_POLYGONS_GROUP_DISPLAY_NAME, group_id=new_group_id + 4, name_prefix=CONSTRUCTION_TERRAFORM_POLYGON_NAME_PREFIX, tiles=self.tiles, flatten=False)
        if not industrial_terraform_polygons.empty:
            self.shapes[INDUSTRIAL_TERRAFORM_POLYGONS_GROUP_DISPLAY_NAME] = MsfsShapes(shape_gdf=industrial_terraform_polygons, group_display_name=INDUSTRIAL_TERRAFORM_POLYGONS_GROUP_DISPLAY_NAME, group_id=new_group_id + 5, name_prefix=INDUSTRIAL_TERRAFORM_POLYGON_NAME_PREFIX, tiles=self.tiles, flatten=False)
        if not forests_vegetation_polygons.empty:
            self.shapes[FORESTS_VEGETATION_POLYGONS_GROUP_DISPLAY_NAME] = MsfsShapes(shape_gdf=forests_vegetation_polygons, group_display_name=FORESTS_VEGETATION_POLYGONS_GROUP_DISPLAY_NAME, group_id=new_group_id + 6, name_prefix=FORESTS_VEGETATION_POLYGON_NAME_PREFIX, tiles=self.tiles, create_vegetation=True)
        if not woods_vegetation_polygons.empty:
            self.shapes[WOODS_VEGETATION_POLYGONS_GROUP_DISPLAY_NAME] = MsfsShapes(shape_gdf=woods_vegetation_polygons, group_display_name=WOODS_VEGETATION_POLYGONS_GROUP_DISPLAY_NAME, group_id=new_group_id + 7, name_prefix=WOODS_VEGETATION_POLYGON_NAME_PREFIX, tiles=self.tiles, create_vegetation=True)

        # reload the xml file to retrieve the last updates
        self.objects_xml = ObjectsXml(self.scene_folder, self.SCENE_OBJECTS_FILE)
        for group_name, shape in self.shapes.items():
            shape.remove_from_xml(self.objects_xml, group_name)
            shape.to_xml(self.objects_xml)

    def __generate_isolated_height_data(self, b, construction, roads, bridges, hidden_roads, airport, building, water, exclusion, amenity, residential, industrial, rocks, keep_roads=False, keep_residential_and_industrial=False, keep_constructions=False, process_all=False):
        self.__create_exclusion_masks_from_tiles(b, exclusion, building_mask=building, construction_mask=construction if keep_constructions else None, road_mask=roads if keep_roads else None, bridges_mask=bridges if keep_roads else None, hidden_roads=hidden_roads if keep_roads else None, amenity_mask=resize_gdf(amenity, -4) if keep_roads else None, residential_mask=residential if keep_residential_and_industrial else None, industrial_mask=industrial if keep_residential_and_industrial else None, airport_mask=airport, file_prefix=GROUND_OSM_KEY + "_" + EXCLUSION_OSM_FILE_PREFIX, title="CREATE GROUND EXCLUSION MASKS OSM FILES", process_all=process_all)
        self.__create_exclusion_masks_from_tiles(b, resize_gdf(building, -10), construction_mask=construction if keep_constructions else None, residential_mask=residential if keep_residential_and_industrial else None, industrial_mask=industrial if keep_residential_and_industrial else None, airport_mask=airport, file_prefix=BUILDING_OSM_KEY + "_" + EXCLUSION_OSM_FILE_PREFIX, title="CREATE BUILDING EXCLUSION MASKS OSM FILES", process_all=process_all)
        self.__create_exclusion_masks_from_tiles(b, exclusion, rocks_mask=resize_gdf(rocks, -5), file_prefix=ROCKS_OSM_KEY + "_" + EXCLUSION_OSM_FILE_PREFIX, title="CREATE ROCKS EXCLUSION MASKS OSM FILES", process_all=process_all)
        self.__create_exclusion_masks_from_tiles(b, resize_gdf(water, 10), keep_holes=False, file_prefix=WATER_OSM_KEY + "_" + EXCLUSION_OSM_FILE_PREFIX, title="CREATE WATER EXCLUSION MASKS OSM FILES", process_all=process_all)

    def __generate_excluded_height_data(self, b, construction, roads, bridges, hidden_roads, airport, building, water, bbox, exclusion, rocks, keep_roads=False, keep_constructions=False, process_all=False):
        self.__create_exclusion_masks_from_tiles(b, exclusion, building_mask=building, construction_mask=construction if keep_constructions else None, road_mask=roads if keep_roads else None, bridges_mask=bridges if keep_roads else None, hidden_roads=hidden_roads if keep_roads else None, airport_mask=airport, file_prefix=GROUND_OSM_KEY + "_" + EXCLUSION_OSM_FILE_PREFIX, title="CREATE GROUND EXCLUSION MASKS OSM FILES", process_all=process_all)
        self.__create_exclusion_masks_from_tiles(b, resize_gdf(building, -10), construction_mask=construction if keep_constructions else None, airport_mask=airport, file_prefix=BUILDING_OSM_KEY + "_" + EXCLUSION_OSM_FILE_PREFIX, title="CREATE BUILDING EXCLUSION MASKS OSM FILES", process_all=process_all)
        self.__create_exclusion_masks_from_tiles(b, bbox, rocks_mask=resize_gdf(rocks, -5), file_prefix=ROCKS_OSM_KEY + "_" + EXCLUSION_OSM_FILE_PREFIX, title="CREATE ROCKS EXCLUSION MASKS OSM FILES", process_all=process_all)
        self.__create_exclusion_masks_from_tiles(b, resize_gdf(water, 10), keep_holes=False, file_prefix=WATER_OSM_KEY + "_" + EXCLUSION_OSM_FILE_PREFIX, title="CREATE WATER EXCLUSION MASKS OSM FILES", process_all=process_all)

    def __create_exclusion_masks_from_tiles(self, b, exclusion_mask, building_mask=None, water_mask=None, construction_mask=None, road_mask=None, bridges_mask=None, hidden_roads=None, amenity_mask=None, residential_mask=None, industrial_mask=None, airport_mask=None, rocks_mask=None, keep_holes=True, file_prefix="", title="CREATE EXCLUSION MASKS OSM FILES", process_all=False):
        valid_tiles = [tile for tile in list(self.tiles.values()) if tile.valid]

        if not process_all:
            valid_tiles = [tile for tile in valid_tiles if not tile.cleaned]

        if construction_mask is not None:
            if not construction_mask.empty:
                construction_mask = construction_mask.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)

        if road_mask is not None:
            if not road_mask.empty:
                road_mask = road_mask.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)

        if hidden_roads is not None:
            if not hidden_roads.empty:
                hidden_roads.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)

        if bridges_mask is not None:
            if not bridges_mask.empty:
                bridges_mask = bridges_mask.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)

        if amenity_mask is not None:
            if not amenity_mask.empty:
                amenity_mask = amenity_mask.dissolve().assign(boundary=BOUNDING_BOX_OSM_KEY)

        pbar = ProgressBar(valid_tiles, title=title)
        exclusion = exclusion_mask.copy()

        for i, tile in enumerate(valid_tiles):
            # if tile.name != "30604050607051455" and tile.name != "30604160614140752" and tile.name != "30604160614140773" and tile.name != "30604160614140770" and tile.name != "30604160614140650" and tile.name != "30604160614140453" and tile.name != "30604143504360660" and tile.name != "30604050607051672" and tile.name != "21615350715260724":
            #     continue

            tile.create_exclusion_mask_osm_file(self.osmfiles_folder, b, exclusion, building_mask, water_mask, construction_mask, road_mask, bridges_mask, hidden_roads, amenity_mask, residential_mask, industrial_mask, airport_mask, rocks_mask, keep_holes, file_prefix)
            pbar.update("exclusion mask created for %s tile" % tile.name)

    def __load_geodataframes(self, settings, orig_bbox, b):
        # load all necessary GeoPandas Dataframes
        load_gdf_list = [None] * 24
        pbar = ProgressBar(load_gdf_list, title="RETRIEVE GEODATAFRAMES (THE FIRST TIME, MAY TAKE SOME TIME TO COMPLETE, BE PATIENT...)", sleep=0.0)
        pbar.update("retrieving land mass geodataframe...", stall=True)
        orig_land_mass = create_land_mass_gdf(self.sources_folder, orig_bbox, b)
        pbar.update("land mass geodataframe retrieved")
        pbar.update("retrieving boundary geodataframe...", stall=True)
        orig_boundary = load_gdf(self.coords, BOUNDARY_OSM_KEY, True, shp_file_path=os.path.join(self.shpfiles_folder, BOUNDARY_OSM_KEY + SHP_FILE_EXT))
        pbar.update("boundary geodataframe retrieved")
        pbar.update("retrieving roads geodataframe...", stall=True)
        orig_road = load_gdf(self.coords, ROAD_OSM_KEY, True, shp_file_path=os.path.join(self.shpfiles_folder, ROAD_OSM_KEY + SHP_FILE_EXT), is_roads=True)
        pbar.update("roads geodataframe retrieved")
        pbar.update("retrieving railways geodataframe...", stall=True)
        orig_railway = load_gdf(self.coords, RAILWAY_OSM_KEY, True, shp_file_path=os.path.join(self.shpfiles_folder, RAILWAY_OSM_KEY + SHP_FILE_EXT), is_roads=True)
        pbar.update("railways geodataframe retrieved")
        pbar.update("retrieving sea geodataframe...", stall=True)
        orig_sea = load_gdf(self.coords, BOUNDARY_OSM_KEY, True, shp_file_path=os.path.join(self.shpfiles_folder, SEA_OSM_TAG + SHP_FILE_EXT), is_sea=True, land_mass=orig_land_mass, bbox=orig_bbox)
        pbar.update("sea geodataframe retrieved")
        pbar.update("retrieving landuses geodataframe...", stall=True)
        orig_landuse = load_gdf(self.coords, LANDUSE_OSM_KEY, OSM_TAGS[LANDUSE_OSM_KEY], shp_file_path=os.path.join(self.shpfiles_folder, LANDUSE_OSM_KEY + SHP_FILE_EXT))
        pbar.update("landuses geodataframe retrieved")
        pbar.update("retrieving grass geodataframe...", stall=True)
        orig_grass = load_gdf(self.coords, LANDUSE_OSM_KEY, OSM_TAGS[GRASS_OSM_KEY], shp_file_path=os.path.join(self.shpfiles_folder, GRASS_OSM_KEY + SHP_FILE_EXT), is_grass=True)
        pbar.update("grass geodataframe retrieved")
        pbar.update("retrieving nature reserves geodataframe...", stall=True)
        orig_nature_reserve = load_gdf(self.coords, LEISURE_OSM_KEY, OSM_TAGS[LEISURE_OSM_KEY], shp_file_path=os.path.join(self.shpfiles_folder, NATURE_RESERVE_OSM_TAG + SHP_FILE_EXT))
        pbar.update("nature reserves geodataframe retrieved")
        pbar.update("retrieving other naturals geodataframe...", stall=True)
        orig_natural = load_gdf(self.coords, NATURAL_OSM_KEY, OSM_TAGS[NATURAL_OSM_KEY], shp_file_path=os.path.join(self.shpfiles_folder, NATURAL_OSM_KEY + SHP_FILE_EXT))
        pbar.update("other naturals geodataframe retrieved")
        pbar.update("retrieving waters geodataframe...", stall=True)
        orig_natural_water = load_gdf(self.coords, NATURAL_OSM_KEY, OSM_TAGS[NATURAL_WATER_OSM_KEY], shp_file_path=os.path.join(self.shpfiles_folder, NATURAL_WATER_OSM_KEY + SHP_FILE_EXT))
        pbar.update("natural waters geodataframe retrieved")
        pbar.update("retrieving other waters geodataframe...", stall=True)
        orig_water = load_gdf(self.coords, WATER_OSM_KEY, OSM_TAGS[WATER_OSM_KEY], shp_file_path=os.path.join(self.shpfiles_folder, WATER_OSM_KEY + SHP_FILE_EXT))
        pbar.update("other waters geodataframe retrieved")
        pbar.update("retrieving waterways geodataframe...", stall=True)
        orig_waterway = load_gdf(self.coords, WATERWAY_OSM_KEY, OSM_TAGS[WATERWAY_OSM_KEY], shp_file_path=os.path.join(self.shpfiles_folder, WATERWAY_OSM_KEY + SHP_FILE_EXT), is_waterway=True)
        pbar.update("waterways geodataframe retrieved")
        pbar.update("retrieving aeroways geodataframe...", stall=True)
        orig_aeroway = load_gdf(self.coords, AEROWAY_OSM_KEY, True, shp_file_path=os.path.join(self.shpfiles_folder, AEROWAY_OSM_KEY + SHP_FILE_EXT))
        pbar.update("aeroways geodataframe retrieved")
        pbar.update("retrieving pitches geodataframe...", stall=True)
        orig_pitch = load_gdf(self.coords, LEISURE_OSM_KEY, OSM_TAGS[PITCH_OSM_KEY], shp_file_path=os.path.join(self.shpfiles_folder, PITCH_OSM_KEY + SHP_FILE_EXT))
        pbar.update("pitches geodataframe retrieved")
        pbar.update("retrieving constructions geodataframe...", stall=True)
        orig_construction = load_gdf(self.coords, LANDUSE_OSM_KEY, OSM_TAGS[CONSTRUCTION_OSM_KEY], shp_file_path=os.path.join(self.shpfiles_folder, CONSTRUCTION_OSM_KEY + SHP_FILE_EXT))
        pbar.update("constructions geodataframe retrieved")
        pbar.update("retrieving parks geodataframe...", stall=True)
        orig_park = load_gdf(self.coords, LEISURE_OSM_KEY, OSM_TAGS[PARK_OSM_KEY], shp_file_path=os.path.join(self.shpfiles_folder, PARK_OSM_KEY + SHP_FILE_EXT))
        pbar.update("parks geodataframe retrieved")
        pbar.update("retrieving buildings geodataframe...", stall=True)
        orig_building = load_gdf(self.coords, BUILDING_OSM_KEY, True, shp_file_path=os.path.join(self.shpfiles_folder, BUILDING_OSM_KEY + SHP_FILE_EXT))
        pbar.update("buildings geodataframe retrieved")
        pbar.update("retrieving walls geodataframe...", stall=True)
        orig_wall = load_gdf(self.coords, BARRIER_OSM_KEY, OSM_TAGS[BARRIER_OSM_KEY], shp_file_path=os.path.join(self.shpfiles_folder, WALL_OSM_TAG + SHP_FILE_EXT), is_wall=True)
        pbar.update("walls geodataframe retrieved")
        pbar.update("retrieving man mades geodataframe...", stall=True)
        orig_man_made = load_gdf(self.coords, MAN_MADE_OSM_KEY, OSM_TAGS[MAN_MADE_OSM_KEY], shp_file_path=os.path.join(self.shpfiles_folder, MAN_MADE_OSM_KEY + SHP_FILE_EXT))
        pbar.update("man mades geodataframe retrieved")
        pbar.update("retrieving rocks geodataframe...", stall=True)
        orig_rocks = load_gdf(self.coords, NATURAL_OSM_KEY, OSM_TAGS[ROCKS_OSM_KEY], shp_file_path=os.path.join(self.shpfiles_folder, ROCKS_OSM_KEY + SHP_FILE_EXT))
        pbar.update("rocks geodataframe retrieved")
        pbar.update("retrieving amenity geodataframe...", stall=True)
        orig_amenity = load_gdf(self.coords, AMENITY_OSM_KEY, True, shp_file_path=os.path.join(self.shpfiles_folder, AMENITY_OSM_KEY + SHP_FILE_EXT))
        pbar.update("amenity geodataframe retrieved")
        pbar.update("retrieving residential geodataframe...", stall=True)
        orig_residential = load_gdf(self.coords, LANDUSE_OSM_KEY, OSM_TAGS[RESIDENTIAL_OSM_KEY], shp_file_path=os.path.join(self.shpfiles_folder, RESIDENTIAL_OSM_KEY + SHP_FILE_EXT))
        pbar.update("residential geodataframe retrieved")
        pbar.update("retrieving industrial geodataframe...", stall=True)
        orig_industrial = load_gdf(self.coords, LANDUSE_OSM_KEY, OSM_TAGS[INDUSTRIAL_OSM_KEY], shp_file_path=os.path.join(self.shpfiles_folder, INDUSTRIAL_OSM_KEY + SHP_FILE_EXT))
        pbar.update("industrial geodataframe retrieved")
        pbar.update("retrieving airports geodataframe...", stall=True)
        orig_airport = load_gdf_from_geocode(AIRPORT_GEOCODE + ", " + self.settings.airport_city.lower(), settings.overpass_api_uri, shpfiles_folder=self.shpfiles_folder, coords=self.coords, keep_data=True, display_warnings=False)
        pbar.update("airports geodataframe retrieved")

        return orig_land_mass, orig_boundary, orig_road, orig_railway, orig_sea, orig_landuse, orig_grass, orig_nature_reserve, \
               orig_natural, orig_natural_water, orig_water, orig_waterway, orig_aeroway, orig_pitch, orig_construction, orig_park, orig_building, \
               orig_wall, orig_man_made, orig_rocks, orig_amenity, orig_residential, orig_industrial, orig_airport

    def __create_geocode_osm_exclusion_files(self, geocode, settings, b, geocode_margin, preserve_roads, preserve_buildings, coords, shpfiles_folder):
        print_title("RETRIEVE GEOCODE OSM FILES")

        geocode_gdf = load_gdf_from_geocode(geocode, settings.overpass_api_uri, geocode_margin=geocode_margin, preserve_roads=preserve_roads, preserve_buildings=preserve_buildings, coords=coords, shpfiles_folder=shpfiles_folder)

        if geocode_gdf is None:
            return geocode_gdf

        if not geocode_gdf.empty:
            # for debugging purpose, generate the osm file
            osm_xml = OsmXml(self.osmfiles_folder, GEOCODE_OSM_FILE_PREFIX + "_" + EXCLUSION_OSM_FILE_PREFIX + OSM_FILE_EXT)
            osm_xml.create_from_geodataframes([preserve_holes(geocode_gdf)], b, extrude=True, additional_tags=[(HEIGHT_OSM_TAG, 3000)])

        return geocode_gdf

    def __remove_full_water_tiles(self, water):
        tiles_to_remove = []
        valid_tiles = [tile for tile in list(self.tiles.values()) if tile.valid]
        for tile in valid_tiles:
            not_in_water = difference_gdf(tile.bbox_gdf, water)
            if not_in_water.empty:
                tiles_to_remove.append(tile)

        pbar = ProgressBar(tiles_to_remove, title="REMOVE TILES THAT COVER ONLY WATER")
        for tile in tiles_to_remove:
            tile.remove_files()
            pbar.update("%s removed" % tile.name)

    def __create_geocode_osm_files(self, geocode, settings, preserve_roads, preserve_buildings, coords, shpfiles_folder):
        ox.config(overpass_endpoint=settings.overpass_api_uri, log_console=False, use_cache=False, log_level=lg.ERROR)
        return self.__create_geocode_osm_exclusion_files(geocode, settings, bbox_to_poly(self.coords[1], self.coords[0], self.coords[2], self.coords[3]), float(self.settings.geocode_margin), preserve_roads, preserve_buildings, coords, shpfiles_folder)

    def __reduce_number_of_vertices(self, nb_parallel_blender_tasks):
        lods_data = self.__retrieve_lods_to_decimate(nb_parallel_blender_tasks)
        self.__multithread_blender_process_data(lods_data, "reduce_lod_number_of_vertices.py", "REDUCE THE NUMBER OF VERTICES FOR ALL TILE LODS", "number of vertices reduced")

    def __process_lods_3d_data(self, nb_parallel_blender_tasks, process_all=False):
        tiles_with_collider, lods_data = self.__retrieve_lods_to_process(nb_parallel_blender_tasks, force_cleanup=process_all)
        self.__multithread_blender_process_data(lods_data, "cleanup_lod_3d_data.py", "CLEAN LODS 3D DATA TILES", "cleaned")
        for tile in tiles_with_collider:
            for lod in tile.lods:
                lod.remove_road_and_collision_tags()
            tile.add_collider()

    def __exclude_lods_3d_data_from_geocode(self, geocode, geocode_gdf, settings):
        modified_tiles, tiles_with_collider, lods_data = self.__retrieve_lods_to_exclude_3d_data_from_geocode(geocode, geocode_gdf, "exclude_3d_data_from_geocode", settings)
        self.__multithread_blender_process_data(lods_data, "cleanup_lod_3d_data.py", "EXCLUDE LODS 3D DATA TILES FROM GEOCODE", "excluded")
        for tile in tiles_with_collider:
            for lod in tile.lods:
                lod.remove_road_and_collision_tags()
            tile.add_collider()
        lods = [lod for tile in modified_tiles for lod in tile.lods]
        pbar = ProgressBar(list(lods), title="PREPARE THE TILES FOR MSFS")
        for lod in lods:
            lod.optimization_in_progress = False
            lod.prepare_for_msfs()
            pbar.update("%s prepared for msfs" % lod.name)

    def __isolate_lods_3d_data_from_geocode(self, geocode, geocode_gdf, settings):
        new_tiles = []
        src_tiles, lods_data = self.__retrieve_lods_to_isolate_3d_data_from_geocode(geocode, geocode_gdf, "isolate_3d_data_from_geocode", settings)
        self.__multithread_blender_process_data(lods_data, "isolate_lod_3d_data.py", "ISOLATE LODS 3D DATA TILES FROM GEOCODE", "isolated")

        for tile in src_tiles:
            new_tile = tile
            new_tile.name = self.__get_geocode_file_prefix(geocode) + "_" + tile.name
            new_tile.definition_file = new_tile.name + XML_FILE_EXT
            new_tile.xml.file_path = os.path.join(new_tile.folder, new_tile.definition_file)

            if os.path.exists(new_tile.xml.file_path):
                return

            new_tile.xml.guid = "{" + str(new_tile.generate_guid()) + "}"
            new_tile.xml.root.set(new_tile.xml.GUID_ATTR, new_tile.xml.guid)
            new_tile.xml.save()

            for lod in new_tile.lods:
                new_lod_name = self.__get_geocode_file_prefix(geocode) + "_" + lod.name
                replace_in_file(new_tile.xml.file_path, lod.name, new_lod_name)
                lod.name = new_lod_name
                lod.model_file = new_lod_name + GLTF_FILE_EXT

            new_tile.to_xml(self.objects_xml, new_tile.xml.guid)

        lods = [lod for tile in new_tiles for lod in tile.lods]
        pbar = ProgressBar(list(lods), title="PREPARE THE TILES FOR MSFS")
        for lod in lods:
            lod.optimization_in_progress = False
            lod.prepare_for_msfs()
            pbar.update("%s prepared for msfs" % lod.name)

    def __create_landmark_from_geocode(self, geocode, settings, coords):
        ox.config(overpass_endpoint=settings.overpass_api_uri, log_console=False, use_cache=False, log_level=lg.ERROR)
        alt = 0.0

        print_title("RETRIEVE OSM GEOCODE DATA")
        geocode_gdf = load_gdf_from_geocode(geocode, settings.overpass_api_uri, coords=coords, keep_data=True, shpfiles_folder=self.shpfiles_folder)

        if geocode_gdf.empty:
            return

        # self.__create_tiles_bounding_boxes()
        #
        # for tile in self.tiles.values():
        #     if tile.valid:
        #         processed = clip_gdf(geocode_gdf, tile.bbox_gdf)
        #         if not processed.empty:
        #             alt = tile.pos.alt

        print_title("WRITE LANDMARK TO SCENERY XML FILE")
        landmarks = MsfsLandmarks(geocode_gdf=geocode_gdf, tiles=self.tiles, owner=settings.author_name, type=self.settings.landmark_type, alt=alt, offset=self.settings.landmark_offset)

        for landmark_location in landmarks.landmark_locations:
            # if a landmark has a correct altitude, it is valid
            if landmark_location.is_in_tiles:
                self.objects_xml.remove_landmarks(name=landmark_location.name)
                landmark_location.to_xml(self.objects_xml)
            else:
                pr_bg_orange("Geocode (" + geocode + ") found in OSM data, but not in the scenery" + EOL + CEND)

    def __add_lights_to_geocode(self, geocode, geocode_gdf, lat, lon, settings):
        try:
            shutil.copytree(self.light_models_path, self.model_lib_folder, dirs_exist_ok=True)
        except WindowsError:
            raise ScriptError("File copy not possible from " + self.light_models_path + " to " + self.model_lib_folder)

        process_data = self.__retrieve_process_data_to_add_lights_to_geocode(geocode, geocode_gdf, lat, lon, settings)
        self.__multithread_blender_process_data(process_data, "add_lights.py", "ADD LIGHTS TO GEOCODE", "lights created")

    def __import_old_google_earth_decoder_tiles(self, settings):
        obj_files = [model_file for model_file in Path(settings.decoder_output_path).glob(OBJ_FILE_PATTERN)]
        if not obj_files:
            return

        lod_levels = self.__guess_lods_from_obj_files(obj_files)

        if not lod_levels: return

        min_lod = lod_levels[0]
        depth = len(lod_levels)
        objects_xml_path = os.path.join(self.scene_folder, self.SCENE_OBJECTS_FILE)

        if os.path.isfile(objects_xml_path):
            os.remove(objects_xml_path)
            print(objects_xml_path, "removed")

        self.objects_xml = ObjectsXml(self.scene_folder, self.SCENE_OBJECTS_FILE)

        pbar = ProgressBar(obj_files, title="CONVERT THE DECODED GOOGLE EARTH TILES TO GLTF")
        for obj_file in pbar.iterable:
            obj_file_name = os.path.basename(obj_file).replace(OBJ_FILE_EXT, str())

            if len(obj_file_name) == min_lod:
                alt = 0.0
                from blender.scene import convert_obj_file_to_gltf_file
                convert_obj_file_to_gltf_file(obj_file, self.model_lib_folder, TEXTURE_FOLDER, depth)
                create_new_definition_file(os.path.join(self.model_lib_folder, obj_file_name + XML_FILE_EXT))
                xml = MsfsObjectXml(self.model_lib_folder, obj_file_name + XML_FILE_EXT)
                tile = MsfsTile(self.model_lib_folder, obj_file_name, obj_file_name + XML_FILE_EXT)

                for lod in tile.lods:
                    add_new_lod(xml.file_path, lod.model_file, lod.min_size)
                    lod.prepare_for_msfs()

                # reinitialize the tile to get the updated lod definitions
                tile = MsfsTile(self.model_lib_folder, obj_file_name, obj_file_name + XML_FILE_EXT)

                for lod in tile.lods:
                    lod.adjust_texture_colors(settings)
                    lod.fix_imported_texture_names()

                tile.update_min_size_values(self.settings.target_min_size_values)
                data = load_json_file(os.path.join(settings.decoder_output_path, obj_file_name + POS_FILE_EXT))
                if data:
                    alt = data[2] - EARTH_RADIUS
                tile.pos.alt = alt
                tile.to_xml(self.objects_xml, xml.guid)

            pbar.update("%s converted" % obj_file_name)

    def __adjust_altitude(self, altitude_adjustment):
        self.objects_xml.adjust_altitude(altitude_adjustment)

    def __find_different_tiles(self, tiles, tiles_to_compare):
        different_tiles = []
        pbar = ProgressBar(tiles.items(), title="FIND THE DIFFERENT TILES")
        for guid, tile in pbar.iterable:
            found_tile = self.__find_by_tile_name(tile, tiles_to_compare)
            if not found_tile:
                different_tiles.append(tile)
            elif len(tile.lods) != len(found_tile.lods):
                different_tiles.append(tile)

            pbar.update("%s found" % tile.name)

        return different_tiles

    def __get_tile_collider(self, tile_name):
        for guid, collider in self.colliders.items():
            if collider.name.replace(COLLIDER_SUFFIX, str()) == tile_name:
                return collider

        return None

    def __find_backup_path(self, backup_root_folder):
        backup_subfolder = os.path.join(self.PACKAGE_SOURCES_FOLDER, os.path.basename(self.model_lib_folder))
        return os.path.join(os.path.join(self.backup_folder, backup_root_folder), backup_subfolder)

    def __multithread_blender_process_data(self, processed_data, script_name, title, update_msg):
        params = [str(bpy.app.binary_path), "--background", "--python", os.path.join(os.path.dirname(os.path.dirname(__file__)), script_name), "--"]
        self.__multithread_process_data(processed_data, params, script_name, title, update_msg)


    def __prepare_geodataframes(self, orig_road, orig_railway, orig_sea, orig_bbox, orig_land_mass, orig_boundary, orig_landuse, orig_natural, orig_natural_water,
                                orig_water, orig_waterway, orig_aeroway, orig_pitch, orig_construction, orig_airport, orig_building, orig_wall, orig_man_made,
                                orig_park, orig_nature_reserve, orig_rocks, orig_amenity, orig_residential, orig_industrial, settings):
        # prepare all the necessary GeoPandas Dataframes
        itasks = 23

        if self.settings.keep_residential_and_industrial:
            itasks = itasks+1

        if self.settings.exclude_forests:
            itasks = itasks+1

        if self.settings.exclude_woods:
            itasks = itasks+1

        if self.settings.exclude_parks:
            itasks = itasks+1

        if self.settings.exclude_nature_reserves:
            itasks = itasks+1

        prepare_gdf_list = [None] * itasks
        pbar = ProgressBar(prepare_gdf_list, title="PREPARE GEODATAFRAMES", sleep=0.0)

        pbar.update("preparing sea geodataframe...", stall=True)
        sea = prepare_sea_gdf(orig_sea)
        pbar.update("sea geodataframe prepared")
        pbar.update("preparing bounding box geodataframe...", stall=True)
        bbox = prepare_bbox_gdf(orig_bbox, orig_land_mass, orig_boundary)
        pbar.update("bounding box geodataframe prepared")
        pbar.update("preparing landuse geodataframe...", stall=True)
        landuse = clip_gdf(prepare_landuse_gdf(orig_landuse), bbox)
        pbar.update("landuse geodataframe prepared")
        pbar.update("preparing hidden_roads geodataframe...", stall=True)
        hidden_roads = clip_gdf(prepare_hidden_roads_gdf(orig_landuse, orig_natural), bbox)
        pbar.update("hidden_roads landuse geodataframe prepared")
        pbar.update("preparing natural geodataframe...", stall=True)
        natural = clip_gdf(prepare_natural_gdf(orig_natural), bbox)
        pbar.update("natural geodataframe prepared")
        pbar.update("preparing natural water geodataframe...", stall=True)
        natural_water = clip_gdf(prepare_gdf(orig_natural_water), bbox)
        pbar.update("natural water geodataframe prepared")
        pbar.update("preparing water geodataframe...", stall=True)
        water = clip_gdf(prepare_water_gdf(orig_water, orig_waterway), bbox)
        pbar.update("water geodataframe prepared")
        pbar.update("preparing bridges geodataframe...", stall=True)
        bridges = prepare_roads_gdf(orig_road, orig_railway, bridge_only=True, automatic_road_width_calculation=False)
        pbar.update("bridges geodataframe prepared")
        pbar.update("preparing roads and places geodataframes...", stall=True)
        roads = prepare_roads_gdf(orig_road, orig_railway, bridge_only=False, automatic_road_width_calculation=False)
        pbar.update("roads and places geodataframes prepared")
        pbar.update("preparing aeroway geodataframe...", stall=True)
        aeroway = clip_gdf(prepare_gdf(orig_aeroway), bbox)
        pbar.update("aeroway geodataframe prepared")
        pbar.update("preparing pitches geodataframe...", stall=True)
        pitches = clip_gdf(prepare_gdf(orig_pitch), bbox)
        pbar.update("pitches geodataframe prepared")
        pbar.update("preparing constructions geodataframe...", stall=True)
        constructions = clip_gdf(prepare_gdf(orig_construction), bbox)
        pbar.update("constructions geodataframe prepared")
        pbar.update("preparing amenities geodataframe...", stall=True)
        amenities = prepare_amenity_gdf(orig_amenity, water, natural_water, orig_airport)
        pbar.update("amenities geodataframe prepared")
        pbar.update("preparing airport geodataframe...", stall=True)
        airport = prepare_gdf(orig_airport)
        pbar.update("airport geodataframe prepared")
        pbar.update("preparing walls geodataframe...", stall=True)
        walls = clip_gdf(prepare_wall_gdf(orig_wall), bbox)
        pbar.update("walls geodataframe prepared")
        pbar.update("preparing man mades geodataframe...", stall=True)
        man_made = clip_gdf(prepare_wall_gdf(orig_man_made), bbox)
        pbar.update("man mades geodataframe prepared")
        pbar.update("preparing buildings geodataframe...", stall=True)
        buildings = clip_gdf(prepare_building_gdf(orig_building, walls, man_made), bbox)
        pbar.update("buildings geodataframe prepared")
        pbar.update("preparing rocks geodataframe...", stall=True)
        rocks = prepare_gdf(orig_rocks)
        pbar.update("rock geodataframe prepared")

        if self.settings.exclude_forests or self.settings.create_forests_vegetation:
            pbar.update("preparing forests geodataframe...", stall=True)
            forests = clip_gdf(prepare_forest_gdf(orig_landuse, orig_natural), bbox)
            pbar.update("forests geodataframe prepared")
        else:
            forests = create_empty_gdf()

        if self.settings.exclude_woods or self.settings.create_woods_vegetation:
            pbar.update("preparing woods geodataframe...", stall=True)
            woods = clip_gdf(prepare_wood_gdf(orig_natural), bbox)
            pbar.update("woods geodataframe prepared")
        else:
            woods = create_empty_gdf()

        if self.settings.exclude_parks:
            pbar.update("preparing parks geodataframe...", stall=True)
            parks = clip_gdf(prepare_park_gdf(orig_park, bridges), bbox)
            pbar.update("parks geodataframe prepared")
        else:
            parks = create_empty_gdf()

        if self.settings.exclude_nature_reserves:
            pbar.update("preparing nature_reserves geodataframe...", stall=True)
            nature_reserves = clip_gdf(prepare_gdf(orig_nature_reserve), bbox)
            pbar.update("nature reserve geodataframe prepared")
        else:
            nature_reserves = create_empty_gdf()

        if self.settings.keep_residential_and_industrial:
            pbar.update("preparing residentials geodataframe...", stall=True)
            residentials = prepare_residential_gdf(orig_residential, water, natural, natural_water, forests, woods, parks, orig_airport)
            pbar.update("residentials geodataframe prepared")
        else:
            residentials = create_empty_gdf()

        pbar.update("preparing industrials geodataframe...", stall=True)
        industrials = clip_gdf(prepare_gdf(orig_industrial), bbox)
        pbar.update("industrials geodataframe prepared")

        pbar.update("creating whole water geodataframe...", stall=True)
        whole_water = create_whole_water_gdf(natural_water, water, sea)
        pbar.update("whole water geodataframe created")
        # create water exclusion masks to cleanup 3d data tiles
        pbar.update("creating water exclusion geodataframe...", stall=True)
        water_exclusion = prepare_water_exclusion_gdf(whole_water, buildings, bridges)
        pbar.update("water exclusion geodataframe created")
        # create ground exclusion masks to cleanup 3d data tiles
        pbar.update("creating ground exclusion geodataframe...", stall=True)
        ground_exclusion = create_ground_exclusion_gdf(landuse, forests, woods, nature_reserves, natural, aeroway, bridges, parks, airport, self.settings)
        pbar.update("ground exclusion geodataframe created")
        pbar.update("creating exclusion geodataframe...", stall=True)
        exclusion = union_gdf(water_exclusion, ground_exclusion if self.settings.exclude_ground else create_empty_gdf())
        pbar.update("exclusion geodataframe created")

        return bbox, roads, bridges, hidden_roads, sea, pitches, constructions, airport, buildings, \
               whole_water, water_exclusion, exclusion, rocks, amenities, residentials, industrials, forests, woods

    @staticmethod
    def __backup_objects(objects: dict, backup_path, pbar_title="backup files"):
        pbar = ProgressBar(list())
        for guid, object in objects.items():
            object.backup_files(backup_path, dry_mode=True, pbar=pbar)
        if pbar.range > 0:
            pbar.display_title(pbar_title)
            for guid, object in objects.items():
                object.backup_files(backup_path, pbar=pbar)

    @staticmethod
    def __backup_textures(objects: dict, backup_path, pbar_title="backup textures"):
        pbar = ProgressBar(list())
        for guid, object in objects.items():
            object.backup_files(backup_path, dry_mode=True, texture_only=True, pbar=pbar)
        if pbar.range > 0:
            pbar.display_title(pbar_title)
            for guid, object in objects.items():
                object.backup_files(backup_path, texture_only=True, pbar=pbar)

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
    def __multithread_process_data(processed_data, params, script_name, title, update_msg):
        ON_POSIX = 'posix' in sys.builtin_module_names

        processed_data, data = itertools.tee(processed_data)
        pbar = ProgressBar(list(data), title=title)

        try:
            for chunck in processed_data:
                # create a pipe to get data
                input_fd, output_fd = os.pipe()

                for obj in chunck:
                    isolated_print("-------------------------------------------------------------------------------")
                    isolated_print("\"" + str(bpy.app.binary_path) + "\" --background --python \"" + os.path.join(os.path.dirname(os.path.dirname(__file__)), script_name) + "\" -- " + str(" ").join(obj["params"]))

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

    @staticmethod
    def __find_by_tile_name(tile, tiles_to_compare):
        for guid, tile_to_compare in tiles_to_compare.items():
            if tile.name == tile_to_compare.name:
                return tile_to_compare

        return False

    @staticmethod
    def __guess_lods_from_obj_files(obj_files):
        result = []
        for obj_file in obj_files:
            obj_file_name = os.path.basename(obj_file).replace(OBJ_FILE_EXT, str())
            lod = len(obj_file_name)
            if lod not in result:
                result.append(lod)

        if result:
            result.sort()

        return result

    @staticmethod
    def __get_geocode_file_prefix(geocode):
        res = geocode

        split = geocode.split(",")
        if split:
            res = split[0]

        res = remove_accents("_".join(filter(str.isalnum, res.split(" "))))
        return res

    @staticmethod
    def __copy_and_backup(obj, file, dest_folder, src_backup_folder, dest_backup_folder, backup_objects_to_cleanup=False, optimized=False, cleaned=False):
        shutil.copyfile(os.path.join(obj.folder, file), os.path.join(dest_folder, file))

        if backup_objects_to_cleanup:
            if cleaned and os.path.isdir(src_backup_folder) and os.path.isdir(dest_backup_folder):
                shutil.copyfile(os.path.join(src_backup_folder, file), os.path.join(dest_backup_folder, file))
            elif optimized and os.path.isdir(dest_backup_folder):
                shutil.copyfile(os.path.join(obj.folder, file), os.path.join(dest_backup_folder, file))
