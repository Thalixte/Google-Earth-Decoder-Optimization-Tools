from msfs_project.object import MsfsObject
from msfs_project.position import MsfsPosition
from utils import get_position_from_file_name


class MsfsTile(MsfsObject):

    def __init__(self, name, definition_file):
        super().__init__(name, definition_file)
        pos = get_position_from_file_name(self.name)
        self.pos = MsfsPosition(pos[0], pos[1], 0)
