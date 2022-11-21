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

from mathutils.bvhtree import BVHTree
from collections import defaultdict
from pathlib import Path
from utils import install_python_lib

try:
    import numpy as np
except ModuleNotFoundError:
    install_python_lib('numpy')
    import numpy as np

try:
    import pygeodesy
except ModuleNotFoundError:
    install_python_lib('pygeodesy')
    import pygeodesy

try:
    import scipy
except ModuleNotFoundError:
    install_python_lib('scipy')
    import scipy

try:
    import shapely
except ModuleNotFoundError:
    install_python_lib('shapely')
    import shapely

from pygeodesy.ellipsoidalKarney import LatLon
from scipy.spatial import cKDTree
from shapely import geometry

import bmesh
import bpy
import mathutils
from blender.blender_gis import import_osm_file, OSM_MATERIAL_NAME
from blender.image import get_image_node, fix_texture_size_for_package_compilation
from blender.memory import remove_mesh_from_memory
from blender.material import set_msfs_material, add_new_obj_material
from constants import EOL, GEOIDS_DATASET_FOLDER, EGM2008_5_DATASET, OBJ_FILE_EXT, BOUNDING_BOX_OSM_KEY, LESS_DETAILED_LODS_LIMIT
from msfs_project.gltf import MsfsGltf
from utils import ScriptError, isolated_print
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
SUB_TILES_RANGE = "[0-7]"
TILE_LOD_SUFFIX = "_LOD0"
OBJECT_NAME_SEP = "_"
GEOID_HEIGHT_ORIGIN_MARGIN = 5.0
FACES_ONLY_DELETE_CONTEXT = "FACES_ONLY"
FACES_DELETE_CONTEXT = "FACES"
VERTICES_DELETE_CONTEXT = "VERTS"


class BOOLEAN_MODIFIER_OPERATION:
    DIFFERENCE = "DIFFERENCE"
    INTERSECT = "INTERSECT"


class EXCLUSION_TYPE:
    GROUND = "GROUND"
    WATER = "WATER"


def keep_objects(objects_to_keep):
    if len(objects_to_keep) > 0:
        for obj_to_keep in objects_to_keep:
            obj_to_keep.select_set(False)


def clean_scene(objects_to_keep=[], keep_materials=False):
    if not bpy.data:
        return

    bpy.ops.object.select_all(action=SELECT_ACTION)

    keep_objects(objects_to_keep)

    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)

    if not keep_materials:
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

    print(EOL)
    print("3d scene cleaned", EOL)


##################################################################
# Import the gltf files located in a specific folder
##################################################################
def import_model_files(model_files, clean=True, objects_to_keep=[]):
    if clean:
        clean_scene(objects_to_keep=objects_to_keep)

    for model_file in model_files:
        try:
            print("import ", model_file)
            bpy.ops.import_scene.gltf(filepath=str(model_file))
        except:
            continue

    if not objects_to_keep:
        # clean non mesh data
        objs = bpy.context.selected_objects
        bpy.ops.object.select_all(action=DESELECT_ACTION)

        for obj in objs:
            if obj.type != MESH_OBJECT_TYPE:
                obj.select_set(True)
                bpy.ops.object.delete()

        bpy.ops.object.select_all(action=SELECT_ACTION)


##############################################################################
# Export and optimize the tile in a new gltf file, with bin file and textures
##############################################################################
def export_to_optimized_gltf_files(file, texture_folder, use_selection=False, export_extras=True, apply_modifiers=False):
    isolated_print("export to", file, "with associated textures", EOL)

    bpy.ops.export_scene.gltf(export_format=GLTF_SEPARATE_EXPORT_FORMAT, export_extras=export_extras, export_keep_originals=True, filepath=file, export_texture_dir=texture_folder, use_selection=use_selection, use_mesh_edges=False, export_apply=apply_modifiers)
    model_file = MsfsGltf(file)
    model_file.clean_empty_meshes()
    model_file.fix_gltf_nodes()
    model_file.add_optimization_tag()
    model_file.dump()


