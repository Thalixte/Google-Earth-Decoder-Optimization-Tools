from msfs_project.object import MsfsObject
from msfs_project.position import MsfsPosition
from msfs_project.lod import MsfsLod


class MsfsSceneObject(MsfsObject):
    pos: MsfsPosition
    lods: list

    def __init__(self, path, name, definition_file):
        super().__init__(path, name, definition_file)
        self.pos = MsfsPosition(0, 0, 0)
        self.lods = self.__retrieve_lods()

    def __retrieve_lods(self):
        lods = []
        lods_definition = self.xml.find_scenery_lods()

        for lod_definition in lods_definition:
            lods.append(MsfsLod(lod_definition.get(self.xml.MIN_SIZE_TAG), lod_definition.get(self.xml.MODEL_FILE_TAG)))

        return lods
