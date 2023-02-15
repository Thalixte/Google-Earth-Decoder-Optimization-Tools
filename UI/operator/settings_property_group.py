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

import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty
from constants import TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX, PNG_TEXTURE_FORMAT, JPG_TEXTURE_FORMAT, MAX_PHOTOGRAMMETRY_LOD, POI_LANDMARK_FORMAT_TYPE, CITY_LANDMARK_FORMAT_TYPE, LIGHT_WARM_DISPLAY_NAME, LIGHT_COLD_DISPLAY_NAME, LIGHT_WARM_GUID, LIGHT_COLD_GUID, LIGHT_100_BLUE_GUID, LIGHT_500_BLUE_GUID, LIGHT_1000_BLUE_GUID, LIGHT_100_BLUE_DISPLAY_NAME, LIGHT_500_BLUE_DISPLAY_NAME, LIGHT_1000_BLUE_DISPLAY_NAME, LIGHT_100_GREEN_GUID, LIGHT_100_GREEN_DISPLAY_NAME, LIGHT_500_GREEN_GUID, \
    LIGHT_500_GREEN_DISPLAY_NAME, LIGHT_1000_GREEN_GUID, LIGHT_1000_GREEN_DISPLAY_NAME, LIGHT_100_SOFT_GREEN_GUID, LIGHT_100_SOFT_GREEN_DISPLAY_NAME, LIGHT_500_SOFT_GREEN_GUID, LIGHT_500_SOFT_GREEN_DISPLAY_NAME, LIGHT_1000_SOFT_GREEN_GUID, LIGHT_1000_SOFT_GREEN_DISPLAY_NAME, LIGHT_100_WHITE_GUID, LIGHT_100_WHITE_DISPLAY_NAME, LIGHT_500_WHITE_GUID, LIGHT_500_WHITE_DISPLAY_NAME, LIGHT_1000_WHITE_GUID, LIGHT_1000_WHITE_DISPLAY_NAME, LIGHT_100_MINT_GREEN_GUID, LIGHT_100_MINT_GREEN_DISPLAY_NAME, \
    LIGHT_500_MINT_GREEN_GUID, LIGHT_500_MINT_GREEN_DISPLAY_NAME, LIGHT_1000_MINT_GREEN_GUID, LIGHT_1000_MINT_GREEN_DISPLAY_NAME, LIGHT_100_PINK_GUID, LIGHT_100_PINK_DISPLAY_NAME, LIGHT_500_PINK_GUID, LIGHT_500_PINK_DISPLAY_NAME, LIGHT_1000_PINK_GUID, LIGHT_1000_PINK_DISPLAY_NAME, LIGHT_100_RED_GUID, LIGHT_100_RED_DISPLAY_NAME, LIGHT_500_RED_GUID, LIGHT_500_RED_DISPLAY_NAME, LIGHT_1000_RED_GUID, LIGHT_1000_RED_DISPLAY_NAME, LIGHT_100_SKY_BLUE_GUID, LIGHT_100_SKY_BLUE_DISPLAY_NAME, \
    LIGHT_500_SKY_BLUE_GUID, LIGHT_500_SKY_BLUE_DISPLAY_NAME, LIGHT_1000_SKY_BLUE_GUID, LIGHT_1000_SKY_BLUE_DISPLAY_NAME, LIGHT_100_PURPLE_GUID, LIGHT_100_PURPLE_DISPLAY_NAME, LIGHT_500_PURPLE_GUID, LIGHT_500_PURPLE_DISPLAY_NAME, LIGHT_1000_PURPLE_GUID, LIGHT_1000_PURPLE_DISPLAY_NAME, LIGHT_100_YELLOW_GUID, LIGHT_100_YELLOW_DISPLAY_NAME, LIGHT_500_YELLOW_GUID, LIGHT_500_YELLOW_DISPLAY_NAME, LIGHT_1000_YELLOW_GUID, LIGHT_1000_YELLOW_DISPLAY_NAME