##############################################################################
# Convert an obj file to a gltf file
##############################################################################
def convert_obj_file_to_gltf_file(file, output_folder, texture_folder, depth):
    file_name = os.path.basename(file).replace(OBJ_FILE_EXT, str())
    file_path = os.path.dirname(file)
    current_depth = depth
    while current_depth > 0:
        clean_scene()
        name_filter = file_name
        for i in range(0, current_depth-1):
            name_filter = name_filter + SUB_TILES_RANGE
        for lod_file in Path(file_path).glob(name_filter + OBJ_FILE_EXT):
            lod_file_name = os.path.basename(lod_file).replace(OBJ_FILE_EXT, str())
            prior_objects = [obj for obj in bpy.context.scene.objects]
            bpy.ops.import_scene.obj(filepath=str(lod_file), axis_up='Z', axis_forward='-X')
            new_current_objects = [obj for obj in bpy.context.scene.objects]
            new_objects = set(new_current_objects) - set(prior_objects)
            for i, obj in enumerate(new_objects):
                obj.name = lod_file_name + "_" + str(i)

        set_msfs_material()
        # fix tile optimization placement by applying rotation on the imported tile
        bpy.ops.object.select_all(action=SELECT_ACTION)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        current_name = file_name + TILE_LOD_SUFFIX + str(depth - current_depth)
        bpy.ops.export_scene.gltf(export_format=GLTF_SEPARATE_EXPORT_FORMAT, filepath=output_folder + os.path.sep + current_name, export_texture_dir=texture_folder)
        current_depth -= 1
        clean_scene()


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
        if image_node.image is not None:
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


def align_model_with_mask(model_file_path, positioning_file_path, mask_file_path, objects_to_keep=[]):
    if not bpy.context.scene:
        return False

    import_model_files([model_file_path], objects_to_keep=objects_to_keep)
    bpy.ops.object.select_all(action=SELECT_ACTION)
    objs = bpy.context.selected_objects
    bpy.ops.object.select_all(action=DESELECT_ACTION)
    mesh = None

    for obj in objs:
        if obj.type != MESH_OBJECT_TYPE:
            obj.select_set(True)
            bpy.ops.object.delete()
        else:
            mesh = obj

    bpy.context.view_layer.objects.active = mesh
    bpy.ops.object.select_all(action=SELECT_ACTION)
    keep_objects(objects_to_keep)

    bpy.ops.object.join()
    rot_z = 0.0

    import_osm_file(positioning_file_path)
    bpy.ops.transform.resize(value=(1.0045, 1.0045, 1))

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

    bpy.ops.object.align(bb_quality=True, align_mode='OPT_3', relative_to='OPT_2', align_axis={'X', 'Y'})

    bpy.ops.object.select_all(action=DESELECT_ACTION)

    src = bpy.context.scene.objects.get("Ways")

    transform_x = src.matrix_world.translation[0]
    transform_y = src.matrix_world.translation[1]
    transform_z = src.matrix_world.translation[2]

    clean_scene(objects_to_keep=objects_to_keep)

    bpy.ops.object.select_all(action=DESELECT_ACTION)

    import_osm_file(mask_file_path)
    for obj in bpy.context.selected_objects:
        obj.name = "Areas"
    target = bpy.context.scene.objects.get("Areas")
    bpy.ops.object.select_all(action=SELECT_ACTION)
    keep_objects(objects_to_keep)
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.join()

    bpy.ops.transform.mirror(constraint_axis=(True, True, False), orient_type='GLOBAL')
    for obj in bpy.context.selected_objects:
        obj_loc_x = obj.location.x
        obj.location.x = obj_loc_x * -1

    target.rotation_euler = rot_z
    target.location[0] = transform_x
    target.location[1] = transform_y
    target.location[2] = transform_z

    bpy.ops.object.select_all(action=DESELECT_ACTION)


