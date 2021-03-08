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
MSFS_BUILD_EXE_FILE = "fspackagetool.exe"

# folder where the scenery projects are placed
projects_folder = "E:\\MSFSProjects"

# folder of the scenery project you want to add to the final scenery project
src_project_name = "My_src_project"

# folder of the final scenery project you want to merge into
dest_project_name = "My_dest_project"

# folder that contains the fspackagetool exe that builds the MSFS packages
fspackagetool_folder = "C:\\MSFS SDK\\Tools\\bin"

# name of the xml file that embeds the project definition (by default, project_name.xml or author_name+src_project_name.xml)
# for the scenery project you want to add to the final scenery project
src_project_file_name = "author_name-src_project_name.xml"

# name of the xml file that embeds the project definition (by default, project_name.xml or author_name+dest_project_name.xml)
# for the final scenery project you want to merge into
dest_project_file_name = "author_name-dest_project_name.xml"

# name of the xml file that embeds the tile descriptions (by default, objects.xml)
# for the scenery project you want to add to the final scenery project
src_scene_file_name = "objects.xml"

# name of the xml file that embeds the tile descriptions (by default, objects.xml) 
# for the final scenery project you want to merge into
dest_scene_file_name = "objects.xml"

# name of the xml file that embeds the package definitions (by default, project_name.xml or author_name+dest_project_name.xml)
# for the scenery project you want to add to the final scenery project
src_package_definitions_file_name = "author_name-src_project_name.xml"

# name of the xml file that embeds the package definitions (by default, project_name.xml or author_name+src_project_name.xml)
# for the final scenery project you want to merge into
dest_package_definitions_file_name = "author_name-dest_project_name.xml"

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

src_project_folder = projects_folder + "\\" + src_project_name
dest_project_folder = projects_folder + "\\" + dest_project_name

# project file names fallback
if not os.path.isfile(src_project_folder + "\\" + src_project_file_name):
    if os.path.isfile(src_project_folder + author_name.lower() + "-" + src_project_name.lower() + ".xml"):
        src_project_file_name = src_project_folder + author_name.lower() + "-" + src_project_name.lower() + ".xml"
    else:
        src_project_file_name = src_project_name.lower() + ".xml"
        
if not os.path.isfile(dest_project_folder + "\\" + dest_project_file_name):
    if os.path.isfile(dest_project_folder + author_name.lower() + "-" + dest_project_name.lower() + ".xml"):
        dest_project_file_name = dest_project_folder + author_name.lower() + "-" + dest_project_name.lower() + ".xml"
    else:
        dest_project_file_name = dest_project_name.lower() + ".xml"
    
# package definitions folder
src_package_definitions_folder = src_project_folder + "\\PackageDefinitions\\"
dest_package_definitions_folder = dest_project_folder + "\\PackageDefinitions\\"

# package definitions file names fallback
if not os.path.isfile(src_package_definitions_folder + src_package_definitions_file_name):
    if os.path.isfile(src_package_definitions_folder + author_name.lower() + "-" + src_project_name.lower() + ".xml"):
        src_package_definitions_file_name = author_name.lower() + "-" + src_project_name.lower() + ".xml"
    else:
        src_package_definitions_file_name = src_project_name.lower() + ".xml"        

if not os.path.isfile(dest_package_definitions_folder + dest_package_definitions_file_name):
    if os.path.isfile(dest_package_definitions_folder + author_name.lower() + "-" + dest_project_name.lower() + ".xml"):
        dest_package_definitions_file_name = author_name.lower() + "-" + dest_project_name.lower() + ".xml"
    else:
        dest_package_definitions_file_name = dest_project_name.lower() + ".xml"

