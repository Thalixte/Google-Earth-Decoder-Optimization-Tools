import os
import site
import sys
import bpy

CONSTANTS_FOLDER = "constants"
UTILS_FOLDER = "utils"
SCRIPT_FOLDER = "scripts"

# Check if script is executed in Blender and get absolute path of current folder
if bpy.context.space_data is not None:
    files_dir = os.path.dirname(bpy.context.space_data.text.filepath)
else:
    files_dir = os.path.dirname(os.path.abspath(__file__))

# Get scripts folder and add it to the search path for modules
os.chdir(files_dir)

sys.path.append(site.USER_SITE)

if files_dir not in sys.path:
    sys.path.append(files_dir)

# Get scripts folder and add it to the search path for modules
cwd = os.path.join(files_dir, CONSTANTS_FOLDER)
if cwd not in sys.path:
    sys.path.append(cwd)

# Get scripts folder and add it to the search path for modules
cwd = os.path.join(files_dir, UTILS_FOLDER)
if cwd not in sys.path:
    sys.path.append(cwd)

# Get scripts folder and add it to the search path for modules
cwd = os.path.join(files_dir, SCRIPT_FOLDER)
if cwd not in sys.path:
    sys.path.append(cwd)

from utils import *
from constants import *

# clear and open the system console
open_console()

# Specify the script to be included
scriptFiles = ["clean_package_files_script.py"]

for scriptFile in scriptFiles:
    # Compile and execute script file
    file = os.path.join(cwd, scriptFile)
    exec(compile(open(file).read(), scriptFile, PYTHON_COMPIL_OPTION))
