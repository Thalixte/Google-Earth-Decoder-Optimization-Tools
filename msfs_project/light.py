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

from constants import GEOMETRY_OSM_COLUMN, LIGHT_WARM_GUID, LIGHT_COLD_GUID, LIGHT_HEADING, LIGHT_COLD_DISPLAY_NAME, LIGHT_WARM_DISPLAY_NAME, LIGHTS_DISPLAY_NAME
from msfs_project.position import MsfsPosition


class MsfsLightsGroup:
    tag: str
    display_name: str
    group_index: int
    group_id: int
    group_generated: bool

    def __init__(self, xml=None, elem=None, group_display_name=LIGHTS_DISPLAY_NAME, group_id=None):
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
            group_index = elem.get(xml.GROUP_INDEX_ATTR)
            self.group_index = int(group_index) if group_index is not None else -1
            self.group_id = int(group.get(xml.GROUP_ID_ATTR))
            self.group_generated = bool(group.get(xml.GROUP_GENERATED_ATTR))


class MsfsLight:
    class LIGHT_GUID:
        warm = LIGHT_WARM_GUID
        cold = LIGHT_COLD_GUID

    class LIGHT_DISPLAY_NAME:
        warm = LIGHT_WARM_DISPLAY_NAME
        cold = LIGHT_COLD_DISPLAY_NAME

    guid: str
    name: str
    pos: MsfsPosition
    heading: float
    group: MsfsLightsGroup

    def __init__(self, light_gdf=None, guid=None, prefix=None, name=None, idx=None, xml=None, elem=None, group_id=None):
        # default light guid is of light warm type
        self.guid = guid or self.LIGHT_GUID.warm
        prefix = str() if prefix is None else prefix
        group_suffix = str() if prefix is None else prefix.replace(" ", "_")
        self.name = prefix + (name or self.LIGHT_DISPLAY_NAME.warm + " ") + (str(idx).zfill(4) or str())
        self.heading = float(LIGHT_HEADING)

        if light_gdf is not None:
            self.__init_from_gdf(light_gdf, group_id, group_suffix)

        if xml is not None:
            self.__init_from_xml(xml, elem)

    def to_xml(self, xml):
        xml.add_light(self)

    def __init_from_gdf(self, light_gdf, group_id, group_suffix):
        if light_gdf.empty:
            return

        self.pos = MsfsPosition(light_gdf[GEOMETRY_OSM_COLUMN][0], light_gdf[GEOMETRY_OSM_COLUMN][1], light_gdf[GEOMETRY_OSM_COLUMN][2])
        self.group = MsfsLightsGroup(group_id=group_id, group_display_name=LIGHTS_DISPLAY_NAME + "_" + group_suffix)

    def __init_from_xml(self, xml, elem):
        children = list(elem.iter(xml.LIBRARY_OBJECT_TAG))

        for child in children:
            self.guid = child.get(xml.NAME_ATTR)

        self.name = elem.get(xml.DISPLAY_NAME_ATTR)
        self.pos = MsfsPosition(elem.get(xml.LAT_ATTR), elem.get(xml.LON_ATTR), elem.get(xml.ALT_ATTR))
        self.heading = float(elem.get(xml.HEADING_ATTR))
        self.group = MsfsLightsGroup(elem.get(xml.PARENT_GROUP_ID_ATTR))


class MsfsLights:
    lights: list
    group: MsfsLightsGroup

    def __init__(self, lights_gdf=None, guid=None, prefix=None, name=None, xml=None, group_display_name=None, group_id=None):
        self.lights = []

        if lights_gdf is not None:
            self.__init_from_gdf(lights_gdf, guid=guid, prefix=prefix, name=name, group_id=group_id)

        if xml is not None:
            self.__init_from_xml(xml, group_display_name)

    def __init_from_gdf(self, lights_gdf, guid=None, prefix=None, name=None, group_id=None):
        for index, row in lights_gdf.iterrows():
            self.lights.append(MsfsLight(light_gdf=row, guid=guid, prefix=prefix, name=name, idx=index, group_id=group_id))

    def __init_from_xml(self, xml, group_name):
        lights = xml.find_lights() if group_name is None else xml.find_lights(group_name=group_name)

        for elem in lights:
            self.lights.append(MsfsLight(xml=xml, elem=elem))

    def to_xml(self, xml):
        light = None

        for light in self.lights:
            light.to_xml(xml)

        if light is not None:
            xml.add_light_group(light)

        xml.save()
