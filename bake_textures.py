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
NODE_JS_SCRIPT = "retrievepos.js"
MSFS_BUILD_EXE_FILE = "fspackagetool.exe"
JPG_FORMAT = "jpg"
PNG_FORMAT = "png"
JPG_EXTENSION = "." + JPG_FORMAT
PNG_EXTENSION = "." + PNG_FORMAT
JPG_PATTERN = "*." + JPG_FORMAT
PNG_PATTERN = "*." + PNG_FORMAT
JPG_COMPRESSION_RATIO = 0.75
BASE_COLOR_INDEX = 0

# reduce number of texture files (Lily Texture Packer addon is necessary https://gumroad.com/l/DFExj)
bake_textures_enabled = True

# folder where the scenery projects are placed
projects_folder = "E:\\MSFSProjects"

# folder of the scenery project you want to optimize
project_name = "My_project"

# folder that contains the node js script that retrieves the Google Earth coords
node_js_folder = "C:\\MSFS SDK"

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
build_package_enabled = False

# output format of the texture files (jpg or png)
output_texture_format = PNG_FORMAT
output_texture_format_pattern = "*." + output_texture_format

#######################****************###########################

import sys, bpy, glob, os, shutil, json, uuid, mathutils, math, subprocess
from math import radians, cos, sin, asin, sqrt
from xml.dom.minidom import *
from mathutils import Vector 
from xml.dom.minidom import *
from os.path import dirname, join, normpath
from bpy.app import binary_path_python
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
# MSFS temp folder
msfs_temp_folder = project_folder + "\\_PackageInt"

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
        
    # check if the folder containing the textures of the scene exists
    if not os.path.isdir(textures_folder):
        pr_ko_red   ("textures_folder value              ")
        raise ScriptError(error_msg + "The folder containing the textures of the scene (" + textures_folder + ") was not found. Please check the textures_folder value")
    pr_ok_green     ("textures_folder value              ")
    
    print(EOL + "-------------------------------------------------------------------------------")
    
######################################################
# Memory management code
######################################################
def removeObjectFromMemory(passedName):
    print("removeObjectFromMemory:[%s]." % passedName)
    # Extra test because this can crash Blender if not done correctly.
    result = False
    ob = bpy.data.objects.get(passedName)
    if ob != None:
        if ob.users > 0:
            try:
                ob.user_clear()
                can_continue = True
            except:
                can_continue = False
            
        if ob.users == 0:
            if can_continue == True:
                try:
                    bpy.data.objects.remove(ob)
                    result = True
                    print("removeObjectFromMemory: OB [" + passedName + "] removed from memory.")
                except:
                    result = False
                    print("removeObjectFromMemory: FAILED to remove OB [" + passedName + "] from memory.")
            else:
                # Unable to clear users, something is holding a reference to it.
                # Can't risk removing. Favor leaving it in memory instead of risking a crash.
                print("removeObjectFromMemory: Unable to clear users for OBJECT, something is holding a reference to it.")
                result = False
        else:
            print ("removeObjectFromMemory: Unable to remove OBJECT because it still has [" + str(ob.users) + "] users.") 
    else:
        # We could not fetch it, it does not exist in memory, essentially removed.
        print("We could not fetch OB [%s], it does not exist in memory, essentially removed." % passedName)
        result = True
    return result 
    
def removeMeshFromMemory(passedName):
    print("removeMeshFromMemory:[%s]." % passedName)
    # Extra test because this can crash Blender if not done correctly.
    result = False
    mesh = bpy.data.meshes.get(passedName)
    if mesh != None:
        if mesh.users == 0:
            try:
                mesh.user_clear()
                can_continue = True
            except:
                can_continue = False
            
            if can_continue == True:
                try:
                    bpy.data.meshes.remove(mesh)
                    result = True
                    print("removeMeshFromMemory: MESH [" + passedName + "] removed from memory.")
                except:
                    result = False
                    print("removeMeshFromMemory: FAILED to remove [" + passedName + "] from memory.")
            else:
                # Unable to clear users, something is holding a reference to it.
                # Can't risk removing. Favor leaving it in memory instead of risking a crash.
                print("removeMeshFromMemory: Unable to clear users for MESH, something is holding a reference to it.")
                result = False
        else:
            print ("removeMeshFromMemory: Unable to remove MESH because it still has [" + str(mesh.users) + "] users.")
    else:
        # We could not fetch it, it does not exist in memory, essentially removed.
        print("We could not fetch MESH [%s], it does not exist in memory, essentially removed." % passedName)
        result = True
    return result
    
def copy_objects(from_col, to_col, linked):
    for o in from_col.objects:
        dupe = o.copy()
        if not linked and o.data:
            dupe.data = dupe.data.copy()
        to_col.objects.link(dupe)

def clean_scene(): 
    context = bpy.context
    scene = context.scene       
    bpy.ops.object.select_all(action="SELECT")
        
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)

    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

    for block in bpy.data.textures:
        if block.users == 0:
            bpy.data.textures.remove(block)

    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)   
    
    # Unlink and remove objects first.
    # for ob in bpy.data.objects:
    #     r = removeObjectFromMemory(ob.name)
    #     if r == False:
    #         print ("Unable to remove [%s]." % ob.name) 
            
    bpy.ops.object.delete()
            
    # Now cycles through the dangling datablocks and remove them.
    for me in bpy.data.meshes:
        r = removeMeshFromMemory(me.name)
        if r == False:
            print ("Unable to remove [%s]." % me.name)

