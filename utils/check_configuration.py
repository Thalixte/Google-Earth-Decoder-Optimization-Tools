import os

from constants import *
from utils import pr_ko_red, pr_ok_green, pr_ko_orange
from utils.script_errors import ScriptError


######################################################
# check configuration methods
######################################################
def check_configuration(settings, msfs_project):
    error_msg = "Configuration error found ! "
    warning_msg = "Configuration warning ! "

    # check if the projects folder exists
    if not os.path.isdir(msfs_project.parent_path):
        pr_ko_red("projects_path value              ")
        raise ScriptError(
            error_msg + "The folder containing your projects (" + msfs_project.parent_path + ") was not found. Please check the projects_path value")
    pr_ok_green("projects_path value              ")

    # check the projects name
    if not os.path.isdir(msfs_project.project_folder):
        pr_ko_red("project_name value                 ")
        raise ScriptError(
            error_msg + "Project folder " + msfs_project.project_folder + " not found. Please check the project_name value")
    pr_ok_green("project_name value                 ")

    # check if the msfs_project file is reachable
    if not os.path.isfile(msfs_project.project_definition_xml_path):
        pr_ko_red("project_file_name value            ")
        raise ScriptError(
            error_msg + "Project file (" + msfs_project.project_definition_xml_path + ") not found. Please check the project_file_name value")
    pr_ok_green("project_file_name value            ")

    # check if the fspackagetool.exe file is reachable
    if not os.path.isfile(settings.fspackagetool_folder + "\\" + MSFS_BUILD_EXE):
        pr_ko_orange("fspackagetool_folder value         ")
        settings.build_package_enabled = False
        print(CORANGE + warning_msg + MSFS_BUILD_EXE + " bin file not found. Automatic package building disabled" + CEND + EOL)
    else:
        pr_ok_green("fspackagetool_folder value         ")

    # check if the package definitions folder exists
    if not os.path.isdir(msfs_project.package_definitions_folder):
        pr_ko_red("package_definitions_folder value   ")
        raise ScriptError(
            error_msg + "The folder containing the package definitions of the msfs_project (" + msfs_project.package_definitions_folder + ") was not found. Please check the package_definitions_folder value")
    pr_ok_green("package_definitions_folder value   ")

    # check if the package definitions file name is reachable
    if not os.path.isfile(msfs_project.package_definitions_xml_path):
        pr_ko_red("package_definitions_file_name value")
        raise ScriptError(
            error_msg + "Package definitions file (" + msfs_project.package_definitions_xml_path + ") not found. Please check the package_definitions_file_name value")
    pr_ok_green("package_definitions_file_name value")

    # check if the objects folder exists
    if not os.path.isdir(msfs_project.modelLib_folder):
        pr_ko_red("objects_folder value               ")
        raise ScriptError(
            error_msg + "The folder containing the objects of the msfs_project (" + msfs_project.modelLib_folder + ") was not found. Please check the objects_folder value")
    pr_ok_green("objects_folder value               ")

    # check if the folder containing the description files of the scene exists
    if not os.path.isdir(msfs_project.scene_folder):
        pr_ko_red("scene_folder value                 ")
        raise ScriptError(
            error_msg + "The folder containing the description files of the scene (" + msfs_project.scene_folder + ") was not found. Please check the scene_folder value")
    pr_ok_green("scene_folder value                 ")

    # check if the description file of the scene is reachable
    if not os.path.isfile(msfs_project.scene_objects_xml_file_path):
        pr_ko_red("scene_file_name value              ")
        raise ScriptError(
            error_msg + "Description file of the scene (" + msfs_project.scene_objects_xml_file_path + ") not found. Please check the scene_file_name value")
    pr_ok_green("scene_file_name value              ")

    # check if the folder containing the textures of the scene exists
    if not os.path.isdir(msfs_project.texture_folder):
        pr_ko_red("textures_folder value              ")
        raise ScriptError(
            error_msg + "The folder containing the textures of the scene (" + msfs_project.texture_folder + ") was not found. Please check the textures_folder value")
    pr_ok_green("textures_folder value              ")
