from utils import Xml
from utils.progress_bar import ProgressBar


class ObjectsXml(Xml):
    GUID_TAG = "name"
    LIBRARY_OBJECTS_SEARCH_PATTERN = "./SceneryObject/LibraryObject"
    SCENERY_OBJECT_SEARCH_PATTERN = "./SceneryObject/LibraryObject[@name='"
    SCENERY_OBJECT_GROUP_SEARCH_PATTERN = "./Group/SceneryObject/LibraryObject[@name='"

    def __init__(self, file_folder, file_name):
        super().__init__(file_folder, file_name)
        self.__convert_objects_guid_to_upper()

    def update_objects_position(self, msfs_project, settings):
        self.__update_tiles_pos(msfs_project, settings)
        self.__update_colliders_pos(msfs_project, settings)
        self.save()

    def __convert_objects_guid_to_upper(self):
        for tag in self.root.findall(self.LIBRARY_OBJECTS_SEARCH_PATTERN):
            if tag.get(self.GUID_TAG):
                tag.set(self.GUID_TAG, tag.get(self.GUID_TAG).upper())

        self.save()

    def __retrieve_library_objects(self):
        return self.root.findall(self.LIBRARY_OBJECTS_SEARCH_PATTERN)

    def __find_scenery_objects(self, guid):
        return self.root.findall(self.SCENERY_OBJECT_SEARCH_PATTERN + guid.upper() + self.PARENT_PATTERN_SUFFIX)

    def __find_scenery_objects_in_group(self, guid):
        return self.root.findall(self.SCENERY_OBJECT_GROUP_SEARCH_PATTERN + guid.upper() + self.PARENT_PATTERN_SUFFIX)

    def __update_tiles_pos(self, msfs_project, settings):
        if not msfs_project.tiles.items():
            return

        pbar = ProgressBar(msfs_project.tiles.items(), title="update tiles positions", sleep=0.000001)
        for guid, tile in pbar.iterable:

            self.__update_scenery_object_pos(tile, self.__find_scenery_objects(guid), settings)
            self.__update_scenery_object_pos(tile, self.__find_scenery_objects_in_group(guid), settings)

            pbar.update("%s" % tile.name + " : new lat: " + str(tile.pos.lat + settings.lat_correction) + " : new lon: " + str(tile.pos.lon + settings.lon_correction))

    def __update_colliders_pos(self, msfs_project, settings):
        if not msfs_project.colliders.items():
            return

        pbar = ProgressBar(msfs_project.colliders.items(), title="update colliders positions", sleep=0.000001)
        for guid, collider in msfs_project.colliders.items():

            self.__update_scenery_object_pos(collider, self.__find_scenery_objects(guid), settings)
            self.__update_scenery_object_pos(collider, self.__find_scenery_objects_in_group(guid), settings)

            pbar.update("%s" % guid + " : " + collider.name + " : new lat: " + str(collider.pos.lat + settings.lat_correction) + " : new lon: " + str(collider.pos.lon + settings.lon_correction))

    @staticmethod
    def __update_scenery_object_pos(tile, found_scenery_objects, settings):
        for scenery_object in found_scenery_objects:
            new_lat = tile.pos.lat + settings.lat_correction
            new_lon = tile.pos.lon + settings.lon_correction
            scenery_object.set("lat", str(new_lat))
            scenery_object.set("lon", str(new_lon))
