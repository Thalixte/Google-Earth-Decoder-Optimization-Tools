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
from bpy.props import IntProperty
from msfs_project.project import MsfsProject
from . import SettingsPropertyGroup
from constants import TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX, MAX_PHOTOGRAMMETRY_LOD
from utils import GlobalSettings


def reload_topbar_menu():
    try:
        if hasattr(bpy.types.TOPBAR_MT_editor_menus.draw, "_draw_funcs"):
            for f in bpy.types.TOPBAR_MT_editor_menus.draw._draw_funcs:
                if not repr(f).startswith("<function TOPBAR_MT_editor_menus.draw"):
                    bpy.types.TOPBAR_MT_editor_menus.draw._draw_funcs.remove(f)
    except AttributeError:
        pass


def reload_current_operator(context):
    panel_props = context.scene.panel_props
    context.window.cursor_warp(panel_props.first_mouse_x, panel_props.first_mouse_y)
    panel_props.invocation_type = "INVOKE_SCREEN"
    invoke_current_operator(context, panel_props.invocation_type)


def invoke_current_operator(context, invocation_type):
    eval("bpy.ops." + context.scene.panel_props.current_operator + "(\"" + invocation_type + "\")")


def reload_project_path(context):
    if os.path.isdir(context.scene.global_settings.projects_path):
        context.scene.setting_props.project_path = os.path.join(context.scene.global_settings.projects_path, context.scene.global_settings.project_name) + os.path.sep
    else:
        context.scene.setting_props.project_path = str()


def reload_project_name(context):
    if os.path.isdir(os.path.join(context.scene.global_settings.projects_path, context.scene.global_settings.project_name)):
        context.scene.setting_props.project_name = context.scene.global_settings.project_name
    else:
        context.scene.setting_props.project_name = str()


def reload_definition_file(context):
    context.scene.setting_props.definition_file = context.scene.global_settings.definition_file


def reload_nb_parallel_blender_tasks(context):
    context.scene.setting_props.nb_parallel_blender_tasks = int(context.scene.global_settings.nb_parallel_blender_tasks)


def reload_project_path_to_merge(context):
    if context.scene.project_settings is not None and os.path.isdir(context.scene.setting_props.project_path_to_merge):
        context.scene.setting_props.project_path_to_merge = context.scene.project_settings.project_path_to_merge + os.path.sep
    else:
        context.scene.setting_props.project_path_to_merge = str()

