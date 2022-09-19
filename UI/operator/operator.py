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
from msfs_project import MsfsProject
from scripts.add_tile_colliders_script import add_tile_colliders
from scripts.clean_package_files_script import clean_package_files
from scripts.fix_tiles_lightning_issues_script import fix_tiles_lightning_issues
from scripts.init_msfs_scenery_project_script import init_msfs_scenery_project
from scripts.merge_sceneries_script import merge_sceneries
from scripts.optimize_scenery_script import optimize_scenery
from scripts.remove_tile_colliders_script import remove_tile_colliders
from scripts.update_min_size_values_script import update_min_size_values
from scripts.compress_built_package_script import compress_built_package
from scripts.update_tiles_position_script import update_tiles_position
from scripts.create_terraform_and_exclusion_polygons_script import create_terraform_and_exclusion_polygons
from utils import open_console
from .tools import reload_current_operator, reload_setting_props
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


class OT_MsfsBuildExePathOperator(FileBrowserOperator):
    bl_idname = "wm.msfs_build_exe_path_operator"
    bl_label = "Path to the MSFS bin exe that builds the MSFS packages..."

    filter_glob: StringProperty(
        default="*.exe",
        options={"HIDDEN"},
    )
    filepath: bpy.props.StringProperty(
        subtype="FILE_PATH"
    )

    def draw(self, context):
        super().draw(context)

    def execute(self, context):
        context.scene.setting_props.msfs_build_exe_path = self.filepath
        reload_current_operator(context)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.filepath = context.scene.setting_props.msfs_build_exe_path
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class OT_CompressonatorExePathOperator(FileBrowserOperator):
    bl_idname = "wm.compressonator_exe_path_operator"
    bl_label = "Path to the compressonator bin exe that compresses the package texture files..."

    filter_glob: StringProperty(
        default="*.exe",
        options={"HIDDEN"},
    )
    filepath: bpy.props.StringProperty(
        subtype="FILE_PATH"
    )

    def draw(self, context):
        super().draw(context)

    def execute(self, context):
        context.scene.setting_props.compressonator_exe_path = self.filepath
        reload_current_operator(context)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.filepath = context.scene.setting_props.compressonator_exe_path
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class OT_CompressonatorExePathOperator(FileBrowserOperator):
    bl_idname = "wm.compressonator_exe_path_operator"
    bl_label = "Path to the compressonator bin exe that compresses the package texture files..."

    filter_glob: StringProperty(
        default="*.exe",
        options={"HIDDEN"},
    )
    filepath: bpy.props.StringProperty(
        subtype="FILE_PATH"
    )

    def draw(self, context):
        super().draw(context)

    def execute(self, context):
        context.scene.setting_props.compressonator_exe_path = self.filepath
        reload_current_operator(context)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.filepath = context.scene.setting_props.compressonator_exe_path
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class ActionOperator(Operator):
    @classmethod
    def poll(cls, context):
        settings = context.scene.settings
        return MsfsProject(settings.projects_path, settings.project_name, settings.definition_file, settings.author_name, settings.sources_path, fast_init=True)

    def execute(self, context):
        # clear and open the system console
        open_console()


class OT_InitMsfsSceneryProjectOperator(ActionOperator):
    bl_idname = "wm.init_msfs_scenery_project"
    bl_label = "Initialize a new MSFS project scenery..."

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        return not os.path.isdir(msfs_project.scene_folder)

    def execute(self, context):
        super().execute(context)
        init_msfs_scenery_project(context.scene.settings)
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
        optimize_scenery(context.scene.settings)
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
        clean_package_files(context.scene.settings)
        return {'FINISHED'}


class OT_MergeSceneriesOperator(ActionOperator):
    bl_idname = "wm.merge_sceneries"
    bl_label = "Merge an existing MSFS scenery project into another one..."

    @classmethod
    def poll(cls, context):
        msfs_project = super().poll(context)
        settings = context.scene.settings
        project_folder_to_merge = os.path.dirname(settings.project_path_to_merge) + os.path.sep
        project_name_to_merge = os.path.relpath(settings.project_path_to_merge, start=project_folder_to_merge)
        definition_file_to_merge = settings.definition_file_to_merge
        msfs_project_to_merge = MsfsProject(settings.projects_path, project_name_to_merge, definition_file_to_merge, settings.author_name, settings.sources_path, fast_init=True)
        return (os.path.isdir(msfs_project.scene_folder) and os.path.isdir(msfs_project_to_merge.scene_folder)) and msfs_project.project_folder != msfs_project_to_merge.project_folder

    def execute(self, context):
        super().execute(context)
        merge_sceneries(context.scene.settings)
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
        update_tiles_position(context.scene.settings)
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
        update_min_size_values(context.scene.settings)
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
        fix_tiles_lightning_issues(context.scene.settings)
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
        create_terraform_and_exclusion_polygons(context.scene.settings)
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
        add_tile_colliders(context.scene.settings)
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
        remove_tile_colliders(context.scene.settings)
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
        compress_built_package(context.scene.settings)
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
        context.scene.settings.save()
        return {'FINISHED'}


class OT_openSettingsFileOperator(Operator):
    bl_idname = "wm.open_settings_file_operator"
    bl_label = "Open ini file..."

    def execute(self, context):
        os.startfile(os.path.join(context.scene.settings.sources_path, INI_FILE))
        return {'FINISHED'}


class OT_addLodOperator(Operator):
    bl_idname = "wm.add_lod_operator"
    bl_label = "Add a new lod..."

    @classmethod
    def poll(cls, context):
        return len(context.scene.settings.target_min_size_values) <= MAX_PHOTOGRAMMETRY_LOD

    def execute(self, context):
        context.scene.settings.add_lod()
        reload_setting_props(context, reload_settings_file=False)
        return {'FINISHED'}


class OT_removeLowerLodOperator(Operator):
    bl_idname = "wm.remove_lower_lod_operator"
    bl_label = "Remove the lower lod..."

    @classmethod
    def poll(cls, context):
        return len(context.scene.settings.target_min_size_values) > 1

    def execute(self, context):
        context.scene.settings.remove_lower_lod()
        reload_setting_props(context, reload_settings_file=False)
        return {'FINISHED'}
