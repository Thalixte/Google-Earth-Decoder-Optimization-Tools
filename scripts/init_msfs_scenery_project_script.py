from utils import Settings, get_sources_path, reload_modules, print_title

settings = Settings(get_sources_path())

# reload modules if the option is enabled in the optimization_tools.ini file
reload_modules(settings)

import os

from constants import *
from utils import ScriptError, pr_bg_green, pr_bg_red
from msfs_project import MsfsProject

##################################################################
#                        Main process
##################################################################

try:
    print_title("INIT SCENERY PROJECT")

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