######################################################
# Material management methods
######################################################            
def get_material_output(material):
    for node in material.node_tree.nodes:
        if node.type == "OUTPUT_MATERIAL":
            return node

######################################################
# Image management methods
######################################################  
def list_image_nodes(node, weight=0):
    if node.type == "TEX_IMAGE":
        return [(node, weight)]
    image_nodes = []
    for i, in_socket in enumerate(node.inputs):
        w = weight
        if node.type == "BSDF_PRINCIPLED" and i == BASE_COLOR_INDEX:
            w += 100
        for l in in_socket.links:
            image_nodes += list_image_nodes(l.from_node, weight=w - 1)
    return image_nodes

def get_image_node(obj):
    material = obj.material_slots[0].material
    material_output = get_material_output(material)
    image_nodes = list_image_nodes(material_output)
    image_nodes.sort(key=lambda x: -x[1])
    
    if len(image_nodes) <= 0:
        nodes = material.node_tree.nodes
        node_texture = nodes.new(type='ShaderNodeTexImage')
        node_texture.image = bpy.data.images.new(name = 'blank', width=256, height=256, color=(0.0, 0.0, 0.0, 1.0), alpha=True)
        node_texture.location = 0,0  
        links = material.node_tree.links
        link = links.new(node_texture.outputs[0], nodes.get("Principled BSDF").inputs[0])
        print("texture added to ", obj)
        
    return image_nodes[0][0] if len(image_nodes) > 0 else None

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
    
def fix_texture_files_links(gltf_file, current_format, new_format):
    replace_in_file(gltf_file, "." + current_format, "." + new_format)
    replace_in_file(gltf_file, '''"mimeType" : "image/''' + current_format + '''"''', '''"mimeType" : "image/''' + new_format + '''"''')
    
def add_asobo_extensions(gltf_file):
    replace_in_file(gltf_file, '''        "version" : "2.0"
    },''', 
                        '''        "version" : "2.0"
    },
    "extensionsUsed" : [
        "ASOBO_normal_map_convention",
        "ASOBO_tags",
        "ASOBO_material_day_night_switch"
    ],''')
    
def add_asobo_traffic_and_collisions(gltf_file):
    replace_in_file(gltf_file, '''            "emissiveFactor" : [''', 
                        '''            "doubleSided" : false,
            "extensions" : {
                "ASOBO_tags" : {
                    "tags" : [
                        "Road"
                    ],
                    "Collision" : true
                },
                "ASOBO_material_day_night_switch" : {
                    "enabled" : true
                }
            },
            "emissiveFactor" : [''')

def fix_texture_links():
    os.chdir(objects_folder)
    
    for gltf_file in glob.glob("*.gltf"):            
        # replace texture files format refs
        if output_texture_format == PNG_FORMAT:
            fix_texture_files_links(gltf_file, JPG_FORMAT, PNG_FORMAT)
        else:
            fix_texture_files_links(gltf_file, PNG_FORMAT, JPG_FORMAT)
        print("-------------------------------------------------------------------------------")
        print(gltf_file + " treated")
            
def fix_doublesided():
    print("fix wrong doublesided attributes in gltf files")
    os.chdir(objects_folder)
    
    for gltf_file in glob.glob("*.gltf"):
        replace_in_file(gltf_file, '''{
            "doubleSided" : true,
            "doubleSided" : false,
            "extensions" : {''', 
                '''{
            "doubleSided" : false,
            "extensions" : {''')
        replace_in_file(gltf_file, '''{
            "doubleSided" : false,
            "doubleSided" : false,
            "extensions" : {''', 
                '''{
            "doubleSided" : false,
            "extensions" : {''')
        
        print("-------------------------------------------------------------------------------")
        print(gltf_file + " treated")
    
def fix_texture_path(gltf_file):
    replace_in_file(gltf_file, '''texture/''', '''''')

def add_optimisation_tag(gltf_file):
    replace_in_file(gltf_file, '''"generator" : "''', '''"generator" : "Scenery optimized ''')

def fix_xml_group_indent(xml_file):    
    replace_in_file(xml_file,
    '''        </Group>''', 
    '''    </Group>''')

######################################################
# Checking methods
######################################################           
def check_optimisation_tag(gltf_file):
    if not os.path.isfile(gltf_file):
        return False
    checked_gltf_file = open(gltf_file, "rt")
    data = checked_gltf_file.read()
    result = ('''"generator" : "Scenery optimized ''' in data)
    # previous fps optimisation script compatibility check
    if not result:
        result = ('''"generator" : "FPS optimized ''' in data)
    checked_gltf_file.close()
    return result

def check_baked_textures_optimisation_tag(gltf_file):
    if not os.path.isfile(gltf_file):
        return False
    checked_gltf_file = open(gltf_file, "rt")
    data = checked_gltf_file.read()
    result = ('''"generator" : "Optimized ''' in data)
    checked_gltf_file.close()
    return result

def check_backed_texture_files(dir, file_name):
    os.chdir(textures_folder)
    
    for texture_file in glob.glob(dir + "\\" + file_name + "_" + output_texture_format_pattern):
        if os.path.isfile(texture_file):
            os.chdir(objects_folder)
            return True 
             
    os.chdir(objects_folder)
    return False

