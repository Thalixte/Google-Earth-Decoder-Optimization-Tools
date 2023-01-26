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
from constants import LIGHT_WARM_GUID
from utils import Xml
import xml.etree.ElementTree as Et


class LightsXml(Xml):
    FS_DATA_TAG = "FSData"
    GROUP_TAG = "Group"
    SCENERY_OBJECT_TAG = "SceneryObject"
    LIBRARY_OBJECT_TAG = "LibraryObject"
    NAME_ATTR = "name"
    DISPLAY_NAME_ATTR = "displayName"
    ALT_ATTR = "alt"
    ALTITUDE_IS_AGL_ATTR = "altitudeIsAgl"
    BANK_ATTR = "bank"
    HEADING_ATTR = "heading"
    IMAGE_COMPLEXITY_ATTR = "imageComplexity"
    LAT_ATTR = "lat"
    LON_ATTR = "lon"
    PITCH_ATTR = "pitch"
    SNAP_TO_GROUND_ATTR = "snapToGround"
    SNAP_TO_NORMAL_ATTR = "snapToNormal"
    SCALE_ATTR = "scale"

    GROUPS_SEARCH_PATTERN = "./" + GROUP_TAG
    SCENERY_OBJECTS_SEARCH_PATTERN = "./" + SCENERY_OBJECT_TAG
    SCENERY_OBJECTS_GROUP_SEARCH_PATTERN = GROUPS_SEARCH_PATTERN + "/" + SCENERY_OBJECT_TAG
    LIBRARY_OBJECTS_SEARCH_PATTERN = SCENERY_OBJECTS_SEARCH_PATTERN + "/" + LIBRARY_OBJECT_TAG
    SCENERY_OBJECT_SEARCH_PATTERN = LIBRARY_OBJECTS_SEARCH_PATTERN + "[@" + NAME_ATTR + "='"
    SCENERY_OBJECT_GROUP_SEARCH_PATTERN = SCENERY_OBJECTS_GROUP_SEARCH_PATTERN + "/" + LIBRARY_OBJECT_TAG + "[@" + NAME_ATTR + "='"

    def __init__(self, file_folder, file_name):
        super().__init__(file_folder, file_name)

    def add_light(self, light):
        self.__add_light(light)
        self.save()

    def remove_lights(self, light_guid=LIGHT_WARM_GUID, lat=None, lon=None, alt=None):
        lights = self.find_lights(light_guid)
        lights_to_remove = [light for light in lights if float(light.get(self.LAT_ATTR)) == float(lat) and float(light.get(self.LON_ATTR)) == float(lon) and float(light.get(self.ALT_ATTR)) == float(alt)]

        for light in lights_to_remove:
            self.root.remove(light)

    def find_lights(self, light_guid=LIGHT_WARM_GUID):
        res = []

        for scenery_object in self.root.findall(self.SCENERY_OBJECT_SEARCH_PATTERN + light_guid.upper() + self.PARENT_PATTERN_SUFFIX):
            res.append(scenery_object)
        for scenery_object in self.root.findall(self.SCENERY_OBJECT_GROUP_SEARCH_PATTERN + light_guid.upper() + self.PARENT_PATTERN_SUFFIX):
            res.append(scenery_object)

        return res

    def __add_light(self, light):
        light_elem = Et.SubElement(self.root, self.SCENERY_OBJECT_TAG, attrib={
            self.DISPLAY_NAME_ATTR: light.name,
            self.ALT_ATTR: str(light.pos.alt),
            self.ALTITUDE_IS_AGL_ATTR: str(True).upper(),
            self.BANK_ATTR: str(0.0),
            self.HEADING_ATTR: str(light.heading),
            self.IMAGE_COMPLEXITY_ATTR: "VERY_SPARSE",
            self.LAT_ATTR: str(light.pos.lat),
            self.LON_ATTR: str(light.pos.lon),
            self.PITCH_ATTR: str(0.0),
            self.SNAP_TO_GROUND_ATTR: str(False).upper(),
            self.SNAP_TO_NORMAL_ATTR: str(False).upper()
        })

        Et.SubElement(light_elem, self.LIBRARY_OBJECT_TAG, attrib={
            self.NAME_ATTR: light.guid,
            self.SCALE_ATTR: str(1.0)
        })

        return light_elem
