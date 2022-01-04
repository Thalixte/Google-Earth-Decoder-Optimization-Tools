import os

from tools import invoke_current_operator
from utils import Settings, get_sources_path

settings = Settings(get_sources_path())

TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX = "target_min_size_value_"


def projects_path_updated(self, context):
    settings.projects_path = self.projects_path_readonly = self.projects_path
    panel_props = context.scene.panel_props
    context.window.cursor_warp(panel_props.first_mouse_x, panel_props.first_mouse_y)
    invoke_current_operator()


def project_path_updated(self, context):
    settings.projects_path = self.projects_path = os.path.dirname(os.path.dirname(self.project_path)) + os.path.sep
    settings.project_name = self.project_name = os.path.relpath(self.project_path, start=self.projects_path)


def project_name_updated(self, context):
    settings.project_name = self.project_name
    settings.project_path = os.path.join(settings.projects_path, settings.project_name)


def author_name_updated(self, context):
    settings.author_name = self.author_name


def bake_textures_enabled_updated(self, context):
    settings.bake_textures_enabled_updated = self.bake_textures_enabled_updated


def output_texture_format_updated(self, context):
    settings.output_texture_format = self.output_texture_format


def backup_enabled_updated(self, context):
    settings.backup_enabled = self.backup_enabled


def lat_correction_updated(self, context):
    settings.lat_correction = "{:.9f}".format(float(str(self.lat_correction))).rstrip("0").rstrip(".")


def lon_correction_updated(self, context):
    settings.lon_correction = "{:.9f}".format(float(str(self.lon_correction))).rstrip("0").rstrip(".")


def target_min_size_value_updated(self, context):
    idx = 0
    prev_value = -1
    for name in self.__annotations__.keys():
        if TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX in name:
            cur_value = int(eval("self." + name))
            cur_value = prev_value if cur_value < prev_value else cur_value
            self[name] = cur_value
            settings.target_min_size_values[idx] = str(cur_value)
            prev_value = int(settings.target_min_size_values[idx])
            idx = idx + 1


def build_package_enabled_updated(self, context):
    settings.build_package_enabled = self.build_package_enabled


def msfs_build_exe_path_updated(self, context):
    settings.msfs_build_exe_path = self.msfs_build_exe_path_readonly = self.msfs_build_exe_path
    invoke_current_operator()


def msfs_steam_version_updated(self, context):
    settings.msfs_steam_version = self.msfs_steam_version


def compressonator_exe_path_updated(self, context):
    settings.compressonator_exe_path = self.compressonator_exe_path_readonly = self.compressonator_exe_path
    invoke_current_operator()


def python_reload_modules_updated(self, context):
    settings.reload_modules = self.python_reload_modules


def setting_sections_updated(self, context):
    self.current_section = self.setting_sections
