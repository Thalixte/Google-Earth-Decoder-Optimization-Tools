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
from msfs_project import MsfsLandmarkLocation, LightsXml

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
    "-m", "--model_files_paths", dest="model_files_paths", type=str, required=True,
    help="names of the gltf model files",
)

parser.add_argument(
    "-p", "--positioning_files_paths", dest="positioning_files_paths", type=str, required=True,
    help="paths of the positioning mask files",
)

parser.add_argument(
    "-lloc", "--landmark_location_file_path", dest="landmark_location_file_path", type=str, required=True,
    help="path of the landmark location file",
)

parser.add_argument(
    "-msk", "--mask_file_path", dest="mask_file_path", type=str, required=True,
    help="path of the mask file",
)

parser.add_argument(
    "-lxf", "--lights_xml_folder", dest="lights_xml_folder", type=str, required=True,
    help="folder of the lights xml file",
)

parser.add_argument(
    "-lat", "--lat", dest="lat", type=str, required=True,
    help="latitude of the geocode",
)

parser.add_argument(
    "-lon", "--lon", dest="lon", type=str, required=True,
    help="longitude of the geocode",
)

parser.add_argument(
    "-alt", "--alt", dest="alt", type=str, required=True,
    help="altitude of the geocode",
)

parser.add_argument(
    "-gpr", "--geocode_prefix", dest="geocode_prefix", type=str, required=True,
    help="prefix of the lights display name, based on the geocode",
)

parser.add_argument(
    "-dbg", "--debug", dest="debug", type=str, required=False,
    help="Debug the lights creation in blender",
)

args = parser.parse_args(argv)

if not argv:
    raise ScriptError("Error: arguments not given, aborting.")

if not args.model_files_paths:
    raise ScriptError("Error: --model_files_paths=\"some string\" argument not given, aborting.")

if not args.positioning_files_paths:
    raise ScriptError("Error: --positioning_files_paths=\"some string\" argument not given, aborting.")

if not args.mask_file_path:
    raise ScriptError("Error: --landmark_location_file_path=\"some string\" argument not given, aborting.")

if not args.mask_file_path:
    raise ScriptError("Error: --mask_file_path=\"some string\" argument not given, aborting.")

if not args.lights_xml_folder:
    raise ScriptError("Error: --lights_xml_folder=\"some string\" argument not given, aborting.")

if not args.lat:
    raise ScriptError("Error: --lat=\"some string\" argument not given, aborting.")

if not args.alt:
    raise ScriptError("Error: --alt=\"some string\" argument not given, aborting.")

if not args.geocode_prefix:
    raise ScriptError("Error: --geocode_prefix=\"some string\" argument not given, aborting.")

clean_scene()

if args.debug:
    debug = json.loads(args.debug.lower())
else:
    debug = False

model_files_paths = args.model_files_paths.replace('"', '').split("|")
positioning_files_paths = args.positioning_files_paths.replace('"', '').split("|")

# sanitize the file paths
lights_xml_folder = args.lights_xml_folder.replace('"', '')
landmark_location_file_path = args.landmark_location_file_path.replace('"', '')
mask_file_path = args.mask_file_path.replace('"', '')
geocode_prefix = args.geocode_prefix.replace('"', '')

landmarkLocation = MsfsLandmarkLocation()

landmarkLocation.add_lights(LightsXml(lights_xml_folder, GEOCODE_LIGHTS_PREFIX + XML_FILE_EXT), model_files_paths, positioning_files_paths, landmark_location_file_path, mask_file_path, float(args.lat), float(args.lon), float(args.alt), geocode_prefix, debug=debug)
# except:
#     pass
