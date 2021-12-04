import os

from constants import *
from utils import Settings, check_configuration, ScriptError, pr_bg_green, pr_bg_red, get_sources_path
from msfs_project import MsfsProject

##################################################################
#                        Main process
##################################################################

settings = Settings(get_sources_path())

try:
    print("-------------------------------------------------------------------------------")
    print("----------------------------- INIT SCENERY PROJECT ----------------------------")
    print("-------------------------------------------------------------------------------")

    # instantiate the msfsProject and create the necessary resources if it does not exist
    msfs_project = MsfsProject(settings.projects_path, settings.project_name, settings.author_name, settings.sources_path)

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
