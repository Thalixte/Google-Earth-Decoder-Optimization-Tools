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


class MsfsObjectXml(Xml):
    guid: str
    LODS_TAG = "LODS"
    LOD_TAG = "LOD"
    GUID_TAG = "guid"
    MIN_SIZE_TAG = "MinSize"
    MODEL_FILE_TAG = "ModelFile"

    SCENERY_OBJECT_LODS_SEARCH_PATTERN = "./" + LODS_TAG + "/" + LOD_TAG
    SCENERY_OBJECT_LOD_MODEL_FILE_SEARCH_PATTERN = SCENERY_OBJECT_LODS_SEARCH_PATTERN + "[@ModelFile='"
    
    def __init__(self, file_folder, file_name):
        super().__init__(file_folder, file_name)
        guid = self.root.get(self.GUID_TAG)
        if not guid is None:
            self.guid = guid.upper()

    def find_scenery_lods(self):
        return self.root.findall(self.SCENERY_OBJECT_LODS_SEARCH_PATTERN)

    def find_scenery_lod_models(self, file_name):
        return self.root.findall(self.SCENERY_OBJECT_LOD_MODEL_FILE_SEARCH_PATTERN + file_name + self.PATTERN_SUFFIX)


