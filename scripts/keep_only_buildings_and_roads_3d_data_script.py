#  #
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 2
#   of the License, or (at your option) any later version.
#  #
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#  #
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#  #
#
#  <pep8 compliant>

from utils import Settings, get_sources_path, reload_modules, print_title, isolated_print

settings = Settings(get_sources_path())

# reload modules if the option is enabled in the optimization_tools.ini file
reload_modules(settings)

import os
import warnings
from shapely.errors import ShapelyDeprecationWarning

warnings.simplefilter(action="ignore", category=UserWarning, append=True)
warnings.simplefilter(action="ignore", category=FutureWarning, append=True)
warnings.simplefilter(action="ignore", category=DeprecationWarning, append=True)
warnings.simplefilter(action="ignore", category=ShapelyDeprecationWarning, append=True)

from pathlib import Path
from constants import *
from utils import check_configuration, ScriptError, build_package, pr_bg_green, pr_bg_red
from msfs_project import MsfsProject


def keep_only_buildings_and_roads_3d_data(script_settings):
    try:
        # instantiate the msfsProject and create the necessary resources if it does not exist
        msfs_project = MsfsProject(script_settings.projects_path, script_settings.project_name, script_settings.definition_file, script_settings.author_name, script_settings.sources_path)

        check_configuration(script_settings, msfs_project)

        msfs_project.backup(os.path.join(msfs_project.backup_folder, CLEANUP_3D_DATA_BACKUP_FOLDER))

        isolated_print(EOL)
        print_title("CLEANUP 3D DATA")

        script_settings.exclude_ground = True
        script_settings.exclude_nature_reserve = True
        script_settings.exclude_parks = True
        script_settings.isolate_3d_data = True
        script_settings.keep_constructions = True
        script_settings.keep_roads = True
        script_settings.disable_terraform = True
        script_settings.building_margin = 8.0
        script_settings.save()
        msfs_project.prepare_3d_data(script_settings, generate_height_data=False, process_3d_data=True, create_polygons=False, process_all=False)

        isolated_print(EOL)
        print_title("CLEAN PACKAGE FILES")

        msfs_project = MsfsProject(script_settings.projects_path, script_settings.project_name, script_settings.definition_file, script_settings.author_name, script_settings.sources_path)
        msfs_project.clean()

        if script_settings.build_package_enabled:
            build_package(msfs_project, script_settings)

        pr_bg_green("Script correctly applied" + constants.CEND)

    except ScriptError as ex:
        error_report = "".join(ex.value)
        isolated_print(constants.EOL + error_report)
        pr_bg_red("Script aborted" + constants.CEND)
    except RuntimeError as ex:
        isolated_print(constants.EOL + str(ex))
        pr_bg_red("Script aborted" + constants.CEND)


##################################################################
#                        Main process
##################################################################


if __name__ == "__main__":
    keep_only_buildings_and_roads_3d_data(settings)
