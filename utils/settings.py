import configparser as cp
import json
import os

from constants import ENCODING


class Settings:
    projects_path: str
    project_name: str
    author_name: str
    node_js_folder: str
    fspackagetool_folder: str
    msfs_steam_version: str
    build_package_enabled: str
    sources_path: str
    lat_correction: float
    lon_correction: float
    lods: list

    def __init__(self, sources_path=""):
        self.projects_path = ""
        self.project_name = ""
        self.author_name = ""
        self.node_js_folder = ""
        self.fspackagetool_folder = ""
        self.msfs_steam_version = "False"
        self.build_package_enabled = "False"
        self.sources_path = sources_path
        self.lat_correction = 0.0
        self.lon_correction = 0.0

        config = cp.ConfigParser()
        config.read('optimisation_tools.ini', encoding=ENCODING)

        for section_name in config.sections():
            for name, value in config.items(section_name):
                setattr(self, name, value.replace('"', ''))

        # check if the package is built at the end of the script
        self.msfs_steam_version = json.loads(self.msfs_steam_version.lower())

        # check if the package is built at the end of the script
        self.build_package_enabled = json.loads(self.build_package_enabled.lower())

        # ensure to convert float settings values
        self.lat_correction = float(self.lat_correction)
        self.lon_correction = float(self.lon_correction)

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)
            