def reduce_number_of_vertices(model_file_path):
    import_model_files([model_file_path], clean=False)
    objects = bpy.context.scene.objects

    for obj in objects:
        bpy.context.view_layer.objects.active = obj
        decimate = obj.modifiers.new(name="decimate", type="DECIMATE")

        if not decimate:
            continue

        decimate.decimate_type = "DISSOLVE"
        for modifier in obj.modifiers:
            bpy.ops.object.modifier_apply(modifier=modifier.name)

    for obj in objects:
        bpy.context.view_layer.objects.active = obj
        weighted_normal = obj.modifiers.new(name="weighty", type="WEIGHTED_NORMAL")

        if not weighted_normal:
            continue

        weighted_normal.weight = 50
        weighted_normal.thresh = 0.0
        weighted_normal.keep_sharp = True
        weighted_normal.use_face_influence = True
        for modifier in obj.modifiers:
            bpy.ops.object.modifier_apply(modifier=modifier.name)

    bpy.ops.object.select_all(action=SELECT_ACTION)


def process_3d_data(model_file_path, intersect=False):
    import_model_files([model_file_path], clean=False)

    objects = bpy.context.scene.objects

    mask = bpy.context.scene.objects.get("Areas")
    grid = bpy.context.scene.objects.get("grid")
    height_grid = bpy.context.scene.objects.get("height_grid")

    new_collection = bpy.data.collections.new(name="inclusion_points")
    assert (new_collection is not bpy.context.scene.collection)
    bpy.context.scene.collection.children.link(new_collection)

    bpy.ops.object.select_all(action=DESELECT_ACTION)

    updated_objects = []

    if mask:
        for obj in objects:
            if obj == mask or obj == grid or obj == height_grid or BOUNDING_BOX_OSM_KEY in obj.name:
                continue

            # only cleanup objects contained in the mask, or touched by the mask
            if object_touches_mask(obj, mask) or intersect:
                bpy.context.view_layer.objects.active = obj
                add_new_obj_material(obj, OSM_MATERIAL_NAME)

                if not add_boolean_modifier(obj, mask, BOOLEAN_MODIFIER_OPERATION.INTERSECT if intersect else BOOLEAN_MODIFIER_OPERATION.DIFFERENCE):
                    continue

                for modifier in obj.modifiers:
                    bpy.ops.object.modifier_apply(modifier=modifier.name)

                updated_objects.append(obj)

    for obj in updated_objects:
        if obj == mask or obj == grid or obj == height_grid or BOUNDING_BOX_OSM_KEY in obj.name:
            continue

        if obj.type != MESH_OBJECT_TYPE:
            continue

        # flat faces to prevent wrong cleaning on less detailed object lods
        if retrieve_tile_object_lod(obj) <= LESS_DETAILED_LODS_LIMIT:
            flat_cutted_faces(obj)

    bpy.ops.object.select_all(action=DESELECT_ACTION)
    mask.select_set(True)
    bpy.ops.object.delete()
    bpy.ops.object.select_all(action=SELECT_ACTION)

    # cleanup the cutted faces
    cleanup_cutted_faces(updated_objects)

    clean_scene(objects_to_keep=bpy.context.scene.objects)
    bpy.ops.object.select_all(action=SELECT_ACTION)

    # Fix 3d normals
    for obj in updated_objects:
        if BOUNDING_BOX_OSM_KEY not in obj.name and obj.type == MESH_OBJECT_TYPE:
            bpy.context.view_layer.objects.active = obj

            if not add_weighted_normal_modifier(obj):
                continue

    bpy.ops.object.select_all(action=SELECT_ACTION)


