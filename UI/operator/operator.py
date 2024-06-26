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
from bpy.props import StringProperty
from constants import MAX_PHOTOGRAMMETRY_LOD, INI_FILE
from msfs_project.project import MsfsProject
from scripts.cleanup_3d_data_script import cleanup_3d_data
from scripts.add_tile_colliders_script import add_tile_colliders
from scripts.clean_package_files_script import clean_package_files
from scripts.fix_tiles_lightning_issues_script import fix_tiles_lightning_issues
from scripts.init_msfs_scenery_project_script import init_msfs_scenery_project
from scripts.merge_sceneries_script import merge_sceneries
from scripts.optimize_scenery_script import optimize_scenery
from scripts.remove_tile_colliders_script import remove_tile_colliders
from scripts.resize_scenery_textures_script import resize_scenery_textures
from scripts.update_min_size_values_script import update_min_size_values
from scripts.compress_built_package_script import compress_built_package
from scripts.update_tiles_position_script import update_tiles_position
from scripts.create_terraform_and_exclusion_polygons_script import create_terraform_and_exclusion_polygons
from scripts.generate_height_data_script import generate_height_data
from scripts.remove_water_from_3d_data_script import remove_water_from_3d_data
from scripts.remove_forests_and_woods_from_3d_data_script import remove_forests_and_woods_from_3d_data
from scripts.remove_forests_woods_and_parks_from_3d_data_script import remove_forests_woods_and_parks_from_3d_data
from scripts.keep_only_buildings_3d_data_script import keep_only_buildings_3d_data
from scripts.keep_only_buildings_and_roads_3d_data_script import keep_only_buildings_and_roads_3d_data
from scripts.create_landmark_from_geocode_script import create_landmark_from_geocode
from scripts.add_lights_to_geocode_script import add_lights_to_geocode
from scripts.exclude_3d_data_from_geocode_script import exclude_3d_data_from_geocode
from scripts.isolate_3d_data_from_geocode_script import isolate_3d_data_from_geocode
from scripts.adjust_scenery_altitude_script import adjust_scenery_altitude
from utils import open_console
from .tools import reload_current_operator, reload_setting_props, reload_project_settings
from bpy_extras.io_utils import ImportHelper
from bpy_types import Operator


class FileBrowserOperator(Operator, ImportHelper):
    def draw(self, context):
        space = context.space_data
        params = space.params
        params.display_size = "NORMAL"


class DirectoryBrowserOperator(Operator, ImportHelper):
    def draw(self, context):
        space = context.space_data
        params = space.params
        params.use_filter = True
        params.use_filter_folder = True
        params.display_size = "NORMAL"


class OT_ProjectsPathOperator(DirectoryBrowserOperator):
    bl_idname = "wm.projects_path_operator"
    bl_label = "Path of the MSFS projects..."

    directory: bpy.props.StringProperty(subtype="DIR_PATH")

    def draw(self, context):
        super().draw(context)

    def execute(self, context):
        context.scene.setting_props.projects_path = self.directory
        reload_current_operator(context)
        reload_project_settings(context)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.directory = context.scene.setting_props.projects_path
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class OT_ProjectPathOperator(DirectoryBrowserOperator):
    bl_idname = "wm.project_path_operator"
    bl_label = "Path of the MSFS project definition file..."

    filter_glob: StringProperty(
        default="*.xml",
        options={"HIDDEN"},
    )
    filepath: bpy.props.StringProperty(
        subtype="FILE_PATH"
    )

    def draw(self, context):
        super().draw(context)

    def execute(self, context):
        context.scene.setting_props.definition_file = os.path.basename(self.filepath)
        context.scene.setting_props.project_path = os.path.dirname(self.filepath) + os.sep
        reload_current_operator(context)
        reload_project_settings(context)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.filepath = os.path.join(context.scene.setting_props.project_path, context.scene.setting_props.definition_file)
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class OT_ProjectPathToMergeOperator(DirectoryBrowserOperator):
    bl_idname = "wm.project_path_to_merge_operator"
    bl_label = "Path of the project definition file you want to merge into the final one..."

    filter_glob: StringProperty(
        default="*.xml",
        options={"HIDDEN"},
    )
    filepath: bpy.props.StringProperty(
        subtype="FILE_PATH"
    )

    def draw(self, context):
        super().draw(context)

    def execute(self, context):
        context.scene.setting_props.definition_file_to_merge = os.path.basename(self.filepath)
        context.scene.setting_props.project_path_to_merge = os.path.dirname(self.filepath) + os.sep
        reload_current_operator(context)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.filepath = os.path.join(context.scene.setting_props.project_path_to_merge, context.scene.setting_props.definition_file_to_merge)
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class ActionOperator(Operator):
    @classmethod
    def poll(cls, context):
        global_settings = context.scene.global_settings
        return MsfsProject(global_settings.projects_path, global_settings.project_name, global_settings.definition_file, global_settings.path, global_settings.author_name, fast_init=True)

    def execute(self, context):
        # clear and open the system console
        open_console()


