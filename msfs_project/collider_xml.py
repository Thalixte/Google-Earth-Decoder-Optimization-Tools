from utils import Xml


class ColliderXml(Xml):
    guid: str
    GUID_TAG = "guid"

    def __init__(self, file_folder, file_name):
        super().__init__(file_folder, file_name)
        self.guid = self.root.get(self.GUID_TAG)
