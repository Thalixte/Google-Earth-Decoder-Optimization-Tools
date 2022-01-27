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
from uuid import uuid4

from msfs_project.object_xml import MsfsObjectXml
from utils import backup_file, ScriptError


class MsfsObject:
    name: str
    folder: str
    definition_file: str
    xml: MsfsObjectXml

    def __init__(self, folder, name, definition_file):
        self.name = name
        self.folder = folder
        self.definition_file = definition_file
        if not os.path.isfile(os.path.join(self.folder, definition_file)): raise ScriptError("Xml definition file " + os.path.join(self.folder, definition_file) + " does not exist. Check the project folder structure")
        self.xml = MsfsObjectXml(folder, definition_file)

    def backup_files(self, backup_path, dry_mode=False, pbar=None):
        self.backup_file(backup_path, dry_mode=dry_mode, pbar=pbar)

    def remove_files(self):
        self.remove_file()

    def backup_file(self, backup_path, dry_mode=False, pbar=None):
        backup_file(backup_path, self.folder, self.definition_file, dry_mode=dry_mode, pbar=pbar)

    def remove_file(self):
        file_path = os.path.join(self.folder, self.definition_file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(self.definition_file, "removed")

    @staticmethod
    def generate_guid():
        return uuid4()

