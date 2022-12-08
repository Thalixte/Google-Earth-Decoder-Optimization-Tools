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

import configparser as cp
import json
import os

from constants import ENCODING, PNG_TEXTURE_FORMAT, INI_FILE, MSFS_SDK_INI_SECTION, BUILD_INI_SECTION, \
    COMPRESSONATOR_INI_SECTION, BACKUP_INI_SECTION, PYTHON_INI_SECTION, XML_FILE_EXT


class Settings:
    sources_path: str
    projects_path: str
    project_name: str
    definition_file: str
    nb_parallel_blender_tasks: float
    project_path_to_merge: str
    definition_file_to_merge: str
    author_name: str
    msfs_build_exe_path: str
    backup_enabled: str
    bake_textures_enabled: str
    msfs_steam_version: str
    build_package_enabled: str
    reload_modules = str
    sources_path: str
    target_min_size_values: list
    output_texture_format: str
    lat_correction: float
    lon_correction: float
    compressonator_exe_path = str
    airport_city: str
    geocode: str
    geocode_margin: float
    ground_exclusion_margin: float
    landmark_type: str
    height_adjustment: float
    landmark_offset: float
    sections = list
    decoder_output_path = str
    red_level: float
    green_level: float
    blue_level: float
    brightness: float
    contrast: float
    saturation: float
    hue: float
    high_precision: str
    exclude_ground: str
    exclude_nature_reserve: str
    exclude_parks: str

    LODS_SECTION = "LODS"
    TARGET_MIN_SIZE_VALUES_SETTING = "target_min_size_values"

    def __init__(self, sources_path=str()):
        self.sources_path = sources_path
        self.projects_path = str()
        self.project_name = str()
        self.definition_file = str()
        self.nb_parallel_blender_tasks = 4.0
        self.project_path_to_merge = str()
        self.definition_file_to_merge = str()
        self.author_name = str()
        self.msfs_build_exe_path = str()
        self.backup_enabled = "False"
        self.bake_textures_enabled = "False"
        self.msfs_steam_version = "False"
        self.build_package_enabled = "False"
        self.reload_modules = "False"
        self.sources_path = sources_path
        self.target_min_size_values = []
        self.output_texture_format = PNG_TEXTURE_FORMAT
        self.lat_correction = 0.0
        self.lon_correction = 0.0
        self.compressonator_exe_path = str()
        self.airport_city = str()
        self.geocode = str()
        self.geocode_margin = 5.0
        self.ground_exclusion_margin = 10.0
        self.preserve_roads = "True"
        self.preserve_buildings = "True"
        self.landmark_type = str()
        self.height_adjustment = 0.0
        self.landmark_offset = 0.0
        self.sections = []
        self.decoder_output_path = str()
        self.red_level = 1.0
        self.green_level = 1.0
        self.blue_level = 1.0
        self.brightness = 1.0
        self.contrast = 1.0
        self.saturation = 1.0
        self.hue = 1.0
        self.high_precision = "False"
        self.exclude_ground = "False"
        self.exclude_nature_reserve = "False"
        self.exclude_parks = "False"
        self.isolate_3d_data = "False"
        self.keep_roads = "False"
        self.disable_terraform = "False"

        config = cp.ConfigParser()
        if os.path.isfile(INI_FILE):
            config.read(INI_FILE, encoding=ENCODING)
        else:
            config.read(os.path.join(sources_path, INI_FILE), encoding=ENCODING)

        self.__rename_and_reorder_sections(config)

        for section_name in config.sections():
            self.sections.append((section_name, section_name, section_name))
            for name, value in config.items(section_name):
                setattr(self, name, value.replace('"', str()))

        if self.definition_file == str() and self.project_name != str():
            self.definition_file = self.project_name.capitalize() + XML_FILE_EXT

        # reduce the number of texture files (Lily Texture Packer addon is necessary https://gumroad.com/l/DFExj)
        self.bake_textures_enabled = json.loads(self.bake_textures_enabled.lower())

        # check if the package is built at the end of the script
        self.msfs_steam_version = json.loads(self.msfs_steam_version.lower())

        # check if the backup of the project files is enabled
        self.backup_enabled = json.loads(self.backup_enabled.lower())

        # check if the package is built at the end of the script
        self.build_package_enabled = json.loads(self.build_package_enabled.lower())

        # check if modules have to be reloaded (mostly for blender dev purpose)
        self.reload_modules = json.loads(self.reload_modules.lower())

        # get the target lod values
        self.target_min_size_values = str().join(self.target_min_size_values.split()).split(",")

        # ensure to convert float settings values
        self.nb_parallel_blender_tasks = int(self.nb_parallel_blender_tasks)

        self.lat_correction = "{:.9f}".format(float(str(self.lat_correction))).rstrip("0").rstrip(".")
        self.lon_correction = "{:.9f}".format(float(str(self.lon_correction))).rstrip("0").rstrip(".")

        self.height_adjustment = "{:.9f}".format(float(str(self.height_adjustment))).rstrip("0").rstrip(".")

        self.landmark_offset = "{:.9f}".format(float(str(self.landmark_offset))).rstrip("0").rstrip(".")

        self.geocode_margin = "{:.2f}".format(float(str(self.geocode_margin))).rstrip("0").rstrip(".")

        self.ground_exclusion_margin = "{:.2f}".format(float(str(self.ground_exclusion_margin))).rstrip("0").rstrip(".")

        self.red_level = "{:.2f}".format(float(str(self.red_level))).rstrip("0").rstrip(".")
        self.green_level = "{:.2f}".format(float(str(self.green_level))).rstrip("0").rstrip(".")
        self.blue_level = "{:.2f}".format(float(str(self.blue_level))).rstrip("0").rstrip(".")
        self.brightness = "{:.2f}".format(float(str(self.brightness))).rstrip("0").rstrip(".")
        self.contrast = "{:.2f}".format(float(str(self.contrast))).rstrip("0").rstrip(".")
        self.saturation = "{:.2f}".format(float(str(self.saturation))).rstrip("0").rstrip(".")
        self.hue = "{:.2f}".format(float(str(self.hue))).rstrip("0").rstrip(".")

        self.high_precision = json.loads(self.high_precision.lower())
        self.exclude_ground = json.loads(self.exclude_ground.lower())
        self.exclude_nature_reserve = json.loads(self.exclude_nature_reserve.lower())
        self.exclude_parks = json.loads(self.exclude_parks.lower())
        self.isolate_3d_data = json.loads(self.isolate_3d_data.lower())
        self.keep_roads = json.loads(self.keep_roads.lower())
        self.disable_terraform = json.loads(self.disable_terraform.lower())

        self.preserve_roads = json.loads(self.preserve_roads.lower())
        self.preserve_buildings = json.loads(self.preserve_buildings.lower())

        if self.definition_file_to_merge == str() and self.project_path_to_merge != str():
            self.definition_file_to_merge = os.path.basename(self.project_path_to_merge).capitalize() + XML_FILE_EXT

    def save(self):
        config = cp.ConfigParser(comment_prefixes='# ', allow_no_value=True)
        if os.path.isfile(INI_FILE):
            config.read(INI_FILE, encoding=ENCODING)
        else:
            config.read(os.path.join(self.sources_path, INI_FILE), encoding=ENCODING)

        for section_name in config.sections():
            for name, value in config.items(section_name):
                config.set(section_name, name, str(getattr(self, name)))

        config.set(self.LODS_SECTION, self.TARGET_MIN_SIZE_VALUES_SETTING, ", ".join(self.target_min_size_values))

        with open(os.path.join(self.sources_path, INI_FILE), "w", encoding=ENCODING) as configfile:
            config.write(configfile)

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)

    def add_lod(self):
        self.target_min_size_values.insert(0, "0")

    def remove_lower_lod(self):
        self.target_min_size_values.pop(0)

    def __rename_and_reorder_sections(self, config):
        config = self.rename_section(config, MSFS_SDK_INI_SECTION, BUILD_INI_SECTION)
        config = self.rename_section(config, COMPRESSONATOR_INI_SECTION, COMPRESSONATOR_INI_SECTION)
        config = self.rename_section(config, BACKUP_INI_SECTION, BACKUP_INI_SECTION)
        config = self.rename_section(config, PYTHON_INI_SECTION, PYTHON_INI_SECTION)

        if config is not None:
            with open(os.path.join(self.sources_path, INI_FILE), "w", encoding=ENCODING) as configfile:
                config.write(configfile)

    @staticmethod
    def rename_section(config, section_from, section_to):
        items = []

        if config is None: return
        if section_from is not section_to and config.has_section(section_to): return

        if config.has_section(section_from):
            items = config.items(section_from)

        config.remove_section(section_from)
        config.add_section(section_to)
        for item in items:
            config.set(section_to, item[0], item[1])

        return config
