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
from utils import install_python_lib

try:
    import geopandas as gpd
except ModuleNotFoundError:
    install_python_lib('geopandas')
    import geopandas as gpd

from constants import GLTF_FILE_EXT, COLLIDER_SUFFIX, XML_FILE_EXT, BOUNDARY_OSM_KEY, OSM_FILE_EXT, BOUNDING_BOX_OSM_FILE_PREFIX, HEIGHT_OSM_TAG, BOUNDING_BOX_OSM_KEY, GEOCODE_SUFFIX
from msfs_project.height_map import MsfsHeightMap
from msfs_project.collider import MsfsCollider
from msfs_project.scene_object import MsfsSceneObject
from msfs_project.position import MsfsPosition
from utils import get_coords_from_file_name, get_position_from_file_name, resize_gdf, preserve_holes, clip_gdf, create_bounding_box, union_gdf, difference_gdf, PRESERVE_HOLES_METHOD
from utils.minidom_xml import create_new_definition_file
from msfs_project.osm_xml import OsmXml


class MsfsTile(MsfsSceneObject):
    new_tiles: dict
    exclusion_osm_file: str
    bbox_osm_file: str
    has_rocks: bool
    bbox_gdf: gpd.GeoDataFrame
    exclusion_mask_gdf: gpd.GeoDataFrame
    isolation_mask_gdf: gpd.GeoDataFrame
    height_map: MsfsHeightMap | None

    GE_TILE_ROOF_LIMIT = 18

    def __init__(self, folder, name, definition_file, objects_xml=None):
        super().__init__(folder, name, definition_file)
        self.__calculate_coords()
        pos = self.__calculate_pos()
        altitude = 0.0
        if objects_xml is not None:
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
            if pbar is not None:
                if dry_mode and not os.path.isdir(os.path.join(lod.folder, lod.name)):
                    pbar.range += 1
                else:
                    pbar.update("folder %s created" % lod.name)

    def add_collider(self):
        new_collider = None
        for idx, lod in enumerate(self.lods):
            if idx < (len(self.lods) - 1): continue
            if not os.path.isfile(os.path.join(lod.folder, lod.model_file)): continue
            collider_model_file = self.name + COLLIDER_SUFFIX + GLTF_FILE_EXT
            collider_definition_file_name = self.name + COLLIDER_SUFFIX + XML_FILE_EXT
            lod.create_collider(collider_model_file)
            create_new_definition_file(os.path.join(self.folder, collider_definition_file_name), has_lods=False)
            new_collider = MsfsCollider(self.folder, self.name + COLLIDER_SUFFIX, os.path.join(self.folder, collider_definition_file_name))

        return new_collider

    def add_geocode(self):
        new_geocode = None
        for idx, lod in enumerate(self.lods):
            if idx < (len(self.lods) - 1): continue
            if not os.path.isfile(os.path.join(lod.folder, lod.model_file)): continue
            collider_definition_file_name = self.name + GEOCODE_SUFFIX + XML_FILE_EXT
            create_new_definition_file(os.path.join(self.folder, collider_definition_file_name), has_lods=False)

        return new_geocode

    def define_max_coords(self, other_coords):
        if not self.coords: return tuple([0, 0, 0, 0])
        if not other_coords: return self.coords

        n1, s1, w1, e1 = self.coords
        n2, s2, w2, e2 = other_coords

        if n2 == 0 or s2 == 0 or w2 == 0 or e2 == 0:
            return self.coords

        return tuple([n1 if n1 >= n2 else n2, s1 if s1 <= s2 else s2, w1 if w1 <= w2 else w2, e1 if e1 >= e2 else e2])

    def create_bbox_osm_file(self, dest_folder, min_lod_level):
        if not self.lods:
            return

        min_lod_idx = len(self.lods) - 1
        lod = self.lods[min_lod_idx]
        subtiles = lod.get_subtiles()
        coords = self.coords

        for subtile in subtiles:
            subtile_coords = get_coords_from_file_name(subtile)
            coords = self.define_max_coords(subtile_coords)

        self.bbox_gdf, b = create_bounding_box(coords)
        osm_xml = OsmXml(dest_folder, BOUNDING_BOX_OSM_FILE_PREFIX + "_" + self.name + OSM_FILE_EXT)
        osm_xml.create_from_geodataframes([self.bbox_gdf.drop(labels=BOUNDARY_OSM_KEY, axis=1, errors='ignore')], b)

    def create_exclusion_mask_osm_file(self, dest_folder, b, exclusion_mask, building_mask, water_mask, construction_mask, road_mask, bridges_mask, hidden_roads, amenity_mask, residential_mask, airport_mask, rocks_mask, keep_holes, file_prefix):
        bbox_gdf = resize_gdf(self.bbox_gdf, 10 if keep_holes else 200)
        exclusion_mask_gdf = exclusion_mask.clip(bbox_gdf)

        if rocks_mask is not None:
            tile_rocks = clip_gdf(rocks_mask, self.bbox_gdf)
            self.has_rocks = not tile_rocks.empty

        if not exclusion_mask_gdf.empty:
            if building_mask is not None:
                if not building_mask.empty:
                    building_mask = clip_gdf(building_mask, bbox_gdf)
                    exclusion_mask_gdf = difference_gdf(exclusion_mask_gdf, building_mask)

            if construction_mask is not None:
                if not construction_mask.empty:
                    construction_mask = clip_gdf(construction_mask, bbox_gdf)
                    exclusion_mask_gdf = difference_gdf(exclusion_mask_gdf, construction_mask)

            if road_mask is not None:
                if not road_mask.empty:
                    road_mask = clip_gdf(road_mask, bbox_gdf)

                    if hidden_roads is not None:
                        if not hidden_roads.empty:
                            hidden_roads = clip_gdf(hidden_roads, bbox_gdf)
                            road_mask = difference_gdf(road_mask, hidden_roads)

                    if bridges_mask is not None:
                        if not bridges_mask.empty:
                            bridges_mask = clip_gdf(bridges_mask, bbox_gdf)
                            road_mask = union_gdf(road_mask, bridges_mask)

                    exclusion_mask_gdf = difference_gdf(exclusion_mask_gdf, road_mask)

            if amenity_mask is not None:
                if not amenity_mask.empty:
                    amenity_mask = clip_gdf(amenity_mask, bbox_gdf)
                    exclusion_mask_gdf = difference_gdf(exclusion_mask_gdf, amenity_mask)

            if residential_mask is not None:
                if not residential_mask.empty:
                    residential_mask = clip_gdf(residential_mask, bbox_gdf)
                    exclusion_mask_gdf = difference_gdf(exclusion_mask_gdf, residential_mask)

            if airport_mask is not None:
                if not airport_mask.empty:
                    airport_mask = clip_gdf(airport_mask, bbox_gdf)
                    exclusion_mask_gdf = union_gdf(exclusion_mask_gdf, airport_mask)

            if water_mask is not None:
                if not water_mask.empty:
                    water_mask = clip_gdf(water_mask, bbox_gdf)
                    exclusion_mask_gdf = union_gdf(exclusion_mask_gdf, water_mask)

            file_name = file_prefix + "_" + self.name + OSM_FILE_EXT
            exclusion_mask = exclusion_mask_gdf.drop(labels=BOUNDARY_OSM_KEY, axis=1, errors='ignore')
            if keep_holes:
                exclusion_mask = preserve_holes(exclusion_mask, split_method=PRESERVE_HOLES_METHOD.derivation_split)

            if not exclusion_mask.empty:
                osm_xml = OsmXml(dest_folder, file_name)
                osm_xml.create_from_geodataframes([exclusion_mask], b, True, [(HEIGHT_OSM_TAG, 1000)])

        if not file_prefix:
            self.exclusion_mask_gdf = exclusion_mask_gdf

        return self.name

    def generate_height_data(self, height_map_xml, group_id, altitude, height_adjustment, height_noise_reduction, high_precision=False, inverted=False, positioning_file_path="", water_mask_file_path="", ground_mask_file_path="", debug=False):
        if not self.lods:
            return

        min_lod_idx = len(self.lods) - 1
        lod = self.lods[min_lod_idx]

        if high_precision and len(self.lods) > 0:
            lod = self.lods[0]

        if os.path.isdir(lod.folder):
            height_data, width, altitude = lod.calculate_height_data(self.coords[0], self.coords[2], altitude, height_adjustment, height_noise_reduction, inverted=inverted, positioning_file_path=positioning_file_path, water_mask_file_path=water_mask_file_path, ground_mask_file_path=ground_mask_file_path, debug=debug)
            self.height_map = MsfsHeightMap(tile=self, height_data=height_data, width=width, altitude=altitude, group_id=group_id)
            self.height_map.to_xml(height_map_xml)

    def split(self, settings):
        for i, lod in enumerate(self.lods):
            lod.split(self.name, str(settings.target_min_size_values[(len(self.lods) - 1) - i]), self)

        self.remove_file()

    def __calculate_coords(self):
        self.coords = get_coords_from_file_name(self.name)
        if self.lods:
            lod = self.lods[0]
            subtiles = lod.get_subtiles()

            for subtile in subtiles:
                subtile_coords = get_coords_from_file_name(subtile, is_subtile=True)
                if subtile_coords:
                    self.coords = self.define_max_coords(subtile_coords)

    def __calculate_pos(self):
        result = get_position_from_file_name(self.name.split("_")[-1])

        if self.lods:
            lod = self.lods[0]
            subtiles = lod.get_subtiles()

            for subtile in subtiles:
                subtile_pos = get_position_from_file_name(subtile, is_subtile=True)
                if subtile_pos:
                    result = self.__define_min_pos(result, subtile_pos)

        return result

    @staticmethod
    def __define_min_pos(pos, other_pos):
        lat1, lon1 = pos
        lat2, lon2 = other_pos

        if lat2 == 0 or lon2 == 0:
            return pos

        return [lat1 if lat1 <= lat2 else lat2, lon1 if lon1 <= lon2 else lon2]
