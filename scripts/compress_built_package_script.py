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

from constants import *
from utils import check_configuration, ScriptError, build_package, pr_bg_green, pr_bg_red
from msfs_project import MsfsProject


def compress_built_package(global_settings):
    try:
        # instantiate the msfsProject and create the necessary resources if it does not exist
        msfs_project = MsfsProject(global_settings.projects_path, global_settings.project_name, global_settings.definition_file, global_settings.path, global_settings.author_name, fast_init=True)

        check_configuration(global_settings, msfs_project, check_built_package=True, check_compressonator=True)

        isolated_print(EOL)
        print_title("COMPRESS BUILT PACKAGE")

        msfs_project.compress_built_package()

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
    compress_built_package(settings)
