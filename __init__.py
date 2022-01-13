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

bl_info = {
    'name': 'Google Earth Decoder Optimization Tools Addon',
    'blender': (2, 83, 0),
    'category': 'Scene',
    'version': (1, 0, 0),
    'author': 'Thalixte',
    'description': 'Bundle of tools to optimize MSFS scenery projects that uses tiles retrieved from the Google Earth Decoder Tool',
}

import os
import sys

import site

import bpy

UI_FOLDER = "UI"

# Check if script is executed in Blender and get absolute path of current folder
files_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(site.USER_SITE)

if files_dir not in sys.path:
    sys.path.append(files_dir)

# Get scripts folder and add it to the search path for modules
cwd = os.path.join(files_dir, UI_FOLDER)
if cwd not in sys.path:
    sys.path.append(cwd)

from .UI import menu


def register():
    menu.register()


def unregister():
    menu.unregister()


if __name__ == "__main__":
    register()
