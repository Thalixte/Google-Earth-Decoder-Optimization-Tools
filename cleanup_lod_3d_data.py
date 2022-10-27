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

# 21615171614242537

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
from msfs_project import MsfsLod, PROCESS_TYPE

# clear and open the system console
# open_console()

try:
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
        help="folder of the original MsfsLod model file",
    )

    parser.add_argument(
        "-of", "--output_folder", dest="output_folder", type=str, required=True,
        help="folder of the modified MsfsLod model file",
    )

    parser.add_argument(
        "-m", "--model_file", dest="model_file", type=str, required=True,
        help="name of the gltf model file",
    )

    parser.add_argument(
        "-p", "--positioning_file_path", dest="positioning_file_path", type=str, required=True,
        help="path of the positioning mask file",
    )

    parser.add_argument(
        "-msk", "--mask_file_path", dest="mask_file_path", type=str, required=True,
        help="path of the exclusion mask file",
    )

    args = parser.parse_args(argv)

    if not argv:
        raise ScriptError("Error: arguments not given, aborting.")

    if not args.folder:
        raise ScriptError("Error: --folder=\"some string\" argument not given, aborting.")

    if not args.output_folder:
        raise ScriptError("Error: --output_folder=\"some string\" argument not given, aborting.")

    if not args.model_file:
        raise ScriptError("Error: --model_file=\"some string\" argument not given, aborting.")

    if not args.positioning_file_path:
        raise ScriptError("Error: --positioning_file=\"some string\" argument not given, aborting.")

    if not args.mask_file_path:
        raise ScriptError("Error: --mask_file=\"some string\" argument not given, aborting.")

    clean_scene()

    settings = Settings(get_sources_path())

    lod = MsfsLod(os.path.splitext(args.model_file)[0][-2:], 0, args.folder, args.model_file)
    lod.process_3d_data(args.positioning_file_path, args.mask_file_path, args.output_folder, process_type=PROCESS_TYPE.cleanup_3d_data)
except:
    pass
