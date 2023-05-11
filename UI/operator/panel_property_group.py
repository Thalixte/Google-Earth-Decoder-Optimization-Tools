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
from bpy.props import StringProperty, IntProperty, EnumProperty
from .panel import *


def retrieve_section_items(self, context):
    items = []
    displayed_sections = eval(self.current_operator_class_name + ".displayed_sections")
    for item in bpy.types.Scene.global_settings.sections:
        if item[0] in displayed_sections:
            items.append((item[0], item[1], item[2]))
    if bpy.types.Scene.project_settings is not None:
        for item in bpy.types.Scene.project_settings.sections:
            if item[0] in displayed_sections and item not in items:
                items.append((item[0], item[1], item[2]))
    return items


class PanelPropertyGroup(bpy.types.PropertyGroup):
    def setting_sections_updated(self, context):
        self.current_section = self.setting_sections

    current_operator_class_name: StringProperty(
        default=str()
    )
    current_operator: StringProperty(
        default=str()
    )
    current_section: StringProperty(
        default=str()
    )
    invocation_type: StringProperty(
        default=str()
    )
    first_mouse_x: IntProperty(
        default=-1
    )
    first_mouse_y: IntProperty(
        default=-1
    )
    setting_sections: EnumProperty(
        items=retrieve_section_items,
        update=setting_sections_updated,
    )
