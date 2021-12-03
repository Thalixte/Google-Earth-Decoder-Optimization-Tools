from msfs_project.scene_object import MsfsSceneObject
from msfs_project.position import MsfsPosition
from utils import get_position_from_file_name


class MsfsTile(MsfsSceneObject):

    def __init__(self, path, name, definition_file):
        super().__init__(path, name, definition_file)
        pos = get_position_from_file_name(self.name)
        self.pos = MsfsPosition(pos[0], pos[1], 0)
