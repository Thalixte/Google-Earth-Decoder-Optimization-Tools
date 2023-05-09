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

import argparse
import os
import site
import sys

import bpy

CONSTANTS_FOLDER = "constants"
UTILS_FOLDER = "utils"
SCRIPT_FOLDER = "scripts"

# Check if script is executed in Blender and get absolute path of current folder
if bpy.context.space_data is not None:
    sources_path = os.path.dirname(bpy.context.space_data.text.filepath)
else:
    sources_path = os.path.dirname(os.path.abspath(__file__))

# Get scripts folder and add it to the search path for modules
os.chdir(sources_path)

sys.path.append(site.USER_SITE)

if sources_path not in sys.path:
    sys.path.append(sources_path)

# Get scripts folder and add it to the search path for modules
cwd = os.path.join(sources_path, CONSTANTS_FOLDER)
if cwd not in sys.path:
    sys.path.append(cwd)

# Get scripts folder and add it to the search path for modules
cwd = os.path.join(sources_path, UTILS_FOLDER)
if cwd not in sys.path:
    sys.path.append(cwd)

# Get scripts folder and add it to the search path for modules
cwd = os.path.join(sources_path, SCRIPT_FOLDER)
if cwd not in sys.path:
    sys.path.append(cwd)

from utils import *
from blender import clean_scene
from msfs_project import MsfsTile, ObjectsXml

# clear and open the system console
# open_console()

# get the args passed to blender after "--", all of which are ignored by
# blender so scripts may receive their own arguments
argv = sys.argv

if "--" not in argv:
    argv = []  # as if no args are passed
else:
    argv = argv[argv.index("--") + 1:]  # get all args after "--"

# When --help or no args are given, print this help
usage_text = (
        "Run blender in background mode with this script:"
        "  blender --background --python " + __file__ + " -- [options]"
)

parser = argparse.ArgumentParser(description=usage_text)

parser.add_argument(
    "-f", "--folder", dest="folder", type=str, required=True,
    help="folder of the MsfsTile definition file",
)

parser.add_argument(
    "-n", "--name", dest="name", type=str, required=True,
    help="name of the tile",
)

parser.add_argument(
    "-d", "--definition_file", dest="definition_file", type=str, required=True,
    help="name of the xml definition file of the tile",
)

parser.add_argument(
    "-oxf", "--objects_xml_folder", dest="objects_xml_folder", type=str, required=True,
    help="folder of the xml definition file of the scene",
)

parser.add_argument(
    "-oxn", "--objects_xml_file", dest="objects_xml_file", type=str, required=True,
    help="name of the xml definition file of the scene",
)

try:
    args = parser.parse_args(argv)

    if not argv:
        raise ScriptError("Error: arguments not given, aborting.")

    if not args.folder:
        raise ScriptError("Error: --folder=\"some string\" argument not given, aborting.")

    if not args.name:
        raise ScriptError("Error: --name=\"some string\" argument not given, aborting.")

    if not args.definition_file:
        raise ScriptError("Error: --definition_file=\"some string\" argument not given, aborting.")

    if not args.objects_xml_folder:
        raise ScriptError("Error: --objects_xml_folder=\"some string\" argument not given, aborting.")

    if not args.objects_xml_file:
        raise ScriptError("Error: --objects_xml_file=\"some string\" argument not given, aborting.")

    clean_scene()

    settings = Settings(get_global_path())

    tile = MsfsTile(args.folder, args.name, args.definition_file)
    tile.split(settings)
except:
    pass
