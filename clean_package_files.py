######################################################
# script settings
######################################################

# constants
CEND = "\033[0m"
BOLD = "\033[01m"
CRED = "\033[31m"
CGREEN = "\033[32m"
CORANGE = "\033[38;5;214m"
CREDBG = "\033[41m"
CGREENBG = "\033[6;30;42m"
OK = "OK"
KO = "KO"
EOL = "\n"
NODE_JS_SCRIPT="retrievelpos.js"
MSFS_BUILD_EXE_FILE="fspackagetool.exe"

# folder where the scenery projects are placed
projects_folder = "E:\\MSFSProjects"

# folder of the scenery project you want to optimize
project_name = "My_project"

# folder that contains the fspackagetool exe that builds the MSFS packages
fspackagetool_folder = "C:\\MSFS SDK\\Tools\\bin"

# minsize values per LOD, starting from a minLod of 17 (from the less detailed lod to the most detailed)
target_lods = [0, 15, 50, 70, 80, 90, 100]
# if you use a minLod of 16, consider using this array instead
# target_lods = [0, 5, 15, 50, 70, 80, 90, 100]

# name of the xml file that embeds the project definition (by default, project_name.xml or author_name+project_name.xml)
project_file_name = "author_name-project_name.xml"

# name of the xml file that embeds the tile descriptions (by default, objects.xml)
scene_file_name = "objects.xml"

# name of the xml file that embeds the package definitions (by default, project_name.xml or author_name+project_name.xml)
package_definitions_file_name = "author_name-project_name.xml"

# author name
author_name = "author_name"

# enable the package compilation when the script has finished
build_package_enabled = True

#######################****************###########################

import sys, bpy, glob, os, shutil, json, uuid, mathutils, math, subprocess
from math import radians, cos, sin, asin, sqrt
from xml.dom.minidom import *
from mathutils import Vector 
from xml.dom.minidom import *
import xml.etree.ElementTree as ET

class ScriptError(Exception):      
    def __init__(self, value):
       self.value = CREDBG + value + CEND + EOL
    def __str__(self):
        return repr(CREDBG + self.value + CEND + EOL)

# clear the system console
os.system("cls")

# initial directory 
cwd = os.path.dirname(__file__)

project_folder = projects_folder + "\\" + project_name
# project file name fallback
if not os.path.isfile(project_folder + "\\" + project_file_name):
    if os.path.isfile(project_folder + "\\" + author_name.lower() + "-" + project_name.lower() + ".xml"):
        project_file_name = project_folder + "\\" + author_name.lower() + "-" + project_name.lower() + ".xml"
    else:
        project_file_name = project_name.lower() + ".xml"
    
# package definitions folder
package_definitions_folder = project_folder + "\\PackageDefinitions\\"

# package definitions file name fallback
if not os.path.isfile(package_definitions_folder + package_definitions_file_name):
    if os.path.isfile(package_definitions_folder + author_name.lower() + "-" + project_name.lower() + ".xml"):
        package_definitions_file_name = author_name.lower() + "-" + project_name.lower() + ".xml"
    else:
        package_definitions_file_name = project_name.lower() + ".xml"
    
# objects folder
objects_folder = project_folder + "\\PackageSources\\modelLib\\"
# scene folder
scene_folder = project_folder + "\\PackageSources\\scene\\"
# backup folder
backup_folder = project_folder + "\\backup\\clean_package_files"
# backup fps_modelLib folder
backup_modelLib_folder = backup_folder + "\\modelLib"
# backup scene folder
backup_scene_folder = backup_folder + "\\scene"


######################################################
# colored print methods
######################################################
def pr_red(skk):       print(CRED, format(skk), CEND)
def pr_green(skk):     print(CGREEN, format(skk), CEND)
def pr_ko_red(skk):    print("-", format(skk), BOLD + CRED, KO, CEND)
def pr_ko_orange(skk): print("-", format(skk), BOLD + CORANGE, KO, CEND)
def pr_ok_green(skk):  print("-", format(skk), BOLD + CGREEN, OK, CEND)
def pr_bg_red(skk):    print(CREDBG, format(skk), CEND)
def pr_bg_green(skk):  print(CGREENBG, format(skk), CEND)

######################################################
# check configuration methods
######################################################

