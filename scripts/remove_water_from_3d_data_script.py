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

from utils import GlobalSettings, get_global_path, reload_modules, print_title, isolated_print

settings = GlobalSettings(get_global_path())

# reload modules if the option is enabled in the optimization_tools.ini file
reload_modules(settings)

import warnings
from shapely.errors import ShapelyDeprecationWarning

warnings.simplefilter(action="ignore", category=UserWarning, append=True)
warnings.simplefilter(action="ignore", category=FutureWarning, append=True)
warnings.simplefilter(action="ignore", category=DeprecationWarning, append=True)
warnings.simplefilter(action="ignore", category=ShapelyDeprecationWarning, append=True)

import os
from constants import *
from utils import check_configuration, ScriptError, build_package, pr_bg_green, pr_bg_red
from msfs_project import MsfsProject


def remove_water_from_3d_data(global_settings):
    try:
        # instantiate the msfsProject and create the necessary resources if it does not exist
        msfs_project = MsfsProject(global_settings.projects_path, global_settings.project_name, global_settings.definition_file, global_settings.path, global_settings.author_name)

        check_configuration(global_settings, msfs_project, check_blendergis_addon=True)

        msfs_project.backup(os.path.join(msfs_project.backup_folder, CLEANUP_3D_DATA_BACKUP_FOLDER))

        isolated_print(EOL)
        print_title("CLEANUP 3D DATA")

        msfs_project.settings.exclude_water = True
        msfs_project.settings.exclude_ground = False
        msfs_project.settings.exclude_forests = False
        msfs_project.settings.exclude_woods = False
        msfs_project.settings.exclude_parks = False
        msfs_project.settings.exclude_nature_reserves = False
        msfs_project.settings.exclude_parks = False
        msfs_project.settings.isolate_3d_data = False
        msfs_project.settings.disable_terraform = False
        msfs_project.settings.save()
        msfs_project.prepare_3d_data(global_settings, generate_height_data=False, process_3d_data=True, create_polygons=False, process_all=msfs_project.settings.process_all)

        isolated_print(EOL)
        print_title("CLEAN PACKAGE FILES")

        msfs_project = MsfsProject(global_settings.projects_path, global_settings.project_name, global_settings.definition_file, global_settings.path, global_settings.author_name)
        msfs_project.clean()

        if msfs_project.settings.build_package_enabled:
            build_package(global_settings, msfs_project)

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
    remove_water_from_3d_data(settings)