def jpg_textures_exist():
    os.chdir(textures_folder)
    for file in glob.glob(JPG_PATTERN):
        return True
    
    return False

def png_textures_exist():
    os.chdir(textures_folder)
    for file in glob.glob(PNG_PATTERN):
        return True
    
    return False
        
######################################################
# File manipulation methods
###################################################### 
def line_prepender(filename, line):
    with open(filename, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip("\r\n") + "\n" + content)        

######################################################
# Fix meshes placement method
###################################################### 
def center_origin(obj):
    #Get active object    
    # act_obj = bpy.context.active_object
    act_obj = obj
        
    #Get cursor
    cursor = bpy.context.scene.cursor

    #Get original cursor location
    original_cursor_location = (cursor.location[0], cursor.location[1], cursor.location[2])       

    # Make sure origin is set to geometry for cursor z move 
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS") 
    
    print("act_obj.location: ", act_obj.location)

    #Set cursor location to object location
    cursor.location = act_obj.location

    cursor.location[2] = original_cursor_location[2] 

    # Get cursor x move
    half_act_obj_x_dim = act_obj.dimensions[0] / 2
    cursor_x_move = cursor.location[0] + half_act_obj_x_dim
    cursor.location[0] = cursor_x_move

    # Get cursor y move  
    half_act_obj_y_dim = act_obj.dimensions[1] / 2
    cursor_y_move = cursor.location[1] + half_act_obj_y_dim
    cursor.location[1] = cursor_y_move

    #Set origin to cursor
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR", center="MEDIAN")
    
    #Reset cursor back to original location
    cursor.location = original_cursor_location

    #Assuming you're wanting object center to grid
    bpy.ops.object.location_clear(clear_delta=False)
    
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
            print("first tile old lat: ", lat)
            print("first tile old lon: ", lon)
            print("first tile old alt: ", alt)
            return [lat, lon, alt]
                
        for scenery_object in root.findall("./Group/SceneryObject"):
            print("guid found: ", guid)
            lat = scenery_object.get("lat")
            lon = scenery_object.get("lon")
            alt = scenery_object.get("alt")
            print("first tile old lat: ", lat)
            print("first tile old lon: ", lon)
            print("first tile old alt: ", alt)
            return [lat, lon, alt]
        
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
    processes = [subprocess.Popen(["node", node_js_folder + "\\" + NODE_JS_SCRIPT, obj['id'], positions_folder, obj['lat'], obj['lon']], stdout=output_fd,
                       close_fds=ON_POSIX) # close input_fd in children
                 for obj in data]
    os.close(output_fd) # close unused end of the pipe

    # read output line by line as soon as it is available
    with io.open(input_fd, 'r', buffering=1) as file:
        for line in file:
            print(line, end='')

    for p in processes:
        p.wait()
    
#######################****************###########################

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
# Python lib installation
######################################################    
def install_python_lib(lib):
    # path to blender python.exe
    python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
    # path to other python folders
    os_python_path = os.path.expandvars(R"%USERPROFILE%\AppData\Roaming\Python")
    python_path = bpy.app.binary_path_python
    # path to blender python lib folders
    python_lib_path = normpath(join(dirname(bpy.app.binary_path_python), '..', '..', 'python\\lib'))
    error_msg = "pip and " + lib + " installation failed in blender lib folder. Please consider running this script as an administrator"

    # print(python_lib_path)
    # print(os_python_path)     
    
    if os.path.isdir(python_lib_path + "\\pip") and os.path.isdir(python_lib_path + "\\PIL") and glob.glob(python_lib_path + "\\Pillow*"):
        print("pip and " + lib + " correctly installed in blender lib folder")
        return
    
    try: 
        # install or upgrade pip
        subprocess.run([python_exe, "-m", "ensurepip"], shell=True, check=True)
        subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", "pip", "--target", python_lib_path], shell=True, check=True)
         
        # install required packages
        subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", lib, "--target", python_lib_path], shell=True, check=True)
    except:
        raise ScriptError(error_msg)   
    
    if os.path.isdir(python_lib_path + "\\pip") and os.path.isdir(python_lib_path + "\\PIL") and glob.glob(python_lib_path + "\\Pillow*"):
        print("pip and " + lib + " correctly installed in blender lib folder")

#############################################################################################
# Convert PNG texture files to JPG, then remove them, and compress existing JPG texture files
#############################################################################################
def compress_jpg_texture_files():
    from PIL import Image
    os.chdir(textures_folder)  
    
    jpg_compression_ratio = int(JPG_COMPRESSION_RATIO*100)
    
    # compress existing jpg texture files
    for jpg_file in glob.glob(JPG_PATTERN): 
        file_name = os.path.splitext(jpg_file)[0]
        compress_jpg_texture_file(file_name + JPG_EXTENSION)
    
    # convert png texture files to jpg
    for png_file in glob.glob(PNG_PATTERN): 
        file_name = os.path.splitext(png_file)[0]
        print("Convert", textures_folder + file_name + PNG_EXTENSION, "to", textures_folder + "\\" + file_name + JPG_EXTENSION, "with", str(JPG_COMPRESSION_RATIO), "compression_ratio")
        try:
            png_image = Image.open(png_file)            
            if png_image.mode in ("RGBA", "P"):
                png_image = png_image.convert("RGB")
            png_image.save(file_name + JPG_EXTENSION, optimize=True, quality=jpg_compression_ratio)
            print("File converted. Remove", textures_folder + file_name + PNG_EXTENSION) 
            os.remove(png_file)
        except:
            print("Conversion failed")
            return False
    
    return True

