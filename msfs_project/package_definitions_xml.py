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


class MsfsPackageDefinitionsXml(Xml):
    ASSETS_GROUP_TAG = "AssetGroups"
    ASSET_GROUP_TAG = "AssetGroup"
    ASSET_DIR_TAG = "AssetDir"
    OUTPUT_DIR_TAG = "OutputDir"

    ASSETS_GROUP_SEARCH_PATTERN = "./ASSETS_GROUP"
    SCENERY_OBJECT_LOD_MODEL_FILE_SEARCH_PATTERN = "./" + ASSETS_GROUP_TAG + "/" + ASSET_GROUP_TAG
    
    def __init__(self, file_folder, file_name):
        super().__init__(file_folder, file_name)

    def find_model_lib_asset_group(self, model_lib_folder):
        assets_group = self.root.findall(self.SCENERY_OBJECT_LOD_MODEL_FILE_SEARCH_PATTERN)
        for asset_group in assets_group:
            if model_lib_folder in asset_group.find(self.ASSET_DIR_TAG).text:
                return asset_group.find(self.OUTPUT_DIR_TAG).text.replace("/", "\\")

        return str()


