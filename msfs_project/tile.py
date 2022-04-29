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

import pandas as pd
import geopandas as gpd
from osmnx.utils_geo import bbox_to_poly

from constants import GLTF_FILE_EXT, COLLIDER_SUFFIX, XML_FILE_EXT, EPSG_KEY, EPSG_VALUE, \
    BOUNDARY_OSM_KEY, OSM_FILE_EXT, BOUNDING_BOX_OSM_FILE_PREFIX, BOUNDING_BOX_OSM_KEY
from msfs_project.collider import MsfsCollider
from msfs_project.scene_object import MsfsSceneObject
from msfs_project.position import MsfsPosition
from utils import get_coords_from_file_name, get_position_from_file_name
from utils.minidom_xml import create_new_definition_file
from msfs_project.osm_xml import OsmXml


class MsfsTile(MsfsSceneObject):
    new_tiles: dict
    exclusion_osm_file: str
    bbox_osm_file: str
    bbox_gdf: gpd.GeoDataFrame

    def __init__(self, folder, name, definition_file):
        super().__init__(folder, name, definition_file)
        self.coords = get_coords_from_file_name(self.name)
        pos = get_position_from_file_name(self.name)
        self.pos = MsfsPosition(pos[0], pos[1], 0)
        self.new_tiles = {}

    def create_optimization_folders(self, linked_tiles, dry_mode=False, pbar=None):
        other_tiles = [tile for tile in linked_tiles if tile.name != self.name]
        for lod in self.lods:
            if lod.optimized: continue
            if not dry_mode:
                lod.create_optimization_folder(other_tiles)
            if not pbar is None:
                if dry_mode and not os.path.isdir(os.path.join(lod.folder, lod.name)):
                    pbar.range += 1
                else:
                    pbar.update("folder %s created" % lod.name)

    def add_collider(self):
        new_collider = None
        for idx, lod in enumerate(self.lods):
            if idx < (len(self.lods) - 1): continue
            collider_model_file = self.name + COLLIDER_SUFFIX + GLTF_FILE_EXT
            collider_definition_file_name = self.name + COLLIDER_SUFFIX + XML_FILE_EXT
            lod.create_collider(collider_model_file)
            create_new_definition_file(os.path.join(self.folder, collider_definition_file_name), has_lods=False)
            new_collider = MsfsCollider(self.folder, self.name + COLLIDER_SUFFIX, os.path.join(self.folder, collider_definition_file_name))

        return new_collider

    def define_max_coords(self, max_coords):
        n1, s1, w1, e1 = self.coords
        n2, s2, w2, e2 = max_coords

        if n2 == 0 or s2 == 0 or w2 == 0 or e2 == 0:
            return self.coords

        return tuple([n1 if n1 >= n2 else n2, s1 if s1 <= s2 else s2, w1 if w1 <= w2 else w2, e1 if e1 >= e2 else e2])

    def create_osm_files(self, osm_path):
        self.__create_bbox_osm_file(osm_path)

    def split(self, settings):
        for i, lod in enumerate(self.lods):
            lod.split(self.name, str(settings.target_min_size_values[(len(self.lods) - 1) - i]), self)

        self.remove_file()

    def __create_bbox_osm_file(self, osm_path):
        b = bbox_to_poly(self.coords[1], self.coords[0], self.coords[2], self.coords[3])
        self.bbox_gdf = gpd.GeoDataFrame(pd.DataFrame([BOUNDING_BOX_OSM_FILE_PREFIX + "/1"], index=[(BOUNDING_BOX_OSM_FILE_PREFIX, 1)], columns=[BOUNDARY_OSM_KEY]), crs={"init": EPSG_KEY + str(EPSG_VALUE)}, geometry=[b])
        osm_xml = OsmXml(osm_path, BOUNDING_BOX_OSM_FILE_PREFIX + "_" + self.name + OSM_FILE_EXT)
        osm_xml.create_from_geodataframes([self.bbox_gdf], b, [("height", 100)])
