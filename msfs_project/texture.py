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
import importlib
import os

from PIL import ImageEnhance
from PIL.Image import merge

from msfs_project.lod_resource import MsfsLodResource
from msfs_project.gltf import MsfsGltf


class MsfsTexture(MsfsLodResource):
    idx: str
    mime_type: str

    RGB_FORMAT = "RGB"
    RGBA_FORMAT = "RGBA"
    HSV_FORMAT = "HSV"
    RED_RGB_IDX = 0
    GREEN_RGB_IDX = 1
    BLUE_RGB_IDX = 2
    HUE_IDX = 0
    SATURATION_IDX = 1
    VALUE_IDX = 2

    def __init__(self, idx, model_file_path, folder, file, mime_type=str()):
        super().__init__(model_file_path, folder, file)
        self.idx = idx
        self.mime_type = mime_type

    def convert_format(self, src_format, dest_format):
        import PIL
        importlib.reload(PIL)
        from PIL import Image

        try:
            file_path = os.path.join(self.folder, self.file)
            new_file = self.file.replace(src_format, dest_format)

            if os.path.isfile(file_path):
                image = Image.open(file_path)
                if image.mode in (self.RGBA_FORMAT, "P"): image = image.convert(self.RGB_FORMAT)
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

    def adjust_colors(self, settings):
        import PIL
        importlib.reload(PIL)
        from PIL import Image

        try:
            file_path = os.path.join(self.folder, self.file)

            if os.path.isfile(file_path):
                image = Image.open(file_path)
                image = self.__adjust_colors(image, float(settings.red_level), float(settings.green_level), float(settings.blue_level))
                image = self.__adjust_brightness(image, float(settings.brightness))
                image = self.__adjust_contrast(image, float(settings.contrast))
                image = self.__adjust_saturation(image, float(settings.saturation))
                image = self.__adjust_hue(image, float(settings.hue))
                image.save(file_path)
        except:
            print("Colors adjustment failed")
            return False

        return True

    def __update_model_file(self):
        model_file = MsfsGltf(os.path.join(self.model_file_path))
        model_file.update_image(self.idx, self.file, self.mime_type)

    def __adjust_colors(self, image, red_factor, green_factor, blue_factor):
        image = image.convert(self.RGB_FORMAT)
        rr, gg, bb = image.split()
        rr = rr.point(lambda p: 0 if p == 0 else int(p * red_factor))
        gg = gg.point(lambda p: 0 if p == 0 else int(p * green_factor))
        bb = bb.point(lambda p: 0 if p == 0 else int(p * blue_factor))
        image = merge(self.RGB_FORMAT, (rr, gg, bb))

        return image.convert(self.RGBA_FORMAT)

    def __adjust_hue(self, image, deviation):
        image = image.convert(self.HSV_FORMAT)
        hh, ss, vv = image.split()
        hh = hh.point(lambda p: 0 if p == 0 else int(p + deviation))
        image = merge(self.HSV_FORMAT, (hh, ss, vv))
        return image.convert(self.RGBA_FORMAT)

    @staticmethod
    def __adjust_brightness(image, factor):
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)

    @staticmethod
    def __adjust_contrast(image, factor):
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)

    @staticmethod
    def __adjust_saturation(image, factor):
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(factor)
