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

from uuid import uuid4

from shapely.geometry import Polygon, MultiPolygon

from constants import TERRAFORMING_POLYGONS_DISPLAY_NAME
from utils import SHAPELY_TYPE


class MsfsShapeAttribute:
    tag: str
    name: str
    guid: str
    type: str
    value: str

    def __init__(self, name, guid, type, value):
        self.tag = "Attribute"
        self.name = name
        self.guid = guid
        self.type = type
        self.value = value


class MsfsShapeVertex:
    tag: str
    lat: float
    lon: float

    def __init__(self, point):
        self.tag = "Vertex"
        self.lat = point[1]
        self.lon = point[0]


class MsfsShapePolygon:
    class SHAPE_ATTRIBUTE_TYPE:
        uint8 = "UINT8"
        uint32 = "UINT32"
        float32 = "FLOAT32"
        guid = "GUID"

    tag: str
    altitude: float
    parent_group_id: int
    group_index: int
    vertices: list
    unique_guid = MsfsShapeAttribute
    flatten_falloff = MsfsShapeAttribute
    flatten_mode = MsfsShapeAttribute
    exclude_tin = MsfsShapeAttribute
    exclude_detected_buildings = MsfsShapeAttribute
    exclude_osm_buildings = MsfsShapeAttribute
    exclude_ms_buildings = MsfsShapeAttribute
    building_on_tin = MsfsShapeAttribute
    force_detected_building = MsfsShapeAttribute
    exclusion_flags = MsfsShapeAttribute
    vegetation_scale = MsfsShapeAttribute
    vegetation_density = MsfsShapeAttribute
    vegetation_falloff = MsfsShapeAttribute
    tree_brightness_factor = MsfsShapeAttribute
    water_type = MsfsShapeAttribute
    land_class_remap = MsfsShapeAttribute
    airport_size = MsfsShapeAttribute
    layer = MsfsShapeAttribute

    def __init__(self, polygon=None, xml=None, elem=None, parent_group_id=None, group_index=None, flatten=False, exclude_buildings=False, exclude_roads=False, exclude_vegetation=False):
        self.tag = SHAPELY_TYPE.polygon
        self.altitude = 0.0
        self.parent_group_id = parent_group_id
        self.group_index = group_index
        self.attributes = []
        self.vertices = []
        self.unique_guid = MsfsShapeAttribute(name="UniqueGUID", guid="{359C73E8-06BE-4FB2-ABCB-EC942F7761D0}", type=self.SHAPE_ATTRIBUTE_TYPE.guid, value="{FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF}")
        self.flatten_falloff = MsfsShapeAttribute(name="FlattenFalloff", guid="{5548FDB5-2267-4328-8E6F-FD0A45ADEC8F}", type=self.SHAPE_ATTRIBUTE_TYPE.float32, value="200.000000")
        self.flatten_mode = MsfsShapeAttribute(name="FlattenMode", guid="{065E9D4D-6984-4D2A-91FD-3C33C4F53B22}", type=self.SHAPE_ATTRIBUTE_TYPE.uint8, value="0")
        self.exclude_tin = MsfsShapeAttribute(name="ExcludeTIN", guid="{18B58CBF-AE02-4A19-8AA9-3809E8E73400}", type=self.SHAPE_ATTRIBUTE_TYPE.uint8, value="0")
        self.exclude_detected_buildings = MsfsShapeAttribute(name="ExcludeDetectedBuildings", guid="{5C1A2387-1F07-47DF-A569-962CF6258E55}", type=self.SHAPE_ATTRIBUTE_TYPE.uint8, value="0")
        self.exclude_osm_buildings = MsfsShapeAttribute(name="ExcludeOSMBuildings", guid="{F3C2635D-9F2F-458F-8663-90B3837BED09}", type=self.SHAPE_ATTRIBUTE_TYPE.uint8, value="0")
        self.exclude_ms_buildings = MsfsShapeAttribute(name="ExcludeMSBuildings", guid="{F78A3074-8AD5-4B8B-92C4-C1C948BB7AA5}", type=self.SHAPE_ATTRIBUTE_TYPE.uint8, value="0")
        self.building_on_tin = MsfsShapeAttribute(name="BuildingOnTIN", guid="{4C252581-63E9-4C22-8A3D-14B31F3C8157}", type=self.SHAPE_ATTRIBUTE_TYPE.uint8, value="0")
        self.force_detected_building = MsfsShapeAttribute(name="ForceDetectedBuilding", guid="{69A63EDD-FBE5-4F0D-88E6-6FA01963D613}", type=self.SHAPE_ATTRIBUTE_TYPE.uint8, value="0")
        self.exclusion_flags = MsfsShapeAttribute(name="ExclusionFlags", guid="{4CACC252-E6DC-419A-B20C-16EC601DF70E}", type=self.SHAPE_ATTRIBUTE_TYPE.uint32, value="0")
        self.vegetation_scale = MsfsShapeAttribute(name="VegetationScale", guid="{6A043F59-E6F2-4117-A2E4-D510E7317C29}", type=self.SHAPE_ATTRIBUTE_TYPE.uint32, value="127")
        self.vegetation_density = MsfsShapeAttribute(name="VegetationDensity", guid="{41EFF715-C392-4B31-A457-50A504353A90}", type=self.SHAPE_ATTRIBUTE_TYPE.uint32, value="31")
        self.vegetation_falloff = MsfsShapeAttribute(name="VegetationFalloff", guid="{E82ABE17-FB4C-4F67-A28C-ED41969AEAD6}", type=self.SHAPE_ATTRIBUTE_TYPE.float32, value="0.0")
        self.tree_brightness_factor = MsfsShapeAttribute(name="TreeBrightnessFactor", guid="{63040596-0B21-48FD-8B5F-A9E84A5B7BC9}", type=self.SHAPE_ATTRIBUTE_TYPE.uint32, value="127")
        self.water_type = MsfsShapeAttribute(name="WaterType", guid="{3F8514F8-FAA8-4B94-AB7F-DC2078A4B888}", type=self.SHAPE_ATTRIBUTE_TYPE.uint32, value="0")
        self.land_class_remap = MsfsShapeAttribute(name="LandClassRemap", guid="{0A685EB0-0E01-44FE-B9EF-BFFFBC968ADE}", type=self.SHAPE_ATTRIBUTE_TYPE.uint8, value="0")
        self.airport_size = MsfsShapeAttribute(name="AirportSize", guid="{86A147E9-ACF2-4780-9D3C-416373ECB451}", type=self.SHAPE_ATTRIBUTE_TYPE.uint8, value="0")
        self.layer = MsfsShapeAttribute(name="Layer", guid="{9E2B4C3E-7D84-453F-9DCC-B6498FF46703}", type=self.SHAPE_ATTRIBUTE_TYPE.uint32, value="1")

        if polygon is not None:
            self.__init_from_polygon(polygon, flatten=flatten, exclude_buildings=exclude_buildings, exclude_roads=exclude_roads, exclude_vegetation=exclude_vegetation)

        if xml is not None and elem is not None:
            self.__init_from_xml(xml, elem)

    def __init_from_polygon(self, polygon, flatten=False, exclude_buildings=False, exclude_roads=False, exclude_vegetation=False):
        self.unique_guid.value = uuid4()
        self.exclude_detected_buildings.value = "1" if exclude_buildings else "0"
        self.exclude_osm_buildings.value = "1" if exclude_buildings else "0"
        self.exclude_ms_buildings.value = "1" if exclude_buildings else "0"
        self.exclude_tin.value = "1" if exclude_buildings else "0"
        self.exclusion_flags.value = "1" if exclude_roads else "0"
        self.layer.value = "50000"
        self.flatten_mode.value = "1" if flatten else "0"
        self.flatten_falloff.value = "150.000000"

        self.attributes += [
            self.unique_guid,
            self.exclude_detected_buildings,
            self.exclude_osm_buildings,
            self.exclude_ms_buildings,
            self.exclude_tin,
            self.exclusion_flags,
            self.layer,
            self.flatten_mode,
            self.flatten_falloff
        ]

        if exclude_vegetation:
            self.vegetation_scale.value = "0"
            self.vegetation_density.value = "0"
            self.attributes.extend([self.vegetation_scale, self.vegetation_density])

        for point in polygon.exterior.coords:
            self.vertices.append(MsfsShapeVertex(point))

    def __init_from_xml(self, xml, elem):
        parent_group_id = elem.get(xml.PARENT_GROUP_ID_ATTR)
        self.parent_group_id = int(parent_group_id) if parent_group_id is not None else -1
        group_index = elem.get(xml.GROUP_INDEX_ATTR)
        self.group_index = int(group_index) if group_index is not None else -1
        self.altitude = float(elem.get(xml.ALTITUDE_ATTR))

        attributes = xml.find_polygon_attributes(elem)
        for attribute in attributes:
            self.attributes.append(self.__set_attribute_from_xml(xml, attribute))

        vertices = xml.find_polygon_vertices(elem)
        for vertice in vertices:
            self.vertices.append(self.__set_vertice_from_xml(xml, vertice))

    @staticmethod
    def __set_vertice_from_xml(xml, elem):
        return MsfsShapeVertex((float(elem.get(xml.LAT_ATTR)), float(elem.get(xml.LON_ATTR))))

    @staticmethod
    def __set_attribute_from_xml(xml, elem):
        return MsfsShapeAttribute(elem.get(xml.NAME_ATTR), elem.get(xml.GUID_ATTR), elem.get(xml.TYPE_ATTR), elem.get(xml.VALUE_ATTR))


