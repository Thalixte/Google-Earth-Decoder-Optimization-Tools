import os

from msfs_project.object_xml import MsfsObjectXml
from utils import backup_file


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

    def backup_files(self, backup_path, dry_mode=False, pbar=None):
        self.backup_file(backup_path, dry_mode=dry_mode, pbar=pbar)

    def remove_files(self):
        self.remove_file()

    def backup_file(self, backup_path, dry_mode=False, pbar=None):
        backup_file(backup_path, self.folder, self.definition_file, dry_mode=dry_mode, pbar=pbar)

    def remove_file(self):
        file_path = os.path.join(self.folder, self.definition_file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(self.definition_file, "removed")