def compress_jpg_texture_file(jpg_file):
    from PIL import Image
    os.chdir(textures_folder)
    
    jpg_compression_ratio = int(JPG_COMPRESSION_RATIO*100)
    file_name = os.path.splitext(jpg_file)[0]
    print("Compress", textures_folder + file_name + JPG_EXTENSION, "with", str(JPG_COMPRESSION_RATIO), "compression_ratio")
    try:
        jpg_image = Image.open(jpg_file)
        jpg_image.save(file_name + JPG_EXTENSION, optimize=True, quality=jpg_compression_ratio)
        print("File compressed") 
    except:
        print("Compression failed")
        return False
    
    return True

######################################################
# Convert JPG texture files to PNG, then remove them
######################################################
def convert_jpg_texture_files_to_png():
    from PIL import Image
    os.chdir(textures_folder)
    for jpg_file in glob.glob(JPG_PATTERN): 
        file_name = os.path.splitext(jpg_file)[0]
        print("Convert", textures_folder + file_name + JPG_EXTENSION, "to", textures_folder + "\\" + file_name + PNG_EXTENSION)
        try:
            jpg_image = Image.open(jpg_file)
            jpg_image.save(file_name + PNG_EXTENSION)
            print("File converted. Remove", textures_folder + file_name + JPG_EXTENSION) 
            os.remove(jpg_file)
        except:
            print("Conversion failed")
            return False  
    
    return True
        
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
        
##################################################################
# Retrieve objects position from Google Earth API
################################################################## 
def retrieve_objects_position(objects_tree):
    os.chdir(objects_folder)
    objects_root = objects_tree.getroot()
    
    data = retrieve_pos_file_to_treat(objects_root)
    # retrieve_pos(data)

############################################################################
# Group linked objects (objects with similar coords) into dedicated folders
############################################################################ 
def group_linked_objects(objects_tree):
    os.chdir(objects_folder)
    objects_root = objects_tree.getroot()

    for file in glob.glob("*.gltf"):
        print("-------------------------------------------------------------------------------")

        file_name = os.path.splitext(file)[0]  
        
        gltf_file = file_name + ".gltf"
        bin_file = file_name + ".bin"
        
        if not os.path.isfile(gltf_file):
            continue
        
        if not os.path.isfile(bin_file):
            continue
        
        if check_optimisation_tag(gltf_file):
            print("Skip already optimized file: ", gltf_file)
            os.chdir(objects_folder)
            continue
        
        object_name = file_name.split("_")[0]  
        lod = file_name.split("_")[1]  
        
        if not os.path.isdir(file_name):
            print("create " + file_name + " folder")
            os.mkdir(file_name)
        
        print("move", gltf_file, "into", file_name, "folder")    
        shutil.move(gltf_file, file_name + "\\" + gltf_file)
        print("move", bin_file, "into", file_name, "folder")  
        shutil.move(bin_file, file_name + "\\" + bin_file)
        
        
        os.chdir(textures_folder)
        for texture_file in glob.glob(file_name + output_texture_format_pattern):
            if os.path.isfile(texture_file):
                print("move", texture_file, "into", file_name, "folder")   
                shutil.move(texture_file, "../" + file_name + "\\" + texture_file)   
                 
        os.chdir(objects_folder)

        pos_file_name = object_name + ".pos"
        print("pos file name: ", pos_file_name)
        if os.path.isfile(positions_folder + "\\" + pos_file_name):
            with open(positions_folder + "\\" + pos_file_name) as pos_file:
                pos = json.load(pos_file)
                lat = pos[0]
                lon = pos[1]
                
            for second_file in glob.glob("*.gltf"):        
                second_file_name = os.path.splitext(second_file)[0]
                second_gltf_file = second_file_name + ".gltf"
                second_bin_file = second_file_name + ".bin"
                second_texture_file = second_file_name + output_texture_format_pattern
                
                second_object_name = second_file_name.split("_")[0]
                second_lod = second_file_name.split("_")[1]  
                second_pos_file_name = second_object_name + ".pos"
                second_xml_file_name = second_object_name + ".xml"
                
                if second_pos_file_name == pos_file_name:
                    continue
                
                if second_lod != lod:
                    continue
        
                if not os.path.isfile(second_gltf_file):
                    continue
                
                if not os.path.isfile(second_bin_file):
                    continue
                
                # link objects that are inside the tile
                if os.path.isfile(positions_folder + "\\" + second_pos_file_name):
                    with open(positions_folder + "\\" + second_pos_file_name) as second_pos_file:
                        second_pos = json.load(second_pos_file)
                        if (lat - second_pos[0]) > -0.001 and (lat - second_pos[0]) < 0.001 and (lon - second_pos[1]) > -0.001 and (lon - second_pos[1]) < 0.001:
                            print("move", second_gltf_file, "into", file_name, "folder")    
                            shutil.move(second_gltf_file, file_name + "\\" + second_gltf_file)
                            print("move", second_bin_file, "into", file_name, "folder")
                            shutil.move(second_bin_file, file_name + "\\" + second_bin_file)
                            
                            os.chdir(textures_folder)
                            for second_texture_file in glob.glob(second_file_name + output_texture_format_pattern):
                                if os.path.isfile(second_texture_file):
                                    print("move ", second_texture_file, " into ", file_name, " folder")     
                                    shutil.move(second_texture_file, "../" + file_name + "\\" + second_texture_file) 
                                
                            os.chdir(objects_folder)
                                
                            if os.path.isfile(objects_folder + "\\" + second_xml_file_name):
                                print("move", second_xml_file_name, "into", file_name, "folder") 
                                shutil.move(second_xml_file_name, file_name + "\\" + second_xml_file_name)
                                tree = ET.parse(file_name + "\\" + second_xml_file_name)
                                root = tree.getroot()
                                guid  = root.get("guid")
                                print("remove guid: ", guid, " from ", scene_file_name)
                                print("./SceneryObject/LibraryObject/[@name='" + guid.upper() + "']/..")
                                for scenery_object in objects_root.findall("./SceneryObject/LibraryObject[@name='" + guid.upper() + "']/.."):
                                    print("guid found: ", guid)
                                    scenery_object_parent = objects_root.find("./SceneryObject/LibraryObject[@name='" + guid.upper() + "']/../..")
                                    scenery_object_parent.remove(scenery_object)
                                print("./Group/SceneryObject/LibraryObject/[@name='" + guid.upper() + "']/..")    
                                for scenery_object in objects_root.findall("./Group/SceneryObject/LibraryObject[@name='" + guid.upper() + "']/.."):
                                    print("guid found: ", guid)
                                    scenery_object_parent = objects_root.find("./Group/SceneryObject/LibraryObject[@name='" + guid.upper() + "']/../..")
                                    scenery_object_parent.remove(scenery_object)
                                
                                objects_tree.write(scene_folder + scene_file_name)    
                                line_prepender(scene_folder + scene_file_name, '<?xml version="1.0"?>')
                                fix_xml_group_indent(scene_folder + scene_file_name)
                                
