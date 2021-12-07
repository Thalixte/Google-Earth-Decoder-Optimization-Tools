import configparser as cp
import json

from constants import ENCODING, PNG_TEXTURE_FORMAT, INI_FILE


class Settings:
    projects_path: str
    project_name: str
    author_name: str
    node_js_folder: str
    fspackagetool_folder: str
    msfs_steam_version: str
    build_package_enabled: str
    sources_path: str
    output_texture_format: str
    lat_correction: float
    lon_correction: float
    lods: list

    def __init__(self, sources_path=str()):
        self.projects_path = str()
        self.project_name = str()
        self.author_name = str()
        self.node_js_folder = str()
        self.fspackagetool_folder = str()
        self.msfs_steam_version = "False"
        self.build_package_enabled = "False"
        self.reload_modules = "False"
        self.sources_path = sources_path
        self.output_texture_format = PNG_TEXTURE_FORMAT
        self.lat_correction = 0.0
        self.lon_correction = 0.0

        config = cp.ConfigParser()
        config.read(INI_FILE, encoding=ENCODING)

        for section_name in config.sections():
            for name, value in config.items(section_name):
                setattr(self, name, value.replace('"', str()))

        # check if the package is built at the end of the script
        self.msfs_steam_version = json.loads(self.msfs_steam_version.lower())

        # check if the package is built at the end of the script
        self.build_package_enabled = json.loads(self.build_package_enabled.lower())

        # check if modules have to be reloaded (mostly for blender dev purpose)
        self.reload_modules = json.loads(self.reload_modules.lower())

        # ensure to convert float settings values
        self.lat_correction = float(str(self.lat_correction))
        self.lon_correction = float(str(self.lon_correction))

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)
            