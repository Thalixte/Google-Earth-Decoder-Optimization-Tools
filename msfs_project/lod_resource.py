import os


class MsfsLodResource:
    folder: str
    file: str

    def __init__(self, folder, file):
        self.folder = folder
        self.file = file

    def remove_file(self):
        file_path = os.path.join(self.folder, self.file)
        if os.path.isfile(file_path):
            os.remove(os.path.join(file_path))
            print(self.file, "removed")