# objects folders
src_objects_folder = src_project_folder + "\\PackageSources\\modelLib\\"
dest_objects_folder = dest_project_folder + "\\PackageSources\\modelLib\\"
# scene folders
src_scene_folder = src_project_folder + "\\PackageSources\\scene\\"
dest_scene_folder = dest_project_folder + "\\PackageSources\\scene\\"
# backup folders
src_backup_folder = src_project_folder + "\\backup"
dest_backup_folder = dest_project_folder + "\\backup\\merge_sceneries"
# backup fps_modelLib folders
src_backup_modelLib_folder = src_backup_folder + "\\modelLib"
dest_backup_modelLib_folder = dest_backup_folder + "\\modelLib"
# backup scene folders
src_backup_scene_folder = src_backup_folder + "\\scene"
dest_backup_scene_folder = dest_backup_folder + "\\scene"
# positions folders
src_positions_folder = src_project_folder + "\\positions"
dest_positions_folder = dest_project_folder + "\\positions"
# MSFS temp folder
msfs_temp_folder = dest_project_folder + "\\_PackageInt"

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
        pr_ko_red   ("projects_folder value                   ")
        raise ScriptError(error_msg + "The folder containing your projects (" + projects_folder + ") was not found. Please check the projects_folder value")
    pr_ok_green     ("projects_folder value                   ")
        
    # check the projects names
    if not os.path.isdir(src_project_folder):
        pr_ko_red   ("src_project_name value                  ")
        raise ScriptError(error_msg + "Source project folder " + src_project_folder + " not found. Please check the src_project_name value")
    pr_ok_green     ("src_project_name value                  ")    
    if not os.path.isdir(dest_project_folder):
        pr_ko_red   ("dest_project_name value                 ")
        raise ScriptError(error_msg + "Destination project folder " + dest_project_folder + " not found. Please check the dest_project_name value")
    pr_ok_green     ("dest_project_name value                 ") 
             
    # check if the project files are reachable
    if not os.path.isfile(src_project_folder + "\\" + src_project_file_name):
        pr_ko_red   ("src_project_file_name value             ")
        raise ScriptError(error_msg + "Source project file (" + src_project_folder + "\\" + src_project_file_name + ") not found. Please check the src_project_file_name value")
    pr_ok_green     ("src_project_file_name value             ")
    if not os.path.isfile(dest_project_folder + "\\" + dest_project_file_name):
        pr_ko_red   ("dest_project_file_name value            ")
        raise ScriptError(error_msg + "Destination project file (" + dest_project_folder + "\\" + dest_project_file_name + ") not found. Please check the dest_project_file_name value")
    pr_ok_green     ("dest_project_file_name value            ")
        
    # check if the fspackagetool.exe file is reachable
    if not os.path.isfile(fspackagetool_folder + "\\" + MSFS_BUILD_EXE_FILE):
        pr_ko_orange("fspackagetool_folder value              ")
        build_package_enabled = False
        print(CORANGE + warning_msg + MSFS_BUILD_EXE_FILE + " bin file not found. Automatic package building disabled" + CEND + EOL)
    pr_ok_green     ("fspackagetool_folder value              ")
        
    # check if the package definitions folders exist
    if not os.path.isdir(src_package_definitions_folder):
        pr_ko_red   ("src_package_definitions_folder value    ")
        raise ScriptError(error_msg + "The folder containing the package definitions of the source project (" + src_package_definitions_folder + ") was not found. Please check the src_package_definitions_folder value")
    pr_ok_green     ("src_package_definitions_folder value    ")
    if not os.path.isdir(dest_package_definitions_folder):
        pr_ko_red   ("dest_package_definitions_folder value   ")
        raise ScriptError(error_msg + "The folder containing the package definitions of the destination project (" + dest_package_definitions_folder + ") was not found. Please check the dest_package_definitions_folder value")
    pr_ok_green     ("dest_package_definitions_folder value   ")
    
    # check if the package definitions file names are reachable
    if not os.path.isfile(src_package_definitions_folder + src_package_definitions_file_name):
        pr_ko_red   ("src_package_definitions_file_name value ")
        raise ScriptError(error_msg + "Source package definitions file (" + src_package_definitions_folder + src_package_definitions_file_name + ") not found. Please check the src_package_definitions_file_name value")
    pr_ok_green     ("src_package_definitions_file_name value ")
    if not os.path.isfile(dest_package_definitions_folder + dest_package_definitions_file_name):
        pr_ko_red   ("dest_package_definitions_file_name value")
        raise ScriptError(error_msg + "Destination package definitions file (" + dest_package_definitions_folder + dest_package_definitions_file_name + ") not found. Please check the dest_package_definitions_file_name value")
    pr_ok_green     ("dest_package_definitions_file_name value")

