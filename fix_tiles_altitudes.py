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
EARTH_RADIUS = 6371010

# folder where the scenery projects are placed
projects_folder = "E:\\MSFSProjects"

# folder of the scenery project you want to optimize
project_name = "My_project"

# folder that contains the node js script that retrieves the Google Earth coords
node_js_folder = "C:\\MSFS SDK"

# folder that contains the fspackagetool exe that builds the MSFS packages
fspackagetool_folder = "C:\\MSFS SDK\\Tools\\bin"

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

# the fix comes with two methods:
# the default one uses the backup of the old objects.xml data (the one produced by the Google Earth Decoder tool)
# the other method tries to retrieve the altitude based on the Google Earth data
fix_with_googleEarthDecoder_data = True

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
backup_folder = project_folder + "\\backup"
# backup fps_modelLib folder
backup_modelLib_folder = backup_folder + "\\modelLib"
# backup scene folder
backup_scene_folder = backup_folder + "\\scene"
# positions folder
positions_folder = project_folder + "\\positions"

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
        
    # check if the retrievepos.js file is reachable
    if not os.path.isfile(node_js_folder + "\\" + NODE_JS_SCRIPT):
        pr_ko_red   ("node_js_folder value               ")
        raise ScriptError(error_msg + "Node js script " + NODE_JS_SCRIPT + " not found. Please check the node_js_folder value") 
    pr_ok_green     ("node_js_folder value               ")
        
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
    
    print(EOL + "-------------------------------------------------------------------------------")
        
######################################################
# XHR2 node js module installation
######################################################  
def install_xhr2():
    os.chdir(node_js_folder)
    error_msg = "xhr2 node js module installation failed"
    
    try: 
        subprocess.run("npm install xhr2", shell=True, check=True)
    except:
        raise ScriptError(error_msg)

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
              
######################################################
# Retrieve Google Earth position data methods
######################################################
def retrieve_first_tile_old_position():
    xml_file = backup_scene_folder + scene_file_name
    
    if os.path.isfile(backup_scene_folder + scene_file_name):
        tree = ET.parse(xml_file)
        root = tree.getroot()
         
        for scenery_object in root.findall("./SceneryObject"):
            lat = scenery_object.get("lat")
            lon = scenery_object.get("lon")
            alt = scenery_object.get("alt")
            return [lat, lon, alt]
                
        for scenery_object in root.findall("./Group/SceneryObject"):
            print("guid found: ", guid)
            lat = scenery_object.get("lat")
            lon = scenery_object.get("lon")
            alt = scenery_object.get("alt")
            return [lat, lon, alt]
    else:
        for pos_file_name in glob.glob(positions_folder + "\\*.pos"):
            with open(pos_file_name) as pos_file:
                pos = json.load(pos_file)            
                lat = pos[0]
                lon = pos[1]
                alt = pos[2]-EARTH_RADIUS
                return [lat, lon, alt]
            break
        
    return [0, 0, 0]

def retrieve_pos_file_to_treat(objects_root):
    data = []
    for xml_file in glob.glob("*.xml"):
        print("-------------------------------------------------------------------------------")
        print("xml file: ", os.path.basename(xml_file))
        file_name = os.path.splitext(xml_file)[0]
        pos_name = file_name + ".pos"
        print("pos_file: ", positions_folder + "\\" + file_name + ".pos")
        
        if not os.path.isfile(positions_folder + "\\" + file_name + ".pos"):
            tree = ET.parse(xml_file)
            root = tree.getroot()
            guid  = root.get("guid")
            lat = "0"
            lon = "0"
            
            for scenery_object in objects_root.findall("./SceneryObject/LibraryObject[@name='" + guid.upper() + "']/.."):
                print("guid found: ", guid)
                lat = scenery_object.get("lat")
                lon = scenery_object.get("lon")
                print("lat: ", lat)
                print("lon: ", lon)
                
            print("./Group/SceneryObject/LibraryObject/[@name='" + guid.upper() + "']/..")    
            for scenery_object in objects_root.findall("./Group/SceneryObject/LibraryObject[@name='" + guid.upper() + "']/.."):
                print("guid found: ", guid)
                lat = scenery_object.get("lat")
                lon = scenery_object.get("lon")
                print("lat: ", lat)
                print("lon: ", lon)
           
            data.append({'id': file_name, 'lat': lat, 'lon': lon}) 
            retrieve_pos(data)
            data = []
    
    return data
     
