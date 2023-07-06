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

import os
import tempfile

import addon_utils
import bpy
from utils.install_lib import download_file
from utils.script_errors import ScriptError

DEFAULT_TARGET = "DEFAULT"
FILTER_GLOB = "*.py;*.zip"

def is_blender_addon_installed(name):
    if bpy.context.preferences is None:
        return True

    return name in bpy.context.preferences.addons.keys()

def install_blender_addon(name, repo, archive, overwrite=False):
    tmp_file = os.path.join(tempfile.gettempdir(), archive)
    error_msg = name + " blender addon installation failed. Try to install it manually instead"

    if is_blender_addon_installed(name):
        return True

    try:
        download_file(repo + archive, tmp_file)
        bpy.ops.preferences.addon_install(overwrite=overwrite, target='DEFAULT', filepath=tmp_file, filter_folder=True, filter_python=False, filter_glob=FILTER_GLOB)
        bpy.ops.preferences.addon_enable(module=name)
        addon_utils.modules_refresh()
    except:
        raise ScriptError(error_msg)

    return True