def generate_model_height_data(model_file_path, lat, lon, altitude, height_adjustment, inverted=False, positioning_file_path="", water_mask_file_path="", ground_mask_file_path="", debug=False):
    if not bpy.context.scene:
        return False

    tile = get_tile_for_ray_cast(model_file_path)
    coords, width, grid, grid_dimension, height_grid_coords, height_grid = prepare_ray_cast(tile)

    bpy.ops.object.select_all(action=DESELECT_ACTION)
    # ensure to select the tile
    tile.select_set(False)

    depsgraph = bpy.context.evaluated_depsgraph_get()
    depsgraph.update()
    hmatrix = calculate_height_map_from_coords_from_bottom(tile, grid_dimension, coords, depsgraph, lat, lon, altitude, height_adjustment)

    # fix wrong height data for ground tiles
    if os.path.exists(positioning_file_path) and os.path.exists(ground_mask_file_path):
        align_model_with_mask(model_file_path, positioning_file_path, ground_mask_file_path, objects_to_keep=[grid, height_grid])
        process_3d_data(model_file_path, intersect=True)
        tile = get_tile_for_ray_cast(model_file_path, imported=False, objects_to_keep=[grid, height_grid])
        if inverted:
            hmatrix = calculate_height_map_from_coords_from_top(tile, grid_dimension, coords, depsgraph, lat, lon, altitude, hmatrix_base=hmatrix)
        else:
            hmatrix = adjust_height_data_on_ground_exclusion(tile, depsgraph, lat, lon, altitude, hmatrix_base=hmatrix)

    # fix wrong height data for bridges on water
    if os.path.exists(positioning_file_path) and os.path.exists(water_mask_file_path):
        align_model_with_mask(model_file_path, positioning_file_path, water_mask_file_path, objects_to_keep=[grid, height_grid])
        process_3d_data(model_file_path, intersect=True)
        tile = get_tile_for_ray_cast(model_file_path, imported=False, objects_to_keep=[grid, height_grid])
        hmatrix = fix_bridge_height_data_on_water(tile, depsgraph, lat, lon, altitude, hmatrix_base=hmatrix)

    results = {}

    for y, heights in hmatrix.items():
        results[y] = [h for i, h in enumerate(list(heights.values())) if i % 2 == 1]

    if debug:
        new_collection = bpy.data.collections.new(name="coords")
        assert (new_collection is not bpy.context.scene.collection)
        bpy.context.scene.collection.children.link(new_collection)

        debug_height_data(new_collection, hmatrix, height_grid, height_grid_coords)

    bpy.ops.object.select_all(action=DESELECT_ACTION)
    grid.select_set(True)
    bpy.ops.object.delete()
    tile.select_set(True)
    bpy.ops.object.select_all(action=SELECT_ACTION)

    if not debug:
        clean_scene()

    return results, width, altitude


def debug_height_data(new_collection, hmatrix, height_grid, height_grid_coords):
    i = 0
    not_updated_coords = height_grid_coords.copy()

    for y, heights in hmatrix.items():
        n = 0

        # debug height data
        for x, h in heights.items():
            if n % 2 == 1:
                # debug display of the cloud of points
                p = point_cloud("p" + str(i), [(x, y, h)])
                new_collection.objects.link(p)
                i = i + 1

            for p in height_grid_coords:
                if p[0] == x and p[1] == y:
                    for nup in not_updated_coords:
                        if p[0] == nup[0] and p[1] == nup[1]:
                            not_updated_coords.remove(nup)

                    p[2] = h

            n = n + 1

    for p in not_updated_coords:
        p[0] = 0
        p[1] = 0
        p[2] = 0

    delete_origin_points(height_grid)


def get_tile_for_ray_cast(model_file_path, imported=True, objects_to_keep=[]):
    tile = None

    if imported:
        import_model_files([model_file_path])
    bpy.ops.object.select_all(action=SELECT_ACTION)
    keep_objects(objects_to_keep)
    objs = bpy.context.selected_objects
    bpy.ops.object.select_all(action=DESELECT_ACTION)
    mesh = None

    for obj in objs:
        if obj.type != MESH_OBJECT_TYPE:
            obj.select_set(True)
            bpy.ops.object.delete()
        else:
            mesh = obj

    bpy.context.view_layer.objects.active = mesh
    bpy.ops.object.select_all(action=SELECT_ACTION)
    keep_objects(objects_to_keep)
    bpy.ops.object.join()

    objs = bpy.context.selected_objects
    for obj in objs:
        tile = obj

    return tile


