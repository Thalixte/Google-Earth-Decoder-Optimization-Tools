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
import os, bpy
from bpy.types import Header, Menu, Panel


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
        layout.operator("wm.splash")


classes = (
    TOPBAR_MT_google_earth_optimization_menus,
    TOPBAR_MT_google_earth_optimization_menu,
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
