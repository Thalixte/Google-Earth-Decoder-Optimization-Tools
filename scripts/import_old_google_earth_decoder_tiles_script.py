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
import shutil

from utils import Settings, get_sources_path, reload_modules, isolated_print

global_sources_path = get_sources_path()
settings = Settings(global_sources_path)

# reload modules if the option is enabled in the optimization_tools.ini file
reload_modules(settings)

import os
import shutil

from pathlib import Path
from constants import *
from utils import check_configuration, ScriptError, build_package, pr_bg_green, pr_bg_red
from msfs_project import MsfsProject
from blender import clean_scene


def import_old_google_earth_decoder_tiles(script_settings):
    try:
        script_settings.save()

        # instantiate the msfsProject and create the necessary resources if it does not exist
        msfs_project = MsfsProject(script_settings.projects_path, script_settings.project_name, script_settings.definition_file, script_settings.author_name, script_settings.sources_path, fast_init=True)

        try: shutil.rmtree(msfs_project.model_lib_folder, ignore_errors=True)
        except: pass

        try: shutil.rmtree(msfs_project.scene_folder, ignore_errors=True)
        except: pass

        try: shutil.rmtree(msfs_project.texture_folder, ignore_errors=True)
        except: pass

        if not os.path.isdir(msfs_project.model_lib_folder):
            os.makedirs(msfs_project.model_lib_folder, exist_ok=True)
        if not os.path.isdir(msfs_project.scene_folder):
            os.makedirs(msfs_project.scene_folder, exist_ok=True)
        if not os.path.isdir(msfs_project.texture_folder):
            os.makedirs(msfs_project.texture_folder, exist_ok=True)

        if not os.path.exists(os.path.join(msfs_project.project_folder, INI_FILE)):
            shutil.copyfile(os.path.join(global_sources_path, INI_FILE), os.path.join(msfs_project.project_folder, INI_FILE))
        script_settings = Settings(msfs_project.project_folder)

        check_configuration(script_settings, msfs_project, check_description_file=False)

        print(EOL)

        clean_scene()
        msfs_project.import_old_google_earth_decoder_tiles(script_settings)

        if script_settings.build_package_enabled:
            build_package(msfs_project, script_settings)

        pr_bg_green("Script correctly applied" + CEND)

    except ScriptError as ex:
        error_report = "".join(ex.value)
        isolated_print(constants.EOL + error_report)
        pr_bg_red("Script aborted" + CEND)
    except RuntimeError as ex:
        isolated_print(constants.EOL + str(ex))
        pr_bg_red("Script aborted" + CEND)


##################################################################
#                        Main process
##################################################################

if __name__ == "__main__":
    import_old_google_earth_decoder_tiles(settings)