#######################################################################
# Update objects position with the one retrieved from Google Earth API
#######################################################################
def update_objects_position(objects_tree):
    os.chdir(objects_folder)
    objects_root = objects_tree.getroot()
    old_pos = retrieve_first_tile_old_position()
        
    for xml_file in glob.glob("*.xml"):
        print("-------------------------------------------------------------------------------")
        print("xml file: ", os.path.basename(xml_file))
        file_name = os.path.splitext(xml_file)[0]
        pos_name = file_name + ".pos"
        tree = ET.parse(xml_file)
        root = tree.getroot()
        guid  = root.get("guid")
        already_optimized = True
        lat = 0
        lon = 0
        
        for gltf_file in glob.glob(file_name + "*.gltf"):
            if not check_optimisation_tag(gltf_file):
                already_optimized = False
                continue
        
        if already_optimized == True:
            print("object", file_name, "already optimized. Skip position update")
            continue
        
        for pos_file_name in glob.glob(positions_folder  + "\\" + file_name + "*.pos"):
            with open(pos_file_name) as pos_file:
                print("pos file ", pos_file.name)
                pos = json.load(pos_file) 
                lat = pos[0]
                lon = pos[1]
                alt = old_pos[2]
            break
        
        print("./SceneryObject/LibraryObject[@name='" + guid.upper() + "']/..")    
        for scenery_object in objects_root.findall("./SceneryObject/LibraryObject[@name='" + guid.upper() + "']/.."):
            print("new lat: ", lat)
            print("new lon: ", lon)
            scenery_object.set("lat", str(lat))
            scenery_object.set("lon", str(lon))
            
        print("./Group/SceneryObject/LibraryObject/[@name='" + guid.upper() + "']/..")    
        for scenery_object in objects_root.findall("./Group/SceneryObject/LibraryObject[@name='" + guid.upper() + "']/.."):
            print("new lat: ", lat)
            print("new lon: ", lon)
            scenery_object.set("lat", str(lat))
            scenery_object.set("lon", str(lon))
                
        objects_tree.write(scene_folder + scene_file_name)
        line_prepender(scene_folder + scene_file_name, '<?xml version="1.0"?>')

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
             

##################################################################
# Optimization methods
################################################################## 

##################################################################
# Import the gltf files located in a specific folder
################################################################## 
def import_dir_files(dir):
    for file in glob.glob("*.gltf"):
        file_name = os.path.splitext(file)[0]
    
        gltf_file = file_name + ".gltf"
        bin_file = file_name + ".bin"        
        
        if check_optimisation_tag(gltf_file):
            print("Skip file: ", gltf_file)
            os.chdir(objects_folder)
            continue
        
        try:
            print("import gltf " + file_name + ".gltf")
            bpy.ops.import_scene.gltf(filepath=file) 
        except:
            continue
            
