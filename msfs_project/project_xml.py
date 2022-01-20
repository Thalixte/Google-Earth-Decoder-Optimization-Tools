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

from utils import Xml


class MsfsProjectXml(Xml):
    definition_file: str
    OUTPUT_DIRECTORY_TAG = "OutputDirectory"
    PACKAGES_TAG = "Packages"
    PACKAGE_TAG = "Package"

    PACKAGES_SEARCH_PATTERN = "./" + PACKAGES_TAG + "/" + PACKAGE_TAG
    
    def __init__(self, file_folder, file_name):
        super().__init__(file_folder, file_name)
        self.definition_file = str()
        for package in self.find_project_packages():
            self.definition_file = package.text

    def find_project_packages(self):
        return self.root.findall(self.PACKAGES_SEARCH_PATTERN)


