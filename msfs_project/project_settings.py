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

import json
import os
import shutil

from utils.settings import Settings

from constants import ENCODING, PNG_TEXTURE_FORMAT, XML_FILE_EXT, LIGHT_COLD_GUID, CONFIG_TEMPLATES_FOLDER, PROJECT_SETTINGS_TEMPLATE_FILE, INI_FILE_EXT


class ProjectSettings(Settings):
    project_path_to_merge: str
    definition_file_to_merge: str
    backup_enabled: str
    build_package_enabled: str
    target_min_size_values: list
    output_texture_format: str
    lat_correction: float
    lon_correction: float
    airport_city: str
    geocode: str
    geocode_margin: float
    building_margin: float
    ground_exclusion_margin: float
    landmark_type: str
    height_adjustment: float
    height_noise_reduction: float
    landmark_offset: float
    altitude_adjustment: float
    sections = list
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
    keep_residential_and_industrial: str
    process_all: str
    keep_constructions: str
    keep_roads: str
    add_lights: str
    light_guid: str
    collider_as_lower_lod: str

    LODS_SECTION = "LODS"
    TARGET_MIN_SIZE_VALUES_SETTING = "target_min_size_values"

    def __init__(self, global_path, path, project_name):
        self.file_name = project_name + INI_FILE_EXT
        self.project_path_to_merge = str()
        self.definition_file_to_merge = str()
        self.backup_enabled = "True"
        self.build_package_enabled = "True"
        self.target_min_size_values = str()
        self.output_texture_format = PNG_TEXTURE_FORMAT
        self.lat_correction = 0.0
        self.lon_correction = 0.0
        self.airport_city = str()
        self.geocode = str()
        self.geocode_margin = 5.0
        self.building_margin = 0.0
        self.ground_exclusion_margin = 10.0
        self.preserve_roads = "True"
        self.preserve_buildings = "True"
        self.landmark_type = str()
        self.height_adjustment = 0.0
        self.height_noise_reduction = 0.0
        self.landmark_offset = 0.0
        self.altitude_adjustment = 0.0
        self.sections = []
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
        self.keep_residential_and_industrial = "False"
        self.process_all = "False"
        self.isolate_3d_data = "False"
        self.keep_constructions = "False"
        self.keep_roads = "False"
        self.disable_terraform = "False"
        self.add_lights = "False"
        self.light_guid = LIGHT_COLD_GUID
        self.collider_as_lower_lod = "False"

        if not os.path.isfile(os.path.join(path, self.file_name)) and os.path.isdir(path):
            config_template_path = os.path.join(global_path, CONFIG_TEMPLATES_FOLDER)
            shutil.copyfile(os.path.join(config_template_path, PROJECT_SETTINGS_TEMPLATE_FILE), os.path.join(path, self.file_name))

        super().__init__(path)

        # check if the backup of the project files is enabled
        self.backup_enabled = json.loads(self.backup_enabled.lower())

        # check if the package is built at the end of the script
        self.build_package_enabled = json.loads(self.build_package_enabled.lower())

        # get the target lod values
        self.target_min_size_values = str().join(self.target_min_size_values.split()).split(",")

        self.lat_correction = "{:.9f}".format(float(str(self.lat_correction))).rstrip("0").rstrip(".")
        self.lon_correction = "{:.9f}".format(float(str(self.lon_correction))).rstrip("0").rstrip(".")

        self.height_adjustment = "{:.9f}".format(float(str(self.height_adjustment))).rstrip("0").rstrip(".")

        self.height_noise_reduction = "{:.9f}".format(float(str(self.height_noise_reduction))).rstrip("0").rstrip(".")

        self.landmark_offset = "{:.9f}".format(float(str(self.landmark_offset))).rstrip("0").rstrip(".")

        self.altitude_adjustment = "{:.2f}".format(float(str(self.altitude_adjustment))).rstrip("0").rstrip(".")

        self.geocode_margin = "{:.2f}".format(float(str(self.geocode_margin))).rstrip("0").rstrip(".")

        self.building_margin = "{:.2f}".format(float(str(self.geocode_margin))).rstrip("0").rstrip(".")

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
        self.keep_residential_and_industrial = json.loads(self.keep_residential_and_industrial.lower())
        self.process_all = json.loads(self.process_all.lower())
        self.isolate_3d_data = json.loads(self.isolate_3d_data.lower())
        self.keep_constructions = json.loads(self.keep_constructions.lower())
        self.keep_roads = json.loads(self.keep_roads.lower())
        self.disable_terraform = json.loads(self.disable_terraform.lower())
        self.add_lights = json.loads(self.add_lights.lower())

        self.preserve_roads = json.loads(self.preserve_roads.lower())
        self.preserve_buildings = json.loads(self.preserve_buildings.lower())

        self.collider_as_lower_lod = json.loads(self.collider_as_lower_lod.lower())

        if self.definition_file_to_merge == str() and self.project_path_to_merge != str():
            self.definition_file_to_merge = os.path.basename(self.project_path_to_merge).capitalize() + XML_FILE_EXT

    def save(self):
        config = super().set_config(self.path, self.file_name)
        config.set(self.LODS_SECTION, self.TARGET_MIN_SIZE_VALUES_SETTING, ", ".join(self.target_min_size_values))

        with open(os.path.join(self.path, self.file_name), "w", encoding=ENCODING) as configfile:
            config.write(configfile)

    def add_lod(self):
        self.target_min_size_values.insert(0, "0")

    def remove_lower_lod(self):
        self.target_min_size_values.pop(0)
