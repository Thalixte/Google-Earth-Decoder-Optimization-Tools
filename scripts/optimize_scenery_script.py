from utils import Settings, get_sources_path, reload_modules

settings = Settings(get_sources_path())

# reload modules if the option is enabled in the optimization_tools.ini file
reload_modules(settings)

import os

from pathlib import Path
from constants import *
from utils import check_configuration, ScriptError, build_package, pr_bg_green, pr_bg_red
from msfs_project import MsfsProject
from blender import clean_scene

BACKUP_ENABLED = False

##################################################################
#                        Main process
##################################################################

try:
    # instantiate the msfsProject and create the necessary resources if it does not exist
    msfs_project = MsfsProject(settings.projects_path, settings.project_name, settings.author_name, settings.sources_path)

    check_configuration(settings, msfs_project)

    if BACKUP_ENABLED:
        msfs_project.backup(Path(os.path.abspath(__file__)).stem, False)

    print("-------------------------------------------------------------------------------")
    print("------------------------------- OPTIMIZE SCENERY ------------------------------")
    print("-------------------------------------------------------------------------------")

    clean_scene()

    # msfs_project.optimize()

    if settings.build_package_enabled:
        build_package(msfs_project, settings)

    pr_bg_green("Script correctly applied" + CEND)

except ScriptError as ex:
    error_report = "".join(ex.value)
    print(constants.EOL + error_report)
    pr_bg_red("Script aborted" + CEND)
except RuntimeError as ex:
    print(constants.EOL + ex)
    pr_bg_red("Script aborted" + CEND)
finally:
    os.chdir(os.path.dirname(__file__))
