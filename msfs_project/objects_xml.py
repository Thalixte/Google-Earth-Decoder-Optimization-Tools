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

import copy
import os
from decimal import Decimal

from constants import HEIGHT_MAP_DISPLAY_NAME, LIGHT_WARM_GUID, LIGHT_HEADING, LIGHTS_DISPLAY_NAME
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
    LANDMARK_LOCATION_TAG = "LandmarkLocation"
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
    INSTANCE_ID_ATTR = "instanceId"
    OFFSET_ATTR = "offset"
    OWNER_ATTR = "owner"
    VERSION_ATTR = "version"

    GROUPS_SEARCH_PATTERN = "./" + GROUP_TAG
    SCENERY_OBJECTS_SEARCH_PATTERN = "./" + SCENERY_OBJECT_TAG
    SCENERY_OBJECTS_GROUP_SEARCH_PATTERN = GROUPS_SEARCH_PATTERN + "/" + SCENERY_OBJECT_TAG
    LIBRARY_OBJECTS_SEARCH_PATTERN = SCENERY_OBJECTS_SEARCH_PATTERN + "/" + LIBRARY_OBJECT_TAG
    SCENERY_OBJECT_SEARCH_PATTERN = LIBRARY_OBJECTS_SEARCH_PATTERN + "[@" + NAME_ATTR + "='"
    SCENERY_OBJECT_GROUP_SEARCH_PATTERN = SCENERY_OBJECTS_GROUP_SEARCH_PATTERN + "/" + LIBRARY_OBJECT_TAG + "[@" + NAME_ATTR + "='"
    SCENERY_OBJECT_GROUP_ID_SEARCH_PATTERN = SCENERY_OBJECTS_SEARCH_PATTERN + "[@" + PARENT_GROUP_ID_ATTR + "='"
    POLYGONS_SEARCH_PATTERN = "./" + POLYGON_TAG
    POLYGONS_GROUP_SEARCH_PATTERN = GROUPS_SEARCH_PATTERN + "./" + POLYGON_TAG
    POLYGON_ATTRIBUTES_SEARCH_PATTERN = "./" + ATTRIBUTE_TAG
    POLYGON_VERTICES_SEARCH_PATTERN = "./" + VERTEX_TAG
    RECTANGLES_SEARCH_PATTERN = "./" + RECTANGLE_TAG
    RECTANGLE_HEIGHT_DATA_SEARCH_PATTERN = "./" + HEIGHT_MAP_TAG
    PARENT_GROUP_SEARCH_PATTERN = GROUPS_SEARCH_PATTERN + "[@" + GROUP_ID_ATTR + "='"
    GROUP_SEARCH_PATTERN = GROUPS_SEARCH_PATTERN + "[@" + DISPLAY_NAME_ATTR + "='"
    POLYGON_SEARCH_PATTERN = POLYGONS_SEARCH_PATTERN + "[@" + PARENT_GROUP_ID_ATTR + "='"
    HEIGHT_MAP_SEARCH_PATTERN = RECTANGLES_SEARCH_PATTERN + "[@" + PARENT_GROUP_ID_ATTR + "='"
    LANDMARKS_SEARCH_PATTERN = "./" + LANDMARK_LOCATION_TAG
    LANDMARK_LOCATION_SEARCH_PATTERN = LANDMARKS_SEARCH_PATTERN + "[@" + NAME_ATTR + "='"
    LANDMARK_LOCATION_INSTANCE_ID_SEARCH_PATTERN = LANDMARKS_SEARCH_PATTERN + "[@" + INSTANCE_ID_ATTR + "='"
    RECTANGLE_DISPLAY_NAME_SEARCH_PATTERN = RECTANGLES_SEARCH_PATTERN + "[@" + DISPLAY_NAME_ATTR + "='"

    FS_DATA_VERSION = 9.0

    def __init__(self, file_folder, file_name):
        super().__init__(file_folder, file_name)

        if not os.path.isfile(self.file_path):
            self.root = Et.Element(self.FS_DATA_TAG)
            self.root.set(self.VERSION_ATTR, str(self.FS_DATA_VERSION))
            self.tree = Et.ElementTree(self.root)

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

    def remove_lights(self, group_name, remove_groups):
        for light in self.find_lights(group_name=group_name):
            self.root.remove(light)

        if remove_groups:
            for group in self.find_groups(group_name=group_name):
                self.root.remove(group)
            self.save()

    def remove_shapes(self, group_name):
        for polygon in self.find_polygons(group_name=group_name):
            self.root.remove(polygon)

        for group in self.find_groups(group_name=group_name):
            self.root.remove(group)

        self.save()

    def remove_height_maps(self, group_name, remove_groups):
        for rectangle in self.find_rectangles(display_name=HEIGHT_MAP_DISPLAY_NAME):
            self.root.remove(rectangle)

        for rectangle in self.find_rectangles(group_name=group_name):
            self.root.remove(rectangle)

        if remove_groups:
            for group in self.find_groups(group_name=group_name):
                self.root.remove(group)
            self.save()

    def remove_landmarks(self, name):
        landmarks = self.find_landmarks(name=name)
        if landmarks:
            for landmark_location in landmarks:
                self.root.remove(landmark_location)

        self.save()

    def add_scenery_object(self, scenery_object, guid):
        self.__add_scenery_object(scenery_object, guid)

    def add_shapes(self, shape, disable_terraform=False):
        for polygon in shape.polygons:
            if not polygon.vertices:
                continue

            polygon_elem = self.__add_shape_polygon(polygon)

            for attribute in polygon.attributes:
                self.__add_shape_polygon_attribute(polygon_elem, attribute)

            for vertex in polygon.vertices:
                self.__add_shape_polygon_vertex(polygon_elem, vertex)

        if hasattr(shape, "group"):
            groups = self.find_groups(group_name=shape.group.display_name)

            if not groups:
                self.__add_generated_group(shape.group)

        self.save()

    def add_height_map(self, height_map):
        if height_map.height_data:
            rectangle_elem = self.__add_height_map_rectangle(height_map)
            self.__add_height_map(rectangle_elem, height_map)

    def add_height_map_group(self, height_map):
        self.__add_generated_group(height_map.group)

    def add_light_group(self, light):
        self.__add_generated_group(light.group)

    def add_landmark_location(self, landmark_location):
        self.__add_landmark_location(landmark_location)

    def add_light(self, light):
        self.__add_light(light)

    def find_all_scenery_objects(self, parent=None):
        root = self.root

        if parent is not None:
            root = parent

        return root.findall(self.SCENERY_OBJECTS_SEARCH_PATTERN)

    def find_scenery_objects(self, guid):
        return self.root.findall(self.SCENERY_OBJECT_SEARCH_PATTERN + guid.upper() + self.PARENT_PATTERN_SUFFIX)

    def find_scenery_objects_parents(self, guid):
        return self.root.findall(self.SCENERY_OBJECT_SEARCH_PATTERN + guid.upper() + self.PARENT_PATTERN_SUFFIX + self.PARENT_SUFFIX)

    def find_scenery_objects_in_group(self, guid):
        return self.root.findall(self.SCENERY_OBJECT_GROUP_SEARCH_PATTERN + guid.upper() + self.PARENT_PATTERN_SUFFIX)

    def find_scenery_objects_in_group_parents(self, guid):
        return self.root.findall(self.SCENERY_OBJECT_GROUP_SEARCH_PATTERN + guid.upper() + self.PARENT_PATTERN_SUFFIX + self.PARENT_SUFFIX)

    def find_groups(self, group_name=None, parent=None):
        pattern = self.GROUPS_SEARCH_PATTERN
        root = self.root

        if parent is not None:
            root = parent

        if group_name is not None:
            pattern = self.GROUP_SEARCH_PATTERN + str(group_name) + self.PATTERN_SUFFIX

        return root.findall(pattern)

    def find_polygons(self, group_name=None, parent=None):
        group_id = -1
        pattern = self.POLYGONS_SEARCH_PATTERN
        root = self.root

        if parent is not None:
            root = parent

        if group_name is not None:
            related_groups = self.find_groups(group_name=group_name)
            for group in related_groups:
                group_id = group.get(self.GROUP_ID_ATTR)
            pattern = self.POLYGON_SEARCH_PATTERN + str(group_id) + self.PATTERN_SUFFIX

        return root.findall(pattern)

    def find_rectangles(self, display_name=None, group_name=None, parent=None):
        group_id = -1
        pattern = self.RECTANGLES_SEARCH_PATTERN
        root = self.root

        if parent is not None:
            root = parent

        if display_name is not None:
            pattern = self.RECTANGLE_DISPLAY_NAME_SEARCH_PATTERN + str(display_name) + self.PATTERN_SUFFIX
            return root.findall(pattern)

        if group_name is not None:
            related_groups = self.find_groups(group_name=group_name)
            for group in related_groups:
                group_id = group.get(self.GROUP_ID_ATTR)
            pattern = self.HEIGHT_MAP_SEARCH_PATTERN + str(group_id) + self.PATTERN_SUFFIX
            return root.findall(pattern)

        return root.findall(pattern)

    def find_polygon_attributes(self, root):
        return root.findall(self.POLYGON_ATTRIBUTES_SEARCH_PATTERN)

    def find_polygon_vertices(self, root):
        return root.findall(self.POLYGON_VERTICES_SEARCH_PATTERN)

    def find_rectangle_height_data(self, root):
        return root.findall(self.RECTANGLE_HEIGHT_DATA_SEARCH_PATTERN)

    def find_landmarks(self, name=None, parent=None):
        result = []
        pattern = self.LANDMARKS_SEARCH_PATTERN
        root = self.root

        if parent is not None:
            root = parent

        if name is not None:
            pattern = self.remove_accents((self.LANDMARK_LOCATION_SEARCH_PATTERN + str(name).replace("'", "") + self.PATTERN_SUFFIX).lower())
            parse_tree = self.to_parseable(copy.deepcopy(self.root))
            elems = parse_tree.findall(pattern)
            for elem in elems:
                instance_id = elem.get(self.INSTANCE_ID_ATTR.lower())
                result = root.findall(self.LANDMARK_LOCATION_INSTANCE_ID_SEARCH_PATTERN + instance_id.upper() + self.PATTERN_SUFFIX)
        else:
            result = root.findall(pattern)

        return result

    def find_lights(self, light_guid=None, group_name=None, parent=None):
        res = []
        group_id = -1
        root = self.root

        if parent is not None:
            root = parent

        if light_guid is not None:
            for scenery_object in self.find_scenery_objects(light_guid):
                res.append(scenery_object)
            for scenery_object in self.find_scenery_objects_in_group(light_guid):
                res.append(scenery_object)

        if group_name is not None:
            related_groups = self.find_groups(group_name=group_name)
            for group in related_groups:
                group_id = group.get(self.GROUP_ID_ATTR)
            pattern = self.SCENERY_OBJECT_GROUP_ID_SEARCH_PATTERN + str(group_id) + self.PATTERN_SUFFIX
            return root.findall(pattern)

        return res

    def get_new_group_id(self):
        result = 0
        groups = self.root.findall(self.GROUPS_SEARCH_PATTERN)

        for group in groups:
            gid = group.get(self.GROUP_ID_ATTR)
            if gid is None:
                continue
            group_id = int(gid)
            result = group_id if group_id > result else result

        return result + 1

    def adjust_altitude(self, altitude_adjustment):
        self.__adjust_all_altitude(self.root, altitude_adjustment)

        scenery_groups = self.find_groups()
        for scenery_group in scenery_groups:
            self.__adjust_all_altitude(scenery_group, altitude_adjustment)

        self.save()

    def __adjust_all_altitude(self, root, altitude_adjustment):
        scenery_objects = self.find_all_scenery_objects(parent=root)
        self.__adjust_scenery_object_altitude(scenery_objects, altitude_adjustment)
        polygons = self.find_polygons(parent=root)
        self.__adjust_polygon_altitude(polygons, altitude_adjustment)
        landmarks = self.find_landmarks(parent=root)
        self.__adjust_landmark_altitude(landmarks, altitude_adjustment)
        rectangles = self.find_rectangles(parent=root)
        self.__adjust_rectangle_altitude(rectangles, altitude_adjustment)

        for rectangle in rectangles:
            height_data = self.find_rectangle_height_data(rectangle)
            self.__adjust_height_map_altitude(height_data, altitude_adjustment)

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

    def __add_scenery_object(self, scenery_object, guid):
        scenery_object_elem = Et.SubElement(self.root, self.SCENERY_OBJECT_TAG, attrib={
            self.ALT_ATTR: "{:.14f}".format(scenery_object.pos.alt),
            self.ALTITUDE_IS_AGL_ATTR: str(False).upper(),
            self.BANK_ATTR: "{:.6f}".format(0.0),
            self.HEADING_ATTR: "{:.6f}".format(0.0),
            self.IMAGE_COMPLEXITY_ATTR: str("VERY_SPARSE"),
            self.LAT_ATTR: "{:.14f}".format(scenery_object.pos.lat),
            self.LON_ATTR: "{:.14f}".format(scenery_object.pos.lon),
            self.PITCH_ATTR: "{:.6f}".format(0.0),
            self.SNAP_TO_GROUND_ATTR: str(False).upper(),
            self.SNAP_TO_NORMAL_ATTR: str(False).upper()
        })

        Et.SubElement(scenery_object_elem, self.LIBRARY_OBJECT_TAG, attrib={
            self.NAME_ATTR: guid,
            self.SCALE_ATTR: "{:.6f}".format(1.0)
        })

        return scenery_object_elem

    def __add_generated_group(self, group):
        attrib = {
            self.DISPLAY_NAME_ATTR: group.display_name,
            self.GROUP_ID_ATTR: str(group.group_id),
            self.GROUP_GENERATED_ATTR: str(group.group_generated).upper()
        }

        if group.group_index > 0:
            attrib[self.GROUP_INDEX_ATTR] = str(group.group_index)

        return Et.SubElement(self.root, group.tag, attrib=attrib)

    def __add_shape_polygon(self, polygon):
        attrib = {
            self.PARENT_GROUP_ID_ATTR: str(polygon.parent_group_id),
            self.ALTITUDE_ATTR: str(polygon.altitude)
        }

        if polygon.group_index > 0:
            attrib[self.GROUP_INDEX_ATTR] = str(polygon.group_index)

        return Et.SubElement(self.root, polygon.tag, attrib=attrib)

    def __add_shape_polygon_attribute(self, polygon, attribute):
        return Et.SubElement(polygon, attribute.tag, attrib={
            self.NAME_ATTR: attribute.name,
            self.GUID_ATTR: attribute.guid,
            self.TYPE_ATTR: attribute.type,
            self.VALUE_ATTR: str(attribute.value)
        })

    def __add_shape_polygon_vertex(self, polygon, vertex):
        return Et.SubElement(polygon, vertex.tag, attrib={
            self.LAT_ATTR: str(vertex.lat),
            self.LON_ATTR: str(vertex.lon)
        })

    def __add_height_map_rectangle(self, height_map):
        return Et.SubElement(self.root, self.RECTANGLE_TAG, attrib={
            self.PARENT_GROUP_ID_ATTR: str(height_map.group.group_id),
            self.DISPLAY_NAME_ATTR: str(height_map.display_name),
            self.WIDTH_ATTR: str(height_map.width),
            self.FALLOFF_ATTR: str(height_map.falloff),
            self.SURFACE_ATTR: height_map.surface,
            self.PRIORITY_ATTR: str(height_map.priority),
            self.LATITUDE_ATTR: str(height_map.pos.lat),
            self.LONGITUDE_ATTR: str(height_map.mid.lon),
            self.ALTITUDE_ATTR: str(height_map.altitude),
            self.LATITUDE2_ATTR: str(height_map.pos2.lat),
            self.LONGITUDE2_ATTR: str(height_map.mid.lon),
            self.ALTITUDE2_ATTR: str(height_map.altitude)
        })

    def __add_height_map(self, rectangle, height_map):
        return Et.SubElement(rectangle, self.HEIGHT_MAP_TAG, attrib={
            self.WIDTH_ATTR: str(height_map.size),
            self.DATA_ATTR: str(height_map.height_data)
        })

    def __add_landmark_location(self, landmark_location):
        attrib = {
            self.INSTANCE_ID_ATTR: str(landmark_location.instance_id),
            self.NAME_ATTR: str(landmark_location.name),
            self.LAT_ATTR: str(landmark_location.pos.lat),
            self.LON_ATTR: str(landmark_location.pos.lon),
            self.ALT_ATTR: str(landmark_location.pos.alt),
            self.OFFSET_ATTR: str(landmark_location.offset),
            self.TYPE_ATTR: str(landmark_location.type)
        }

        if landmark_location.type == landmark_location.LANDMARK_LOCATION_TYPE.city:
            attrib[self.OWNER_ATTR] = str(landmark_location.owner)

        return Et.SubElement(self.root, self.LANDMARK_LOCATION_TAG, attrib=attrib)

    def __add_light(self, light):
        light_elem = Et.SubElement(self.root, self.SCENERY_OBJECT_TAG, attrib={
            self.PARENT_GROUP_ID_ATTR: str(light.group.group_id),
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

    def __update_scenery_object_pos(self, tile, found_scenery_objects, settings):
        for scenery_object in found_scenery_objects:
            new_lat = Decimal(tile.pos.lat) + Decimal(settings.lat_correction)
            new_lon = Decimal(tile.pos.lon) + Decimal(settings.lon_correction)
            scenery_object.set(self.LAT_ATTR, str(new_lat))
            scenery_object.set(self.LON_ATTR, str(new_lon))

    def __adjust_scenery_object_altitude(self, found_scenery_objects, altitude_adjustment):
        for scenery_object in found_scenery_objects:
            cur_alt = float(scenery_object.get(self.ALT_ATTR))
            new_alt = float(Decimal(cur_alt) + Decimal(altitude_adjustment))
            scenery_object.set(self.ALT_ATTR, str(new_alt))

    def __adjust_landmark_altitude(self, found_landmarks, altitude_adjustment):
        for scenery_landmark in found_landmarks:
            cur_alt = float(scenery_landmark.get(self.ALT_ATTR))
            new_alt = float(Decimal(cur_alt) + Decimal(altitude_adjustment))
            scenery_landmark.set(self.ALT_ATTR, str(new_alt))

    def __adjust_polygon_altitude(self, found_polygons, altitude_adjustment):
        for scenery_polygon in found_polygons:
            cur_alt = float(scenery_polygon.get(self.ALTITUDE_ATTR))
            new_alt = float(Decimal(cur_alt) + Decimal(altitude_adjustment))
            scenery_polygon.set(self.ALTITUDE_ATTR, str(new_alt))

    def __adjust_rectangle_altitude(self, found_rectangles, altitude_adjustment):
        for scenery_rectangle in found_rectangles:
            cur_alt = float(scenery_rectangle.get(self.ALTITUDE_ATTR))
            new_alt = float(Decimal(cur_alt) + Decimal(altitude_adjustment))
            scenery_rectangle.set(self.ALTITUDE_ATTR, str(new_alt))

            if scenery_rectangle.get(self.ALTITUDE2_ATTR) is not None:
                cur_alt2 = float(scenery_rectangle.get(self.ALTITUDE2_ATTR))
                new_alt2 = float(Decimal(cur_alt2) + Decimal(altitude_adjustment))
                scenery_rectangle.set(self.ALTITUDE2_ATTR, str(new_alt2))

    def __adjust_height_map_altitude(self, found_height_maps, altitude_adjustment):
        for scenery_height_map in found_height_maps:
            height_data = scenery_height_map.get(self.DATA_ATTR).split()
            for i, height in enumerate(height_data):
                height_data[i] = float(Decimal(height) + Decimal(altitude_adjustment))
            scenery_height_map.set(self.DATA_ATTR, " ".join([str(h) for h in height_data]))
