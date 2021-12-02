from msfs_project.object import MsfsObject
from msfs_project.position import MsfsPosition
from utils import get_position_from_file_name


class MsfsCollider(MsfsObject):
    associated_tile: str

    def __init__(self, name, definition_file):
        super().__init__(name, definition_file)
        pos = get_position_from_file_name(name.split("_")[0])
        self.pos = MsfsPosition(pos[0], pos[1], 0)