def prepare_ray_cast(tile, grid_dimension=80.0):
    width = 0.0

    bpy.ops.object.select_all(action=SELECT_ACTION)
    bpy.ops.object.join()
    objs = bpy.context.selected_objects
    bpy.ops.object.select_all(action=DESELECT_ACTION)

    for obj in objs:
        if obj.type != MESH_OBJECT_TYPE:
            obj.select_set(True)
            bpy.ops.object.delete()
        else:
            width = obj.dimensions.x

    # create the grid
    new_collection = bpy.data.collections.new(name="grids")
    assert (new_collection is not bpy.context.scene.collection)
    bpy.context.scene.collection.children.link(new_collection)

    grid = create_grid(tile, "grid", grid_dimension)
    coords = [v.co for v in grid.data.vertices]

    height_grid = create_grid(tile, "height_grid", grid_dimension)
    heigth_grid_coords = [v.co for v in height_grid.data.vertices]

    return coords, width, grid, grid_dimension, heigth_grid_coords, height_grid


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

        return dupe


def get_geoid_height(lat, lon):
    interpolator = pygeodesy.GeoidKarney(os.path.join(GEOIDS_DATASET_FOLDER, EGM2008_5_DATASET))
    single_position = LatLon(lat, lon)
    h = interpolator(single_position)
    return h


def point_cloud(ob_name, coords, edges=[], faces=[]):
    """Create point cloud object based on given coordinates and name.

    Keyword arguments:
    ob_name -- new object name
    coords -- float triplets eg: [(-1.0, 1.0, 0.0), (-1.0, -1.0, 0.0)]
    """

    # Create new mesh and a new object
    me = bpy.data.meshes.new(ob_name + "Mesh")
    ob = bpy.data.objects.new(ob_name, me)

    # Make a mesh from a list of vertices/edges/faces
    me.from_pydata(coords, edges, faces)

    # Display name and update the mesh
    ob.show_name = True
    me.update()
    return ob


def apply_transform(ob, use_location=False, use_rotation=False, use_scale=False):
    mb = ob.matrix_basis
    I = mathutils.Matrix()
    loc, rot, scale = mb.decompose()

    # rotation
    T = mathutils.Matrix.Translation(loc)
    R = mb.to_3x3().normalized().to_4x4()
    S = mathutils.Matrix.Diagonal(scale).to_4x4()

    transform = [I, I, I]
    basis = [T, R, S]

    def swap(i):
        transform[i], basis[i] = basis[i], transform[i]

    if use_location:
        swap(0)
    if use_rotation:
        swap(1)
    if use_scale:
        swap(2)

    M = transform[0] @ transform[1] @ transform[2]
    if hasattr(ob.data, "transform"):
        ob.data.transform(M)
    for c in ob.children:
        c.matrix_local = M @ c.matrix_local

    ob.matrix_basis = basis[0] @ basis[1] @ basis[2]


def calculate_height_map_from_coords_from_bottom(tile, grid_dimension, coords, depsgraph, lat, lon, altitude, height_adjustment):
    results = defaultdict(dict)
    geoid_height = get_geoid_height(lat, lon)

    # downsample the grid for bottom ray casting
    coords = [co for i, co in enumerate(coords)]

    for co in coords:
        p = co
        ray_direction = [0, 0, 1]
        result = tile.evaluated_get(depsgraph).ray_cast(p, ray_direction, distance=1000)
        if result[0]:
            x = result[1][0]
            y = result[1][1]
            h = result[1][2]
            if len(results[y]) <= (grid_dimension-1):
                h = h + altitude + geoid_height
                # h = h if h >= geoid_height - GEOID_HEIGHT_ORIGIN_MARGIN else geoid_height - height_adjustment
                results[y][x] = h + height_adjustment

    return results