def check_configuration():
    error_msg = "Configuration error found ! "    
    warning_msg = "Configuration warning ! "
    
    # check if the projects folder exists
    if not os.path.isdir(projects_folder):
        pr_ko_red   ("projects_folder value              ")
        raise ScriptError(error_msg + "The folder containing your projects (" + projects_folder + ") was not found. Please check the projects_folder value")
    pr_ok_green     ("projects_folder value              ")
        
    # check the projects name
    if not os.path.isdir(project_folder):
        pr_ko_red   ("project_name value                 ")
        raise ScriptError(error_msg + "Project folder " + project_folder + " not found. Please check the project_name value")
    pr_ok_green     ("project_name value                 ")    
             
    # check if the project file is reachable
    if not os.path.isfile(project_folder + "\\" + project_file_name):
        pr_ko_red   ("project_file_name value            ")
        raise ScriptError(error_msg + "Project file (" + project_folder + "\\" + project_file_name + ") not found. Please check the project_file_name value")
    pr_ok_green     ("project_file_name value            ")
    
    # check if the fspackagetool.exe file is reachable
    if not os.path.isfile(fspackagetool_folder + "\\" + MSFS_BUILD_EXE_FILE):
        pr_ko_orange("fspackagetool_folder value         ")
        build_package_enabled = False
        print(CORANGE + warning_msg + MSFS_BUILD_EXE_FILE + " bin file not found. Automatic package building disabled" + CEND + EOL)
    pr_ok_green     ("fspackagetool_folder value         ")
        
    # check if the package definitions folder exists
    if not os.path.isdir(package_definitions_folder):
        pr_ko_red   ("package_definitions_folder value   ")
        raise ScriptError(error_msg + "The folder containing the package definitions of the project (" + package_definitions_folder + ") was not found. Please check the package_definitions_folder value")
    pr_ok_green     ("package_definitions_folder value   ")
    
    # check if the package definitions file name is reachable
    if not os.path.isfile(package_definitions_folder + package_definitions_file_name):
        pr_ko_red   ("package_definitions_file_name value")
        raise ScriptError(error_msg + "Package definitions file (" + package_definitions_folder + package_definitions_file_name + ") not found. Please check the package_definitions_file_name value")
    pr_ok_green     ("package_definitions_file_name value")

def check_package_sources_configuration():
    error_msg = "Configuration error found ! "

    # check if the objects folder exists
    if not os.path.isdir(objects_folder):
        pr_ko_red   ("objects_folder value               ")
        raise ScriptError(error_msg + "The folder containing the objects of the project (" + objects_folder + ") was not found. Please check the objects_folder value")
    pr_ok_green     ("objects_folder value               ")
            
    # check if the folder containing the description files of the scene exists
    if not os.path.isdir(scene_folder):
        pr_ko_red   ("scene_folder value                 ")
        raise ScriptError(error_msg + "The folder containing the description files of the scene (" + scene_folder + ") was not found. Please check the scene_folder value")
    pr_ok_green     ("scene_folder value                 ")
    
    # check if the description file of the scene is reachable
    if not os.path.isfile(scene_folder + scene_file_name):
        pr_ko_red   ("scene_file_name value              ")
        raise ScriptError(error_msg + "Description file of the scene (" + scene_folder + scene_file_name + ") not found. Please check the scene_file_name value")
    pr_ok_green     ("scene_file_name value              ")
        
    # check if the folder containing the textures of the scene exists
    if not os.path.isdir(textures_folder):
        pr_ko_red   ("textures_folder value              ")
        raise ScriptError(error_msg + "The folder containing the textures of the scene (" + textures_folder + ") was not found. Please check the textures_folder value")
    pr_ok_green     ("textures_folder value              ")
        
##################################################################
# Backup the packageSources files before the optimisation process
##################################################################      
def backup_files():
    os.chdir(objects_folder)
    for file in glob.glob("*.*"):
        file_name = os.path.basename(file)
        if not os.path.isfile(backup_modelLib_folder + "\\" + file_name):
            print("backup file ", file_name)
            shutil.copyfile(file, backup_modelLib_folder + "\\" + file_name)
            
    os.chdir(textures_folder)
    for file in glob.glob("*.*"):
        file_name = os.path.basename(file)
        if not os.path.isfile(backup_modelLib_folder + "\\texture\\" + file_name):
            print("backup texture file ", file_name)
            shutil.copyfile(file, backup_modelLib_folder + "\\texture\\" + file_name)
            
    os.chdir(scene_folder)
    for file in glob.glob("*.*"):
        file_name = os.path.basename(file)
        if not os.path.isfile(backup_scene_folder + "\\" + file_name):
            shutil.copyfile(file, backup_scene_folder + "\\" + file_name)
        