def check_package_sources_configuration():
    error_msg = "Configuration error found ! "

    # check if the objects folders exist
    if not os.path.isdir(src_objects_folder):
        pr_ko_red   ("src_objects_folder value                ")
        raise ScriptError(error_msg + "The folder containing the objects of the source project (" + src_objects_folder + ") was not found. Please check the src_objects_folder value")
    pr_ok_green     ("src_objects_folder value                ")
    if not os.path.isdir(dest_objects_folder):
        pr_ko_red   ("dest_objects_folder value               ")
        raise ScriptError(error_msg + "The folder containing the objects of the destination project (" + dest_objects_folder + ") was not found. Please check the dest_objects_folder value")
    pr_ok_green     ("dest_objects_folder value               ")
            
    # check if the folders containing the description files of the scene exist
    if not os.path.isdir(src_scene_folder):
        pr_ko_red   ("src_scene_folder value                  ")
        raise ScriptError(error_msg + "The folder containing the description files of the source scene (" + src_scene_folder + ") was not found. Please check the src_scene_folder value")
    pr_ok_green     ("src_scene_folder value                  ")
    if not os.path.isdir(dest_scene_folder):
        pr_ko_red   ("dest_scene_folder value                 ")
        raise ScriptError(error_msg + "The folder containing the description files of the destination scene (" + dest_scene_folder + ") was not found. Please check the dest_scene_folder value")
    pr_ok_green     ("dest_scene_folder value                 ")
    
    # check if the description file of the scene is reachable
    if not os.path.isfile(src_scene_folder + src_scene_file_name):
        pr_ko_red   ("src_scene_file_name value               ")
        raise ScriptError(error_msg + "Description file of the source scene (" + src_scene_folder + src_scene_file_name + ") not found. Please check the src_scene_file_name value")
    pr_ok_green     ("src_scene_file_name value               ")
    if not os.path.isfile(dest_scene_folder + dest_scene_file_name):
        pr_ko_red   ("dest_scene_file_name value              ")
        raise ScriptError(error_msg + "Description file of the destination scene (" + dest_scene_folder + dest_scene_file_name + ") not found. Please check the dest_scene_file_name value")
    pr_ok_green     ("dest_scene_file_name value              ")
        
    # check if the folders containing the textures of the scene exist
    if not os.path.isdir(src_textures_folder):
        pr_ko_red   ("src_textures_folder value               ")
        raise ScriptError(error_msg + "The folder containing the textures of the source scene (" + src_textures_folder + ") was not found. Please check the src_textures_folder value")
    pr_ok_green     ("src_textures_folder value               ")
    if not os.path.isdir(dest_textures_folder):
        pr_ko_red   ("dest_textures_folder value              ")
        raise ScriptError(error_msg + "The folder containing the textures of the destination scene (" + dest_textures_folder + ") was not found. Please check the dest_textures_folder value")
    pr_ok_green     ("dest_textures_folder value              ")
    
    print(EOL + "-------------------------------------------------------------------------------")

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
    updated_file = open(file, "rt")
    data = updated_file.read()
    data = data.replace(text,replacement)
    updated_file.close()
    updated_file = open(file, "wt")
    updated_file.write(data)
    updated_file.close()

##########################################################################
# function to pretty print the XML code
##########################################################################
def prettyPrint(element, level=0):
    '''
    Function taken from elementTree site:
    http://effbot.org/zone/element-lib.htm#prettyprint

    '''
    indent = '\n' + level * '  '
    if len(element):
        if not element.text or not element.text.strip():
            element.text = indent + '  '

        if not element.tail or not element.tail.strip():
            element.tail = indent

        for element in element:
            prettyPrint(element, level + 1)

        if not element.tail or not element.tail.strip():
            element.tail = indent

    else:
        if level and (not element.tail or not element.tail.strip()):
            element.tail = indent

    return element

##########################################################################
# Backup the destination packageSources files before the merging process
##########################################################################     
def backup_files():
    os.chdir(dest_objects_folder)
    for file in glob.glob("*.*"):
        file_name = os.path.basename(file)
        if not os.path.isfile(dest_backup_modelLib_folder + "\\" + file_name):
            print("backup file ", file_name)
            shutil.copyfile(file, dest_backup_modelLib_folder + "\\" + file_name)
            
    os.chdir(dest_textures_folder)
    for file in glob.glob("*.*"):
        file_name = os.path.basename(file)
        if not os.path.isfile(dest_backup_modelLib_folder + "\\texture\\" + file_name):
            print("backup texture file ", file_name)
            shutil.copyfile(file, dest_backup_modelLib_folder + "\\texture\\" + file_name)
            
    os.chdir(dest_scene_folder)
    for file in glob.glob("*.*"):
        file_name = os.path.basename(file)
        if not os.path.isfile(dest_backup_scene_folder + "\\" + file_name):
            shutil.copyfile(file, dest_backup_scene_folder + "\\" + file_name)

