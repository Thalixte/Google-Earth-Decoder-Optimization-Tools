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

import bpy


def remove_mesh_from_memory(passed_name):
    print("removeMeshFromMemory:[%s]." % passed_name)
    # Extra test because this can crash Blender if not done correctly.
    mesh = bpy.data.meshes.get(passed_name)
    if mesh is not None:
        if mesh.users == 0:
            try:
                mesh.user_clear()
                can_continue = True
            except:
                can_continue = False

            if can_continue:
                try:
                    bpy.data.meshes.remove(mesh)
                    print("removeMeshFromMemory: MESH [", passed_name, "] removed from memory.")
                    return True
                except:
                    print("removeMeshFromMemory: FAILED to remove [", passed_name, "] from memory.")
                    return False
            else:
                # Unable to clear users, something is holding a reference to it.
                # Can't risk removing. Favor leaving it in memory instead of risking a crash.
                print("removeMeshFromMemory: Unable to clear users for MESH, something is holding a reference to it.")
                return False
        else:
            print("removeMeshFromMemory: Unable to remove MESH because it still has [", str(mesh.users), "] users.")
            return False
    else:
        # We could not fetch it, it does not exist in memory, essentially removed.
        print("We could not fetch MESH [%s], it does not exist in memory, essentially removed." % passed_name)
        return False
