import bpy
from bpy import context
from bpy.props import StringProperty, IntProperty, EnumProperty


class PanelPropertyGroup(bpy.types.PropertyGroup):
    def setting_sections_updated(self, context):
        self.current_section = self.setting_sections

    current_operator: StringProperty(
        default=str()
    )
    current_section: StringProperty(
        default=str()
    )
    first_mouse_x: IntProperty(
        default=-1
    )
    first_mouse_y: IntProperty(
        default=-1
    )
    setting_sections: EnumProperty(
        items=context.scene.settings.sections,
        default="PROJECT",
        update=setting_sections_updated,
    )