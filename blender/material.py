######################################################
# Material management methods
######################################################
OUTPUT_MATERIAL_NODE_TYPE = "OUTPUT_MATERIAL"


def get_material_output(material):
    for node in material.node_tree.nodes:
        if node.type == OUTPUT_MATERIAL_NODE_TYPE:
            return node