def retrieve_pos(data):        
    ON_POSIX = 'posix' in sys.builtin_module_names

    # create a pipe to get data
    input_fd, output_fd = os.pipe()

    # start several subprocesses
    processes = [subprocess.Popen(["node", node_js_folder + "\\retrievepos.js", obj['id'], positions_folder, obj['lat'], obj['lon']], stdout=output_fd,
                       close_fds=ON_POSIX) # close input_fd in children
                 for obj in data]
    os.close(output_fd) # close unused end of the pipe

    # read output line by line as soon as it is available
    with io.open(input_fd, 'r', buffering=1) as file:
        for line in file:
            print(line, end='')
            
    for p in processes:
        p.wait()

##################################################################
# Retrieve objects position from Google Earth API
################################################################## 
def retrieve_objects_position(objects_tree):
    os.chdir(objects_folder)
    objects_root = objects_tree.getroot()
    
    data = retrieve_pos_file_to_treat(objects_root)
    # retrieve_pos(data)
                                
#######################################################################
# Update objects position with the one retrieved from Google Earth API
#######################################################################
def update_objects_position(objects_tree):
    os.chdir(objects_folder)
    objects_root = objects_tree.getroot()
    old_pos = retrieve_first_tile_old_position()
    print("first tile old position: ", old_pos)
        
    for xml_file in glob.glob("*.xml"):
        print("-------------------------------------------------------------------------------")
        print("xml file: ", os.path.basename(xml_file))
        file_name = os.path.splitext(xml_file)[0]
        pos_file_name = file_name + ".pos"
        tree = ET.parse(xml_file)
        root = tree.getroot()
        guid  = root.get("guid")
        final_pos = [0, 0, 0]
        
        if fix_with_googleEarthDecoder_data :
            final_pos = old_pos
        else:
            for pos_file_name in glob.glob(positions_folder  + "\\" + pos_file_name):
                with open(pos_file_name) as pos_file:
                    print("pos file ", pos_file.name)
                    pos = json.load(pos_file)
                    final_pos = [ pos[0], pos[1], pos[2] - EARTH_RADIUS ]
                break
    
        for scenery_object in objects_root.findall("./SceneryObject/LibraryObject[@name='" + guid.upper() + "']/.."):
            print("fixed alt: ", final_pos[2])
            scenery_object.set("alt", str(final_pos[2]))
            
        for scenery_object in objects_root.findall("./Group/SceneryObject/LibraryObject[@name='" + guid.upper() + "']/.."):
            print("fixed alt: ", final_pos[2])
            scenery_object.set("alt", str(final_pos[2]))
                
        objects_tree.write(scene_folder + scene_file_name)
        line_prepender(scene_folder + scene_file_name, '<?xml version="1.0"?>')

######################################################
# build scenery into new MSFS packagel
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
    # textures folder
    textures_folder = objects_folder + "texture\\"   
     
    check_package_sources_configuration()
    
    # Output folder
    out_folder = textures_folder + "baked"
    # fix package definitions
    replace_in_file(package_definitions_folder + package_definitions_file_name, "PackageSources\\modelLib\\", "PackageSources\\" + project_name.lower() + "-modelLib\\")

    os.chdir(objects_folder)

    # create the positions folder
    if not os.path.isdir(positions_folder):
        os.mkdir(positions_folder)
        
    objects_tree = ET.parse(scene_folder + scene_file_name)
    
    print("-------------------------------------------------------------------------------")
    print("------------------ INSTALL NODE JS XHR2 MODULE, IF NECESSARY ------------------")
    print("-------------------------------------------------------------------------------")
      
    install_xhr2()
    
    if not os.path.isdir(project_folder + "\\PackageSources\\modelLib") and not os.path.isdir(project_folder + "\\PackageSources\\" + project_name.lower() + "-modelLib"):
        raise ScriptError("The modelLib folder was not found for the projet " + project_name + ". Please rename your modelLib folder like this:" + project_folder + "\\PackageSources\\" + project_name.lower() + "-modelLib")
    else:
        print("-------------------------------------------------------------------------------")
        print("------------------------- RETRIEVE OBJECTS POSITION ---------------------------")
        print("-------------------------------------------------------------------------------")

        retrieve_objects_position(objects_tree)

        print("-------------------------------------------------------------------------------")
        print("----------------------------- FIX TILES ALTITUDES -----------------------------")
        print("-------------------------------------------------------------------------------")

        update_objects_position(objects_tree)
        
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