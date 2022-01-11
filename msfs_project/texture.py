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

from msfs_project.lod_resource import MsfsLodResource
from utils import load_json_file, save_json_file, MsfsGltf


class MsfsTexture(MsfsLodResource):
    idx: str
    mime_type: str

    def __init__(self, idx, model_file_path, folder, file, mime_type=str()):
        super().__init__(model_file_path, folder, file)
        self.idx = idx
        self.mime_type = mime_type

    def convert(self, src_format, dest_format):
        from PIL import Image

        try:
            file_path = os.path.join(self.folder, self.file)
            image = Image.open(file_path)
            new_file = self.file.replace(src_format, dest_format)
            image.save(os.path.join(self.folder, new_file))

            try: os.remove(file_path)
            except: pass

            self.file = new_file
            self.mime_type = self.mime_type.replace(src_format, dest_format)
            self.__update_model_file()
        except:
            print("Conversion failed")
            return False

        return True

    def __update_model_file(self):
        model_file = MsfsGltf(os.path.join(self.model_file_path))
        model_file.update_image(self.idx, self.file, self.mime_type)


