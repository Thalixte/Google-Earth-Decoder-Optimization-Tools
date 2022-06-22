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
from constants import HEIGHT_MAPS_DISPLAY_NAME
from utils.progress_bar import ProgressBar
from utils import Xml
import xml.etree.ElementTree as Et


class ObjectsXml(Xml):
    FS_DATA_TAG = "FSData"
    GROUP_TAG = "Group"
    SCENERY_OBJECT_TAG = "SceneryObject"
    LIBRARY_OBJECT_TAG = "LibraryObject"
    POLYGON_TAG = "Polygon"
    ATTRIBUTE_TAG = "Attribute"
    VERTEX_TAG = "Vertex"
    RECTANGLE_TAG = "Rectangle"
    HEIGHT_MAP_TAG = "Heightmap"
    NAME_ATTR = "name"
    GUID_ATTR = "guid"
    DISPLAY_NAME_ATTR = "displayName"
    ALT_ATTR = "alt"
    ALTITUDE_IS_AGL_ATTR = "altitudeIsAgl"
    BANK_ATTR = "bank"
    HEADING_ATTR = "heading"
    IMAGE_COMPLEXITY_ATTR = "imageComplexity"
    LAT_ATTR = "lat"
    LATITUDE_ATTR = "latitude"
    LATITUDE2_ATTR = "latitude2"
    LON_ATTR = "lon"
    LONGITUDE_ATTR = "longitude"
    LONGITUDE2_ATTR = "longitude2"
    PITCH_ATTR = "pitch"
    SNAP_TO_GROUND_ATTR = "snapToGround"
    SNAP_TO_NORMAL_ATTR = "snapToNormal"
    SCALE_ATTR = "scale"
    PARENT_GROUP_ID_ATTR = "parentGroupID"
    GROUP_INDEX_ATTR = "groupIndex"
    ALTITUDE_ATTR = "altitude"
    ALTITUDE2_ATTR = "altitude2"
    TYPE_ATTR = "type"
    VALUE_ATTR = "value"
    GROUP_ID_ATTR = "groupID"
    GROUP_GENERATED_ATTR = "groupGenerated"
    WIDTH_ATTR = "width"
    FALLOFF_ATTR = "falloff"
    SURFACE_ATTR = "surface"
    PRIORITY_ATTR = "priority"
    DATA_ATTR = "data"

    LIBRARY_OBJECTS_SEARCH_PATTERN = "./" + SCENERY_OBJECT_TAG + "/" + LIBRARY_OBJECT_TAG
    SCENERY_OBJECT_SEARCH_PATTERN = LIBRARY_OBJECTS_SEARCH_PATTERN + "[@" + NAME_ATTR + "='"
    SCENERY_OBJECT_GROUP_SEARCH_PATTERN = "./" + GROUP_TAG + "/" + SCENERY_OBJECT_TAG + "/" + LIBRARY_OBJECT_TAG + "[@" + NAME_ATTR + "='"
    POLYGONS_SEARCH_PATTERN = "./" + POLYGON_TAG
    POLYGON_ATTRIBUTES_SEARCH_PATTERN = "./" + ATTRIBUTE_TAG
    POLYGON_VERTICES_SEARCH_PATTERN = "./" + VERTEX_TAG
    GROUPS_SEARCH_PATTERN = "./" + GROUP_TAG
    RECTANGLES_SEARCH_PATTERN = "./" + RECTANGLE_TAG
    PARENT_GROUP_SEARCH_PATTERN = GROUPS_SEARCH_PATTERN + "[@" + GROUP_ID_ATTR + "='"
    GROUP_SEARCH_PATTERN = GROUPS_SEARCH_PATTERN + "[@" + DISPLAY_NAME_ATTR + "='"
    POLYGON_SEARCH_PATTERN = POLYGONS_SEARCH_PATTERN + "[@" + PARENT_GROUP_ID_ATTR + "='"
    HEIGHT_MAP_SEARCH_PATTERN = RECTANGLES_SEARCH_PATTERN + "[@" + PARENT_GROUP_ID_ATTR + "='"

    def __init__(self, file_folder, file_name):
        super().__init__(file_folder, file_name)
        self.__convert_objects_guid_to_upper()

    def get_object_altitude(self, guid):
        result = 0

        for scenery_object in self.find_scenery_objects(guid):
            result = scenery_object.get(self.ALT_ATTR)
        for scenery_object in self.find_scenery_objects_in_group(guid):
            result = scenery_object.get(self.ALT_ATTR)

        return result

    def update_objects_position(self, msfs_project, settings):
        self.__update_tiles_pos(msfs_project, settings)
        self.__update_colliders_pos(msfs_project, settings)
        self.save()

    def remove_object(self, guid):
        for scenery_object in self.find_scenery_objects(guid):
            self.root.remove(scenery_object)
        for scenery_object in self.find_scenery_objects_in_group(guid):
            self.root.remove(scenery_object)
        self.save()

    def remove_shapes(self, group_name):
        group_id = -1
        pattern = self.GROUP_SEARCH_PATTERN + group_name + self.PATTERN_SUFFIX

        groups = self.root.findall(pattern)
        for group in groups:
            group_id = group.get(self.GROUP_ID_ATTR)
            self.root.remove(group)

        for polygon in self.find_polygons(group_id=group_id):
            self.root.remove(polygon)

        self.save()

    def remove_height_maps(self):
        group_id = -1
        pattern = self.GROUP_SEARCH_PATTERN + HEIGHT_MAPS_DISPLAY_NAME + self.PATTERN_SUFFIX

        groups = self.root.findall(pattern)
        for group in groups:
            group_id = group.get(self.GROUP_ID_ATTR)
            self.root.remove(group)

        for height_map in self.find_height_maps(group_id):
            self.root.remove(height_map)

        self.save()

    def add_shape(self, shape):
        for polygon in shape.polygons:
            polygon_elem = self.__add_shape_polygon(polygon)

            for attribute in polygon.attributes:
                self.__add_shape_polygon_attribute(polygon_elem, attribute)

            for vertex in polygon.vertices:
                self.__add_shape_polygon_vertex(polygon_elem, vertex)

        pattern = self.GROUP_SEARCH_PATTERN + shape.group.display_name + self.PATTERN_SUFFIX
        groups = self.root.findall(pattern)

        if not groups:
            self.__add_generated_group(shape.group)

        self.save()

    def add_height_map(self, height_map):
        if height_map.height_data:
            rectangle_elem = self.__add_height_map_rectangle(height_map)
            self.__add_height_map(rectangle_elem, height_map)

    def add_height_map_group(self, height_map):
        self.__add_generated_group(height_map.group)

    def find_scenery_objects(self, guid):
        return self.root.findall(self.SCENERY_OBJECT_SEARCH_PATTERN + guid.upper() + self.PARENT_PATTERN_SUFFIX)

    def find_scenery_objects_parents(self, guid):
        return self.root.findall(self.SCENERY_OBJECT_SEARCH_PATTERN + guid.upper() + self.PARENT_PATTERN_SUFFIX + self.PARENT_SUFFIX)

    def find_scenery_objects_in_group(self, guid):
        return self.root.findall(self.SCENERY_OBJECT_GROUP_SEARCH_PATTERN + guid.upper() + self.PARENT_PATTERN_SUFFIX)

    def find_scenery_objects_in_group_parents(self, guid):
        return self.root.findall(self.SCENERY_OBJECT_GROUP_SEARCH_PATTERN + guid.upper() + self.PARENT_PATTERN_SUFFIX + self.PARENT_SUFFIX)

    def find_polygons(self, group_id=None):
        pattern = self.POLYGONS_SEARCH_PATTERN
        if not group_id is None:
            pattern = self.POLYGON_SEARCH_PATTERN + str(group_id) + self.PATTERN_SUFFIX
        return self.root.findall(pattern)

    def find_polygon_attributes(self, root):
        return root.findall(self.POLYGON_ATTRIBUTES_SEARCH_PATTERN)

    def find_polygon_vertices(self, root):
        return root.findall(self.POLYGON_VERTICES_SEARCH_PATTERN)

    def find_height_maps(self, group_id):
        pattern = self.HEIGHT_MAP_SEARCH_PATTERN + str(group_id) + self.PATTERN_SUFFIX
        return self.root.findall(pattern)

    def get_new_group_id(self):
        result = 0
        groups = self.root.findall(self.GROUPS_SEARCH_PATTERN)

        for group in groups:
            gid = group.get(self.GROUP_ID_ATTR)
            if gid is None:
                continue
            group_id = int(gid)
            result = group_id if group_id > result else result

        return result+1

    def __convert_objects_guid_to_upper(self):
        for tag in self.root.findall(self.LIBRARY_OBJECTS_SEARCH_PATTERN):
            if tag.get(self.NAME_ATTR):
                tag.set(self.NAME_ATTR, tag.get(self.NAME_ATTR).upper())

        self.save()

    def __update_tiles_pos(self, msfs_project, settings):
        if not msfs_project.tiles.items():
            return

        pbar = ProgressBar(msfs_project.tiles.items(), title="update tiles positions", sleep=0.000001)
        for guid, tile in pbar.iterable:
            self.__update_scenery_object_pos(tile, self.find_scenery_objects(guid), settings)
            self.__update_scenery_object_pos(tile, self.find_scenery_objects_in_group(guid), settings)

            pbar.update("%s" % tile.name + " : new lat: " + str(tile.pos.lat + float(settings.lat_correction)) + " : new lon: " + str(tile.pos.lon + float(settings.lon_correction)))

    def __update_colliders_pos(self, msfs_project, settings):
        if not msfs_project.colliders.items():
            return

        pbar = ProgressBar(msfs_project.colliders.items(), title="update colliders positions", sleep=0.000001)
        for guid, collider in msfs_project.colliders.items():
            self.__update_scenery_object_pos(collider, self.find_scenery_objects(guid), settings)
            self.__update_scenery_object_pos(collider, self.find_scenery_objects_in_group(guid), settings)

            pbar.update("%s" % collider.name + " : new lat: " + str(collider.pos.lat + float(settings.lat_correction)) + " : new lon: " + str(collider.pos.lon + float(settings.lon_correction)))

    def __add_generated_group(self, group):
        return Et.SubElement(self.root, group.tag, attrib={
            self.DISPLAY_NAME_ATTR: group.display_name,
            self.GROUP_INDEX_ATTR: str(group.group_index),
            self.GROUP_ID_ATTR: str(group.group_id),
            self.GROUP_GENERATED_ATTR: str(group.group_generated).upper()})

    def __add_shape_polygon(self, polygon):
        return Et.SubElement(self.root, polygon.tag, attrib={
            self.PARENT_GROUP_ID_ATTR: str(polygon.parent_group_id),
            self.GROUP_INDEX_ATTR: str(polygon.group_index),
            self.ALTITUDE_ATTR: str(polygon.altitude)})

    def __add_shape_polygon_attribute(self, polygon, attribute):
        return Et.SubElement(polygon, attribute.tag, attrib={
            self.NAME_ATTR: attribute.name,
            self.GUID_ATTR: attribute.guid,
            self.TYPE_ATTR: attribute.type,
            self.VALUE_ATTR: str(attribute.value)})

    def __add_shape_polygon_vertex(self, polygon, vertex):
        return Et.SubElement(polygon, vertex.tag, attrib={
            self.LAT_ATTR: str(vertex.lat),
            self.LON_ATTR: str(vertex.lon)})

    def __add_height_map_rectangle(self, height_map):
        return Et.SubElement(self.root, self.RECTANGLE_TAG, attrib={
            self.PARENT_GROUP_ID_ATTR: str(height_map.group.group_id),
            self.WIDTH_ATTR: str(height_map.width),
            self.FALLOFF_ATTR: str(height_map.falloff),
            self.SURFACE_ATTR: height_map.surface,
            self.PRIORITY_ATTR: str(height_map.priority),
            self.LATITUDE_ATTR: str(height_map.pos.lat),
            self.LONGITUDE_ATTR: str(height_map.mid.lon),
            self.ALTITUDE_ATTR: str(height_map.altitude),
            self.LATITUDE2_ATTR: str(height_map.pos2.lat),
            self.LONGITUDE2_ATTR: str(height_map.mid.lon),
            self.ALTITUDE2_ATTR: str(height_map.altitude)})

    def __add_height_map(self, rectangle, height_map):
        return Et.SubElement(rectangle, self.HEIGHT_MAP_TAG, attrib={
            self.WIDTH_ATTR: str(height_map.size),
            self.DATA_ATTR: str(height_map.height_data)})

    @staticmethod
    def __update_scenery_object_pos(tile, found_scenery_objects, settings):
        for scenery_object in found_scenery_objects:
            new_lat = tile.pos.lat + float(settings.lat_correction)
            new_lon = tile.pos.lon + float(settings.lon_correction)
            scenery_object.set("lat", str(new_lat))
            scenery_object.set("lon", str(new_lon))
