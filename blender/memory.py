import bpy


def remove_mesh_from_memory(passedName):
    print("removeMeshFromMemory:[%s]." % passedName)
    # Extra test because this can crash Blender if not done correctly.
    result = False
    mesh = bpy.data.meshes.get(passedName)
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
                    # print("removeMeshFromMemory: MESH [", passedName, "] removed from memory.")
                    return True
                except:
                    # print("removeMeshFromMemory: FAILED to remove [", passedName, "] from memory.")
                    return False
            else:
                # Unable to clear users, something is holding a reference to it.
                # Can't risk removing. Favor leaving it in memory instead of risking a crash.
                # print("removeMeshFromMemory: Unable to clear users for MESH, something is holding a reference to it.")
                return False
        else:
            # print("removeMeshFromMemory: Unable to remove MESH because it still has [", str(mesh.users), "] users.")
            return False
    else:
        # We could not fetch it, it does not exist in memory, essentially removed.
        # print("We could not fetch MESH [%s], it does not exist in memory, essentially removed." % passedName)
        return False
