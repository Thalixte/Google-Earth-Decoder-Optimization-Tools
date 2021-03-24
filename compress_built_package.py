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
COMPRESSONATOR_EXE_FILE = "compressonatorcli.exe"
PACKAGES_TEXTURES_SUBFOLDERS = "\\scenery\\global\\scenery\\TEXTURE"
BMP_FORMAT = "BMP"
DDS_FORMAT = "DDS"
BMP_EXTENSION = "." + BMP_FORMAT
DDS_EXTENSION = "." + DDS_FORMAT
BMP_PATTERN = "*." + BMP_FORMAT
DDS_PATTERN = "*." + DDS_FORMAT
DDS_CONVERSION_FORMAT = "DXT1"
BASE_COLOR_INDEX = 0
NB_PARALLEL_TASKS = 20

# reduce number of texture files (Lily Texture Packer addon is necessary https://gumroad.com/l/DFExj)
bake_textures_enabled = True

# folder where the scenery projects are placed
projects_folder = "E:\\MSFSProjects"

# folder of the scenery project you want to optimize
project_name = "My_project"

# folder that contains the compressonator exe that converts dds files
compressonatortool_folder = "compressonator_folder"

# author name
author_name = "author_name"

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
        
# built packages folder
built_packages_folder = project_folder + "\\Packages\\"
# built packages texture folder
built_packages_textures_folder = built_packages_folder + project_name.lower() + PACKAGES_TEXTURES_SUBFOLDERS
# backup folder
backup_folder = project_folder + "\\backup"
# backup packages texture folder
backup_packages_textures_folder = backup_folder + "\\packages_textures"

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
    
    # check if the projects folder exists
    if not os.path.isdir(projects_folder):
        pr_ko_red   ("projects_folder value               ")
        raise ScriptError(error_msg + "The folder containing your projects (" + projects_folder + ") was not found. Please check the projects_folder value")
    pr_ok_green     ("projects_folder value               ")
        
    # check the projects name
    if not os.path.isdir(project_folder):
        pr_ko_red   ("project_name value                  ")
        raise ScriptError(error_msg + "Project folder " + project_folder + " not found. Please check the project_name value")
    pr_ok_green     ("project_name value                  ")    
             
    # check if the built packages folder exists
    if not os.path.isdir(built_packages_folder):
        pr_ko_red   ("built_packages folder value         ")
        raise ScriptError(error_msg + "The folder containing the built packages of the project (" + built_packages_folder + ") was not found. Please check the built_packages_folder value")
    pr_ok_green     ("built_packages folder value         ")
        
    # check if the compressonatorcli.exe file is reachable
    if not os.path.isfile(compressonatortool_folder + "\\" + COMPRESSONATOR_EXE_FILE):
        pr_ko_red("compressonatortool_folder value     ")
        build_package_enabled = False
        raise ScriptError(error_msg + COMPRESSONATOR_EXE_FILE + " bin file not found. DDS conversion disabled" + CEND + EOL)
    pr_ok_green     ("compressonatortool_folder value     ")    

######################################################
# check packages folder configuration methods
######################################################

def check_packages_folder_configuration():
    error_msg = "Configuration error found ! "
    
    # check if the built packages textures folder exists
    if not os.path.isdir(built_packages_textures_folder):        
        pr_ko_red   ("built_packages_textures folder value")
        raise ScriptError(error_msg + "The folder containing the built packages textures of the project (" + built_packages_textures_folder + ") was not found. Please check the built_packages_textures_folder value")
    pr_ok_green     ("built_packages_textures folder value")
        
##################################################################
# Backup the packages textures files before the conversion process
##################################################################      
def backup_files():
    os.chdir(built_packages_textures_folder)
    for file in glob.glob(DDS_PATTERN):
        file_name = os.path.basename(file)
        if not os.path.isfile(backup_packages_textures_folder + "\\" + file_name):
            print("backup file ", file_name)
            shutil.copyfile(file, backup_packages_textures_folder + "\\" + file_name)

