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
from msfs_project import MsfsTile, HeightMapXml

# clear and open the system console
# open_console()

# try:
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
    "-hmxf", "--height_map_xml_folder", dest="height_map_xml_folder", type=str, required=True,
    help="folder of the height map xml file",
)

parser.add_argument(
    "-gi", "--group_id", dest="group_id", type=str, required=True,
    help="id of the group containing the height maps",
)

parser.add_argument(
    "-alt", "--altitude", dest="altitude", type=str, required=True,
    help="altitude of the height map",
)

parser.add_argument(
    "-hadjust", "--height_adjustment", dest="height_adjustment", type=str, required=True,
    help="height adjustment of the height map",
)

parser.add_argument(
    "-p", "--positioning_file_path", dest="positioning_file_path", type=str, required=False,
    help="path of the positioning mask file",
)

parser.add_argument(
    "-gmsk", "--ground_mask_file_path", dest="ground_mask_file_path", type=str, required=False,
    help="path of the ground exclusion mask file",
)

parser.add_argument(
    "-bmsk", "--building_mask_file_path", dest="building_mask_file_path", type=str, required=False,
    help="path of the building exclusion mask file",
)

parser.add_argument(
    "-rmsk", "--rocks_mask_file_path", dest="rocks_mask_file_path", type=str, required=False,
    help="path of the rocks exclusion mask file",
)

parser.add_argument(
    "-wmsk", "--water_mask_file_path", dest="water_mask_file_path", type=str, required=False,
    help="path of the water exclusion mask file",
)

parser.add_argument(
    "-hp", "--high_precision", dest="high_precision", type=str, required=True,
    help="indicates if the the most detailed tile is used for height calculation",
)

parser.add_argument(
    "-dbg", "--debug", dest="debug", type=str, required=False,
    help="Debug the height data in blender",
)

args = parser.parse_args(argv)

if not argv:
    raise ScriptError("Error: arguments not given, aborting.")

if not args.folder:
    raise ScriptError("Error: --folder=\"some string\" argument not given, aborting.")

if not args.name:
    raise ScriptError("Error: --name=\"some string\" argument not given, aborting.")

if not args.definition_file:
    raise ScriptError("Error: --definition_file=\"some string\" argument not given, aborting.")

if not args.height_map_xml_folder:
    raise ScriptError("Error: --height_map_xml_folder=\"some string\" argument not given, aborting.")

if not args.group_id:
    raise ScriptError("Error: --group_id=\"some string\" argument not given, aborting.")

if not args.altitude:
    raise ScriptError("Error: --altitude=\"some string\" argument not given, aborting.")

if not args.height_adjustment:
    raise ScriptError("Error: --height_adjustment=\"some string\" argument not given, aborting.")

if not args.high_precision:
    raise ScriptError("Error: --high_precision=\"true/false\" argument not given, aborting.")

clean_scene()

high_precision = json.loads(args.high_precision.lower())

if args.debug:
    debug = json.loads(args.debug.lower())
else:
    debug = False

positioning_file_path = args.positioning_file_path if args.positioning_file_path else str()
ground_mask_file_path = args.ground_mask_file_path if args.ground_mask_file_path else str()
building_mask_file_path = args.building_mask_file_path if args.building_mask_file_path else str()
rocks_mask_file_path = args.rocks_mask_file_path if args.rocks_mask_file_path else str()
water_mask_file_path = args.water_mask_file_path if args.water_mask_file_path else str()

tile = MsfsTile(args.folder, args.name, args.definition_file)
tile.generate_height_data(HeightMapXml(args.height_map_xml_folder, HEIGHT_MAP_PREFIX + args.name + XML_FILE_EXT), args.group_id, float(args.altitude), float(args.height_adjustment), high_precision=high_precision, positioning_file_path=positioning_file_path, water_mask_file_path=water_mask_file_path, ground_mask_file_path=ground_mask_file_path, rocks_mask_file_path=rocks_mask_file_path, building_mask_file_path=building_mask_file_path, debug=debug)
# except:
#     pass