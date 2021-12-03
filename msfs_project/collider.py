from msfs_project.position import MsfsPosition
from msfs_project.scene_object import MsfsSceneObject
from utils import get_position_from_file_name


class MsfsCollider(MsfsSceneObject):
    associated_tile: str

    def __init__(self, path, name, definition_file):
        super().__init__(path, name, definition_file)
        self.associated_tile = name.split("_")[0]
        pos = get_position_from_file_name(self.associated_tile)
        self.pos = MsfsPosition(pos[0], pos[1], 0)
