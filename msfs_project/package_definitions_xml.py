from utils import Xml


class MsfsPackageDefinitionsXml(Xml):
    ASSETS_GROUP_TAG = "AssetGroups"
    ASSET_GROUP_TAG = "AssetGroup"
    ASSET_DIR_TAG = "AssetDir"
    OUTPUT_DIR_TAG = "OutputDir"

    ASSETS_GROUP_SEARCH_PATTERN = "./ASSETS_GROUP"
    SCENERY_OBJECT_LOD_MODEL_FILE_SEARCH_PATTERN = "./" + ASSETS_GROUP_TAG + "/" + ASSET_GROUP_TAG
    
    def __init__(self, file_folder, file_name):
        super().__init__(file_folder, file_name)

    def find_model_lib_asset_group(self, model_lib_folder):
        assets_group = self.root.findall(self.SCENERY_OBJECT_LOD_MODEL_FILE_SEARCH_PATTERN)
        for asset_group in assets_group:
            if model_lib_folder in asset_group.find(self.ASSET_DIR_TAG).text:
                return asset_group.find(self.OUTPUT_DIR_TAG).text.replace("/", "\\")

        return str()