def calculate_height_map_from_coords_from_top(tile, grid_dimension, coords, depsgraph, lat, lon, altitude, hmatrix_base=None):
    results = defaultdict(dict)
    geoid_height = get_geoid_height(lat, lon)
    new_coords = []

    for co in coords:
        p = mathutils.Vector((co[0], co[1], 500))
        ray_direction_inverted = [0, 0, -1]
        result = tile.evaluated_get(depsgraph).ray_cast(p, ray_direction_inverted, distance=1000)
        if result[0]:
            new_coords.append(result[1])
        else:
            new_coords.append(mathutils.Vector((p[0], p[1], result[1][2])))

    if new_coords:
        # fix noise in the height map data
        new_coords = spatial_median_kdtree(np.array(new_coords), 35)
        # new_coords = spatial_median(np.array(new_coords), 20)

        # downscale the new cords retrieved from top ray casting
        new_coords = [co for i, co in enumerate(new_coords)]

        for i, co in enumerate(new_coords):
            p1 = co
            x = p1[0]
            y = p1[1]
            h = p1[2]
            if len(results[y]) < (grid_dimension-1):
                h = h + altitude + geoid_height
                h = h if h >= geoid_height else geoid_height

                if hmatrix_base is not None:
                    if y in hmatrix_base:
                        if x in hmatrix_base[y]:
                            base_h = hmatrix_base[y][x]
                            h = h + 1.0 if h >= base_h else base_h
                            results[y][x] = h

    return results


def fix_bridge_height_data_on_water(tile, depsgraph, lat, lon, altitude, hmatrix_base=None):
    return adjust_height_data_on_exclusion_area(tile, depsgraph, lat, lon, altitude, EXCLUSION_TYPE.WATER, hmatrix_base)


def adjust_height_data_on_ground_exclusion(tile, depsgraph, lat, lon, altitude, hmatrix_base=None):
    return adjust_height_data_on_exclusion_area(tile, depsgraph, lat, lon, altitude, EXCLUSION_TYPE.GROUND, hmatrix_base)


def adjust_height_data_on_exclusion_area(tile, depsgraph, lat, lon, altitude, exclusion_type, hmatrix_base=None):
    results = hmatrix_base.copy()
    geoid_height = get_geoid_height(lat, lon)
    new_coords = []

    if results is not None:
        for y in results:
            for x in results[y]:
                p1 = mathutils.Vector((x, y, 0))
                p2 = mathutils.Vector((x, y, 500))

                if exclusion_type == EXCLUSION_TYPE.WATER:
                    ray_direction = (0, 0, 1)
                    result = tile.evaluated_get(depsgraph).ray_cast(p1, ray_direction, distance=1000)
                else:
                    ray_direction = (0, 0, -1)
                    result = tile.evaluated_get(depsgraph).ray_cast(p2, ray_direction, distance=1000)

                if result[0]:
                    new_coords.append(result[1])

    if new_coords:
        if exclusion_type == EXCLUSION_TYPE.WATER:
            # fix noise in the height map data
            new_coords = spatial_median_kdtree(np.array(new_coords), 100)
        else:
            new_coords = spatial_median(np.array(new_coords), 20)

    for i, co in enumerate(new_coords):
        p1 = co
        x = p1[0]
        y = p1[1]
        h = p1[2]
        h = h + altitude + geoid_height
        if exclusion_type == EXCLUSION_TYPE.WATER:
            h = h if h >= geoid_height else geoid_height
        else:
            h = h + 1.0 if h >= geoid_height else geoid_height

        if hmatrix_base is not None:
            if y in hmatrix_base:
                if x in hmatrix_base[y]:
                    results[y][x] = h

    return results


