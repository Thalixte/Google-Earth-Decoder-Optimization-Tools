import os

import bpy
from bpy.props import StringProperty, BoolProperty, FloatProperty, EnumProperty
from bpy.types import Menu
from bpy_extras.io_utils import ImportHelper
from bpy_types import Operator
from constants import CLEAR_CONSOLE_CMD
from utils import exec_script_from_menu, Settings

# Check if script is executed in Blender and get absolute path of current folder
if bpy.context.space_data is not None:
    sources_path = os.path.dirname(bpy.context.space_data.text.filepath)
else:
    sources_path = os.path.dirname(os.path.abspath(__file__))

settings = Settings(sources_path)


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

        layout.separator()

        layout.operator("text.optimize_scenery_operator")

        layout.separator()

        layout.operator("wm.simple_operator")


class InitMsfsSceneryProjectOperator(bpy.types.Operator):
    """Tooltip"""
    bl_space_type = 'TEXT_EDITOR'
    bl_idname = "text.init_msfs_scenery_project_operator"
    bl_label = "Init a new MSFS scenery project"

    @classmethod
    def poll(cls, context):
        return not os.path.isdir(os.path.join(settings.projects_path, settings.project_name))

    def execute(self, context):
        script_file = "init_msfs_scenery_project.py"
        exec_script_from_menu(os.path.join(settings.sources_path, script_file))
        return {'FINISHED'}


class OptimizeSceneryOperator(bpy.types.Operator):
    """Tooltip"""
    bl_space_type = 'TEXT_EDITOR'
    bl_idname = "text.optimize_scenery_operator"
    bl_label = "Optimize a MSFS scenery"

    @classmethod
    def poll(cls, context):
        return os.path.isdir(os.path.join(settings.projects_path, settings.project_name))

    def execute(self, context):
        script_file = "optimize_scenery.py"
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
        default=settings.projects_path
    )

    filter_folder: bpy.props.BoolProperty(default=True, options={'HIDDEN'})

    def execute(self, context):
        settings.projects_path = self.directory
        return {'FINISHED'}


class ProjectNameOperator(Operator):
    bl_idname = "scene.project_name_operator"
    bl_label = "Project name"

    project_name: bpy.props.StringProperty(
        name="Name of the project",
        description="Give the name of the project to initialize",
        maxlen=256,
        default=settings.project_name
    )

    def execute(self, context):
        settings.projects_name = self.project_name
        return {'FINISHED'}


class InitMsfsSceneryProjectPanel(bpy.types.Operator):
    bl_idname = 'wm.init_msfs_scenery_project'
    bl_label = 'Initialize a new MSFS project scenery'
    bl_options = {'REGISTER', 'UNDO'}

    prefix: bpy.props.StringProperty(name='Prefix', default='Pref')

    # author_name: bpy.props.StringProperty(
    #     name="Author of the project",
    #     description="Give the name for the author of the project",
    #     maxlen=256,
    #     default=settings.author_name
    # )

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=600)

    def draw(self, context):
        row = self.layout
        row.prop(self, "Prefix", text="Report Hello World")

    def execute(self, context): # test call
        script_file = "init_msfs_scenery_project.py"
        exec_script_from_menu(os.path.join(settings.sources_path, script_file))
        return {'FINISHED'}


def reload_topbar_menu():
    if hasattr(bpy.types.TOPBAR_MT_editor_menus.draw, "_draw_funcs"):
        for f in bpy.types.TOPBAR_MT_editor_menus.draw._draw_funcs:
            if not repr(f).startswith("<function TOPBAR_MT_editor_menus.draw"):
                bpy.types.TOPBAR_MT_editor_menus.draw._draw_funcs.remove(f)


class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "wm.simple_operator"
    bl_label = "Simple Object Operator"
    bl_options = {'REGISTER', 'UNDO'}

    prop: bpy.props.BoolProperty(name="test")

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_popup(self, event)
    
    def draw(self, context):
        self.layout.prop(self, "test")

    def execute(self, context):
        return {'FINISHED'}


class PUPA_OT_FitArmature(bpy.types.Operator):
    bl_idname = "view3d.fit_armature"
    bl_label = "Fit Armature"
    bl_options = {'REGISTER', 'UNDO'}

    options: EnumProperty(
        name="Options",
        default=0,
        items=[
            ('option_a', "Option A", "Active Button", 0),
            ('option_b', "Option B", "Show a Slider", 1)]
    )

    test_checkbox: BoolProperty(
        name="Test Checkbox ",
        description="Test Checkbox",
        default=False
    )

    slider: FloatProperty(
        name="Slider",
        description="Allow Change Some Size",
        default=0.1,
        min=0.01,
        max=2
    )

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "options")

        if self.options == "option_a":
            layout.prop(self, "test_checkbox")
        elif self.options == "option_b":
            layout.prop(self, "slider")

    def testM(self, context):
        print("test")

    def execute(self, context):
        self.testM(bpy.context)

        return {"FINISHED"}


classes = (
    TOPBAR_MT_google_earth_optimization_menus,
    TOPBAR_MT_google_earth_optimization_menu,
    InitMsfsSceneryProjectOperator,
    OptimizeSceneryOperator,
    ProjectsPathOperator,
    ProjectNameOperator,
    InitMsfsSceneryProjectPanel,
    SimpleOperator,
    PUPA_OT_FitArmature
)


def register():
    reload_topbar_menu()

    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            pass

    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_google_earth_optimization_menus.draw)


def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_google_earth_optimization_menus.draw)
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