######################################################
# dds texture files conversion methods
######################################################
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def convert_dds_texture_files():
    os.chdir(built_packages_textures_folder)
    data = retrieve_texture_files_to_treat(DDS_PATTERN, DDS_EXTENSION, BMP_EXTENSION)
    do_convert_dds_texture_files(data)
    data = retrieve_texture_files_to_treat(BMP_PATTERN, BMP_EXTENSION, DDS_EXTENSION)
    compress_dds_texture_files(data)
        
    # clean bmp files
    for bmp_texture_file in glob.glob(BMP_PATTERN):
        file_path = os.path.basename(bmp_texture_file)
        
        try:
            os.remove(file_path)
        except OSError as e:
            error_msg = "Error: " + file_path + " : " + e.strerror
            raise ScriptError(error_msg)
        
        print("bmp temp texture file:", file_path, "removed")  
    

def retrieve_texture_files_to_treat(texture_files_pattern, texture_files_extension, dest_texture_files_extension):
    data = []
    for texture_file in glob.glob(texture_files_pattern):
        print("-------------------------------------------------------------------------------")
        print("texture file: ", os.path.basename(texture_file))
        file_name = os.path.splitext(texture_file)[0]
           
        data.append({'file_name': file_name + texture_files_extension, 'dest_file_name': file_name + dest_texture_files_extension}) 
    
    return chunks(data, NB_PARALLEL_TASKS)
     
def do_convert_dds_texture_files(data):        
    ON_POSIX = 'posix' in sys.builtin_module_names
    
    for chunck in data:
        # create a pipe to get data
        input_fd, output_fd = os.pipe()
        
        processes = [subprocess.Popen([compressonatortool_folder + "\\" + COMPRESSONATOR_EXE_FILE, obj['file_name'], obj['dest_file_name']], stdout=output_fd,
                           close_fds=ON_POSIX) # close input_fd in children
                     for obj in chunck]
        
        os.close(output_fd) # close unused end of the pipe

        # read output line by line as soon as it is available
        with io.open(input_fd, 'r', buffering=1) as file:
            for line in file:
                print(line, end='')

        for p in processes:
            p.wait()
 
def compress_dds_texture_files(data): 
    ON_POSIX = 'posix' in sys.builtin_module_names
    
    for chunck in data:
        # create a pipe to get data
        input_fd, output_fd = os.pipe()
        
        processes = [subprocess.Popen([compressonatortool_folder + "\\" + COMPRESSONATOR_EXE_FILE, "-fd", DDS_CONVERSION_FORMAT, obj['file_name'], obj['dest_file_name']], stdout=output_fd,
                       close_fds=ON_POSIX) # close input_fd in children
                 for obj in chunck]
    
        os.close(output_fd) # close unused end of the pipe

        # read output line by line as soon as it is available
        with io.open(input_fd, 'r', buffering=1) as file:
            for line in file:
                print(line, end='')

        for p in processes:
            p.wait()
                
#######################****************###########################

##################################################################
#                        Main process
################################################################## 

def main():
                
    print("-------------------------------------------------------------------------------")
    print("----------------------- DDS TEXTURE FILES CONVERSION --------------------------")
    print("-------------------------------------------------------------------------------")

    convert_dds_texture_files()

#######################****************###########################

##################################################################
#                           Script
################################################################## 

try:
    check_configuration()    
    
    if not os.path.isdir(built_packages_textures_folder):
        built_packages_textures_folder = built_packages_folder + author_name.lower() + "-" + project_name.lower() + PACKAGES_TEXTURES_SUBFOLDERS
    
    check_packages_folder_configuration()

    os.chdir(built_packages_folder)

    # create the backup folders
    if not os.path.isdir(backup_folder):
        os.mkdir(backup_folder)    
    if not os.path.isdir(backup_packages_textures_folder):
        os.mkdir(backup_packages_textures_folder)
    
    print("-------------------------------------------------------------------------------")
    print("--------------------------------- BACKUP FILES --------------------------------")
    print("-------------------------------------------------------------------------------")

    # backup_files()
        
    main()
    
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
    