# based on Adam Steer's code: https://stackoverflow.com/questions/34972383/improving-a-method-for-a-spatially-aware-median-filter-for-point-clouds-in-pytho
# not really fast, but it an accurate method, and it is fast enough for the number of points treated here
def spatial_median(pointcloud, radius):
    new_p = []

    for i, point in enumerate(pointcloud):
        # pick a point and make it a shapely Point
        point = geometry.Point(pointcloud[i, :])

        # select a patch around the point and make it a shapely
        # MultiPoint
        patch = geometry.MultiPoint(list(pointcloud[
                       (pointcloud[:, 0] > point.x - radius+0.5) &
                       (pointcloud[:, 0] < point.x + radius+0.5) &
                       (pointcloud[:, 1] > point.y - radius+0.5) &
                       (pointcloud[:, 1] < point.y + radius+0.5)
                       ]))

        # buffer the Point by radius
        pbuff = point.buffer(radius)

        # use the intersection method to find points in our
        # patch that lie inside the Point buffer
        isect = pbuff.intersection(patch)

        # initialise another list
        plist = []

        # f or every intersection set,
        # unpack it into a list and collect the median Z value
        if isect.geom_type == 'MultiPoint':
            # isolated_print('point has neighbours')
            for p in isect:
                plist.append(p.z)

            new_p.append((point.x, point.y, np.median(plist)))
        else:
            # if the intersection set isn't MultiPoint,
            # it is an isolated point, whose median Z value
            # is it's own.
            # isolated_print('isolated point')

            # append it to the big list)
            new_p.append((point.x, point.y, isect.z))

    # return a list of new median filtered Z coordinates
    return new_p


# less accurate, but faster method
def spatial_median_kdtree(pointcloud, radius):
    new_p = []
    tree = cKDTree(pointcloud, leafsize=60)

    results = tree.query_ball_point(pointcloud, r=radius)
    for idx, result in enumerate(results):
        if len(result) > 0:
            new_p.append((pointcloud[idx, 0], pointcloud[idx, 1], np.median(pointcloud[result, 2])))

    return new_p


def retrieve_tile_object_lod(obj):
    res = 99

    if OBJECT_NAME_SEP in obj.name:
        res = len(obj.name.split(OBJECT_NAME_SEP, 1)[0])

    return res


def object_touches_mask(obj, mask):
    bounding_box_obj = create_bounding_box(obj, BOUNDING_BOX_OSM_KEY)

    if not add_boolean_modifier(bounding_box_obj, mask, BOOLEAN_MODIFIER_OPERATION.INTERSECT):
        return False

    for modifier in bounding_box_obj.modifiers:
        bpy.ops.object.modifier_apply(modifier=modifier.name)

    intersections = [vertex.co for vertex in bounding_box_obj.data.vertices]
    bounding_box_obj.select_set(True)
    bpy.ops.object.delete()

    return intersections


def add_subsurface_modifier(obj):
    subsurfacy = obj.modifiers.new(name="subsurfacy", type="SUBSURF")

    if not subsurfacy:
        return False

    subsurfacy.subdivision_type = "SIMPLE"
    subsurfacy.levels = 2
    subsurfacy.render_levels = 2
    subsurfacy.use_limit_surface = True

    return True


def add_boolean_modifier(obj, mask, operation):
    booly = obj.modifiers.new(name="booly", type="BOOLEAN")

    if not booly:
        return False

    booly.object = mask
    booly.operation = operation
    booly.solver = "EXACT"
    booly.use_hole_tolerant = True

    return True


def add_weighted_normal_modifier(obj):
    weighty = obj.modifiers.new(name="weighty", type="WEIGHTED_NORMAL")

    if not weighty:
        return False

    weighty.weight = 100
    weighty.thresh = 5.0
    weighty.keep_sharp = True
    weighty.use_face_influence = True

    return True


def flat_cutted_faces(obj):
    me = obj.data

    polygons = me.polygons
    for polygon in polygons:
        polygon.use_smooth = False

    me.update()


def cleanup_cutted_faces(updated_objects):
    mat_osm = bpy.data.materials[OSM_MATERIAL_NAME]

    for obj in updated_objects:
        if obj.type == MESH_OBJECT_TYPE:
            me = obj.data

            osm_slots = [id for id, mat in enumerate(me.materials) if mat == mat_osm]

            faces_mat_osm = []
            bm = bmesh.new()
            bm.from_mesh(me)

            for face in bm.faces:
                if face.material_index in osm_slots:
                    faces_mat_osm.append(face)

            # delete faces with mat_osm
            bmesh.ops.delete(bm, geom=faces_mat_osm, context=FACES_DELETE_CONTEXT)
            bm.to_mesh(me)
            me.update()
            bm.free()
            del bm
        else:
            obj.select_set(False)


