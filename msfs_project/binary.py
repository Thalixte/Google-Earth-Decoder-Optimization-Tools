from msfs_project.lod_resource import MsfsLodResource


class MsfsBinary(MsfsLodResource):

    def __init__(self, model_file_path, folder, file):
        super().__init__(model_file_path, folder, file)
