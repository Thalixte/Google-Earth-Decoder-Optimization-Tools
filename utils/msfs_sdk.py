import os
import subprocess

from constants import MSFS_BUILD_EXE
from utils import ScriptError

MSFS_BUILD_EXE_FORCE_STEAM_OPTION = "-forcesteam"
MSFS_BUILD_EXE_OUTPUT_DIR_OPTION = "-outputdir"
MSFS_BUILD_EXE_OUTPUT_TO_SEPARATE_CONSOLE_OPTION = "-outputtoseparateconsole"
ERROR_MSG = "MSFS SDK tools not installed"


######################################################
# build scenery into new MSFS package
######################################################
def build_package(msfs_project, settings):
    msfs_build_exe_path = "\"" + settings.msfs_build_exe_path + "\""

    if settings.msfs_steam_version:
        msfs_build_exe_path += " " + MSFS_BUILD_EXE_FORCE_STEAM_OPTION

    try:
        print(msfs_build_exe_path + " " + MSFS_BUILD_EXE_OUTPUT_TO_SEPARATE_CONSOLE_OPTION + " \"" + msfs_project.project_definition_xml_path + "\" " + MSFS_BUILD_EXE_OUTPUT_DIR_OPTION + " \"" + msfs_project.project_folder + "\"")
        subprocess.run(msfs_build_exe_path + " " + MSFS_BUILD_EXE_OUTPUT_TO_SEPARATE_CONSOLE_OPTION + " \"" + msfs_project.project_definition_xml_path + "\" " + MSFS_BUILD_EXE_OUTPUT_DIR_OPTION + " \"" + msfs_project.project_folder + "\"", shell=True, check=False)
    except:
        raise ScriptError(ERROR_MSG)
