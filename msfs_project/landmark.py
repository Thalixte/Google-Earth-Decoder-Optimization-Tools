from uuid import uuid4

from constants import DISPLAY_NAME_OSM_TAG
from msfs_project.position import MsfsPosition


class MsfsLandmarkLocation:
    class LANDMARK_LOCATION_TYPE:
        city = "CITY"
        poi = "POI"

    instance_id: str
    name: str
    owner: str
    type: str
    pos: MsfsPosition
    offset: str
    has_alt: bool

    def __init__(self, geocode_gdf=None, tiles=None, owner=None, xml=None, elem=None):
        # default landmark location type is POI
        self.type = self.LANDMARK_LOCATION_TYPE.poi
        self.name = str()
        self.offset = "{:.6f}".format(0.0)
        self.has_alt = False

        if geocode_gdf is not None:
            self.__init_from_gdf(geocode_gdf, tiles=tiles, owner=owner)

        if xml is not None:
            self.__init_from_xml(xml, elem)

    def to_xml(self, xml):
        xml.add_landmark_location(self)
        xml.save()

    def __init_from_gdf(self, geocode_gdf, tiles=None, owner=None):
        if geocode_gdf.empty:
            return

        self.instance_id = "{" + str(uuid4()).upper() + "}"
        self.owner = owner or str()
        self.pos = MsfsPosition(geocode_gdf.lat, geocode_gdf.lon, 0.0)

        if tiles is not None:
            self.__find_altitude_from_tiles(tiles)

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
        self.has_alt = True

    def __find_altitude_from_tiles(self, tiles):
        coords = (self.pos.lat, self.pos.lat, self.pos.lon, self.pos.lon)
        for tile in tiles.values():
            if tile.contains(coords):
                self.pos.alt = tile.pos.alt
                self.has_alt = True
                return


class MsfsLandmarks:
    landmark_locations: list

    def __init__(self, geocode_gdf=None, tiles=None, owner=None, xml=None):
        self.landmark_locations = []

        if geocode_gdf is not None:
            self.__init_from_gdf(geocode_gdf, tiles=tiles, owner=owner)

        if xml is not None:
            self.__init_from_xml(xml)

    def to_xml(self, xml):
        xml.add_landmarks(self)

    def __init_from_gdf(self, geocode_gdf, tiles=None, owner=None):
        for index, row in geocode_gdf.iterrows():
            self.landmark_locations.append(MsfsLandmarkLocation(geocode_gdf=row, tiles=tiles, owner=owner))

    def __init_from_xml(self, xml):
        landmarks = xml.find_landmarks()
        for elem in landmarks:
            self.landmark_locations.append(MsfsLandmarkLocation(xml=xml, elem=elem))

    @staticmethod
    def remove_from_xml(xml, name):
        xml.remove_landmark(name)
