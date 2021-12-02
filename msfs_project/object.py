from msfs_project.position import MsfsPosition


class MsfsObject:
    name: str
    definition_file: str
    pos: MsfsPosition

    def __init__(self, name, definition_file):
        self.name = name
        self.definition_file = definition_file
        self.pos = MsfsPosition(0, 0, 0)

