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
from . import SettingsPropertyGroup
from constants import TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX, MAX_PHOTOGRAMMETRY_LOD
from utils import Settings


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
    context.scene.setting_props.project_path = os.path.join(context.scene.settings.projects_path, context.scene.settings.project_name) + os.path.sep


def reload_project_name(context):
    context.scene.setting_props.project_name = context.scene.settings.project_name


def reload_project_path_to_merge(context):
    context.scene.setting_props.project_path_to_merge = context.scene.settings.project_path_to_merge + os.path.sep


def reload_author_name(context):
    context.scene.setting_props.author_name = context.scene.settings.author_name


def reload_bake_textures_enabled(context):
    context.scene.setting_props.bake_textures_enabled = context.scene.settings.bake_textures_enabled


def reload_output_texture_format(context):
    context.scene.setting_props.output_texture_format = context.scene.settings.output_texture_format


def reload_backup_enabled(context):
    context.scene.setting_props.backup_enabled = context.scene.settings.backup_enabled


def reload_lat_correction(context):
    context.scene.setting_props.lat_correction = float(context.scene.settings.lat_correction)


def reload_lon_correction(context):
    context.scene.setting_props.lon_correction = float(context.scene.settings.lon_correction)


def reload_target_min_size_value(context):
    for idx, min_size_value in enumerate(bpy.types.Scene.settings.target_min_size_values):
        reverse_idx = (len(bpy.types.Scene.settings.target_min_size_values) - 1) - idx
        cur_lod = MAX_PHOTOGRAMMETRY_LOD - reverse_idx
        context.scene.setting_props[TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX + str(cur_lod)] = int(context.scene.settings.target_min_size_values[idx])


def reload_build_package_enabled(context):
    context.scene.setting_props.build_package_enabled = context.scene.settings.build_package_enabled


def reload_msfs_build_exe_path(context):
    context.scene.setting_props.msfs_build_exe_path = context.scene.setting_props.msfs_build_exe_path_readonly = context.scene.settings.msfs_build_exe_path


def reload_msfs_steam_version(context):
    context.scene.setting_props.msfs_steam_version = context.scene.settings.msfs_steam_version


def reload_compressonator_exe_path(context):
    context.scene.setting_props.compressonator_exe_path = context.scene.setting_props.msfs_steam_version_readonly = context.scene.settings.compressonator_exe_path


def reload_python_reload_modules(context):
    context.scene.setting_props.python_reload_modules = context.scene.settings.reload_modules


def reload_setting_props_property_group(context):
    sources_path = context.scene.settings.sources_path
    del bpy.types.Scene.settings
    bpy.types.Scene.settings = Settings(sources_path)

    if hasattr(bpy.types.Scene, "setting_props"):
        del bpy.types.Scene.setting_props

    for idx, min_size_value in enumerate(bpy.types.Scene.settings.target_min_size_values):
        reverse_idx = (len(bpy.types.Scene.settings.target_min_size_values) - 1) - idx
        cur_lod = MAX_PHOTOGRAMMETRY_LOD - reverse_idx

        SettingsPropertyGroup.__annotations__[TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX + str(cur_lod)] = (IntProperty, {
            "name": TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX + str(cur_lod),
            "description": "set the min size value for the lod " + str(cur_lod),
            "default": int(min_size_value),
            "soft_min": 0,
            "soft_max": 100,
            "step": 1,
            "update": SettingsPropertyGroup.target_min_size_value_updated,
        })

    data = {
        'bl_label': "updatedSettingsPropertyGroup",
        'bl_idname': "wm.updatedSettingsPropertyGroup",
        '__annotations__': SettingsPropertyGroup.__annotations__
    }

    updatedSettingsPropertyGroup = type("updatedSettingsPropertyGroup", (bpy.types.PropertyGroup,), data)
    bpy.utils.register_class(updatedSettingsPropertyGroup)

    bpy.types.Scene.setting_props = bpy.props.PointerProperty(type=updatedSettingsPropertyGroup)


def reload_setting_props(context):
    reload_setting_props_property_group(context)

    reload_project_path(context)
    reload_project_name(context)
    reload_project_path_to_merge(context)
    reload_author_name(context)
    reload_bake_textures_enabled(context)
    reload_output_texture_format(context)
    reload_backup_enabled(context)
    reload_lat_correction(context)
    reload_lon_correction(context)
    reload_target_min_size_value(context)
    reload_build_package_enabled(context)
    reload_msfs_build_exe_path(context)
    reload_msfs_steam_version(context)
    reload_compressonator_exe_path(context)
    reload_python_reload_modules(context)
