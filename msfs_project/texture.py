from msfs_project.lod_resource import MsfsLodResource


class MsfsTexture(MsfsLodResource):
    mime_type: str

    def __init__(self, folder, file, mime_type):
        super().__init__(folder, file)
        self.mime_type = mime_type
