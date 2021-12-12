import os

import bpy
from constants import *
from utils import pr_ko_red, pr_ok_green, pr_ko_orange, isolated_print
from utils.script_errors import ScriptError

RESULT_MSG_LENGTH = 40


######################################################
# check configuration methods
######################################################
def check_configuration(settings, msfs_project, check_lily_texture_packer=False, check_built_package=False, check_compressonator=False):
    error_msg = "Configuration error found ! "
    warning_msg = "Configuration warning ! "

    # check if the projects folder exists
    if not os.path.isdir(msfs_project.parent_path):
        pr_ko_red(str("projects_path value").ljust(RESULT_MSG_LENGTH))
        raise ScriptError(error_msg + "The folder containing your projects (" + msfs_project.parent_path + ") was not found. Please check the projects_path value")
    pr_ok_green(str("projects_path value").ljust(RESULT_MSG_LENGTH))

    # check the projects name
    if not os.path.isdir(msfs_project.project_folder):
        pr_ko_red(str("project_name value").ljust(RESULT_MSG_LENGTH))
        raise ScriptError(
            error_msg + "Project folder " + msfs_project.project_folder + " not found. Please check the project_name value")
    pr_ok_green(str("project_name value").ljust(RESULT_MSG_LENGTH))

    # check if the msfs_project file is reachable
    if not os.path.isfile(msfs_project.project_definition_xml_path):
        pr_ko_red(str("project_file_name value").ljust(RESULT_MSG_LENGTH))
        raise ScriptError(error_msg + "Project file (" + msfs_project.project_definition_xml_path + ") not found. Please check the project_file_name value")
    pr_ok_green(str("project_file_name value").ljust(RESULT_MSG_LENGTH))

    # check if the fspackagetool.exe file is reachable
    if not os.path.isfile(settings.fspackagetool_folder + "\\" + MSFS_BUILD_EXE):
        pr_ko_orange(str("fspackagetool_folder value").ljust(RESULT_MSG_LENGTH))
        settings.build_package_enabled = False
        isolated_print(CORANGE + warning_msg + MSFS_BUILD_EXE + " bin file not found. Automatic package building disabled" + CEND + EOL)
    else:
        pr_ok_green(str("fspackagetool_folder value").ljust(RESULT_MSG_LENGTH))

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

    # check if Lily texture packer is installed
    if check_lily_texture_packer and settings.bake_textures_enabled:
        texture_packer_enabled = False
        try:
            if LILY_TEXTURE_PACKER_ADDON in bpy.context.preferences.addons:
                texture_packer_enabled = True
                pr_ok_green(str("Lily texture packer enabled").ljust(RESULT_MSG_LENGTH))
        except:
            pass

        if not texture_packer_enabled:
            pr_ko_orange(str("Lily texture packer enabled").ljust(RESULT_MSG_LENGTH))
            settings.bake_textures_enabled = False
            isolated_print(CORANGE + warning_msg + " Lily texture packer is not enabled in your blender addons. Baking of the tile textures is disabled" + CEND + EOL)

    if check_built_package:
        # check if the folder containing project package exists
        if not os.path.isdir(msfs_project.built_project_package_folder):
            pr_ko_red(str("built_project_package_folder value").ljust(RESULT_MSG_LENGTH))
            raise ScriptError(error_msg + "The folder containing built package of the project (" + msfs_project.built_project_package_folder + ") was not found. Please check the built_project_package_folder value")
        pr_ok_green(str("built_project_package_folder value").ljust(RESULT_MSG_LENGTH))

    if check_compressonator:
        # check if the compressonatorcli.exe file is reachable
        if not os.path.isfile(os.path.join(settings.compressonator_folder, COMPRESSONATOR_EXE)):
            pr_ko_red(str("compressonator_folder value").ljust(RESULT_MSG_LENGTH))
            raise ScriptError(error_msg + COMPRESSONATOR_EXE + "file was not found in " + msfs_project.compressonator_folder + ". Please check the compressonator_folder value or install compressonator")
        else:
            pr_ok_green(str("compressonator_folder value").ljust(RESULT_MSG_LENGTH))

