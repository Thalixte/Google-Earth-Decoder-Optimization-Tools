SHADER_TEX_IMAGE_NODE_TYPE = "ShaderNodeTexImage"
TEX_IMAGE_NODE_TYPE = "TEX_IMAGE"
BSDF_NODE_TYPE = "BSDF_PRINCIPLED"
BASE_COLOR_INDEX = 0
BLANK_IMAGE_NAME = "blank"
BLANK_COLOR = (0.0, 0.0, 0.0, 1.0)
DUMMY_IMAGE_WIDTH = 256
DUMMY_IMAGE_HEIGHT = 256

######################################################
# Image management methods
######################################################
import bpy
from blender.material import get_material_output


def list_image_nodes(node, weight=0):
    if node.type == TEX_IMAGE_NODE_TYPE:
        return [(node, weight)]
    image_nodes = []
    for i, in_socket in enumerate(node.inputs):
        w = weight
        if node.type == BSDF_NODE_TYPE and i == BASE_COLOR_INDEX:
            w += 100
        for l in in_socket.links:
            image_nodes += list_image_nodes(l.from_node, weight=w - 1)

    return image_nodes


def get_image_node(obj):
    material = obj.material_slots[0].material
    material_output = get_material_output(material)
    image_nodes = list_image_nodes(material_output)
    image_nodes.sort(key=lambda x: -x[1])

    if len(image_nodes) <= 0:
        nodes = material.node_tree.nodes
        node_texture = nodes.new(type=SHADER_TEX_IMAGE_NODE_TYPE)
        node_texture.image = bpy.data.images.new(name=BLANK_IMAGE_NAME, width=DUMMY_IMAGE_WIDTH, height=DUMMY_IMAGE_HEIGHT, color=BLANK_COLOR, alpha=True)
        node_texture.location = 0, 0
        links = material.node_tree.links
        links.new(node_texture.outputs[0], nodes.get(BSDF_NODE_TYPE).inputs[0])
        print("texture added to ", obj)

    return image_nodes[0][0] if len(image_nodes) > 0 else None


##################################################################
# fix texture final size for package compilation
##################################################################
def fix_texture_size_for_package_compilation(packed_image):
    new_img_width = packed_image.size[0] + (4 - packed_image.size[0] % 4)
    new_img_height = packed_image.size[1] + (4 - packed_image.size[1] % 4)
    packed_image.scale(new_img_width, new_img_height)
