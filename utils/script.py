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

TEXT_EDITOR_AREA = "TEXT_EDITOR"


def exec_script_from_menu(script_path):
    text = bpy.data.texts.load(script_path)

    for area in bpy.context.screen.areas:
        if area.type == TEXT_EDITOR_AREA:
            area.spaces.active.text = text

            ctx = bpy.context.copy()
            ctx['edit_text'] = text
            ctx['area'] = area
            bpy.ops.text.run_script(ctx)
            bpy.ops.text.unlink(ctx)
            break
