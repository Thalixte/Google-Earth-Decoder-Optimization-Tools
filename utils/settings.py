import configparser as cp
import json
import os

from constants import ENCODING, PNG_TEXTURE_FORMAT, INI_FILE


class Settings:
    sources_path: str
    projects_path: str
    project_name: str
    project_name_to_merge: str
    author_name: str
    msfs_build_exe_path: str
    backup_enabled: str
    bake_textures_enabled: str
    msfs_steam_version: str
    build_package_enabled: str
    reload_modules = str
    sources_path: str
    target_min_size_values: list
    output_texture_format: str
    lat_correction: float
    lon_correction: float
    compressonator_exe_path = str
    sections = list

    def __init__(self, sources_path=str()):
        self.sources_path = sources_path
        self.projects_path = str()
        self.project_name = str()
        self.project_name_to_merge = str()
        self.author_name = str()
        self.msfs_build_exe_path = str()
        self.backup_enabled = "False"
        self.bake_textures_enabled = "False"
        self.msfs_steam_version = "False"
        self.build_package_enabled = "False"
        self.reload_modules = "False"
        self.sources_path = sources_path
        self.target_min_size_values = []
        self.output_texture_format = PNG_TEXTURE_FORMAT
        self.lat_correction = 0.0
        self.lon_correction = 0.0
        self.compressonator_exe_path = str()
        self.sections = []

        config = cp.ConfigParser()
        if os.path.isfile(INI_FILE):
            config.read(INI_FILE, encoding=ENCODING)
        else:
            config.read(os.path.join(sources_path, INI_FILE), encoding=ENCODING)

        for section_name in config.sections():
            self.sections.append((section_name, section_name, section_name))
            for name, value in config.items(section_name):
                setattr(self, name, value.replace('"', str()))

        # reduce the number of texture files (Lily Texture Packer addon is necessary https://gumroad.com/l/DFExj)
        self.bake_textures_enabled = json.loads(self.bake_textures_enabled.lower())

        # check if the package is built at the end of the script
        self.msfs_steam_version = json.loads(self.msfs_steam_version.lower())

        # check if the backup of the project files is enabled
        self.backup_enabled = json.loads(self.backup_enabled.lower())

        # check if the package is built at the end of the script
        self.build_package_enabled = json.loads(self.build_package_enabled.lower())

        # check if modules have to be reloaded (mostly for blender dev purpose)
        self.reload_modules = json.loads(self.reload_modules.lower())

        # get the target lod values
        self.target_min_size_values = str().join(self.target_min_size_values.split()).split(",")

        # ensure to convert float settings values
        self.lat_correction = "{:.9f}".format(float(str(self.lat_correction))).rstrip("0").rstrip(".")
        self.lon_correction = "{:.9f}".format(float(str(self.lon_correction))).rstrip("0").rstrip(".")

    def save(self):
        config = cp.ConfigParser(comment_prefixes='# ', allow_no_value=True)
        if os.path.isfile(INI_FILE):
            config.read(INI_FILE, encoding=ENCODING)
        else:
            config.read(os.path.join(self.sources_path, INI_FILE), encoding=ENCODING)

        for section_name in config.sections():
            for name, value in config.items(section_name):
                config.set(section_name, name, str(getattr(self, name)))

        config.set("LODS", "target_min_size_values", ", ".join(self.target_min_size_values))

        with open(os.path.join(self.sources_path, INI_FILE), "w") as configfile:
            config.write(configfile)

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)
            