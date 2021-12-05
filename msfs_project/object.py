import os

from msfs_project.object_xml import MsfsObjectXml


class MsfsObject:
    name: str
    folder: str
    definition_file: str
    xml: MsfsObjectXml

    def __init__(self, path, name, definition_file):
        self.name = name
        self.folder = path
        self.definition_file = definition_file
        self.xml = MsfsObjectXml(path, definition_file)

    def remove_files(self):
        self.remove_file()

    def remove_file(self):
        file_path = os.path.join(self.folder, self.definition_file)
        if os.path.isfile(file_path):
            os.remove(os.path.join(file_path))
            print(self.definition_file, "removed")
