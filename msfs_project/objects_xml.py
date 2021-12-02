from utils import Xml, settings
from msfs_project.tile_xml import TileXml
from msfs_project.collider_xml import ColliderXml


class ObjectsXml(Xml):
    GUID_TAG = "guid"
    SCENERY_OBJECT_SEARCH_PATTERN = "./SceneryObject/LibraryObject[@name='"
    SCENERY_OBJECT_GROUP_SEARCH_PATTERN = "./Group/SceneryObject/LibraryObject[@name='"
    PATTERN_SUFFIX = "']"
    PARENT_PATTERN_SUFFIX = PATTERN_SUFFIX + "/.."

    def __init__(self, file_folder, file_name):
        super().__init__(file_folder, file_name)

    def update_objects_position(self, msfs_project, settings):
        self.__update_tiles_pos(msfs_project, settings)
        self.__update_colliders_pos(msfs_project, settings)
        self.save()

    def __find_scenery_objects(self, guid):
        return self.root.findall(self.SCENERY_OBJECT_SEARCH_PATTERN + guid.upper() + self.PARENT_PATTERN_SUFFIX)

    def __find_scenery_objects_in_group(self, guid):
        return self.root.findall(self.SCENERY_OBJECT_GROUP_SEARCH_PATTERN + guid.upper() + self.PARENT_PATTERN_SUFFIX)

    def __update_tiles_pos(self, msfs_project, settings):
        for object_name, tile in msfs_project.tiles.items():
            print("-------------------------------------------------------------------------------")
            print("xml tile: ", object_name)
            xml_tile = TileXml(msfs_project.modelLib_folder, tile.definition_file)

            self.__update_scenery_object_pos(tile, self.__find_scenery_objects(xml_tile.guid.upper()), settings)
            self.__update_scenery_object_pos(tile, self.__find_scenery_objects_in_group(xml_tile.guid.upper()), settings)

    def __update_colliders_pos(self, msfs_project, settings):
        for object_name, collider in msfs_project.colliders.items():
            print("-------------------------------------------------------------------------------")
            print("xml collider: ", object_name)
            xml_collider = ColliderXml(msfs_project.modelLib_folder, collider.definition_file)

            self.__update_scenery_object_pos(collider, self.__find_scenery_objects(xml_collider.guid.upper()), settings)
            self.__update_scenery_object_pos(collider, self.__find_scenery_objects_in_group(xml_collider.guid.upper()), settings)

    @staticmethod
    def __update_scenery_object_pos(tile, found_scenery_objects, settings):
        for scenery_object in found_scenery_objects:
            new_lat = tile.pos.lat + settings.lat_correction
            new_lon = tile.pos.lon + settings.lon_correction
            print("new lat: ", new_lat)
            print("new lon: ", new_lon)
            scenery_object.set("lat", str(new_lat))
            scenery_object.set("lon", str(new_lon))