class SettingsPropertyGroup(bpy.types.PropertyGroup):
    def projects_path_updated(self, context):
        context.scene.settings.projects_path = self.projects_path_readonly = self.projects_path

    def project_path_updated(self, context):
        context.scene.settings.projects_path = self.projects_path = self.projects_path_readonly = os.path.dirname(os.path.dirname(self.project_path)) + os.sep
        context.scene.settings.project_path = self.project_path
        context.scene.settings.project_name = self.project_name = os.path.relpath(self.project_path, start=self.projects_path)
        context.scene.settings.definition_file = self.definition_file
        self.project_path_readonly = self.project_path

    def project_name_updated(self, context):
        context.scene.settings.project_name = self.project_name
        context.scene.settings.project_path = os.path.join(context.scene.settings.projects_path, context.scene.settings.project_name)

    def project_path_to_merge_updated(self, context):
        context.scene.settings.project_path_to_merge = os.path.dirname(self.project_path_to_merge)
        context.scene.settings.definition_file_to_merge = self.definition_file_to_merge
        self.project_path_to_merge_readonly = self.project_path_to_merge

    def author_name_updated(self, context):
        context.scene.settings.author_name = self.author_name

    def nb_parallel_blender_tasks_updated(self, context):
        context.scene.settings.nb_parallel_blender_tasks = int(self.nb_parallel_blender_tasks)

    def bake_textures_enabled_updated(self, context):
        context.scene.settings.bake_textures_enabled_updated = self.bake_textures_enabled

    def output_texture_format_updated(self, context):
        context.scene.settings.output_texture_format = self.output_texture_format

    def collider_as_lower_lod_updated(self, context):
        context.scene.settings.collider_as_lower_lod = self.collider_as_lower_lod

    def backup_enabled_updated(self, context):
        context.scene.settings.backup_enabled = self.backup_enabled

    def lat_correction_updated(self, context):
        context.scene.settings.lat_correction = "{:.9f}".format(float(str(self.lat_correction))).rstrip("0").rstrip(".")

    def lon_correction_updated(self, context):
        context.scene.settings.lon_correction = "{:.9f}".format(float(str(self.lon_correction))).rstrip("0").rstrip(".")

    def target_min_size_value_updated(self, context):
        prev_value = -1
        for idx, min_size_value in enumerate(bpy.types.Scene.settings.target_min_size_values):
            reverse_idx = (len(bpy.types.Scene.settings.target_min_size_values) - 1) - idx
            cur_lod = MAX_PHOTOGRAMMETRY_LOD - reverse_idx
            name = TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX + str(cur_lod)
            cur_value = int(eval("self." + name))
            cur_value = prev_value if cur_value < prev_value else cur_value
            self[name] = cur_value
            context.scene.settings.target_min_size_values[idx] = str(cur_value)
            prev_value = int(context.scene.settings.target_min_size_values[idx])

    def airport_city_updated(self, context):
        context.scene.settings.airport_city = self.airport_city

    def exclude_ground_updated(self, context):
        context.scene.settings.exclude_ground = self.exclude_ground

    def exclude_nature_reserve_updated(self, context):
        context.scene.settings.exclude_nature_reserve = self.exclude_nature_reserve

    def exclude_parks_updated(self, context):
        context.scene.settings.exclude_parks = self.exclude_parks

    def keep_residential_and_industrial_updated(self, context):
        context.scene.settings.keep_residential_and_industrial = self.keep_residential_and_industrial

    def process_all_updated(self, context):
        context.scene.settings.process_all = self.process_all

    def high_precision_updated(self, context):
        context.scene.settings.high_precision = self.high_precision

    def height_adjustment_updated(self, context):
        context.scene.settings.height_adjustment = "{:.1f}".format(float(str(self.height_adjustment))).rstrip("0").rstrip(".")

    def height_noise_reduction_updated(self, context):
        context.scene.settings.height_noise_reduction = "{:.1f}".format(float(str(self.height_noise_reduction))).rstrip("0").rstrip(".")

    def geocode_updated(self, context):
        context.scene.settings.geocode = self.geocode

    def geocode_margin_updated(self, context):
        context.scene.settings.geocode_margin = self.geocode_margin

    def preserve_roads_updated(self, context):
        context.scene.settings.preserve_roads = self.preserve_roads

    def preserve_buildings_updated(self, context):
        context.scene.settings.preserve_buildings = self.preserve_buildings

    def landmark_type_updated(self, context):
        context.scene.settings.landmark_type = self.landmark_type

    def landmark_offset_updated(self, context):
        context.scene.settings.landmark_offset = "{:.1f}".format(float(str(self.landmark_offset))).rstrip("0").rstrip(".")

    def add_lights_updated(self, context):
        context.scene.settings.add_lights = self.add_lights

    def light_guid_updated(self, context):
        context.scene.settings.light_guid = self.light_guid

    def altitude_adjustment_updated(self, context):
        context.scene.settings.altitude_adjustment = "{:.2f}".format(float(str(self.altitude_adjustment))).rstrip("0").rstrip(".")

    def build_package_enabled_updated(self, context):
        context.scene.settings.build_package_enabled = self.build_package_enabled

    def msfs_build_exe_path_updated(self, context):
        context.scene.settings.msfs_build_exe_path = self.msfs_build_exe_path_readonly = self.msfs_build_exe_path

    def msfs_steam_version_updated(self, context):
        context.scene.settings.msfs_steam_version = self.msfs_steam_version

    def compressonator_exe_path_updated(self, context):
        context.scene.settings.compressonator_exe_path = self.compressonator_exe_path_readonly = self.compressonator_exe_path

    def python_reload_modules_updated(self, context):
        context.scene.settings.reload_modules = self.python_reload_modules

    projects_path: bpy.props.StringProperty(
        subtype="DIR_PATH",
        name="Path of the projects",
        description="Select the path containing all your MSFS scenery projects",
        maxlen=1024,
        default=bpy.types.Scene.settings.projects_path,
        update=projects_path_updated
    )
    projects_path_readonly: bpy.props.StringProperty(
        name="Path of the projects",
        description="Select the path containing all your MSFS scenery projects",
        default=bpy.types.Scene.settings.projects_path
    )
    project_path: StringProperty(
        subtype="FILE_PATH",
        name="Path of the xml definition_file of the project",
        description="Select the path of the xml definition file of the MSFS scenery project",
        maxlen=1024,
        default=os.path.join(os.path.join(bpy.types.Scene.settings.projects_path, bpy.types.Scene.settings.project_name), bpy.types.Scene.settings.definition_file),
        update=project_path_updated
    )
    project_path_readonly: bpy.props.StringProperty(
        name="Path of the project",
        description="Select the path containing the MSFS scenery project",
        default=os.path.join(bpy.types.Scene.settings.projects_path, bpy.types.Scene.settings.project_name)
    )
    project_name: StringProperty(
        name="Project name",
        description="Name of the project to initialize",
        default=bpy.types.Scene.settings.project_name,
        maxlen=256,
        update=project_name_updated
    )
    definition_file: StringProperty(
        name="Definition file",
        description="Xml definition_file of the MSFS project",
        default=bpy.types.Scene.settings.definition_file,
        maxlen=256
    )
    nb_parallel_blender_tasks: IntProperty(
        name="Number of parallel Blender tasks",
        description="Set the number of parallel Blender tasks to run concurrently",
        soft_min=1,
        soft_max=10,
        step=1,
        default=int(bpy.types.Scene.settings.nb_parallel_blender_tasks),
        update=nb_parallel_blender_tasks_updated
    )
    project_path_to_merge: StringProperty(
        subtype="FILE_PATH",
        name="Path of the xml definition_file of the project you want to merge into the final one",
        description="Select the path of the xml definition file of the the project you want to merge into the final msfs scenery project",
        maxlen=1024,
        default=os.path.join(bpy.types.Scene.settings.project_path_to_merge, bpy.types.Scene.settings.definition_file_to_merge),
        update=project_path_to_merge_updated
    )
    definition_file_to_merge: StringProperty(
        name="Definition file",
        description="Xml definition_file of the project you want to merge into the final one",
        default=bpy.types.Scene.settings.definition_file_to_merge,
        maxlen=256
    )
    project_path_to_merge_readonly: bpy.props.StringProperty(
        name="Path of the project you want to merge into the final msfs scenery project",
        description="Select the path containing the project you want to merge into the final msfs scenery project",
        default=os.path.join(bpy.types.Scene.settings.project_path_to_merge, bpy.types.Scene.settings.definition_file_to_merge)
    )
    author_name: StringProperty(
        name="Author name",
        description="Author of the msfs scenery project",
        default=bpy.types.Scene.settings.author_name,
        maxlen=256,
        update=author_name_updated
    )
    bake_textures_enabled: BoolProperty(
        name="Bake textures enabled",
        description="Reduce the number of texture files (Lily Texture Packer addon is necessary https://gumroad.com/l/DFExj)",
        default=bpy.types.Scene.settings.bake_textures_enabled,
        update=bake_textures_enabled_updated
    )
    output_texture_format: EnumProperty(
        name="Output texture format",
        description="output format of the texture files (jpg or png) used by the photogrammetry tiles",
        items=[
            (PNG_TEXTURE_FORMAT, PNG_TEXTURE_FORMAT, str()),
            (JPG_TEXTURE_FORMAT, JPG_TEXTURE_FORMAT, str()),
        ],
        default=bpy.types.Scene.settings.output_texture_format,
        update=output_texture_format_updated
    )
    collider_as_lower_lod: BoolProperty(
        name="Add the collider as the lower LOD for each tile",
        description="Add the collider as the lower LOD for each tile (make the tiles disappear when they take less than 1% of the screen)",
        default=bpy.types.Scene.settings.collider_as_lower_lod,
        update=collider_as_lower_lod_updated
    )
    backup_enabled: BoolProperty(
        name="Backup enabled",
        description="Enable the backup of the project files before processing",
        default=bpy.types.Scene.settings.backup_enabled,
        update=backup_enabled_updated
    )
    lat_correction: FloatProperty(
        name="Latitude correction",
        description="Set the latitude correction for positioning the tiles",
        soft_min=-0.1,
        soft_max=0.1,
        step=1,
        precision=6,
        default=float(bpy.types.Scene.settings.lat_correction),
        update=lat_correction_updated
    )
    lon_correction: FloatProperty(
        name="Longitude correction",
        description="Set the longitude correction for positioning the tiles",
        soft_min=-0.1,
        soft_max=0.1,
        step=1,
        precision=6,
        default=float(bpy.types.Scene.settings.lon_correction),
        update=lon_correction_updated
    )
    airport_city: StringProperty(
        name="City",
        description="City of the airport to exclude",
        default=bpy.types.Scene.settings.airport_city,
        maxlen=256,
        update=airport_city_updated
    )
    exclude_ground: BoolProperty(
        name="Exclude ground 3d data",
        description="Exclude ground 3d data (forests, woods)",
        default=bpy.types.Scene.settings.exclude_ground,
        update=exclude_ground_updated
    )
    exclude_nature_reserve: BoolProperty(
        name="Exclude nature reserves 3d data",
        description="Exclude nature reserves 3d data",
        default=bpy.types.Scene.settings.exclude_nature_reserve,
        update=exclude_nature_reserve_updated
    )
    exclude_parks: BoolProperty(
        name="Exclude parks 3d data",
        description="Exclude parks 3d data",
        default=bpy.types.Scene.settings.exclude_parks,
        update=exclude_parks_updated
    )
    keep_residential_and_industrial: BoolProperty(
        name="Keep residential and industrial area 3d data",
        description="Keep residential and industrial area 3d data",
        default=bpy.types.Scene.settings.keep_residential_and_industrial,
        update=keep_residential_and_industrial_updated
    )
    process_all: BoolProperty(
        name="Process all the tiles (if unticked, process only the tiles that has not been cleaned)",
        description="Process all the tiles (if unticked, process only the tiles that has not been cleaned)",
        default=bpy.types.Scene.settings.process_all,
        update=process_all_updated
    )
    high_precision: BoolProperty(
        name="High precision height data generation",
        description="Generate the height data, using the most detailed tile lods",
        default=bpy.types.Scene.settings.high_precision,
        update=high_precision_updated
    )
    height_adjustment: FloatProperty(
        name="Height adjustment",
        description="Adjust the height data calculation (in meters)",
        soft_min=-100.0,
        soft_max=100.0,
        step=0.1,
        precision=1,
        default=float(bpy.types.Scene.settings.height_adjustment),
        update=height_adjustment_updated
    )
    height_noise_reduction: FloatProperty(
        name="Height noise reduction",
        description="Adjust the height noise reduction factor for ray-tracing the bottom of the tile",
        soft_min=0.0,
        soft_max=200.0,
        step=0.1,
        precision=1,
        default=float(bpy.types.Scene.settings.height_noise_reduction),
        update=height_noise_reduction_updated
    )
    geocode: StringProperty(
        name="Geocode",
        description="Geocode to search from OSM data (for exclusion or isolation) in the form \"location name, city\", or\"(way|relation), osmid\"",
        default=bpy.types.Scene.settings.geocode,
        maxlen=256,
        update=geocode_updated
    )
    geocode_margin: FloatProperty(
        name="Geocode margin",
        description="Margin of the geocode polygon used to exclude or isolate the 3d data",
        soft_min=-10.0,
        soft_max=20.0,
        step=0.1,
        precision=1,
        default=float(bpy.types.Scene.settings.geocode_margin),
        update=geocode_margin_updated
    )
    preserve_roads: BoolProperty(
        name="Preserve roads",
        description="Preserve neighborhood roads when excluding 3d data from geocode",
        default=bpy.types.Scene.settings.preserve_roads,
        update=preserve_roads_updated
    )
    preserve_buildings: BoolProperty(
        name="Preserve buildings",
        description="Preserve neighborhood buildings when excluding 3d data from geocode",
        default=bpy.types.Scene.settings.preserve_buildings,
        update=preserve_buildings_updated
    )
    landmark_type: EnumProperty(
        name="Landmark type",
        description="Type of the landmark (POI, City, ...)",
        items=[
            (POI_LANDMARK_FORMAT_TYPE, POI_LANDMARK_FORMAT_TYPE, str()),
            (CITY_LANDMARK_FORMAT_TYPE, CITY_LANDMARK_FORMAT_TYPE, str()),
        ],
        default=bpy.types.Scene.settings.landmark_type,
        update=landmark_type_updated

    )
    landmark_offset: FloatProperty(
        name="Landmark offset",
        description="Height offset of the landmark",
        soft_min=-100.0,
        soft_max=100.0,
        step=1.0,
        precision=1,
        default=float(bpy.types.Scene.settings.landmark_offset),
        update=landmark_offset_updated
    )
    altitude_adjustment: FloatProperty(
        name="Altitude update",
        description="Adjustment of the altitude of the whole scenery components (tiles, objects, colliders, landmarks, height maps)",
        soft_min=-10.0,
        soft_max=20.0,
        step=0.1,
        precision=2,
        default=float(bpy.types.Scene.settings.altitude_adjustment),
        update=altitude_adjustment_updated
    )
    add_lights: BoolProperty(
        name="Add lights around the landmark",
        description="Add lights around the geocode landmark",
        default=bpy.types.Scene.settings.add_lights,
        update=add_lights_updated
    )
    light_guid: EnumProperty(
        name="Add lights around the landmark",
        description="Add lights around the geocode landmark",
        items=[
            (LIGHT_WARM_GUID, LIGHT_WARM_DISPLAY_NAME, str()),
            (LIGHT_COLD_GUID, LIGHT_COLD_DISPLAY_NAME, str()),
            (LIGHT_100_BLUE_GUID, LIGHT_100_BLUE_DISPLAY_NAME, str()),
            (LIGHT_500_BLUE_GUID, LIGHT_500_BLUE_DISPLAY_NAME, str()),
            (LIGHT_1000_BLUE_GUID, LIGHT_1000_BLUE_DISPLAY_NAME, str()),
            (LIGHT_100_GREEN_GUID, LIGHT_100_GREEN_DISPLAY_NAME, str()),
            (LIGHT_500_GREEN_GUID, LIGHT_500_GREEN_DISPLAY_NAME, str()),
            (LIGHT_1000_GREEN_GUID, LIGHT_1000_GREEN_DISPLAY_NAME, str()),
            (LIGHT_100_SOFT_GREEN_GUID, LIGHT_100_SOFT_GREEN_DISPLAY_NAME, str()),
            (LIGHT_500_SOFT_GREEN_GUID, LIGHT_500_SOFT_GREEN_DISPLAY_NAME, str()),
            (LIGHT_1000_SOFT_GREEN_GUID, LIGHT_1000_SOFT_GREEN_DISPLAY_NAME, str()),
            (LIGHT_100_WHITE_GUID, LIGHT_100_WHITE_DISPLAY_NAME, str()),
            (LIGHT_500_WHITE_GUID, LIGHT_500_WHITE_DISPLAY_NAME, str()),
            (LIGHT_1000_WHITE_GUID, LIGHT_1000_WHITE_DISPLAY_NAME, str()),
            (LIGHT_100_MINT_GREEN_GUID, LIGHT_100_MINT_GREEN_DISPLAY_NAME, str()),
            (LIGHT_500_MINT_GREEN_GUID, LIGHT_500_MINT_GREEN_DISPLAY_NAME, str()),
            (LIGHT_1000_MINT_GREEN_GUID, LIGHT_1000_MINT_GREEN_DISPLAY_NAME, str()),
            (LIGHT_100_PINK_GUID, LIGHT_100_PINK_DISPLAY_NAME, str()),
            (LIGHT_500_PINK_GUID, LIGHT_500_PINK_DISPLAY_NAME, str()),
            (LIGHT_1000_PINK_GUID, LIGHT_1000_PINK_DISPLAY_NAME, str()),
            (LIGHT_100_RED_GUID, LIGHT_100_RED_DISPLAY_NAME, str()),
            (LIGHT_500_RED_GUID, LIGHT_500_RED_DISPLAY_NAME, str()),
            (LIGHT_1000_RED_GUID, LIGHT_1000_RED_DISPLAY_NAME, str()),
            (LIGHT_100_SKY_BLUE_GUID, LIGHT_100_SKY_BLUE_DISPLAY_NAME, str()),
            (LIGHT_500_SKY_BLUE_GUID, LIGHT_500_SKY_BLUE_DISPLAY_NAME, str()),
            (LIGHT_1000_SKY_BLUE_GUID, LIGHT_1000_SKY_BLUE_DISPLAY_NAME, str()),
            (LIGHT_100_PURPLE_GUID, LIGHT_100_PURPLE_DISPLAY_NAME, str()),
            (LIGHT_500_PURPLE_GUID, LIGHT_500_PURPLE_DISPLAY_NAME, str()),
            (LIGHT_1000_PURPLE_GUID, LIGHT_1000_PURPLE_DISPLAY_NAME, str()),
            (LIGHT_100_YELLOW_GUID, LIGHT_100_YELLOW_DISPLAY_NAME, str()),
            (LIGHT_500_YELLOW_GUID, LIGHT_500_YELLOW_DISPLAY_NAME, str()),
            (LIGHT_1000_YELLOW_GUID, LIGHT_1000_YELLOW_DISPLAY_NAME, str())
        ],
        default=bpy.types.Scene.settings.light_guid,
        update=light_guid_updated
    )
    build_package_enabled: BoolProperty(
        name="Build package enabled",
        description="Enable the package compilation when the script has finished",
        default=bpy.types.Scene.settings.build_package_enabled,
        update=build_package_enabled_updated
    )
    msfs_build_exe_path: StringProperty(
        subtype="FILE_PATH",
        name="Path to the MSFS bin exe that builds the MSFS packages",
        description="Select the path to the MSFS bin exe that builds the MSFS packages",
        maxlen=1024,
        default=bpy.types.Scene.settings.msfs_build_exe_path,
        update=msfs_build_exe_path_updated
    )
    msfs_build_exe_path_readonly: StringProperty(
        name="Path to the MSFS bin exe that builds the MSFS packages",
        description="Select the path to the MSFS bin exe that builds the MSFS packages",
        default=bpy.types.Scene.settings.msfs_build_exe_path
    )
    msfs_steam_version: BoolProperty(
        name="Msfs Steam version",
        description="Set this to true if you have the MSFS 2020 Steam version",
        default=bpy.types.Scene.settings.msfs_steam_version,
        update=msfs_steam_version_updated
    )
    compressonator_exe_path: StringProperty(
        subtype="FILE_PATH",
        name="Path to the compressonator bin exe that compresses the package texture files",
        description="Select the path to the compressonator bin exe that compresses the package texture file",
        maxlen=1024,
        default=bpy.types.Scene.settings.compressonator_exe_path,
        update=compressonator_exe_path_updated
    )
    compressonator_exe_path_readonly: StringProperty(
        name="Path to the compressonator bin exe that compresses the package texture files",
        description="Select the path to the compressonator bin exe that compresses the package texture file",
        default=bpy.types.Scene.settings.compressonator_exe_path,
    )
    python_reload_modules: BoolProperty(
        name="Reload python modules (for dev purpose)",
        description="Set this to true if you want to reload python modules (mainly for dev purpose)",
        default=bpy.types.Scene.settings.reload_modules,
        update=python_reload_modules_updated
    )