##########################################################################################
# Copy files from the destination packageSources to the destination packageSources folder
##########################################################################################

def copy_file(file, dest_folder):    
    file_name = os.path.basename(file)
    
    if not os.path.isfile(dest_folder + "\\" + file_name):
        print("copy file ", file_name)
    else:
        print("overwrite file ", file_name)
        
    shutil.copyfile(file, dest_folder + file_name)

def copy_files():
    os.chdir(src_objects_folder)
    for file in glob.glob("*.*"):
        copy_file(file, dest_objects_folder)
    
    os.chdir(src_textures_folder)
    for file in glob.glob("*.*"):
        copy_file(file, dest_textures_folder)
        
    os.chdir(src_scene_folder)
    for file in glob.glob("*.*"):
        file_name = os.path.basename(file)
        if file_name != src_scene_file_name and file_name != dest_scene_file_name:
            copy_file(file, dest_scene_folder)
        
        
##########################################################################################
# Update the destination scene xml file to display the source tiles
##########################################################################################

def update_dest_scene_file():
    os.chdir(src_objects_folder)
    for file in glob.glob("*.xml"):
        file_name = os.path.basename(file)
        print(src_objects_folder + file_name)
        parser = ET.XMLParser(encoding='utf-8')
        tree = ET.parse(file, parser=parser)
        root = tree.getroot()
        new_guid  = root.get("guid")
        add_guid = False
        
        dest_objects_tree = ET.parse(dest_scene_folder + dest_scene_file_name)
        dest_objects_root = dest_objects_tree.getroot()
            
        src_objects_tree = ET.parse(src_scene_folder + src_scene_file_name)
        src_objects_root = src_objects_tree.getroot()
        
        if not os.path.isfile(dest_objects_folder + file_name):
            add_guid = True

        if not add_guid: 
            guid_found = False
            print(dest_objects_folder + file_name)
            dest_tree = ET.parse(dest_objects_folder + file_name)
            dest_root = dest_tree.getroot()
            guid  = dest_root.get("guid")
                
            for scenery_object in dest_objects_root.findall("./SceneryObject/LibraryObject[@name='" + guid.upper() + "']"):
                print("old guid: ", scenery_object.get("name"))
                print("new guid: ", str(new_guid).upper())
                scenery_object.set("name", str(new_guid).upper())
                guid_found = True
                
            for scenery_object in dest_objects_root.findall("./Group/SceneryObject/LibraryObject[@name='" + guid.upper() + "']"):
                print("old guid: ", scenery_object.get("name"))
                print("new guid: ", str(new_guid).upper())
                scenery_object.set("name", str(new_guid).upper())
                guid_found = True
            
            if not guid_found:
                add_guid = True
        
        if add_guid:         
            for scenery_object in src_objects_root.findall("./SceneryObject/LibraryObject[@name='" + new_guid.upper() + "']/.."):
                print("new guid: ", str(new_guid).upper())    
                src_scenery_object = scenery_object
                print("add new SceneryObject", src_scenery_object.tag, src_scenery_object.attrib)
                dest_objects_root.append(src_scenery_object)
                
            for scenery_object in src_objects_root.findall("./Group/SceneryObject/LibraryObject[@name='" + new_guid.upper() + "']/.."):
                print("new guid: ", str(new_guid).upper()) 
                src_scenery_object = scenery_object            
                print("add new SceneryObject", src_scenery_object.tag, src_scenery_object.attrib)
                dest_objects_root.append(src_scenery_object)
                    
                    
        dest_objects_tree.write(dest_scene_folder + dest_scene_file_name) 
        prettyPrint(element=dest_objects_root)
        line_prepender(dest_scene_folder + dest_scene_file_name, '<?xml version="1.0"?>')
            