######################################################
# File manipulation methods
###################################################### 
def line_prepender(filename, line):
    with open(filename, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip("\r\n") + "\n" + content)
        
######################################################
# File replacement methods
###################################################### 
def replace_in_file(file, text, replacement):
    updated_gltf_file = open(file, "rt")
    data = updated_gltf_file.read()
    data = data.replace(text,replacement)
    updated_gltf_file.close()
    updated_gltf_file = open(file, "wt")
    updated_gltf_file.write(data)
    updated_gltf_file.close()
        
##################################################################
# Clean all package files linked to an orphan xml object file
##################################################################
def clean_linked_package_files(xml_file, xml_file_path):
    os.chdir(objects_folder)
    
    for package_file in glob.glob(xml_file + "_LOD*.*"):
        file_path = os.path.basename(package_file)
        try:
            os.remove(file_path)
        except OSError as e:
            error_msg = "Error: " + file_path + " : " + e.strerror
            raise ScriptError(error_msg)
            
        print("package file:", file_path, "removed")
                
    os.chdir(textures_folder)
    for texture_file in glob.glob(xml_file + "_LOD*.*"):
        file_path = os.path.basename(texture_file)
        try:
            os.remove(file_path)
        except OSError as e:
            error_msg = "Error: " + file_path + " : " + e.strerror
            raise ScriptError(error_msg)
            
        print("texture file:", file_path, "removed")
        
    os.chdir(objects_folder)
    try:
        os.remove(xml_file_path)
    except OSError as e:
        error_msg = "Error: " + xml_file_path + " : " + e.strerror
        raise ScriptError(error_msg)
        
    print("scenery object xml file:", xml_file_path, "removed")

##################################################################
# Clean all package files for lods that do not exist
##################################################################
def clean_unused_lod_package_files():
    os.chdir(objects_folder)
    
    for xml_file in glob.glob("*.xml"):
        file_path = os.path.basename(xml_file)
        file_name = os.path.splitext(xml_file)[0]
        tree = ET.parse(xml_file)
        root = tree.getroot()
         
        for gltf_file in glob.glob(file_name + "_LOD*.gltf"):
            lod_found = False                    
            gltf_file_path = os.path.basename(gltf_file)                    
            gltf_file_name = os.path.splitext(gltf_file)[0]
            
            for scenery_object in root.findall("./LODS/LOD[@ModelFile='" + gltf_file + "']"):
                lod_found = True
            
            if not lod_found:
                bin_file = gltf_file_name + ".bin"
                bin_file_path = os.path.basename(bin_file)
                
                print("unused lod bin file:", bin_file)
                        
                try:
                    os.remove(bin_file)
                except OSError as e:
                    error_msg = "Error: " + bin_file + " : " + e.strerror
                    raise ScriptError(error_msg)
                    
                print("unused lod bin file:", bin_file, "removed")
                
                print("unused lod bin file:", gltf_file)
                        
                try:
                    os.remove(gltf_file)
                except OSError as e:
                    error_msg = "Error: " + gltf_file + " : " + e.strerror
                    raise ScriptError(error_msg)
                    
                print("unused lod gltf file:", gltf_file, "removed")
                    
                os.chdir(textures_folder)
                for texture_file in glob.glob(gltf_file_name + ".*"):
                    file_path = os.path.basename(texture_file)
                
                    print("unused lod bin file:", texture_file)
                
                    try:
                        os.remove(file_path)
                    except OSError as e:
                        error_msg = "Error: " + file_path + " : " + e.strerror
                        raise ScriptError(error_msg)
                        
                    print("unused lod texture file:", file_path, "removed")
                    
            os.chdir(objects_folder)    
                     
