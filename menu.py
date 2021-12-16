# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>
import os
import argparse
import site
import sys
import bpy

from bpy.types import Header, Menu, Panel

CONSTANTS_FOLDER = "constants"
UTILS_FOLDER = "utils"
SCRIPT_FOLDER = "scripts"

# Check if script is executed in Blender and get absolute path of current folder
if bpy.context.space_data is not None:
    files_dir = os.path.dirname(bpy.context.space_data.text.filepath)
else:
    files_dir = os.path.dirname(os.path.abspath(__file__))

# Get scripts folder and add it to the search path for modules
os.chdir(files_dir)

sys.path.append(site.USER_SITE)

if files_dir not in sys.path:
    sys.path.append(files_dir)

# Get scripts folder and add it to the search path for modules
cwd = os.path.join(files_dir, CONSTANTS_FOLDER)
if cwd not in sys.path:
    sys.path.append(cwd)

# Get scripts folder and add it to the search path for modules
cwd = os.path.join(files_dir, UTILS_FOLDER)
if cwd not in sys.path:
    sys.path.append(cwd)

# Get scripts folder and add it to the search path for modules
cwd = os.path.join(files_dir, SCRIPT_FOLDER)
if cwd not in sys.path:
    sys.path.append(cwd)

from utils import *
from blender import clean_scene
from msfs_project import MsfsLod


settings = Settings(get_sources_path())


class TOPBAR_MT_google_earth_optimization_menus(Menu):
    os.system("cls")
    bl_idname = "TOPBAR_MT_google_earth_optimization_menus"
    bl_label = ""

    def draw(self, _context):
        layout = self.layout
        layout.menu("TOPBAR_MT_google_earth_optimization_menu")


class TOPBAR_MT_google_earth_optimization_menu(Menu):
    bl_label = "Google Earth Optimization Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator("screen.init_msfs_scenery_project_operator")


class InitMsfsSceneryProjectOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "screen.init_msfs_scenery_project_operator"
    bl_label = "Init a new MSFS scenery project"

    @classmethod
    def poll(cls, context):
        return not os.path.isdir(os.path.join(settings.projects_path, settings.project_name))

    def execute(self, context):
        script_file = "init_msfs_scenery_project_script.py"
        text = bpy.data.texts.load(os.path.join(cwd, script_file))   # if exists in blend
        ctx = bpy.context.copy()
        ctx[script_file] = text
        lib1 = bpy.data.texts[script_file].as_string()
        exec(text)
        return {'FINISHED'}


classes = (
    TOPBAR_MT_google_earth_optimization_menus,
    TOPBAR_MT_google_earth_optimization_menu,
    InitMsfsSceneryProjectOperator
)


def reload_topbar_menu():
    if hasattr(bpy.types.TOPBAR_MT_editor_menus.draw, "_draw_funcs"):
        for f in bpy.types.TOPBAR_MT_editor_menus.draw._draw_funcs:
            if not repr(f).startswith("<function TOPBAR_MT_editor_menus.draw"):
                bpy.types.TOPBAR_MT_editor_menus.draw._draw_funcs.remove(f)


def register():
    reload_topbar_menu()

    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_google_earth_optimization_menus.draw)


def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_google_earth_optimization_menus.draw)
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
