import bpy
from bpy.props import StringProperty, IntProperty, EnumProperty
from .panel import *


def retrieve_section_items(self, context):
    items = []
    displayed_sections = eval(self.current_operator_class_name + ".displayed_sections")
    for item in bpy.types.Scene.settings.sections:
        if item[0] in displayed_sections:
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