##############################################################################
# Export and optimize the tile in a new gltf file, with bin file and textures
############################################################################## 
def export_to_optimized_gltf_files(file_name):
    print("export to ", objects_folder + file_name, "with associated textures")    
    bpy.ops.export_scene.gltf(export_format="GLTF_SEPARATE", export_extras=True, filepath=objects_folder + file_name, export_texture_dir="texture")
    
    print("add optimisation tag to ", objects_folder + file_name + ".gltf")
    add_optimisation_tag(objects_folder + file_name + ".gltf")
    print("add asobo extensions to ", objects_folder + file_name + ".gltf")
    add_asobo_extensions(objects_folder + file_name + ".gltf")
    print("add traffic and collision detection tags to ", objects_folder + file_name + ".gltf")
    add_asobo_traffic_and_collisions(objects_folder + file_name + ".gltf")    
    fix_texture_path(objects_folder + file_name + ".gltf")

##################################################################
# fix texture final size for package compilation
################################################################## 
def fix_texture_size_for_package_compatibility(packedImage):
    print('Image width: ', packedImage.size[0])
    print('Image height: ', packedImage.size[1])    
    # fix texture final size for package compilation
    newImgWidth = packedImage.size[0] + (4-packedImage.size[0]%4)
    newImgHeight = packedImage.size[1] + (4-packedImage.size[1]%4)
    print('New image width: ', newImgWidth)
    print('New image height: ', newImgHeight)    
    packedImage.scale(newImgWidth, newImgHeight)

##################################################################
# link the tile materials to the new packed texture
##################################################################     
def link_materials_to_packed_texture(objects, dir, file_name):
    img = bpy.data.images.load(dir + file_name + "." + output_texture_format)
    
    for obj in bpy.context.selected_objects:                
        material = obj.material_slots[0].material
        material.msfs_show_road_material = True
        material.msfs_show_collision_material = True
        material.msfs_show_day_night_cycle = True
        material.msfs_road_material = True
        material.msfs_collision_material = True
        material.msfs_day_night_cycle = True
            
        source_image_nodes = [ get_image_node(obj) for obj in objects ]
        source_images = [ node.image for node in source_image_nodes ]
        print("link packed texture to ", obj.name)
        # Update image in materials
        for node in source_image_nodes:
            node.image = img
            node.image.name = file_name
    
##################################################################
# Bake the tile texture files
##################################################################  
def bake_texture_files(dir, file_name):
    print("-------------------------------------------------------------------------------")
    print("------------------------ BAKE TILE TEXTURE FILES ------------------------------")
    print("-------------------------------------------------------------------------------")
    error = False
    
     # cleanup nodes with no materials
    objs = [obj for obj in bpy.context.scene.objects if not obj.material_slots]
    bpy.ops.object.delete({"selected_objects": objs})
            
    objects = bpy.context.scene.objects

    source_image_nodes = []
    for obj in bpy.context.scene.objects:
        image_node = get_image_node(obj)
        if not image_node.image is None:
            source_image_nodes.append(image_node)
        else:
            bpy.data.objects.remove(obj, do_unlink=True)
            
    for node in source_image_nodes:
        if node.image is None:
          error=True
          
    if error is True:
        os.chdir(objects_folder)
        return False      
    if error is True:
        os.chdir(objects_folder)
        return False

    for obj in objects:
        obj.select_set(True)
    
    try:
        bpy.ops.object.lily_texture_packer()
    except:
        print("Texture packer error detected !!!" + file_name)
        os.chdir(objects_folder)
        return False
    
    # create baked texture with Lily texture packer addon
    packedImage = bpy.data.images["LilyPackedImage"]
    
    # fix texture final size for package compilation
    fix_texture_size_for_package_compatibility(packedImage)

    print("Save new baked texture", file_name + "." + output_texture_format)
    packedImage.save_render(dir + file_name + "." + output_texture_format)

    # link the tile materials to the new packed texture    
    # link_materials_to_packed_texture(objects, dir, file_name)
    
    bpy.data.images.remove(packedImage)
    
    return True
    
##################################################################
# Fix the tile bounding box
################################################################## 
def fix_object_bounding_box(context, scene):
    print("-------------------------------------------------------------------------------")
    print("---------------------------- FIX TILE BOUNDING BOX ----------------------------")
    print("-------------------------------------------------------------------------------")
    
    create_collection = bpy.data.collections.new(name="CopyCollection")
    bpy.context.scene.collection.children.link(create_collection)
    assert(create_collection is not scene.collection)

    # copy objects
    copy_objects(scene.collection, create_collection, False)
    
    obs = []
    for obj in create_collection.objects:
        # whatever objects you want to join...
        if obj.type == "MESH":
            obs.append(obj)

    ctx = bpy.context.copy()
    
    if len(obs) < 1:
        return None
    
    ctx["active_object"] = obs[0]

    ctx["selected_objects"] = obs

    # In Blender 2.8x this needs to be the following instead:
    ctx["selected_editable_objects"] = obs
    
    # join copied objects
    bpy.ops.object.join(ctx)
    
    bpy.ops.object.select_all(action="SELECT")
    
    objects = scene.objects
    
    # fix objects origin: this also fixes the bounding box for the whole tile
    for obj in objects:
        center_origin(obj)
        
    bpy.ops.object.select_all(action="DESELECT")            
    
    # remove joined copied objects
    for obj in create_collection.objects:
        obj.select_set(True)            
        bpy.ops.object.delete()   
        
    bpy.ops.object.select_all(action="SELECT")     
        
    for c in scene.collection.children:
        scene.collection.children.unlink(c)
    
    # resize objects to fix spacing between tiles
    bpy.ops.transform.resize(value=(1.0045, 1.0045, 1))
    

