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

from blender.scene import align_models_with_masks, process_3d_data, create_geocode_bounding_box
from constants import DISPLAY_NAME_OSM_TAG
from msfs_project.light import MsfsLights
from msfs_project.position import MsfsPosition
from utils.console import isolated_print


class MsfsLandmarkLocation:
    class LANDMARK_LOCATION_TYPE:
        city = "City"
        poi = "POI"

    instance_id: str
    name: str
    owner: str
    type: str
    pos: MsfsPosition
    offset: str
    is_in_tiles: bool

    def __init__(self, geocode_gdf=None, tiles=None, owner=None, type=None, alt=None, offset=None, xml=None, elem=None):
        # default landmark location type is POI
        self.type = self.LANDMARK_LOCATION_TYPE.poi
        self.name = str()
        self.is_in_tiles = False

        if geocode_gdf is not None:
            self.__init_from_gdf(geocode_gdf, tiles=tiles, owner=owner, type=type, alt=alt, offset=offset)

        if xml is not None:
            self.__init_from_xml(xml, elem)

    def to_xml(self, xml):
        xml.add_landmark_location(self)
        xml.save()

    @staticmethod
    def add_lights(model_files_paths, positioning_files_paths, landmark_location_file_path, mask_file_path, lat, lon, alt, geocode_prefix, xml, debug=False):
        align_models_with_masks(model_files_paths, positioning_files_paths, mask_file_path)
        process_3d_data(intersect=True, no_bounding_box=True, keep_mask=True)
        lights_gdf = create_geocode_bounding_box(lat, lon, alt, landmark_location_file_path, debug=debug)

        if debug:
            isolated_print(lights_gdf)

        lights = MsfsLights(lights_gdf=lights_gdf, guid=None, prefix=geocode_prefix, name=None)

        if xml:
            lights.to_xml(xml)

    def __init_from_gdf(self, geocode_gdf, tiles=None, owner=None, type=None, alt=None, offset=None):
        if geocode_gdf.empty:
            return

        if alt is not None:
            alt = float(alt)

        self.instance_id = "{" + str(uuid4()).upper() + "}"
        self.owner = owner or str()
        self.pos = MsfsPosition(geocode_gdf.lat, geocode_gdf.lon, "{:.6f}".format(alt or 0.0))
        self.offset = "{:.6f}".format(float(offset) or 0.0)

        if type in self.LANDMARK_LOCATION_TYPE.__dict__.values():
            self.type = type

        if tiles is not None:
            self.__is_in_tiles(tiles)

        if DISPLAY_NAME_OSM_TAG in geocode_gdf:
            name = geocode_gdf[DISPLAY_NAME_OSM_TAG].split(",", 1)
            if len(name) > 0:
                self.name = name[0]

    def __init_from_xml(self, xml, elem):
        self.instance_id = elem.get(xml.INSTANCE_ID_ATTR)
        self.name = elem.get(xml.NAME_ATTR)
        self.pos = MsfsPosition(elem.get(xml.LAT_ATTR), elem.get(xml.LON_ATTR), elem.get(xml.ALT_ATTR))
        self.offset = elem.get(xml.OFFSET_ATTR)
        self.owner = elem.get(xml.OWNER_ATTR)
        self.type = elem.get(xml.TYPE_ATTR)
        self.is_in_tiles = True

    def __is_in_tiles(self, tiles):
        coords = (self.pos.lat, self.pos.lat, self.pos.lon, self.pos.lon)
        for tile in tiles.values():
            if tile.contains(coords):
                self.is_in_tiles = True
                return


class MsfsLandmarks:
    landmark_locations: list

    def __init__(self, geocode_gdf=None, tiles=None, owner=None, type=None, alt=None, offset=None, xml=None):
        self.landmark_locations = []

        if geocode_gdf is not None:
            self.__init_from_gdf(geocode_gdf, tiles=tiles, owner=owner, type=type, alt=alt, offset=offset)

        if xml is not None:
            self.__init_from_xml(xml)

    def __init_from_gdf(self, geocode_gdf, tiles=None, owner=None, type=None, alt=None, offset=None):
        for index, row in geocode_gdf.iterrows():
            self.landmark_locations.append(MsfsLandmarkLocation(geocode_gdf=row, tiles=tiles, owner=owner, type=type, alt=alt, offset=offset))

    def __init_from_xml(self, xml):
        landmarks = xml.find_landmarks()
        for elem in landmarks:
            self.landmark_locations.append(MsfsLandmarkLocation(xml=xml, elem=elem))

    @staticmethod
    def remove_from_xml(xml, name):
        xml.remove_landmark(name)