def find_center(obj):
    x, y, z = [sum([v.co[i] for v in obj.data.vertices]) for i in range(3)]
    count = float(len(obj.data.vertices))
    return obj.matrix_world @ (mathutils.Vector((x, y, z)) / count)


def split_obj(obj):
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    center = find_center(obj)

    bpy.ops.object.duplicate(linked=False)
    right = bpy.context.active_object

    obj.select_set(False)
    right.select_set(True)
    bpy.context.view_layer.objects.active = right

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bisect(plane_co=center, plane_no=(1, 0, 0), use_fill=True, clear_inner=True)
    bpy.ops.object.editmode_toggle()

    right.select_set(False)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj # set obj as active

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bisect(plane_co=center, plane_no=(1, 0, 0), use_fill=True, clear_outer=True)
    bpy.ops.object.editmode_toggle()


def face(rows, column, row):
    return column * rows + row, column * rows + row + 1, (column + 1) * rows + row + 1, (column + 1) * rows + row


def create_bounding_box(obj, prefix):
    scale = obj.scale

    minx = obj.bound_box[0][0] * scale.x
    maxx = obj.bound_box[4][0] * scale.x
    miny = obj.bound_box[0][1] * scale.y
    maxy = obj.bound_box[2][1] * scale.y
    minz = obj.bound_box[0][2] * scale.z
    maxz = obj.bound_box[1][2] * scale.z
    dx = maxx - minx
    dy = maxy - miny
    dz = maxz - minz

    new_name = '{0}{1}'.format(prefix, obj.name)

    loc = mathutils.Vector(((minx + 0.5 * dx), (miny + 0.5 * dy), (minz + 0.5 * dz)))
    loc.rotate(obj.rotation_euler)
    loc = loc + obj.location

    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=obj.rotation_euler)
    new_obj = bpy.context.object

    new_obj.name = new_name
    new_obj.dimensions = mathutils.Vector((dx, dy, dz))

    return new_obj


def create_grid(obj, name, grid_dimension):
    bpy.ops.mesh.primitive_plane_add(location=[0.0, 0.0, 0.0], rotation=obj.rotation_euler, scale=obj.scale)
    new_obj = bpy.context.object

    minx = obj.bound_box[0][0]
    maxx = obj.bound_box[4][0]
    miny = obj.bound_box[0][1]
    maxy = obj.bound_box[2][1]
    dx = maxx - minx
    dy = maxy - miny

    new_obj.name = name
    new_obj.dimensions = mathutils.Vector((dx, dy, 0))

    bpy.ops.object.select_all(action=DESELECT_ACTION)

    grid = bpy.context.scene.objects.get(name)
    grid.select_set(True)

    bpy.ops.object.select_all(action=SELECT_ACTION)
    bpy.context.view_layer.objects.active = obj

    bpy.ops.object.align(bb_quality=True, align_mode='OPT_3', relative_to='OPT_4', align_axis={'X', 'Y'})
    apply_transform(grid, use_location=True, use_rotation=True, use_scale=True)
    bpy.ops.object.align(bb_quality=True, align_mode='OPT_1', relative_to='OPT_4', align_axis={'Z'})
    apply_transform(grid, use_location=True, use_rotation=False, use_scale=False)

    me = new_obj.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges, use_grid_fill=True, cuts=int(grid_dimension))
    bmesh.ops.delete(bm, geom=bm.faces, context=FACES_ONLY_DELETE_CONTEXT)
    bm.to_mesh(me)
    me.update()
    bm.free()

    return new_obj


def delete_origin_points(obj):
    bpy.ops.object.select_all(action=DESELECT_ACTION)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    obj = bpy.context.active_object
    me = obj.data

    bm = bmesh.new()
    bm.from_mesh(me)

    vertices = [v for v in bm.verts if (v.co[0] == 0.0 and v.co[1] == 0.0 and v.co[2] == 0.0)]
    bmesh.ops.delete(bm, geom=vertices, context=VERTICES_DELETE_CONTEXT)

    bm.to_mesh(me)
    me.update()
    bm.free()
