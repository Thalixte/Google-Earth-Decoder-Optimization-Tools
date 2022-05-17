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

import os

import bpy
import mathutils
from blender.blender_gis import import_osm_file
from blender.image import get_image_node, fix_texture_size_for_package_compilation
from blender.memory import remove_mesh_from_memory
from constants import EOL
from utils import ScriptError, isolated_print, MsfsGltf
from utils.progress_bar import ProgressBar

SELECT_ACTION = "SELECT"
DESELECT_ACTION = "DESELECT"
ACTIVE_OBJ = "active_object"
SELECTED_OBJ = "selected_objects"
SELECTED_EDITABLE_OBJ = "selected_editable_objects"
PACKED_IMAGE_NAME = "LilyPackedImage"
MESH_OBJECT_TYPE = "MESH"
CURSOR_ORIGIN = "ORIGIN_CURSOR"
GEOMETRY_ORIGIN = "ORIGIN_GEOMETRY"
MEDIAN_POS = "MEDIAN"
BOUNDS_POS = "BOUNDS"
GLTF_SEPARATE_EXPORT_FORMAT = "GLTF_SEPARATE"
COPY_COLLECTION_NAME = "CopyCollection"


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
def import_model_files(model_files, clean=True):
    if clean:
        clean_scene()

    for model_file in model_files:
        try:
            print("import ", model_file)
            bpy.ops.import_scene.gltf(filepath=str(model_file))
        except:
            continue


##############################################################################
# Export and optimize the tile in a new gltf file, with bin file and textures
##############################################################################
def export_to_optimized_gltf_files(file, texture_folder, use_selection=False, export_extras=True):
    isolated_print("export to", file, "with associated textures", EOL)
    bpy.ops.export_scene.gltf(export_format=GLTF_SEPARATE_EXPORT_FORMAT, export_extras=export_extras, export_keep_originals=True, filepath=file, export_texture_dir=texture_folder, use_selection=use_selection)
    model_file = MsfsGltf(file)
    model_file.add_optimization_tag()
    model_file.dump()


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
        raise ScriptError("Lily texture packer error detected when trying to pack the textures for " + file_name)

    # create baked texture with Lily texture packer addon
    packed_image = PACKED_IMAGE_NAME
    for image in bpy.data.images:
        if PACKED_IMAGE_NAME in image.name:
            packed_image = image
            break

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

        try:
            material.msfs_show_road_material = True
            material.msfs_show_collision_material = True
            material.msfs_show_day_night_cycle = True
            material.msfs_road_material = True
            material.msfs_collision_material = True
            material.msfs_day_night_cycle = True
        except AttributeError:
            pass

        source_image_nodes = [get_image_node(obj) for obj in objects]
        pbar.update("link packed texture to %s" % obj.name)
        # Update image in materials
        for node in source_image_nodes:
            node.image = img
            node.image.name = file_name


##################################################################
# Fix the tile bounding box
##################################################################
def fix_object_bounding_box(resize_box=True):
    if not bpy.context.scene: return

    create_collection = bpy.data.collections.new(name=COPY_COLLECTION_NAME)
    bpy.context.scene.collection.children.link(create_collection)
    assert (create_collection is not bpy.context.scene.collection)

    # copy objects
    copy_objects(bpy.context.scene.collection, create_collection, False)

    obs = []
    for obj in create_collection.objects:
        if obj.type == MESH_OBJECT_TYPE:
            obs.append(obj)

    ctx = bpy.context.copy()

    if len(obs) < 1:
        return None

    ctx[ACTIVE_OBJ] = obs[0]

    ctx[SELECTED_OBJ] = obs

    # In Blender 2.8x this needs to be the following instead:
    ctx[SELECTED_EDITABLE_OBJ] = obs

    # join copied objects
    bpy.ops.object.join(ctx)

    bpy.ops.object.select_all(action=SELECT_ACTION)

    objects = bpy.context.scene.objects

    # fix objects origin: this also fixes the bounding box for the whole tile
    pbar = ProgressBar(objects)
    for obj in objects:
        center_origin(obj)
        pbar.update("bounded box updated for %s" % obj.name)

    bpy.ops.object.select_all(action=DESELECT_ACTION)

    # remove joined copied objects
    for obj in create_collection.objects:
        obj.select_set(True)
        bpy.ops.object.delete()

    bpy.ops.object.select_all(action=SELECT_ACTION)

    for c in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.unlink(c)

    if resize_box:
        # resize objects to fix spacing between tiles
        bpy.ops.transform.resize(value=(1.0045, 1.0045, 1))


