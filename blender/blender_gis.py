import bpy


##################################################################
# Import the gltf files located in a specific folder
##################################################################
from blender.material import set_new_msfs_material

OSM_MATERIAL_NAME = "OSM_material"

def import_osm_file(osm_file):

    try:
        print("import ", osm_file)
        bpy.ops.importgis.osm_file(filepath=str(osm_file))
        set_new_msfs_material(OSM_MATERIAL_NAME)

    except:
        pass
