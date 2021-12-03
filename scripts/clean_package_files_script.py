import os

from constants import *
from utils import Settings, check_configuration, ScriptError, \
    build_package, pr_bg_green, pr_bg_red, get_sources_path
from msfs_project import MsfsProject, ObjectsXml

BACKUP_ENABLED: False

##################################################################
#                        Main process
##################################################################

settings = Settings(get_sources_path())

try:
    # instantiate the msfsProject and create the necessary resources if it does not exist
    msfs_project = MsfsProject(settings.projects_path, settings.project_name, settings.author_name, settings.sources_path)

    check_configuration(settings, msfs_project)

    print("-------------------------------------------------------------------------------")
    print("----------------------------- UPDATE TILES POSITION----------------------------")
    print("-------------------------------------------------------------------------------")

    msfs_project.clean()

    if settings.build_package_enabled:
        build_package(msfs_project, settings)

    print(EOL)
    pr_bg_green("Script correctly applied" + constants.CEND)

except ScriptError as ex:
    error_report = "".join(ex.value)
    print(constants.EOL + error_report)
    pr_bg_red("Script aborted" + constants.CEND)
except RuntimeError as ex:
    print(constants.EOL + ex)
    pr_bg_red("Script aborted" + constants.CEND)
finally:
    os.chdir(os.path.dirname(__file__))