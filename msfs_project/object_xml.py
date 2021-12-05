from utils import Xml


class MsfsObjectXml(Xml):
    guid: str
    GUID_TAG = "guid"
    MIN_SIZE_TAG = "MinSize"
    MODEL_FILE_TAG = "ModelFile"

    SCENERY_OBJECT_LODS_SEARCH_PATTERN = "./LODS/LOD"
    SCENERY_OBJECT_LOD_MODEL_FILE_SEARCH_PATTERN = "./LODS/LOD[@ModelFile='"
    
    def __init__(self, file_folder, file_name):
        super().__init__(file_folder, file_name)
        guid = self.root.get(self.GUID_TAG)
        if not guid is None:
            self.guid = guid.upper()

    def find_scenery_lods(self):
        return self.root.findall(self.SCENERY_OBJECT_LODS_SEARCH_PATTERN)

    def find_scenery_lod_models(self, file_name):
        return self.root.findall(self.SCENERY_OBJECT_LOD_MODEL_FILE_SEARCH_PATTERN + file_name + self.PATTERN_SUFFIX)