def reload_definition_file_to_merge(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.definition_file_to_merge = context.scene.project_settings.definition_file_to_merge


def reload_author_name(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.author_name = context.scene.global_settings.author_name


def reload_bake_textures_enabled(context):
    if context.scene.global_settings is not None:
        context.scene.setting_props.bake_textures_enabled = context.scene.global_settings.bake_textures_enabled


def reload_output_texture_format(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.output_texture_format = context.scene.project_settings.output_texture_format


def reload_collider_as_lower_lod(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.collider_as_lower_lod = context.scene.project_settings.collider_as_lower_lod


def reload_backup_enabled(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.backup_enabled = context.scene.project_settings.backup_enabled


def reload_lat_correction(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.lat_correction = float(context.scene.project_settings.lat_correction)


def reload_lon_correction(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.lon_correction = float(context.scene.project_settings.lon_correction)


def reload_target_min_size_value(context):
    if context.scene.project_settings is not None:
        for idx, min_size_value in enumerate(bpy.types.Scene.project_settings.target_min_size_values):
            reverse_idx = (len(bpy.types.Scene.project_settings.target_min_size_values) - 1) - idx
            cur_lod = MAX_PHOTOGRAMMETRY_LOD - reverse_idx
            context.scene.setting_props[TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX + str(cur_lod)] = int(context.scene.project_settings.target_min_size_values[idx])


def reload_airport_city(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.airport_city = context.scene.project_settings.airport_city


def reload_exclude_ground(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.exclude_ground = context.scene.project_settings.exclude_ground


def reload_exclude_nature_reserve(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.exclude_nature_reserve = context.scene.project_settings.exclude_nature_reserve


def reload_exclude_parks(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.exclude_parks = context.scene.project_settings.exclude_parks


def reload_keep_residential_and_industrial(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.keep_residential_and_industrial = context.scene.project_settings.keep_residential_and_industrial


def reload_process_all(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.process_all = context.scene.project_settings.process_all


def reload_high_precision(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.high_precision = context.scene.project_settings.high_precision


def reload_height_adjustment(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.height_adjustment = float(context.scene.project_settings.height_adjustment)


def reload_height_noise_reduction(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.height_noise_reduction = float(context.scene.project_settings.height_noise_reduction)


def reload_geocode(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.geocode = context.scene.project_settings.geocode


def reload_geocode_margin(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.geocode_margin = float(context.scene.project_settings.geocode_margin)


def reload_preserve_roads(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.preserve_roads = context.scene.project_settings.preserve_roads


def reload_preserve_buildings(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.preserve_buildings = context.scene.project_settings.preserve_buildings


def reload_landmark_type(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.landmark_type = context.scene.project_settings.landmark_type


def reload_landmark_offset(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.landmark_offset = float(context.scene.project_settings.landmark_offset)


def reload_add_lights(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.add_lights = context.scene.project_settings.add_lights


def reload_light_guid(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.light_guid = context.scene.project_settings.light_guid


def reload_altitude_adjustment(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.altitude_adjustment = float(context.scene.project_settings.altitude_adjustment)


def reload_build_package_enabled(context):
    if context.scene.project_settings is not None:
        context.scene.setting_props.build_package_enabled = context.scene.project_settings.build_package_enabled


def reload_msfs_build_exe_path(context):
    context.scene.setting_props.msfs_build_exe_path = context.scene.setting_props.msfs_build_exe_path_readonly = context.scene.global_settings.msfs_build_exe_path


def reload_msfs_steam_version(context):
    context.scene.setting_props.msfs_steam_version = context.scene.global_settings.msfs_steam_version


def reload_compressonator_exe_path(context):
    context.scene.setting_props.compressonator_exe_path = context.scene.setting_props.compressonator_exe_path_readonly = context.scene.global_settings.compressonator_exe_path


def reload_python_reload_modules(context):
    context.scene.setting_props.python_reload_modules = context.scene.global_settings.reload_modules


def reload_setting_props_property_group(context, reload_settings_file=True):
    if reload_settings_file:
        sources_path = context.scene.global_settings.path
        del bpy.types.Scene.global_settings
        bpy.types.Scene.global_settings = GlobalSettings(sources_path)

    if hasattr(bpy.types.Scene, "setting_props"):
        del bpy.types.Scene.setting_props

    if bpy.types.Scene.global_settings.projects_path is not str() and bpy.types.Scene.global_settings.project_name is not str():
        project_path = os.path.join(bpy.types.Scene.global_settings.projects_path, bpy.types.Scene.global_settings.project_name)
        if os.path.exists(project_path):
            if reload_settings_file:
                msfs_project = MsfsProject(bpy.types.Scene.global_settings.projects_path, bpy.types.Scene.global_settings.project_name, bpy.types.Scene.global_settings.definition_file, bpy.types.Scene.global_settings.path, bpy.types.Scene.global_settings.author_name, fast_init=True)
                bpy.types.Scene.project_settings = msfs_project.settings

            for idx, min_size_value in enumerate(bpy.types.Scene.project_settings.target_min_size_values):
                reverse_idx = (len(bpy.types.Scene.project_settings.target_min_size_values) - 1) - idx
                cur_lod = MAX_PHOTOGRAMMETRY_LOD - reverse_idx

                SettingsPropertyGroup.__annotations__[TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX + str(cur_lod)] = IntProperty(
                    name=TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX + str(cur_lod),
                    description="set the min size value for the lod " + str(cur_lod),
                    default=int(min_size_value),
                    soft_min=0,
                    soft_max=100,
                    step=1,
                    update=SettingsPropertyGroup.target_min_size_value_updated,
        )

    data = {
        'bl_label': "updatedSettingsPropertyGroup",
        'bl_idname': "wm.updatedSettingsPropertyGroup",
        '__annotations__': SettingsPropertyGroup.__annotations__
    }

    updatedSettingsPropertyGroup = type("updatedSettingsPropertyGroup", (bpy.types.PropertyGroup,), data)
    bpy.utils.register_class(updatedSettingsPropertyGroup)

    bpy.types.Scene.setting_props = bpy.props.PointerProperty(type=updatedSettingsPropertyGroup)


def reload_project_settings(context):
    if context.scene.global_settings.projects_path is not str() and context.scene.global_settings.project_name is not str():
        project_path = os.path.join(context.scene.global_settings.projects_path, context.scene.global_settings.project_name)
        if os.path.exists(project_path) and not hasattr(bpy.types.Scene, "project_settings"):
            msfs_project = MsfsProject(context.scene.global_settings.projects_path, context.scene.global_settings.project_name, context.scene.global_settings.definition_file, context.scene.global_settings.path, context.scene.global_settings.author_name, fast_init=True)
            context.scene.project_settings = bpy.types.Scene.project_settings = msfs_project.settings

def reload_setting_props(context, reload_settings_file=True):
    reload_setting_props_property_group(context, reload_settings_file)

    reload_definition_file(context)
    reload_project_path(context)
    reload_project_name(context)
    reload_definition_file_to_merge(context)
    reload_nb_parallel_blender_tasks(context)
    reload_project_path_to_merge(context)
    reload_author_name(context)
    reload_bake_textures_enabled(context)
    reload_output_texture_format(context)
    reload_collider_as_lower_lod(context)
    reload_backup_enabled(context)
    reload_lat_correction(context)
    reload_lon_correction(context)
    reload_target_min_size_value(context)
    reload_airport_city(context)
    reload_exclude_ground(context)
    reload_exclude_nature_reserve(context)
    reload_exclude_parks(context)
    reload_keep_residential_and_industrial(context)
    reload_process_all(context)
    reload_high_precision(context)
    reload_height_adjustment(context)
    reload_height_noise_reduction(context)
    reload_geocode(context)
    reload_geocode_margin(context)
    reload_preserve_roads(context)
    reload_preserve_buildings(context)
    reload_landmark_type(context)
    reload_landmark_offset(context)
    reload_add_lights(context)
    reload_light_guid(context)
    reload_altitude_adjustment(context)
    reload_build_package_enabled(context)
    reload_msfs_build_exe_path(context)
    reload_msfs_steam_version(context)
    reload_compressonator_exe_path(context)
    reload_python_reload_modules(context)
    reload_project_settings(context)
