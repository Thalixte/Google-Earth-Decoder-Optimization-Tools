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
NODE_JS_SCRIPT="retrievepos.js"
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
# Update objects LODS min size attributes
################################################################## 
def update_object_lods():
    for xml_file in glob.glob("*.xml"):
        print("-------------------------------------------------------------------------------")
        print("xml file: ", os.path.basename(xml_file))
        file_name = os.path.splitext(xml_file)[0]
        pos_name = file_name + ".pos"
        tree = ET.parse(xml_file)
        root = tree.getroot()
        guid  = root.get("guid")
        
        print("guid: ", guid) 
        
        lods = root.findall("./LODS/LOD")
        nb_lods = len(lods)
        print("nb_lods :", nb_lods)
        
        for idx, lod in enumerate(lods):
            lod.set("MinSize", str(target_lods[(nb_lods-1)-idx]))
            min_size = lod.get("MinSize")
            print("min_size: ", min_size)
            
        tree.write(xml_file)
        line_prepender(xml_file, '<?xml version="1.0"?>')

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
      
    check_package_sources_configuration()
    
    os.chdir(objects_folder)
 
    if not os.path.isdir(project_folder + "\\PackageSources\\modelLib") and not os.path.isdir(project_folder + "\\PackageSources\\" + project_name.lower() + "-modelLib"):
        print("The modelLib folder was not found for the projet", project_name, ". Please rename your modelLib folder like this:", project_folder + "\\PackageSources\\" + project_name.lower() + "-modelLib")
    else:       
        print("-------------------------------------------------------------------------------")
        print("----------------------------- UPDATE OBJECTS LODS -----------------------------")
        print("-------------------------------------------------------------------------------")

        update_object_lods()
        
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