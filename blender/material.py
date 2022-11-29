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

######################################################
# Material management methods
######################################################
import bpy

OUTPUT_MATERIAL_NODE_TYPE = "OUTPUT_MATERIAL"
PRINCIPLED_BSDF_SHADER = "Principled BSDF"


def get_material_output(material):
    for node in material.node_tree.nodes:
        if node.type == OUTPUT_MATERIAL_NODE_TYPE:
            return node


def set_msfs_material():
    for obj in bpy.data.objects:
        material = obj.data.materials[0]
        nodes = material.node_tree.nodes
        principled = next(n for n in nodes if n.type == PRINCIPLED_BSDF_SHADER)


def set_new_msfs_material(material_name):
    mat = bpy.data.materials.new(name=material_name)

    if mat.node_tree is None:
        mat.use_nodes = True

    for obj in bpy.data.objects:
        # Assign it to object
        if obj.data.materials:
            # assign to 1st material slot
            obj.data.materials[0] = mat
        else:
            # no slots
            obj.data.materials.append(mat)

        material = obj.data.materials[0]
        material.name = material_name
        nodes = material.node_tree.nodes
        bsdf = nodes.get(PRINCIPLED_BSDF_SHADER)

        if not bsdf:  # make sure it exists to continue
            bsdf = nodes.new(type=PRINCIPLED_BSDF_SHADER)
            bsdf.location = 0, 0

        material.use_nodes = True


def add_new_obj_material(obj, material_name):
    mat = bpy.data.materials[material_name]

    # Assign it to object
    obj.data.materials.append(mat)


def remove_obj_material(obj, material_name):
    mat = bpy.data.materials[material_name]

    obj.data.materials.pop(material_name)


def remove_material(material_name):
    mat = bpy.data.materials[material_name]
    bpy.data.materials.remove(mat, do_unlink=True)
