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

import subprocess

from utils import ScriptError

MSFS_BUILD_EXE_FORCE_STEAM_OPTION = "-forcesteam"
MSFS_BUILD_EXE_OUTPUT_DIR_OPTION = "-outputdir"
MSFS_BUILD_EXE_OUTPUT_TO_SEPARATE_CONSOLE_OPTION = "-outputtoseparateconsole"
ERROR_MSG = "MSFS SDK tools not installed"


######################################################
# build scenery into new MSFS package
######################################################
def build_package(settings, msfs_project):
    msfs_build_exe_path = "\"" + settings.msfs_build_exe_path + "\""

    if settings.msfs_steam_version:
        msfs_build_exe_path += " " + MSFS_BUILD_EXE_FORCE_STEAM_OPTION

    try:
        print(msfs_build_exe_path + " " + MSFS_BUILD_EXE_OUTPUT_TO_SEPARATE_CONSOLE_OPTION + " \"" + msfs_project.project_definition_xml_path + "\" " + MSFS_BUILD_EXE_OUTPUT_DIR_OPTION + " \"" + msfs_project.project_folder + "\"")
        subprocess.run(msfs_build_exe_path + " " + MSFS_BUILD_EXE_OUTPUT_TO_SEPARATE_CONSOLE_OPTION + " \"" + msfs_project.project_definition_xml_path + "\" " + MSFS_BUILD_EXE_OUTPUT_DIR_OPTION + " \"" + msfs_project.project_folder + "\"", shell=True, check=False)
    except:
        raise ScriptError(ERROR_MSG)