class MsfsShapeGroup:
    tag: str
    display_name: str
    group_index: int
    group_id: int
    group_generated: bool

    def __init__(self, xml=None, elem=None, group_display_name=TERRAFORMING_POLYGONS_DISPLAY_NAME, group_id=None):
        self.tag = "Group"
        self.display_name = group_display_name
        self.group_index = 1
        self.group_id = 1 if group_id is None else group_id
        self.group_generated = (group_id is not None)

        if xml is not None and elem is not None:
            self.__init_from_xml(xml, elem)

    def __init_from_xml(self, xml, elem):
        parent_group_id = elem.get(xml.PARENT_GROUP_ID_ATTR)

        if parent_group_id is None:
            return

        groups = xml.root.findall(xml.PARENT_GROUP_SEARCH_PATTERN + elem.get(xml.PARENT_GROUP_ID_ATTR) + xml.PATTERN_SUFFIX)
        for group in groups:
            self.display_name = group.get(xml.DISPLAY_NAME_ATTR)
            self.group_index = int(group.get(xml.GROUP_INDEX_ATTR))
            self.group_id = int(group.get(xml.GROUP_ID_ATTR))
            self.group_generated = bool(group.get(xml.GROUP_GENERATED_ATTR))


class MsfsShapes:
    polygons: list
    group: MsfsShapeGroup

    def __init__(self, shape_gdf=None, xml=None, group_display_name=TERRAFORMING_POLYGONS_DISPLAY_NAME, group_id=None, flatten=False, exclude_buildings=False, exclude_roads=False, exclude_vegetation=False):
        self.polygons = []

        if shape_gdf is not None:
            self.__init_from_gdf(shape_gdf, group_display_name, group_id, flatten=flatten, exclude_buildings=exclude_buildings, exclude_roads=exclude_roads, exclude_vegetation=exclude_vegetation)

        if xml is not None:
            self.__init_from_xml(xml, group_display_name)

    def to_xml(self, xml):
        xml.add_shapes(self)

    @staticmethod
    def remove_from_xml(xml, group_name):
        xml.remove_shapes(group_name)

    def __init_from_gdf(self, shape_gdf, group_display_name, group_id, flatten=False, exclude_buildings=False, exclude_roads=False, exclude_vegetation=False):
        self.group = MsfsShapeGroup(group_display_name=group_display_name, group_id=group_id)

        for index, row in shape_gdf.iterrows():
            if not isinstance(row.geometry, Polygon) and not isinstance(row.geometry, MultiPolygon):
                continue

            if isinstance(row.geometry, Polygon):
                polygons = [row.geometry]
            else:
                polygons = row.geometry

            group_index = index[1]+1 if isinstance(index, list) or isinstance(index, tuple) else index+1
            for polygon in polygons:
                self.polygons.append(MsfsShapePolygon(polygon=polygon, parent_group_id=group_id, group_index=group_index, flatten=flatten, exclude_buildings=exclude_buildings, exclude_roads=exclude_roads, exclude_vegetation=exclude_vegetation))

    def __init_from_xml(self, xml, group_name):
        polygons = xml.find_polygons(group_name=group_name)

        if not polygons:
            return

        for polygon in polygons:
            self.polygons.append(MsfsShapePolygon(xml=xml, elem=polygon))

        self.group = MsfsShapeGroup(xml, polygons[0])

