import bpy
from blender.memory import remove_mesh_from_memory
from constants import EOL

SELECT_ACTION = "SELECT"


def clean_scene():
    if not bpy.data:
        return

    bpy.ops.object.select_all(action=SELECT_ACTION)

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

    bpy.ops.object.delete()

    # Now cycles through the dangling datablocks and remove them.
    for me in bpy.data.meshes:
        if not remove_mesh_from_memory(me.name):
            print("Unable to remove [%s]." % me.name)

    print(EOL, "3d scene cleaned", EOL)
