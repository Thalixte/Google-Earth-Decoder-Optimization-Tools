import os

import bpy
from constants import TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX
from utils import isolated_print


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
    invoke_current_operator(context)


def invoke_current_operator(context):
    eval("bpy.ops." + context.scene.panel_props.current_operator + "(\"INVOKE_DEFAULT\")")


def reload_project_path(operator, context):
    operator.project_path = os.path.join(context.scene.settings.projects_path, context.scene.settings.project_name) + os.path.sep


def reload_project_name(operator, context):
    operator.project_name = context.scene.settings.project_name


def reload_author_name(operator, context):
    operator.author_name = context.scene.settings.author_name


def reload_bake_textures_enabled(operator, context):
    operator.bake_textures_enabled = context.scene.settings.bake_textures_enabled


def reload_output_texture_format(operator, context):
    operator.output_texture_format = context.scene.settings.output_texture_format


def reload_backup_enabled(operator, context):
    operator.backup_enabled = context.scene.settings.backup_enabled


def reload_lat_correction(operator, context):
    operator.lat_correction = float(context.scene.settings.lat_correction)


def reload_lon_correction(operator, context):
    operator.lon_correction = float(context.scene.settings.lon_correction)


def reload_target_min_size_value(operator, context):
    idx = 0
    for name in operator.__annotations__.keys():
        if TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX in name:
            operator[name] = int(context.scene.settings.target_min_size_values[idx])
            idx = idx + 1


def reload_build_package_enabled(operator, context):
    operator.build_package_enabled = context.scene.settings.build_package_enabled


def reload_msfs_build_exe_path(operator, context):
    operator.msfs_build_exe_path = operator.msfs_build_exe_path_readonly = context.scene.settings.msfs_build_exe_path


def reload_msfs_steam_version(operator, context):
    operator.msfs_steam_version = context.scene.settings.msfs_steam_version


def reload_compressonator_exe_path(operator, context):
    operator.compressonator_exe_path = operator.msfs_steam_version_readonly = context.scene.settings.compressonator_exe_path


def reload_python_reload_modules(operator, context):
    operator.python_reload_modules = context.scene.settings.reload_modules


def reload_setting_props(operator, context):
    reload_project_path(operator, context)
    reload_project_name(operator, context)
    reload_author_name(operator, context)
    reload_bake_textures_enabled(operator, context)
    reload_output_texture_format(operator, context)
    reload_backup_enabled(operator, context)
    reload_lat_correction(operator, context)
    reload_lon_correction(operator, context)
    reload_target_min_size_value(operator, context)
    reload_build_package_enabled(operator, context)
    reload_msfs_build_exe_path(operator, context)
    reload_msfs_steam_version(operator, context)
    reload_compressonator_exe_path(operator, context)
    reload_python_reload_modules(operator, context)