class OT_InitMsfsSceneryProjectOperator(ActionOperator):
    bl_idname = "wm.init_msfs_scenery_project"
    bl_label = "Initialize a new MSFS project scenery..."

    @classmethod
    def poll(cls, context):
        global_settings = context.scene.global_settings
        scene_folder = os.path.join(global_settings.projects_path, global_settings.project_name)
        return not os.path.isdir(scene_folder) and global_settings.author_name != str()

    def execute(self, context):
        super().execute(context)
        reload_project_settings(context)
        init_msfs_scenery_project(context.scene.global_settings)
        return {'FINISHED'}


class OT_OptimizeMsfsSceneryOperator(ActionOperator):
    bl_idname = "wm.optimize_msfs_scenery"
    bl_label = "Optimize an existing MSFS scenery..."

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return os.path.isdir(msfs_project.scene_folder)

    def execute(self, context):
        super().execute(context)
        optimize_scenery(context.scene.global_settings)
        return {'FINISHED'}


class OT_CleanPackageFilesOperator(ActionOperator):
    bl_idname = "wm.clean_package_files"
    bl_label = "Clean the unused files of the msfs project..."

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return os.path.isdir(msfs_project.scene_folder)

    def execute(self, context):
        super().execute(context)
        clean_package_files(context.scene.global_settings)
        return {'FINISHED'}


class OT_MergeSceneriesOperator(ActionOperator):
    bl_idname = "wm.merge_sceneries"
    bl_label = "Merge an existing MSFS scenery project into another one..."

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        global_settings = context.scene.global_settings
        project_settings = msfs_project.settings
        project_name_to_merge = str()

        if os.path.isdir(project_settings.project_path_to_merge):
            project_folder_to_merge = os.path.dirname(project_settings.project_path_to_merge) + os.path.sep
            project_name_to_merge = os.path.relpath(project_settings.project_path_to_merge, start=project_folder_to_merge)

        definition_file_to_merge = project_settings.definition_file_to_merge
        msfs_project_to_merge = MsfsProject(global_settings.projects_path, project_name_to_merge, definition_file_to_merge, global_settings.path, global_settings.author_name, fast_init=True)
        return (os.path.isdir(msfs_project.scene_folder) and os.path.isdir(msfs_project_to_merge.scene_folder)) and msfs_project.project_folder != msfs_project_to_merge.project_folder

    def execute(self, context):
        super().execute(context)
        merge_sceneries(context.scene.global_settings)
        return {'FINISHED'}


class OT_UpdateTilesPositionOperator(ActionOperator):
    bl_idname = "wm.update_tiles_position"
    bl_label = "Update the position of the MSFS scenery tiles..."

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return os.path.isdir(msfs_project.scene_folder)

    def execute(self, context):
        super().execute(context)
        update_tiles_position(context.scene.global_settings)
        return {'FINISHED'}


class OT_UpdateMinSizeValuesOperator(ActionOperator):
    bl_idname = "wm.update_min_size_values"
    bl_label = "Update LOD min size values for each tile of the project..."

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return os.path.isdir(msfs_project.scene_folder)

    def execute(self, context):
        super().execute(context)
        update_min_size_values(context.scene.global_settings)
        return {'FINISHED'}


class OT_FixTilesLightningIssuesOperator(ActionOperator):
    bl_idname = "wm.fix_tiles_lightning_issues"
    bl_label = "Fix lightning issues on tiles at dawn or dusk..."

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return os.path.isdir(msfs_project.scene_folder)

    def execute(self, context):
        super().execute(context)
        fix_tiles_lightning_issues(context.scene.global_settings)
        return {'FINISHED'}


