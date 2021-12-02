import os
import bpy


def get_sources_path():
    # Check if script is executed in Blender and get absolute path of current folder
    if bpy.context.space_data is not None:
        cwd = os.path.dirname(os.path.dirname(bpy.context.space_data.text.filepath))
    else:
        cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return cwd
