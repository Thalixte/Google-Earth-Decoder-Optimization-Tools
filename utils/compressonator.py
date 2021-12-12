import itertools
import sys

import io
import os
import subprocess
from pathlib import Path

from utils import ScriptError, chunks
from utils.progress_bar import ProgressBar


class Compressonator:
    path: str
    textures_folder: str
    converted_data: list
    compressed_data: list

    TEXTURE_FOLDER = "texture"
    BMP_FORMAT = "BMP"
    DDS_FORMAT = "DDS"
    BMP_EXTENSION = "." + BMP_FORMAT
    DDS_EXTENSION = "." + DDS_FORMAT
    BMP_PATTERN = "*." + BMP_FORMAT
    DDS_PATTERN = "*." + DDS_FORMAT
    DDS_CONVERSION_FORMAT = "DXT1"
    BASE_COLOR_INDEX = 0
    NB_PARALLEL_TASKS = 20

    def __init__(self, path, model_lib_folder):
        self.path = path
        self.textures_folder = os.path.join(model_lib_folder, self.TEXTURE_FOLDER)
        self.converted_data = self.__retrieve_texture_files_to_treat(self.DDS_PATTERN, self.DDS_EXTENSION, self.BMP_EXTENSION)

    def compress_texture_files(self):
        self.__convert_dds_texture_files()
        self.compressed_data = self.__retrieve_texture_files_to_treat(self.BMP_PATTERN, self.BMP_EXTENSION, self.DDS_EXTENSION)
        self.__compress_dds_texture_files()

        # clean bmp files
        for bmp_texture_file in Path(self.textures_folder).glob(self.BMP_PATTERN):
            file_path = os.path.join(self.textures_folder, bmp_texture_file)

            try:
                os.remove(file_path)
            except OSError as e:
                raise ScriptError("Error: " + file_path + " : " + e.strerror)

            print("bmp temp texture file:", file_path, "removed")

    def __retrieve_texture_files_to_treat(self, texture_files_pattern, texture_files_extension, dest_texture_files_extension):
        data = []
        for texture_file in Path(self.textures_folder).glob(texture_files_pattern):
            print("texture file: ", os.path.basename(texture_file))

            data.append({'file_name': str(texture_file), 'dest_file_name': str(texture_file).replace(texture_files_extension, dest_texture_files_extension)})

        return chunks(data, self.NB_PARALLEL_TASKS)

    def __convert_dds_texture_files(self):
        ON_POSIX = 'posix' in sys.builtin_module_names

        self.converted_data, data = itertools.tee(self.converted_data)
        pbar = ProgressBar(list(data), title="convert " + self.DDS_FORMAT + " textures to " + self.BMP_FORMAT)
        for chunck in self.converted_data:
            # create a pipe to get data
            input_fd, output_fd = os.pipe()

            for obj in chunck:
                print("-------------------------------------------------------------------------------")
                print("prepare command line: ", self.path, obj['file_name'], obj['dest_file_name'])

            processes = [subprocess.Popen([self.path, obj['file_name'], obj['dest_file_name']], stdout=output_fd, close_fds=ON_POSIX) for obj in chunck]

            os.close(output_fd)  # close unused end of the pipe

            # read output line by line as soon as it is available
            with io.open(input_fd, "r") as file:
                for line in file:
                    print(line, end=str())

            for p in processes:
                p.wait()

            pbar.update("%s converted to %s" % (os.path.basename(obj['file_name']), os.path.basename(obj['dest_file_name'])))

    def __compress_dds_texture_files(self):
        ON_POSIX = 'posix' in sys.builtin_module_names

        self.compressed_data, data = itertools.tee(self.compressed_data)
        pbar = ProgressBar(list(data), title="compress " + self.BMP_FORMAT + " textures to " + self.DDS_FORMAT + " " + self.DDS_CONVERSION_FORMAT)
        for chunck in self.compressed_data:
            # create a pipe to get data
            input_fd, output_fd = os.pipe()

            for obj in chunck:
                print("-------------------------------------------------------------------------------")
                print("prepare command line: ", self.path, "-fd", self.DDS_CONVERSION_FORMAT, obj['file_name'], obj['dest_file_name'])

            processes = [subprocess.Popen([self.path, "-fd", self.DDS_CONVERSION_FORMAT, obj['file_name'], obj['dest_file_name']], stdout=output_fd, close_fds=ON_POSIX) for obj in chunck]

            os.close(output_fd)  # close unused end of the pipe

            # read output line by line as soon as it is available
            with io.open(input_fd, "r", buffering=1) as file:
                for line in file:
                    print(line, end=str())

            for p in processes:
                p.wait()

            pbar.update("%s compressed to %s" % (os.path.basename(obj['file_name']), os.path.basename(obj['dest_file_name'])))