class OT_CreateTerraformAndExclusionPolygonsOperator(ActionOperator):
    bl_idname = "wm.create_terraform_and_exclusion_polygons"
    bl_label = "Create the terraform and exclusion polygons for the scenery..."

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return os.path.isdir(msfs_project.scene_folder)

    def execute(self, context):
        super().execute(context)
        create_terraform_and_exclusion_polygons(context.scene.global_settings)
        return {'FINISHED'}


class OT_GenerateHeightDataOperator(ActionOperator):
    bl_idname = "wm.generate_height_data"
    bl_label = "Generate height data based on the Google Earth tiles..."

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return os.path.isdir(msfs_project.scene_folder)

    def execute(self, context):
        super().execute(context)
        generate_height_data(context.scene.global_settings)
        return {'FINISHED'}


class OT_Cleanup3dDataOperator(ActionOperator):
    bl_idname = "wm.cleanup_3d_data"
    bl_label = "Cleanup 3d data from Google Earth tiles"

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return os.path.isdir(msfs_project.scene_folder)

    def execute(self, context):
        super().execute(context)
        cleanup_3d_data(context.scene.global_settings)
        return {'FINISHED'}


class OT_RemoveWaterFrom3dDataOperator(ActionOperator):
    bl_idname = "wm.remove_water_from_3d_data"
    bl_label = "Remove water from Google Earth tiles"

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return os.path.isdir(msfs_project.scene_folder)

    def execute(self, context):
        super().execute(context)
        remove_water_from_3d_data(context.scene.global_settings)
        return {'FINISHED'}


class OT_RemoveForestsAndWoodsFrom3dDataOperator(ActionOperator):
    bl_idname = "wm.remove_forests_and_woods_from_3d_data"
    bl_label = "Remove water, forests and woods from Google Earth tiles"

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return os.path.isdir(msfs_project.scene_folder)

    def execute(self, context):
        super().execute(context)
        remove_forests_and_woods_from_3d_data(context.scene.global_settings)
        return {'FINISHED'}


class OT_RemoveForestsWoodsAndParksFrom3dDataOperator(ActionOperator):
    bl_idname = "wm.remove_forests_woods_and_parks_from_3d_data"
    bl_label = "Remove water, forests, woods and parks from Google Earth tiles"

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return os.path.isdir(msfs_project.scene_folder)

    def execute(self, context):
        super().execute(context)
        remove_forests_woods_and_parks_from_3d_data(context.scene.global_settings)
        return {'FINISHED'}


class OT_KeepOnlyBuildings3dDataOperator(ActionOperator):
    bl_idname = "wm.keep_only_buildings_3d_data"
    bl_label = "Remove everything except buildings from Google Earth tiles"

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return os.path.isdir(msfs_project.scene_folder)

    def execute(self, context):
        super().execute(context)
        keep_only_buildings_3d_data(context.scene.global_settings)
        return {'FINISHED'}


class OT_KeepOnlyBuildingsAndRoads3dDataOperator(ActionOperator):
    bl_idname = "wm.keep_only_buildings_and_roads_3d_data"
    bl_label = "Remove everything except buildings and roads from Google Earth tiles"

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return os.path.isdir(msfs_project.scene_folder)

    def execute(self, context):
        super().execute(context)
        keep_only_buildings_and_roads_3d_data(context.scene.global_settings)
        return {'FINISHED'}


class OT_CreateLandmarkFromGeocodeOperator(ActionOperator):
    bl_idname = "wm.create_landmark_from_geocode"
    bl_label = "Create landmark from geocode"

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return os.path.isdir(msfs_project.scene_folder) and context.scene.project_settings.geocode != str()

    def execute(self, context):
        super().execute(context)
        create_landmark_from_geocode(context.scene.global_settings)
        return {'FINISHED'}


class OT_AddLightsToGeocodeOperator(ActionOperator):
    bl_idname = "wm.add_lights_to_geocode"
    bl_label = "Add lights all around a geocode"

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return os.path.isdir(msfs_project.scene_folder) and context.scene.project_settings.geocode != str()

    def execute(self, context):
        super().execute(context)
        add_lights_to_geocode(context.scene.global_settings)
        return {'FINISHED'}