######################################################
# Fix meshes placement method
######################################################
def center_origin(obj):
    # Get active object
    act_obj = obj

    # Get cursor
    cursor = bpy.context.scene.cursor

    # Get original cursor location
    original_cursor_location = (cursor.location[0], cursor.location[1], cursor.location[2])

    # Make sure origin is set to geometry for cursor z move
    bpy.ops.object.origin_set(type=GEOMETRY_ORIGIN, center=BOUNDS_POS)

    print("act_obj.location:", act_obj.location)

    # Set cursor location to object location
    cursor.location = act_obj.location

    cursor.location[2] = original_cursor_location[2]

    # Get cursor x move
    half_act_obj_x_dim = act_obj.dimensions[0] / 2
    cursor_x_move = cursor.location[0] + half_act_obj_x_dim
    cursor.location[0] = cursor_x_move

    # Get cursor y move
    half_act_obj_y_dim = act_obj.dimensions[1] / 2
    cursor_y_move = cursor.location[1] + half_act_obj_y_dim
    cursor.location[1] = cursor_y_move

    # Set origin to cursor
    bpy.ops.object.origin_set(type=CURSOR_ORIGIN, center=MEDIAN_POS)

    # Reset cursor back to original location
    cursor.location = original_cursor_location

    # Assuming you're wanting object center to grid
    bpy.ops.object.location_clear(clear_delta=False)


def align_model_with_mask(model_file_path, positioning_file_path, mask_file_path):
    if not bpy.context.scene: return False

    import_model_files([model_file_path])
    bpy.ops.object.select_all(action=SELECT_ACTION)
    bpy.ops.object.join()
    rot_z = 0.0

    import_osm_file(positioning_file_path)

    for obj in bpy.context.selected_objects:
        obj.name = "Ways"
        coords = [v.co for v in obj.data.vertices]
        p1 = coords[0]
        p2 = coords[1]
        Vector1 = (p1 - p2).normalized()
        proj_coords = [corner for corner in obj.bound_box]
        b2 = mathutils.Vector((proj_coords[2][0], proj_coords[2][1], proj_coords[2][2]))
        b4 = mathutils.Vector((proj_coords[6][0], proj_coords[6][1], proj_coords[6][2]))
        Vector2 = (b4 - b2).normalized()
        rot_z = Vector1.rotation_difference(Vector2).to_euler()
        obj.select_set(True)
        obj.rotation_euler = rot_z

    bpy.ops.object.select_all(action=SELECT_ACTION)

    bpy.ops.object.align(bb_quality=True, align_mode='OPT_1', relative_to='OPT_4', align_axis={'X', 'Y'})

    bpy.ops.object.select_all(action=DESELECT_ACTION)

    src = bpy.context.scene.objects.get("Ways")

    transform_x = src.matrix_world.translation[0]
    transform_y = src.matrix_world.translation[1]

    clean_scene()

    bpy.ops.object.select_all(action=DESELECT_ACTION)

    import_osm_file(mask_file_path)
    for obj in bpy.context.selected_objects:
        obj.name = "Areas"
    target = bpy.context.scene.objects.get("Areas")
    bpy.ops.object.select_all(action=SELECT_ACTION)
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.join()

    bpy.ops.transform.mirror(constraint_axis=(True, True, False), orient_type='GLOBAL')
    for obj in bpy.context.selected_objects:
        obj_loc_x = obj.location.x
        obj.location.x = obj_loc_x * -1

    target.rotation_euler = rot_z
    target.location[0] = transform_x
    target.location[1] = transform_y

    bpy.ops.object.select_all(action=DESELECT_ACTION)


def cleanup_3d_data(model_file_path):
    import_model_files([model_file_path], clean=False)
    objects = bpy.context.scene.objects

    mask = bpy.context.scene.objects.get("Areas")

    if mask:
        for obj in objects:
            if obj != mask:
                bpy.context.view_layer.objects.active = obj
                booly = obj.modifiers.new(name='booly', type='BOOLEAN')

                if not booly:
                    continue

                booly.object = mask
                booly.operation = 'DIFFERENCE'
                booly.solver = 'EXACT'
                booly.use_hole_tolerant = True
                for modifier in obj.modifiers:
                    bpy.ops.object.modifier_apply(modifier=modifier.name)

    if mask:
        for obj in objects:
            if obj != mask:
                bpy.context.view_layer.objects.active = obj
                weighted_normal = obj.modifiers.new(name='weighty', type='WEIGHTED_NORMAL')

                if not weighted_normal:
                    continue

                weighted_normal.weight = 100
                weighted_normal.thresh = 10.0
                weighted_normal.keep_sharp = True
                weighted_normal.use_face_influence = True
                for modifier in obj.modifiers:
                    bpy.ops.object.modifier_apply(modifier=modifier.name)

    bpy.ops.object.select_all(action=DESELECT_ACTION)
    mask.select_set(True)
    bpy.ops.object.delete()
    bpy.ops.object.select_all(action=SELECT_ACTION)


def extract_splitted_tile(model_file_path, node, texture_folder):
    if not bpy.context.scene: return False

    bpy.ops.object.select_all(action=DESELECT_ACTION)

    objs = [obj for obj in bpy.context.scene.objects if obj.name in node]
    for obj in objs:
        obj.select_set(True)

    export_to_optimized_gltf_files(model_file_path, texture_folder, use_selection=True, export_extras=False)


def copy_objects(from_col, to_col, linked):
    for o in from_col.objects:
        dupe = o.copy()
        if not linked and o.data:
            dupe.data = dupe.data.copy()
        to_col.objects.link(dupe)