##################################################################
# Clean all unused package files
##################################################################  
def clean_package_files(objects_tree):
    os.chdir(objects_folder)
    objects_root = objects_tree.getroot()
        
    for xml_file in glob.glob("*.xml"):
        file_path = os.path.basename(xml_file)
        guid_found = False
        file_name = os.path.splitext(xml_file)[0]
        pos_name = file_name + ".pos"
        tree = ET.parse(xml_file)
        root = tree.getroot()
        guid  = root.get("guid") 
        
        for scenery_object in objects_root.findall("./SceneryObject/LibraryObject[@name='" + guid.upper() + "']"):
            guid_found = True
                
        for scenery_object in objects_root.findall("./Group/SceneryObject/LibraryObject[@name='" + guid.upper() + "']"):
            guid_found = True
        
        for scenery_object in objects_root.findall("./SceneryObject/LibraryObject[@name='" + guid.lower() + "']"):
            guid_found = True
                
        for scenery_object in objects_root.findall("./Group/SceneryObject/LibraryObject[@name='" + guid.lower() + "']"):
            guid_found = True
        
        if not guid_found:
            print("-------------------------------------------------------------------------------")
            print("xml file: ", file_path)
            print("unused package file detected:", os.path.basename(xml_file))
            clean_linked_package_files(file_name, os.path.basename(xml_file)) 
            
        os.chdir(objects_folder)

######################################################
# build scenery into new MSFS package
######################################################  
def build_package():
    error_msg = "MSFS SDK tools not installed"
    
    try: 
        os.chdir(fspackagetool_folder)
        print("fspackagetool.exe \"" + project_folder + "\\" + project_file_name + "\" -outputdir \"" + project_folder)
        subprocess.run("fspackagetool.exe \"" + project_folder + "\\" + project_file_name + "\" -outputdir \"" + project_folder, shell=True, check=True)
    except:
        raise ScriptError(error_msg)
        
#######################****************###########################

##################################################################
#                        Main process
##################################################################
    
try:     
    check_configuration()
    
    # change modelib folder to fix CTD issues (see https://flightsim.to/blog/creators-guide-fix-ctd-issues-on-your-scenery/)
    os.chdir(project_folder)
    if os.path.isdir(objects_folder):
        os.rename(objects_folder, project_folder + "\\PackageSources\\" + project_name.lower() + "-modelLib")

    objects_folder = project_folder + "\\PackageSources\\" + project_name.lower() + "-modelLib\\"
    # fix package definitions
    replace_in_file(package_definitions_folder + package_definitions_file_name, "PackageSources\\modelLib\\", "PackageSources\\" + project_name.lower() + "-modelLib\\")

    # textures folder
    textures_folder = objects_folder + "texture\\"  
        
    check_package_sources_configuration()

    # create the backup folders
    if not os.path.isdir(backup_folder):
        os.mkdir(backup_folder)    
    if not os.path.isdir(backup_scene_folder):
        os.mkdir(backup_scene_folder)    
    if not os.path.isdir(backup_modelLib_folder):
        os.mkdir(backup_modelLib_folder)
    if not os.path.isdir(backup_modelLib_folder + "\\texture"):
        os.mkdir(backup_modelLib_folder + "\\texture")
    
    os.chdir(objects_folder)
 
    if not os.path.isdir(project_folder + "\\PackageSources\\modelLib") and not os.path.isdir(project_folder + "\\PackageSources\\" + project_name.lower() + "-modelLib"):
        print("The modelLib folder was not found for the projet", project_name, ". Please rename your modelLib folder like this:", project_folder + "\\PackageSources\\" + project_name.lower() + "-modelLib")
    else:    
        print("-------------------------------------------------------------------------------")
        print("--------------------------------- BACKUP FILES --------------------------------")
        print("-------------------------------------------------------------------------------")

        backup_files()
    
        print("-------------------------------------------------------------------------------")
        print("----------------------------- CLEAN PACKAGE FILES -----------------------------")
        print("-------------------------------------------------------------------------------")
                
        objects_tree = ET.parse(scene_folder + scene_file_name)
        clean_package_files(objects_tree)
        clean_unused_lod_package_files()
        
        if build_package_enabled:
            build_package()
    
    print(EOL)    
    pr_bg_green("Script correctly applied" + CEND)

except ScriptError as ex:
    error_report = "".join(ex.value)
    print(EOL + error_report)
    pr_bg_red("Script aborted" + CEND)
except RuntimeError as ex:
    print(EOL + ex)
    pr_bg_red("Script aborted" + CEND)
finally:  
    os.chdir(cwd)