class OT_Exclude3dDataFromGeocodeOperator(ActionOperator):
    bl_idname = "wm.exclude_3d_data_from_geocode"
    bl_label = "Remove a building from the Google Earth 3d data"

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return os.path.isdir(msfs_project.scene_folder) and context.scene.project_settings.geocode != str()

    def execute(self, context):
        super().execute(context)
        exclude_3d_data_from_geocode(context.scene.global_settings)
        return {'FINISHED'}


class OT_Isolate3dDataFromGeocodeOperator(ActionOperator):
    bl_idname = "wm.isolate_3d_data_from_geocode"
    bl_label = "Isolate a building from the Google Earth 3d data"

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return os.path.isdir(msfs_project.scene_folder) and context.scene.project_settings.geocode != str()

    def execute(self, context):
        super().execute(context)
        isolate_3d_data_from_geocode(context.scene.global_settings)
        return {'FINISHED'}


class OT_AddTileCollidersOperator(ActionOperator):
    bl_idname = "wm.add_tile_colliders"
    bl_label = "Add a collider for each tile of the project..."

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return os.path.isdir(msfs_project.scene_folder)

    def execute(self, context):
        super().execute(context)
        add_tile_colliders(context.scene.global_settings)
        return {'FINISHED'}


class OT_RemoveTileCollidersOperator(ActionOperator):
    bl_idname = "wm.remove_tile_colliders"
    bl_label = "Remove the colliders for each tile of the project..."

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return os.path.isdir(msfs_project.scene_folder)

    def execute(self, context):
        super().execute(context)
        remove_tile_colliders(context.scene.global_settings)
        return {'FINISHED'}


class OT_AdjustSceneryAltitudeOperator(ActionOperator):
    bl_idname = "wm.adjust_scenery_altitude"
    bl_label = "Adjusts the altitude of the whole scenery (tiles, objects, colliders, landmarks, height maps)..."

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return os.path.isdir(msfs_project.scene_folder)

    def execute(self, context):
        super().execute(context)
        adjust_scenery_altitude(context.scene.global_settings)
        return {'FINISHED'}


class OT_ResizeSceneryTexturesOperator(ActionOperator):
    bl_idname = "wm.resize_scenery_textures"
    bl_label = "Resize the textures of the tiles of the scenery..."

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return os.path.isdir(msfs_project.scene_folder)

    def execute(self, context):
        super().execute(context)
        resize_scenery_textures(context.scene.global_settings)
        return {'FINISHED'}


class OT_CompressBuiltPackageOperator(ActionOperator):
    bl_idname = "wm.compress_built_package"
    bl_label = "Optimize the built package by compressing the texture files..."

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return os.path.isdir(msfs_project.model_lib_output_folder)

    def execute(self, context):
        super().execute(context)
        compress_built_package(context.scene.global_settings)
        return {'FINISHED'}


class OT_ReloadSettingsOperator(Operator):
    bl_idname = "wm.reload_settings_operator"
    bl_label = "Reload settings..."

    def execute(self, context):
        reload_setting_props(context)
        return {'FINISHED'}


class OT_SaveSettingsOperator(Operator):
    bl_idname = "wm.save_settings_operator"
    bl_label = "Save settings..."

    def execute(self, context):
        context.scene.global_settings.save()
        reload_project_settings(context)
        if context.scene.project_settings is not None:
            context.scene.project_settings.save()
        return {'FINISHED'}


class OT_openSettingsFileOperator(Operator):
    bl_idname = "wm.open_settings_file_operator"
    bl_label = "Open ini file..."

    def execute(self, context):
        os.startfile(os.path.join(context.scene.global_settings.path, INI_FILE))
        return {'FINISHED'}


class OT_addLodOperator(Operator):
    bl_idname = "wm.add_lod_operator"
    bl_label = "Add a new lod..."

    @classmethod
    def poll(cls, context):
        return len(context.scene.project_settings.target_min_size_values) <= MAX_PHOTOGRAMMETRY_LOD

    def execute(self, context):
        context.scene.project_settings.add_lod()
        reload_setting_props(context, reload_settings_file=False)
        return {'FINISHED'}


class OT_removeLowerLodOperator(Operator):
    bl_idname = "wm.remove_lower_lod_operator"
    bl_label = "Remove the lower lod..."

    @classmethod
    def poll(cls, context):
        return len(context.scene.project_settings.target_min_size_values) > 1

    def execute(self, context):
        context.scene.project_settings.remove_lower_lod()
        reload_setting_props(context, reload_settings_file=False)
        return {'FINISHED'}
