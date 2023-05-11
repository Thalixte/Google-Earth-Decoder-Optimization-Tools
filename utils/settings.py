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
import os

from constants import ENCODING, MSFS_SDK_INI_SECTION, BUILD_INI_SECTION, \
    COMPRESSONATOR_INI_SECTION, BACKUP_INI_SECTION, PYTHON_INI_SECTION


class Settings:
    file_name = str()
    path = str()
    sections = list

    LODS_SECTION = "LODS"
    TARGET_MIN_SIZE_VALUES_SETTING = "target_min_size_values"

    def __init__(self, path):
        self.path = path
        self.sections = []

        config = cp.ConfigParser()
        if os.path.isfile(os.path.join(path, self.file_name)):
            config.read(os.path.join(path, self.file_name), encoding=ENCODING)
        else:
            return

        self.__rename_and_reorder_sections(config)

        for section_name in config.sections():
            self.sections.append((section_name, section_name, section_name))
            for name, value in config.items(section_name):
                setattr(self, name, value.replace('"', str()))

    def set_config(self, path, file_name):
        config = cp.ConfigParser(comment_prefixes='# ', allow_no_value=True)

        if os.path.isfile(os.path.join(path, file_name)):
            config.read(os.path.join(path, file_name), encoding=ENCODING)
        else:
            return

        for section_name in config.sections():
            for name, value in config.items(section_name):
                config.set(section_name, name, str(getattr(self, name)))

        return config

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)

    def __rename_and_reorder_sections(self, config):
        config = self.rename_section(config, MSFS_SDK_INI_SECTION, BUILD_INI_SECTION)
        config = self.rename_section(config, COMPRESSONATOR_INI_SECTION, COMPRESSONATOR_INI_SECTION)
        config = self.rename_section(config, BACKUP_INI_SECTION, BACKUP_INI_SECTION)
        config = self.rename_section(config, PYTHON_INI_SECTION, PYTHON_INI_SECTION)

        if config is not None:
            with open(os.path.join(self.path, self.file_name), "w", encoding=ENCODING) as configfile:
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
