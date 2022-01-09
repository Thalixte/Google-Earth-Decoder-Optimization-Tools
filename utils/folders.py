import os
import bpy


def get_sources_path():
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Check if script is executed in Blender and get absolute path of current folder
    if hasattr(bpy.context, "space_data"):
        if bpy.context.space_data is not None:
            cwd = os.path.dirname(bpy.context.space_data.text.filepath)

    return cwd