##################################################################
# Optimize an object
################################################################## 
def optimize_object(dir):    
    os.chdir(objects_folder + dir)
    clean_scene()
    print("dir :", objects_folder + dir)
    
    # Import the gltf files located in the object folder
    import_dir_files(dir)

    file_name = dir.split("\\")[0]
    gltf_file = file_name + ".gltf"
    
    context = bpy.context
    scene = context.scene
    
    bake_textures_required = bake_textures_enabled and not check_baked_textures_optimisation_tag(gltf_file) and check_backed_texture_files(objects_folder + dir, file_name)
        
    os.chdir(objects_folder + dir)
    
    if glob.glob("*.gltf"):  
        # check if textures are already baked
        if bake_textures_required:
            # bake texture files for the tile
            bake_texture_files(objects_folder + dir, file_name)
            
        # fix the tile bounding box
        # fix_object_bounding_box(context, scene)
        
        # Export and optimize the tile in a new gltf file, with bin file and textures
        # export_to_optimized_gltf_files(file_name)
                
        if bake_textures_required and output_texture_format == JPG_FORMAT:
            compress_jpg_texture_file(file_name + "." + output_texture_format)
            
        shutil.copy(file_name + "." + output_texture_format, textures_folder + file_name + "." + output_texture_format)
            
        os.chdir(objects_folder)
        shutil.rmtree(dir)

##################################################################
# Optimize all the objects of the scenery
##################################################################        
def optimize_objects():
    os.chdir(objects_folder)

    for dir in glob.glob("*\\"):
        print("-------------------------------------------------------------------------------")
        if dir == "texture\\":
            continue
        
        optimize_object(dir)

##################################################################
# Clean orphan scenery object
##################################################################       
def clean_orphan_scenery_objects(): 
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
        guid_found = False
        
        # if no gltf file or bin file is associated with the current xml scenery object file, the xml is removed
        if not glob.glob(file_name + "_LOD*.gltf") or not glob.glob(file_name + "_LOD*.bin"):
            print("-------------------------------------------------------------------------------")
            print("xml file: ", file_path)
            # remove scenery object reference in the scene file
            print("remove guid: ", guid, " from ", scene_file_name)
            print("./SceneryObject/LibraryObject/[@name='" + guid.upper() + "']/..")
            for scenery_object in objects_root.findall("./SceneryObject/LibraryObject[@name='" + guid.upper() + "']/.."):
                guid_found = True
                print("guid found: ", guid)
                scenery_object_parent = objects_root.find("./SceneryObject/LibraryObject[@name='" + guid.upper() + "']/../..")
                scenery_object_parent.remove(scenery_object)
            print("./Group/SceneryObject/LibraryObject/[@name='" + guid.upper() + "']/..")    
            for scenery_object in objects_root.findall("./Group/SceneryObject/LibraryObject[@name='" + guid.upper() + "']/.."):
                guid_found = True
                print("guid found: ", guid)
                scenery_object_parent = objects_root.find("./Group/SceneryObject/LibraryObject[@name='" + guid.upper() + "']/../..")
                scenery_object_parent.remove(scenery_object)
           
            if guid_found:     
                objects_tree.write(scene_folder + scene_file_name)    
                line_prepender(scene_folder + scene_file_name, '<?xml version="1.0"?>')
                fix_xml_group_indent(scene_folder + scene_file_name)
            
            try:
                os.remove(file_path)
            except OSError as e:
                error_msg = "Error: " + file_path + " : " + e.strerror
                raise ScriptError(error_msg)
            
            print("orphan package file:", file_path, "removed")  
        
######################################################
# build scenery into new MSFS package
######################################################  
def build_package():
    error_msg = "MSFS SDK tools not installed"
    
    try: 
        os.chdir(fspackagetool_folder)
        print(MSFS_BUILD_EXE_FILE + " \"" + project_folder + "\\" + project_file_name + "\" -rebuild -outputdir \"" + project_folder)
        subprocess.run(MSFS_BUILD_EXE_FILE + " \"" + project_folder + "\\" + project_file_name + "\" -rebuild -outputdir \"" + project_folder, shell=True, check=True)
    except:
        raise ScriptError(error_msg)
        
#######################****************###########################

##################################################################
#                        Main process
################################################################## 

def main():        
    objects = Document()
    clean_scene()
                            
    # print("-------------------------------------------------------------------------------")
    # print("------------------------- RETRIEVE OBJECTS POSITION ---------------------------")
    # print("-------------------------------------------------------------------------------")

    # retrieve_objects_position(objects_tree)

    # print("-------------------------------------------------------------------------------")
    # print("--------------------------- UPDATE OBJECTS POSITION ---------------------------")
    # print("-------------------------------------------------------------------------------")

    # update_objects_position(objects_tree)    
    
    print("-------------------------------------------------------------------------------")
    print("----------------------- FIX TEXTURE LINKS IN GLTF FILES -----------------------")
    print("-------------------------------------------------------------------------------")
    
    fix_texture_links()

    print("-------------------------------------------------------------------------------")
    print("----------------- GROUP LINKED OBJECTS INTO DEDICATED FOLDERS -----------------")
    print("-------------------------------------------------------------------------------")

    group_linked_objects(objects_tree)

    # print("-------------------------------------------------------------------------------")
    # print("----------------------------- UPDATE OBJECTS LODS -----------------------------")
    # print("-------------------------------------------------------------------------------")

    # update_object_lods()

    print("-------------------------------------------------------------------------------")
    print("--------------------------- OPTIMIZE SCENERY OBJECTS --------------------------")
    print("-------------------------------------------------------------------------------")

    optimize_objects()

    # print("-------------------------------------------------------------------------------")
    # print("------------------------------- FIX DOUBLESIDED -------------------------------")
    # print("-------------------------------------------------------------------------------")
    
    # fix_doublesided()

    # print("-------------------------------------------------------------------------------")
    # print("------------------------ CLEAN ORPHAN SCENERY OBJECTS -------------------------")
    # print("-------------------------------------------------------------------------------")
    
    # clean_orphan_scenery_objects()

