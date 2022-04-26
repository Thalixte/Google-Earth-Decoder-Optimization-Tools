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
import xml.etree.ElementTree as ET
from osmnx.utils_geo import bbox_to_poly

from constants import GLTF_FILE_EXT, COLLIDER_SUFFIX, XML_FILE_EXT, EPSG_KEY, EPSG_VALUE, \
    BOUNDARY_OSM_KEY, OSM_FILE_EXT, BOUNDING_BOX_OSM_FILE_PREFIX
from msfs_project.collider import MsfsCollider
from msfs_project.scene_object import MsfsSceneObject
from msfs_project.position import MsfsPosition
from utils import get_coords_from_file_name, get_position_from_file_name
from utils.minidom_xml import create_new_definition_file


class MsfsTile(MsfsSceneObject):
    new_tiles: dict
    exclusion_osm_file: str
    bbox_osm_file: str

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

        return tuple([n1 if n1 >= n2 else n2, s1 if s1 <= s2 else s2, w1 if w1 <= w2 else w2, e1 if e1 >= e2 else e2])

    def create_osm_files(self, osm_path):
        self.__create_bbox_osm_file(osm_path)

    def split(self, settings):
        for i, lod in enumerate(self.lods):
            lod.split(self.name, str(settings.target_min_size_values[(len(self.lods) - 1) - i]), self)

        self.remove_file()

    def __create_bbox_osm_file(self, osm_path):
        b = bbox_to_poly(self.coords[1], self.coords[0], self.coords[2], self.coords[3])
        bbox = gpd.GeoDataFrame(pd.DataFrame(["box"], index=[("bbox", 1)], columns=[BOUNDARY_OSM_KEY]), crs={"init": EPSG_KEY + str(EPSG_VALUE)}, geometry=[b])
        self.__export_geopandas_to_osm_xml(osm_path, [bbox], b, BOUNDING_BOX_OSM_FILE_PREFIX + "_" + self.name + OSM_FILE_EXT, [("height", 100)])

    def __export_geopandas_to_osm_xml(self, osm_path, geopandas_data_frames, bbox_poly, file_name, additional_tags=[]):
        osm_root = ET.Element("osm", attrib={
            "version": "0.6",
            "generator": "custom python script"
            })

        ET.SubElement(osm_root, "bounds", attrib={
            "minlat": str(bbox_poly.bounds[0]),
            "minlon": str(bbox_poly.bounds[1]),
            "maxlat": str(bbox_poly.bounds[2]),
            "maxlon": str(bbox_poly.bounds[3])})

        for geopandas_data_frame in geopandas_data_frames:
            for index, row in geopandas_data_frame.iterrows():
                if not row.geometry.geom_type is 'Polygon':
                    continue

                i = -1
                current_way = ET.SubElement(osm_root, "way", attrib={
                    "id": str(index[1]),
                    "visible": "true",
                    "version": "1",
                    "uid": str(index[1]),
                    "changeset": "false"})

                for point in row.geometry.exterior.coords:
                    i = i+1
                    current_node = ET.SubElement(osm_root, "node", attrib={
                        "id": str(index[1])+str(i),
                        "visible": "true",
                        "version": "1",
                        "uid": str(index[1]),
                        "lat": str(point[1]),
                        "lon": str(point[0]),
                        "changeset": "false"})

                    ET.SubElement(current_way, "nd", attrib={
                        "ref": str(index[1])+str(i)})

                i = 0
                ET.SubElement(current_way, "nd", attrib={
                    "ref": str(index[1])+str(i)})

                for column in geopandas_data_frame.columns:
                    if column != "geometry" and str(row[column]) != "nan":
                        ET.SubElement(current_node, "tag", attrib={
                            "k": column,
                            "v": str(row[column])})

                        ET.SubElement(current_way, "tag", attrib={
                            "k": column,
                            "v": str(row[column])})

                for additional_tag in additional_tags:
                    ET.SubElement(current_node, "tag", attrib={
                        "k": additional_tag[0],
                        "v": str(additional_tag[1])})

                    ET.SubElement(current_way, "tag", attrib={
                        "k": additional_tag[0],
                        "v": str(additional_tag[1])})

        output_file = ET.ElementTree(element=osm_root)
        output_file.write(os.path.join(osm_path, file_name))
