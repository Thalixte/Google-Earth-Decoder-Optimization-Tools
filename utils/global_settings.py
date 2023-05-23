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

from utils import Settings

from constants import ENCODING, INI_FILE, XML_FILE_EXT, CONFIG_TEMPLATES_FOLDER, GLOBAL_SETTINGS_TEMPLATE_FILE


class GlobalSettings(Settings):
    sources_path: str
    projects_path: str
    project_name: str
    author_name: str
    definition_file: str
    bake_textures_enabled: str
    nb_parallel_blender_tasks: float
    reload_modules = str
    sources_path: str
    sections = list
    decoder_output_path = str

    LODS_SECTION = "LODS"
    TARGET_MIN_SIZE_VALUES_SETTING = "target_min_size_values"

    def __init__(self, path):
        self.file_name = INI_FILE
        self.projects_path = str()
        self.project_name = str()
        self.author_name = str()
        self.definition_file = str()
        self.bake_textures_enabled = "False"
        self.nb_parallel_blender_tasks = 4.0
        self.reload_modules = "False"
        self.sections = []
        self.decoder_output_path = str()

        if not os.path.isfile(os.path.join(path, self.file_name)):
            config_template_path = os.path.join(path, CONFIG_TEMPLATES_FOLDER)
            shutil.copyfile(os.path.join(config_template_path, GLOBAL_SETTINGS_TEMPLATE_FILE), os.path.join(path, self.file_name))

        super().__init__(path)

        if self.definition_file == str() and self.project_name != str():
            self.definition_file = self.project_name.capitalize() + XML_FILE_EXT

        # reduce the number of texture files (Lily Texture Packer addon is necessary https://gumroad.com/l/DFExj)
        self.bake_textures_enabled = json.loads(self.bake_textures_enabled.lower())

        # check if modules have to be reloaded (mostly for blender dev purpose)
        self.reload_modules = json.loads(self.reload_modules.lower())

        # ensure to convert float settings values
        self.nb_parallel_blender_tasks = int(self.nb_parallel_blender_tasks)

    def save(self):
        config = super().set_config(self.path, self.file_name)

        with open(os.path.join(self.path, self.file_name), "w", encoding=ENCODING) as configfile:
            config.write(configfile)
