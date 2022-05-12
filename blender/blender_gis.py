import bpy


##################################################################
# Import the gltf files located in a specific folder
##################################################################
def import_osm_file(osm_file):
    try:
        print("import ", osm_file)
        bpy.ops.importgis.osm_file(filepath=str(osm_file))
    except:
        pass
