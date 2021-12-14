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
from blender import clean_scene
from msfs_project import MsfsLod

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

    # Example utility, add some text and renders or saves it (with options)
    # Possible types are: string, int, long, choice, float and complex.
    parser.add_argument(
        "-p", "--path", dest="path", type=str, required=True,
        help="path to the MsfsObject definition file",
    )

    # Example utility, add some text and renders or saves it (with options)
    # Possible types are: string, int, long, choice, float and complex.
    parser.add_argument(
        "-m", "--model_file", dest="model_file", type=str, required=True,
        help="name of the gltf model file",
    )

    args = parser.parse_args(argv)

    if not argv:
        raise ScriptError("Error: --path=\"some string\" argument not given, aborting.")

    if not args.path:
        raise ScriptError("Error: --path=\"some string\" argument not given, aborting.")

    clean_scene()

    settings = Settings(get_sources_path())

    lod = MsfsLod(int(args.path[-2:]), 0, args.path, args.model_file)
    lod.optimize(settings.bake_textures_enabled, settings.output_texture_format)

except:
    pass