######################################################
# build merged scenery into new MSFS package
######################################################  
def build_package():
    error_msg = "MSFS SDK tools not installed"
    
    try: 
        os.chdir(fspackagetool_folder)
        print("fspackagetool.exe \"" + dest_project_folder + "\\" + dest_project_file_name + "\" -rebuild -outputdir \"" + dest_project_folder)
        subprocess.run("fspackagetool.exe \"" + dest_project_folder + "\\" + dest_project_file_name + "\" -rebuild -outputdir \"" + dest_project_folder, shell=True, check=True)
    except:
        raise ScriptError(error_msg)

#######################****************###########################

##################################################################
#                        Main process
################################################################## 

try:
    check_configuration()
    
    if not os.path.isdir(src_project_folder + "\\PackageSources\\modelLib") and not os.path.isdir(src_project_folder + "\\PackageSources\\" + src_project_name.lower() + "-modelLib"):
        print("The modelLib folder was not found for the projet", src_project_name, ". Abort optimization script. Please rename your modelLib folder like this:", src_project_folder + "\\PackageSources\\" + src_project_name.lower() + "-modelLib")
    else:      
        if not os.path.isdir(dest_project_folder + "\\PackageSources\\modelLib") and not os.path.isdir(dest_project_folder + "\\PackageSources\\" + dest_project_name.lower() + "-modelLib"):
            print("The modelLib folder was not found for the projet", dest_project_name, ". Abort optimization script. Please rename your modelLib folder like this:", dest_project_folder + "\\PackageSources\\" + dest_project_name.lower() + "-modelLib")
        else:
            # change modelib folder to fix CTD issues (see https://flightsim.to/blog/creators-guide-fix-ctd-issues-on-your-scenery/)
            os.chdir(src_project_folder)
            if os.path.isdir(src_objects_folder):
                os.rename(src_objects_folder, src_project_folder + "\\PackageSources\\" + src_project_name.lower() + "-modelLib")
                
            os.chdir(dest_project_folder)
            if os.path.isdir(dest_objects_folder):
                os.rename(dest_objects_folder, dest_project_folder + "\\PackageSources\\" + dest_project_name.lower() + "-modelLib")

            src_objects_folder = src_project_folder + "\\PackageSources\\" + src_project_name.lower() + "-modelLib\\"
            dest_objects_folder = dest_project_folder + "\\PackageSources\\" + dest_project_name.lower() + "-modelLib\\"
            # textures folder
            src_textures_folder = src_objects_folder + "texture\\"
            dest_textures_folder = dest_objects_folder + "texture\\"            
            
            check_package_sources_configuration()
            
            # fix package definitions
            replace_in_file(src_package_definitions_folder + src_package_definitions_file_name, "PackageSources\\modelLib\\", "PackageSources\\" + src_project_name.lower() + "-modelLib\\")
            replace_in_file(dest_package_definitions_folder + dest_package_definitions_file_name, "PackageSources\\modelLib\\", "PackageSources\\" + dest_project_name.lower() + "-modelLib\\")

            # create the backup folders
            if not os.path.isdir(dest_project_folder + "\\backup"):
                os.mkdir(dest_project_folder + "\\backup")
            if not os.path.isdir(dest_backup_folder):
                os.mkdir(dest_backup_folder)
            if not os.path.isdir(dest_backup_scene_folder):
                os.mkdir(dest_backup_scene_folder)    
            if not os.path.isdir(dest_backup_modelLib_folder):
                os.mkdir(dest_backup_modelLib_folder)
            if not os.path.isdir(dest_backup_modelLib_folder + "\\texture"):
                os.mkdir(dest_backup_modelLib_folder + "\\texture")  
                
            print("-------------------------------------------------------------------------------")
            print("--------------------------------- BACKUP FILES --------------------------------")
            print("-------------------------------------------------------------------------------")

            backup_files()    

            print("-------------------------------------------------------------------------------")
            print("------------------------ UPDATE DESTINATION SCENE FILE ------------------------")
            print("-------------------------------------------------------------------------------")

            update_dest_scene_file()

            print("-------------------------------------------------------------------------------")
            print("---------------------------------- COPY FILES ---------------------------------")
            print("-------------------------------------------------------------------------------")

            copy_files()
        
            if build_package_enabled:
                if os.path.isdir(msfs_temp_folder):
                    print("Remove MSFS temp folder for future build...")
                    shutil.rmtree(msfs_temp_folder)  
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