import os

import bpy
from blender.image import get_image_node, fix_texture_size_for_package_compilation
from blender.memory import remove_mesh_from_memory
from constants import EOL
from utils import ScriptError, isolated_print
from utils.progress_bar import ProgressBar

SELECT_ACTION = "SELECT"
SELECTED_OBJ = "selected_objects"
PACKED_IMAGE_NAME = "LilyPackedImage"


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
            isolated_print("Unable to remove [%s]." % me.name)

    print(EOL)
    print("3d scene cleaned", EOL)


##################################################################
# Import the gltf files located in a specific folder
##################################################################
def import_model_files(model_files):
    clean_scene()
    for model_file in model_files:
        try:
            print("import ", model_file)
            bpy.ops.import_scene.gltf(filepath=str(model_file))
        except:
            continue


##################################################################
# Bake the tile texture files
##################################################################
def bake_texture_files(folder, file_name):
    error = False

    if not bpy.context.scene: return False

    # cleanup nodes with no materials
    objs = [obj for obj in bpy.context.scene.objects if not obj.material_slots]
    bpy.ops.object.delete({SELECTED_OBJ: objs})

    objects = bpy.context.scene.objects

    source_image_nodes = []
    for obj in bpy.context.scene.objects:
        image_node = get_image_node(obj)
        if not image_node.image is None:
            source_image_nodes.append(image_node)
        else:
            bpy.data.objects.remove(obj, do_unlink=True)

    for node in source_image_nodes:
        if node.image is None:
            error = True

    if error is True:
        return False

    for obj in objects:
        obj.select_set(True)

    try:
        bpy.ops.object.lily_texture_packer()
    except:
        raise ScriptError("Texture packer error detected !!!" + file_name)

    # create baked texture with Lily texture packer addon
    packed_image = bpy.data.images[PACKED_IMAGE_NAME]

    # fix texture final size for package compilation
    fix_texture_size_for_package_compilation(packed_image)

    # isolated_print("Save new baked texture", os.path.join(folder, file_name))
    packed_image.save_render(os.path.join(folder, file_name))

    # link the tile materials to the new packed texture
    link_materials_to_packed_texture(objects, folder, file_name)
    bpy.data.images.remove(packed_image)


##################################################################
# link the tile materials to the new packed texture
##################################################################
def link_materials_to_packed_texture(objects, folder, file_name):
    img = bpy.data.images.load(os.path.join(folder, file_name))

    pbar = ProgressBar(bpy.context.scene.objects)
    for obj in pbar.iterable:
        material = obj.material_slots[0].material
        material.msfs_show_road_material = True
        material.msfs_show_collision_material = True
        material.msfs_show_day_night_cycle = True
        material.msfs_road_material = True
        material.msfs_collision_material = True
        material.msfs_day_night_cycle = True

        source_image_nodes = [get_image_node(obj) for obj in objects]
        pbar.update("link packed texture to %s" % obj.name)
        # Update image in materials
        for node in source_image_nodes:
            node.image = img
            node.image.name = file_name
