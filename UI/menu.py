# import the bpy module to access blender API
import os

import bpy
from bpy.props import IntProperty, BoolProperty
from bpy.types import Menu
from bpy_extras.io_utils import ImportHelper
from bpy_types import Operator
from constants import CLEAR_CONSOLE_CMD
from utils import exec_script_from_menu, Settings, get_sources_path, isolated_print

settings = Settings(get_sources_path())
settings.save()


def reload_topbar_menu():
    if hasattr(bpy.types.TOPBAR_MT_editor_menus.draw, "_draw_funcs"):
        for f in bpy.types.TOPBAR_MT_editor_menus.draw._draw_funcs:
            if not repr(f).startswith("<function TOPBAR_MT_editor_menus.draw"):
                bpy.types.TOPBAR_MT_editor_menus.draw._draw_funcs.remove(f)


def projects_path_updated(self, context):
    settings.projects_path = context.scene.custom_props.projects_path
    settings.save()
    panel_props = context.scene.panel_props
    context.window.cursor_warp(panel_props.first_mouse_x, panel_props.first_mouse_y)
    bpy.ops.wm.init_msfs_scenery_project('INVOKE_DEFAULT')


def project_name_updated(self, context):
    settings.project_name = context.scene.custom_props.project_name
    settings.save()


class TOPBAR_MT_google_earth_optimization_menus(Menu):
    os.system(CLEAR_CONSOLE_CMD)
    bl_idname = "TOPBAR_MT_google_earth_optimization_menus"
    bl_label = ""

    def draw(self, _context):
        layout = self.layout
        layout.menu("TOPBAR_MT_google_earth_optimization_menu")


class TOPBAR_MT_google_earth_optimization_menu(Menu):
    bl_label = "Google Earth Optimization Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.init_msfs_scenery_project")


class CustomPropertyGroup(bpy.types.PropertyGroup):
    # float_slider: bpy.props.FloatProperty(name='float value', soft_min=0, soft_max=10)
    # int_slider: bpy.props.IntProperty(name='int value', soft_min=0, soft_max=10)
    # bool_toggle: bpy.props.BoolProperty(name='bool toggle')
    projects_path: bpy.props.StringProperty(
        subtype="DIR_PATH",
        name="Path of the projects",
        description="Select the path containing all your MSFS scenery projects",
        maxlen=1024,
        default=settings.projects_path,
        update=projects_path_updated
    )
    project_name: bpy.props.StringProperty(
        name="Project name",
        description="name of the project to initialize",
        default=settings.project_name,
        maxlen=256,
        update=project_name_updated
    )


class PanelPropertyGroup(bpy.types.PropertyGroup):
    first_mouse_x: IntProperty(default=0)
    first_mouse_y: IntProperty(default=0)


class VIEW_3D_PT_CustomToolShelf(Operator):
    bl_idname = 'wm.init_msfs_scenery_project'
    bl_label = 'Initialize a new MSFS project scenery'
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        layout = self.layout
        subrow = layout.row(align=True)
        layout.prop(context.scene.custom_props, 'projects_path')
        layout.separator()
        layout.prop(context.scene.custom_props, 'project_name')

    def invoke(self, context, event):
        panel_props = context.scene.panel_props
        if panel_props.first_mouse_x == 0 and panel_props.first_mouse_y == 0:
            panel_props.first_mouse_x = event.mouse_x
            panel_props.first_mouse_y = event.mouse_y
        # context.window.cursor_warp(context.window.width / 2, (context.window.height / 2) + 60)
        context.window_manager.invoke_props_dialog(self, width=600)
        return {'RUNNING_MODAL'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        script_file = "init_msfs_scenery_project.py"
        exec_script_from_menu(os.path.join(settings.sources_path, script_file))
        return {'FINISHED'}


class ProjectsPathOperator(Operator, ImportHelper):
    bl_idname = "scene.project_path_operator"
    bl_label = "Select folder..."
    bl_options = {'PRESET', 'UNDO'}

    directory: bpy.props.StringProperty(
        subtype="DIR_PATH",
        name="Path of the projects",
        description="Select the path containing all your MSFS scenery projects",
        maxlen=1024,
        default=settings.projects_path,
        update=projects_path_updated,
    )

    filter_folder: bpy.props.BoolProperty(default=True, options={'HIDDEN'})

    def execute(self, context):
        pass


class InitMsfsSceneryProjectOperator(Operator):
    bl_idname = 'text.init_msfs_scenery_project'
    bl_label = 'Initialize a new MSFS project scenery...'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        script_file = "init_msfs_scenery_project.py"
        exec_script_from_menu(os.path.join(settings.sources_path, script_file))
        return {'FINISHED'}

bl_info = {
    "name": "Ui test addon",
    "category": "tests"
}

classes = (
    TOPBAR_MT_google_earth_optimization_menus,
    TOPBAR_MT_google_earth_optimization_menu,
    CustomPropertyGroup,
    PanelPropertyGroup,
    InitMsfsSceneryProjectOperator,
    VIEW_3D_PT_CustomToolShelf,
)


def register():
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            pass

    bpy.types.Scene.custom_props = bpy.props.PointerProperty(type=CustomPropertyGroup)
    bpy.types.Scene.panel_props = bpy.props.PointerProperty(type=PanelPropertyGroup)
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_google_earth_optimization_menus.draw)


def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_google_earth_optimization_menus.draw)

    del bpy.types.Scene.custom_props
    del bpy.types.Scene.panel_props
    for cls in classes:
        bpy.utils.unregister_class(cls)


# a quick line to autorun the script from the text editor when we hit 'run script'
if __name__ == '__main__':
    register()