#######################****************###########################

##################################################################
#                           Script
################################################################## 

try:
    check_configuration()
    
    # change modelib folder to fix CTD issues (see https://flightsim.to/blog/creators-guide-fix-ctd-issues-on-your-scenery/)
    os.chdir(project_folder)
    if os.path.isdir(objects_folder):
        if os.path.isdir(project_folder + "\\PackageSources\\" + project_name.lower() + "-modelLib"):
            shutil.rmtree(project_folder + "\\PackageSources\\" + project_name.lower() + "-modelLib")
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

    # cleanup the out folder
    if os.path.isdir(out_folder):
        shutil.rmtree(out_folder) 
    os.mkdir(out_folder)
    os.mkdir(out_folder + "\\texture")

    # create the backup folders
    if not os.path.isdir(backup_folder):
        os.mkdir(backup_folder)    
    if not os.path.isdir(backup_scene_folder):
        os.mkdir(backup_scene_folder)    
    if not os.path.isdir(backup_modelLib_folder):
        os.mkdir(backup_modelLib_folder)
    if not os.path.isdir(backup_modelLib_folder + "\\texture"):
        os.mkdir(backup_modelLib_folder + "\\texture")
        
    # create the positions folder
    if not os.path.isdir(positions_folder):
        os.mkdir(positions_folder)
        
    clean_scene()        
    objects_tree = ET.parse(scene_folder + scene_file_name)   
    
    print("-------------------------------------------------------------------------------")
    print("--------------------------------- BACKUP FILES --------------------------------")
    print("-------------------------------------------------------------------------------")

    backup_files()
    
    # print("-------------------------------------------------------------------------------")
    # print("------------------ INSTALL NODE JS XHR2 MODULE, IF NECESSARY ------------------")
    # print("-------------------------------------------------------------------------------") 
    
    # install_xhr2()

    if not os.path.isdir(project_folder + "\\PackageSources\\modelLib") and not os.path.isdir(project_folder + "\\PackageSources\\" + project_name.lower() + "-modelLib"):
        raise ScriptError("The modelLib folder was not found for the projet " + project_name + ". Please rename your modelLib folder like this:" + project_folder + "\\PackageSources\\" + project_name.lower() + "-modelLib")
    else:
        
        if output_texture_format == PNG_FORMAT:
            if jpg_textures_exist():
                print(JPG_FORMAT + " texture files detected in", textures_folder, "! Trying to install pip, then convert them")
                        
                print("-------------------------------------------------------------------------------")
                print("----------------------------- INSTALL PILLOW ----------------------------------")
                print("-------------------------------------------------------------------------------") 
                   
                install_python_lib("Pillow")
            
                print("-------------------------------------------------------------------------------")
                print("-------------------- CONVERT JPG TEXTURE FILES TO PNG -------------------------")
                print("-------------------------------------------------------------------------------")

                if not convert_jpg_texture_files_to_png():
                    raise ScriptError(JPG_FORMAT + " texture files detected in", textures_folder, "! Please convert them to " + PNG_FORMAT + " format prior to launch the script, or remove them")
        else:
            print("-------------------------------------------------------------------------------")
            print("-------------------------------- INSTALL PIP ----------------------------------")
            print("-------------------------------------------------------------------------------") 
               
            install_python_lib("Pillow")
        
            print("-------------------------------------------------------------------------------")
            print("-- CONVERT PNG TEXTURE FILES TO JPG AND COMPRESS EXISTING JPG TEXTURE FILES ---")
            print("-------------------------------------------------------------------------------")

            if not compress_jpg_texture_files():
                raise ScriptError("Please save all texture files to " + JPG_FORMAT + " with a compression ratio of " + str(JPG_COMPRESSION_RATIO) + " format prior to launch the script, and remove existing " + PNG_FORMAT + " remaining texture files")
        
        main()
    
        if build_package_enabled:
            if os.path.isdir(msfs_temp_folder):
                print("Remove MSFS temp folder for future build...")
                shutil.rmtree(msfs_temp_folder)  
            build_package()
    
    clean_scene()
    print(EOL)    
    pr_bg_green("Script correctly applied" + CEND)
                
except ScriptError as ex:
    clean_scene()  
    error_report = "".join(ex.value)
    print(EOL + error_report)
    pr_bg_red("Script aborted" + CEND)
except RuntimeError as ex:
    clean_scene()  
    print(EOL + ex)
    pr_bg_red("Script aborted" + CEND)
finally:  
    os.chdir(cwd)