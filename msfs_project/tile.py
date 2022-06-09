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

import geopandas as gpd

from constants import GLTF_FILE_EXT, COLLIDER_SUFFIX, XML_FILE_EXT, BOUNDARY_OSM_KEY, OSM_FILE_EXT, BOUNDING_BOX_OSM_FILE_PREFIX, EXCLUSION_OSM_FILE_PREFIX, HEIGHT_OSM_TAG, EOL
from msfs_project.height_map import HeightMap
from msfs_project.collider import MsfsCollider
from msfs_project.scene_object import MsfsSceneObject
from msfs_project.position import MsfsPosition
from utils import get_coords_from_file_name, get_position_from_file_name, create_tile_bounding_box, resize_gdf, preserve_holes
from utils.minidom_xml import create_new_definition_file
from msfs_project.osm_xml import OsmXml


class MsfsTile(MsfsSceneObject):
    new_tiles: dict
    exclusion_osm_file: str
    bbox_osm_file: str
    has_rocks: bool
    bbox_gdf: gpd.GeoDataFrame
    exclusion_mask_gdf: gpd.GeoDataFrame
    height_map: HeightMap | None

    GE_TILE_ROOF_LIMIT = 18

    def __init__(self, folder, name, definition_file, objects_xml=None):
        super().__init__(folder, name, definition_file)
        self.coords = get_coords_from_file_name(self.name)
        pos = get_position_from_file_name(self.name)
        altitude = 0.0
        if not objects_xml is None:
            altitude = float(objects_xml.get_object_altitude(self.xml.guid))
        self.pos = MsfsPosition(pos[0], pos[1], altitude)
        self.new_tiles = {}
        self.height_map = None
        self.has_rocks = False

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

    def create_bbox_osm_file(self, dest_folder):
        self.bbox_gdf, b = create_tile_bounding_box(self)
        osm_xml = OsmXml(dest_folder, BOUNDING_BOX_OSM_FILE_PREFIX + "_" + self.name + OSM_FILE_EXT)
        osm_xml.create_from_geodataframes([self.bbox_gdf.drop(labels=BOUNDARY_OSM_KEY, axis=1, errors='ignore')], b)

    def create_exclusion_mask_osm_file(self, dest_folder, b, exclusion_mask, buildings_and_water=False):
        self.exclusion_mask_gdf = exclusion_mask.clip(self.bbox_gdf)

        if not self.exclusion_mask_gdf.empty:
            bbox_gdf = resize_gdf(self.bbox_gdf, 10)
            file_name = EXCLUSION_OSM_FILE_PREFIX + "_" + self.name + ("_buildings_and_water" if buildings_and_water else "") + OSM_FILE_EXT
            exclusion_mask = exclusion_mask.clip(bbox_gdf).drop(labels=BOUNDARY_OSM_KEY, axis=1, errors='ignore')

            if not buildings_and_water:
                exclusion_mask = preserve_holes(exclusion_mask)

            osm_xml = OsmXml(dest_folder, file_name)
            osm_xml.create_from_geodataframes([exclusion_mask], b, True, [(HEIGHT_OSM_TAG, 1000)])

    def generate_height_data(self, name, height_map_xml, group_id, altitude, inverted=False, positioning_file_path="", mask_file_path=""):
        if not self.lods:
            return

        min_lod = len(name)
        min_lod_idx = len(self.lods) - 1
        lod_limit_diff = self.GE_TILE_ROOF_LIMIT - min_lod if self.GE_TILE_ROOF_LIMIT > min_lod else 0
        lod = self.lods[min_lod_idx - lod_limit_diff]

        if os.path.isdir(lod.folder):
            height_data, width, altitude, grid_limit = lod.calculate_height_data(self.coords[0], self.coords[2], altitude, inverted=inverted, positioning_file_path=positioning_file_path, mask_file_path=mask_file_path)
            self.height_map = HeightMap(tile=self, height_data=height_data, width=width, altitude=altitude, grid_limit=grid_limit, group_id=group_id)
            self.height_map.to_xml(height_map_xml)

    def split(self, settings):
        for i, lod in enumerate(self.lods):
            lod.split(self.name, str(settings.target_min_size_values[(len(self.lods) - 1) - i]), self)

        self.remove_file()
