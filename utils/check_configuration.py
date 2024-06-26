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

import os

import bpy
from constants import *
from utils import pr_ko_red, pr_ok_green, pr_ko_orange, isolated_print
from utils.install_lib import install_python_lib, install_alternate_python_lib
from utils.console import print_title
from utils.script_errors import ScriptError

RESULT_MSG_LENGTH = 40


######################################################
# check configuration methods
######################################################
def check_configuration(settings, msfs_project, check_optimization=False, check_lily_texture_packer=False, check_built_package=False, check_compressonator=False, check_description_file=True, check_blendergis_addon=False):
    error_msg = "Configuration error found ! "
    warning_msg = "Configuration warning ! "
    from UI.prefs import get_prefs
    prefs = get_prefs()

    print_title("CHECK CONFIGURATION FOR " + msfs_project.project_name + " PROJECT")

    # check if the projects folder exists
    if not os.path.isdir(msfs_project.parent_path):
        pr_ko_red(str("projects_path value").ljust(RESULT_MSG_LENGTH))
        raise ScriptError(error_msg + "The folder containing your projects (" + msfs_project.parent_path + ") was not found. Please check the projects_path value")
    pr_ok_green(str("projects_path value").ljust(RESULT_MSG_LENGTH))

    # check the projects name
    if not os.path.isdir(msfs_project.project_folder):
        pr_ko_red(str("project_name value").ljust(RESULT_MSG_LENGTH))
        raise ScriptError(error_msg + "Project folder " + msfs_project.project_folder + " not found. Please check the project_name value")
    pr_ok_green(str("project_name value").ljust(RESULT_MSG_LENGTH))

    # check if the msfs_project file is reachable
    if not os.path.isfile(msfs_project.project_definition_xml_path):
        pr_ko_red(str("project_file_name value").ljust(RESULT_MSG_LENGTH))
        raise ScriptError(error_msg + "Project file (" + msfs_project.project_definition_xml_path + ") not found. Please check the project_file_name value")
    pr_ok_green(str("project_file_name value").ljust(RESULT_MSG_LENGTH))

    # check if the fspackagetool.exe file is reachable
    msfs_build_exe_path_check = False
    msfs_build_exe_path = "msfs build exe path"
    if prefs is not None:
        msfs_build_exe_path_check = os.path.isfile(prefs.msfs_build_exe_path)
        msfs_build_exe_path = prefs.msfs_build_exe_path

    if not msfs_build_exe_path_check:
        pr_ko_orange(str("msfs_build_exe_path value").ljust(RESULT_MSG_LENGTH))
        msfs_project.settings.build_package_enabled = False
        msfs_project.settings.save()
        isolated_print(CORANGE + warning_msg + msfs_build_exe_path + " bin file not found. Automatic package building is disabled" + CEND + EOL)
    else:
        pr_ok_green(str("msfs_build_exe_path value").ljust(RESULT_MSG_LENGTH))

    # check if the package definitions folder exists
    if not os.path.isdir(msfs_project.package_definitions_folder):
        pr_ko_red(str("package_definitions_folder value").ljust(RESULT_MSG_LENGTH))
        raise ScriptError(error_msg + "The folder containing the package definitions of the msfs_project (" + msfs_project.package_definitions_folder + ") was not found. Please check the package_definitions_folder value")
    pr_ok_green(str("package_definitions_folder value").ljust(RESULT_MSG_LENGTH))

    # check if the package definitions file name is reachable
    if not os.path.isfile(msfs_project.package_definitions_xml_path):
        pr_ko_red(str("package_definitions_file_name value").ljust(RESULT_MSG_LENGTH))
        raise ScriptError(error_msg + "Package definitions file (" + msfs_project.package_definitions_xml_path + ") not found. Please check the package_definitions_file_name value")
    pr_ok_green(str("package_definitions_file_name value").ljust(RESULT_MSG_LENGTH))

    # check if the objects folder exists
    if not os.path.isdir(msfs_project.model_lib_folder):
        pr_ko_red(str("objects_folder value").ljust(RESULT_MSG_LENGTH))
        raise ScriptError(error_msg + "The folder containing the objects of the msfs_project (" + msfs_project.model_lib_folder + ") was not found. Please check the objects_folder value")
    pr_ok_green(str("objects_folder value").ljust(RESULT_MSG_LENGTH))

    # check if the folder containing the description files of the scene exists
    if not os.path.isdir(msfs_project.scene_folder):
        pr_ko_red(str("scene_folder value").ljust(RESULT_MSG_LENGTH))
        raise ScriptError(error_msg + "The folder containing the description files of the scene (" + msfs_project.scene_folder + ") was not found. Please check the scene_folder value")
    pr_ok_green(str("scene_folder value").ljust(RESULT_MSG_LENGTH))

    # check if the necessary blender addons exist
    if check_blendergis_addon:
        from blender.addons import install_blender_addon
        if not install_blender_addon(BLENDERGIS_ADDON, BLENDERGIS_GITHUB_DOWNLOAD_REPO, BLENDERGIS_ADDON_RELEASE + ZIP_FILE_EXT):
            pr_ko_red(str("Blender GIS addon installation").ljust(RESULT_MSG_LENGTH))
            raise ScriptError(error_msg + "Blender GIS addon is not correctly installed. Try to install it manually instead")
        pr_ok_green(str("Blender GIS addon installation").ljust(RESULT_MSG_LENGTH))
        if bpy.context.preferences is not None:
            bpy.context.preferences.addons[BLENDERGIS_ADDON].preferences.logLevel = CRITICAL_LOG_LEVEL
            bpy.context.preferences.addons[BLENDERGIS_ADDON].preferences.predefCrs = EPSG_WGS84

    if check_description_file:
        # check if the description file of the scene is reachable
        if not os.path.isfile(msfs_project.scene_objects_xml_file_path):
            pr_ko_red(str("scene_file_name value").ljust(RESULT_MSG_LENGTH))
            raise ScriptError(error_msg + "Description file of the scene (" + msfs_project.scene_objects_xml_file_path + ") not found. Please check the scene_file_name value")
        pr_ok_green(str("scene_file_name value").ljust(RESULT_MSG_LENGTH))

    # check if the folder containing the textures of the scene exists
    if not os.path.isdir(msfs_project.texture_folder):
        pr_ko_red(str("textures_folder value").ljust(RESULT_MSG_LENGTH))
        raise ScriptError(error_msg + "The folder containing the textures of the scene (" + msfs_project.texture_folder + ") was not found. Please check the textures_folder value")
    pr_ok_green(str("textures_folder value").ljust(RESULT_MSG_LENGTH))

    if check_optimization:
        if not install_python_lib(PILLOW_LIB):
            pr_ko_red(str("Pillow lib installation").ljust(RESULT_MSG_LENGTH))
            raise ScriptError(error_msg + "Pillow python lib is not correctly installed. Please check what can prevent this library to be installed correctly")
    pr_ok_green(str("Pillow lib installation").ljust(RESULT_MSG_LENGTH))

    if check_optimization:
        if not install_python_lib(NUMPY_LIB, NUMPY_LIB_VERSION):
            pr_ko_red(str("Numpy lib installation").ljust(RESULT_MSG_LENGTH))
            raise ScriptError(error_msg + "Numpy python lib is not correctly installed. Please check what can prevent this library to be installed correctly")
    pr_ok_green(str("Numpy lib installation").ljust(RESULT_MSG_LENGTH))

    if check_optimization:
        if not install_alternate_python_lib(GDAL_LIB_PREFIX):
            pr_ko_red(str("Gdal lib installation").ljust(RESULT_MSG_LENGTH))
            raise ScriptError(error_msg + "Gdal python lib is not correctly installed. Please check what can prevent this library to be installed correctly")
    pr_ok_green(str("Gdal lib installation").ljust(RESULT_MSG_LENGTH))

    if check_optimization:
        if not install_python_lib(NETWORKX_LIB):
            pr_ko_red(str("Networkx lib installation").ljust(RESULT_MSG_LENGTH))
            raise ScriptError(error_msg + "Networkx python lib is not correctly installed. Please check what can prevent this library to be installed correctly")
    pr_ok_green(str("Networkx lib installation").ljust(RESULT_MSG_LENGTH))

    if check_optimization:
        if not install_python_lib(RTREE_LIB):
            pr_ko_red(str("Rtree lib installation").ljust(RESULT_MSG_LENGTH))
            raise ScriptError(error_msg + "Rtree python lib is not correctly installed. Please check what can prevent this library to be installed correctly")
    pr_ok_green(str("Rtree lib installation").ljust(RESULT_MSG_LENGTH))

    if check_optimization:
        if not install_python_lib(MATPLOTLIB_LIB):
            pr_ko_red(str("MatplotLib lib installation").ljust(RESULT_MSG_LENGTH))
            raise ScriptError(error_msg + "MatplotLib python lib is not correctly installed. Please check what can prevent this library to be installed correctly")
    pr_ok_green(str("MatplotLib lib installation").ljust(RESULT_MSG_LENGTH))

    if check_optimization:
        if not install_alternate_python_lib(FIONA_LIB_PREFIX):
            pr_ko_red(str("Fiona lib installation").ljust(RESULT_MSG_LENGTH))
            raise ScriptError(error_msg + "Fiona python lib is not correctly installed. Please check what can prevent this library to be installed correctly")
    pr_ok_green(str("Fiona lib installation").ljust(RESULT_MSG_LENGTH))

    if check_optimization:
        if not install_python_lib(SHAPELY_LIB):
            pr_ko_red(str("Shapely lib installation").ljust(RESULT_MSG_LENGTH))
            raise ScriptError(error_msg + "Shapely python lib is not correctly installed. Please check what can prevent this library to be installed correctly")
    pr_ok_green(str("Shapely lib installation").ljust(RESULT_MSG_LENGTH))

    if check_optimization:
        if not install_python_lib(PANDAS_LIB):
            pr_ko_red(str("Pandas lib installation").ljust(RESULT_MSG_LENGTH))
            raise ScriptError(error_msg + "Pandas python lib is not correctly installed. Please check what can prevent this library to be installed correctly")
    pr_ok_green(str("Pandas lib installation").ljust(RESULT_MSG_LENGTH))

    if check_optimization:
        if not install_python_lib(GEOPANDAS_LIB):
            pr_ko_red(str("GeoPandas lib installation").ljust(RESULT_MSG_LENGTH))
            raise ScriptError(error_msg + "GeoPandas python lib is not correctly installed. Please check what can prevent this library to be installed correctly")
    pr_ok_green(str("GeoPandas lib installation").ljust(RESULT_MSG_LENGTH))

    if check_optimization:
        if not install_python_lib(OSMNX_LIB, OSMNX_LIB_VERSION):
            pr_ko_red(str("Osmnx lib installation").ljust(RESULT_MSG_LENGTH))
            raise ScriptError(error_msg + "Osmnx python lib is not correctly installed. Please check what can prevent this library to be installed correctly")
    pr_ok_green(str("Osmnx lib installation").ljust(RESULT_MSG_LENGTH))

    if check_optimization:
        if not install_python_lib(PYGEODESY_LIB):
            pr_ko_red(str("Pygeodesy lib installation").ljust(RESULT_MSG_LENGTH))
            raise ScriptError(error_msg + "Pygeodesy python lib is not correctly installed. Please check what can prevent this library to be installed correctly")
    pr_ok_green(str("Pygeodesy lib installation").ljust(RESULT_MSG_LENGTH))

    # check if Lily texture packer is installed
    if check_lily_texture_packer and settings.bake_textures_enabled:
        check_lily_texture_packer_availability(settings, warning_msg=warning_msg)

    if check_built_package:
        # check if the folder containing project package exists
        if not os.path.isdir(msfs_project.built_project_package_folder):
            pr_ko_red(str("built_project_package_folder value").ljust(RESULT_MSG_LENGTH))
            raise ScriptError(error_msg + "The folder containing built package of the project (" + msfs_project.built_project_package_folder + ") was not found. Please check the built_project_package_folder value")
        pr_ok_green(str("built_project_package_folder value").ljust(RESULT_MSG_LENGTH))

    if check_compressonator:
        compressonator_exe_path_check = False
        compressonator_exe_path = "compressonator exe path"
        if prefs is not None:
            compressonator_exe_path_check = os.path.isfile(prefs.compressonator_exe_path)
            compressonator_exe_path = prefs.compressonator_exe_path

        # check if the compressonatorcli.exe file is reachable
        if not compressonator_exe_path_check:
            pr_ko_red(str("compressonator_exe_path value").ljust(RESULT_MSG_LENGTH))
            raise ScriptError(error_msg + compressonator_exe_path + "file was not found. Please check the compressonator_exe_path value or install compressonator")
        else:
            pr_ok_green(str("compressonator_exe_path value").ljust(RESULT_MSG_LENGTH))


def check_lily_texture_packer_availability(settings, warning_msg=str()):
    texture_packer_enabled = False
    try:
        if LILY_TEXTURE_PACKER_ADDON in bpy.context.preferences.addons:
            texture_packer_enabled = True
            pr_ok_green(str("Lily texture packer enabled").ljust(RESULT_MSG_LENGTH))
    except:
        pass

    if not texture_packer_enabled:
        pr_ko_orange(str("Lily texture packer disabled").ljust(RESULT_MSG_LENGTH))
        settings.bake_textures_enabled = False
        isolated_print(CORANGE + warning_msg + " Lily texture packer is not enabled in your blender addons. Baking of the tile textures is disabled" + CEND + EOL)
