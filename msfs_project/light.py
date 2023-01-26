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

from constants import GEOMETRY_OSM_COLUMN, LIGHT_WARM_GUID, LIGHT_COLD_GUID, LIGHT_HEADING, LIGHT_COLD_DISPLAY_NAME, LIGHT_WARM_DISPLAY_NAME
from msfs_project.position import MsfsPosition


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

    def __init__(self, light_gdf=None, guid=None, prefix=None, name=None, idx=None, xml=None, elem=None):
        # default light guid is of light warm type
        self.guid = guid or self.LIGHT_GUID.warm
        prefix = str() if prefix is None else prefix
        self.name = prefix + (name or self.LIGHT_DISPLAY_NAME.warm + " ") + (str(idx).zfill(4) or str())
        self.heading = float(LIGHT_HEADING)

        if light_gdf is not None:
            self.__init_from_gdf(light_gdf)

        if xml is not None:
            self.__init_from_xml(xml, elem)

    def to_xml(self, xml):
        self.remove_from_xml(xml)
        xml.add_light(self)
        xml.save()

    def __init_from_gdf(self, light_gdf):
        if light_gdf.empty:
            return

        self.pos = MsfsPosition(light_gdf[GEOMETRY_OSM_COLUMN][0], light_gdf[GEOMETRY_OSM_COLUMN][1], light_gdf[GEOMETRY_OSM_COLUMN][2])

    def __init_from_xml(self, xml, elem):
        children = list(elem.iter(xml.LIBRARY_OBJECT_TAG))

        for child in children:
            self.guid = child.get(xml.NAME_ATTR)

        self.name = elem.get(xml.DISPLAY_NAME_ATTR)
        self.pos = MsfsPosition(elem.get(xml.LAT_ATTR), elem.get(xml.LON_ATTR), elem.get(xml.ALT_ATTR))
        self.heading = float(elem.get(xml.HEADING_ATTR))

    def remove_from_xml(self, xml):
        xml.remove_lights(light_guid=self.guid, lat=self.pos.lat, lon=self.pos.lon, alt=self.pos.alt)


class MsfsLights:
    lights: list

    def __init__(self, lights_gdf=None, guid=None, prefix=None, name=None, xml=None):
        self.lights = []

        if lights_gdf is not None:
            self.__init_from_gdf(lights_gdf, guid=guid, prefix=prefix, name=name)

        if xml is not None:
            self.__init_from_xml(xml)

    def __init_from_gdf(self, lights_gdf, guid=None, prefix=None, name=None):
        for index, row in lights_gdf.iterrows():
            self.lights.append(MsfsLight(light_gdf=row, guid=guid, prefix=prefix, name=name, idx=index))

    def __init_from_xml(self, xml):
        lights = xml.find_lights()
        for elem in lights:
            self.lights.append(MsfsLight(xml=xml, elem=elem))

    def to_xml(self, xml):
        for light in self.lights:
            light.to_xml(xml)
