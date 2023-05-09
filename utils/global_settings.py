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
from utils import Settings

from constants import ENCODING, INI_FILE, XML_FILE_EXT

class GlobalSettings(Settings):
    sources_path: str
    projects_path: str
    project_name: str
    definition_file: str
    nb_parallel_blender_tasks: float
    msfs_build_exe_path: str
    msfs_steam_version: str
    reload_modules = str
    sources_path: str
    compressonator_exe_path = str
    sections = list
    decoder_output_path = str

    LODS_SECTION = "LODS"
    TARGET_MIN_SIZE_VALUES_SETTING = "target_min_size_values"

    def __init__(self, path):
        super().__init__(path)

        self.projects_path = str()
        self.project_name = str()
        self.definition_file = str()
        self.nb_parallel_blender_tasks = 4.0
        self.msfs_build_exe_path = str()
        self.msfs_steam_version = "False"
        self.reload_modules = "False"
        self.compressonator_exe_path = str()
        self.sections = []
        self.decoder_output_path = str()

        if self.definition_file == str() and self.project_name != str():
            self.definition_file = self.project_name.capitalize() + XML_FILE_EXT

        # check if the package is built at the end of the script
        self.msfs_steam_version = json.loads(self.msfs_steam_version.lower())

        # check if modules have to be reloaded (mostly for blender dev purpose)
        self.reload_modules = json.loads(self.reload_modules.lower())

        # ensure to convert float settings values
        self.nb_parallel_blender_tasks = int(self.nb_parallel_blender_tasks)

    def save(self):
        config = super().set_config()

        with open(os.path.join(self.sources_path, INI_FILE), "w", encoding=ENCODING) as configfile:
            config.write(configfile)
