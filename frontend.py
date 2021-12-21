# import the bpy module to access blender API
import sys

import os
import site

import bpy

UI_FOLDER = "UI"
UTILS_FOLDER = "UTILS"
SCRIPTS_FOLDER = "SCRIPTS"

# Check if script is executed in Blender and get absolute path of current folder
if bpy.context.space_data is not None:
    files_dir = os.path.dirname(bpy.context.space_data.text.filepath)
else:
    files_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(site.USER_SITE)

if files_dir not in sys.path:
    sys.path.append(files_dir)

# Get scripts folder and add it to the search path for modules
cwd = os.path.join(files_dir, UI_FOLDER)
if cwd not in sys.path:
    sys.path.append(cwd)

# Get scripts folder and add it to the search path for modules
cwd = os.path.join(files_dir, UTILS_FOLDER)
if cwd not in sys.path:
    sys.path.append(cwd)

# Get scripts folder and add it to the search path for modules
cwd = os.path.join(files_dir, SCRIPTS_FOLDER)
if cwd not in sys.path:
    sys.path.append(cwd)

# Check if script is executed in Blender and get absolute path of current folder
from utils import Settings, exec_script_from_menu

if bpy.context.space_data is not None:
    sources_path = os.path.dirname(bpy.context.space_data.text.filepath)
else:
    sources_path = os.path.dirname(os.path.abspath(__file__))

settings = Settings(sources_path)


def project_name_updated(self, context):
    settings.project_name = context.scene.custom_props.project_name


class CustomPropertyGroup(bpy.types.PropertyGroup):
    # float_slider: bpy.props.FloatProperty(name='float value', soft_min=0, soft_max=10)
    # int_slider: bpy.props.IntProperty(name='int value', soft_min=0, soft_max=10)
    # bool_toggle: bpy.props.BoolProperty(name='bool toggle')
    project_name: bpy.props.StringProperty(
        name="Project name",
        description="name of the project to initialize",
        default=settings.project_name,
        maxlen=256,
        update=project_name_updated
    )


# create a panel (class) by deriving from the bpy Panel, this be the UI
class VIEW_3D_PT_CustomToolShelf(bpy.types.Panel):
    # variable for determining which view this panel will be in
    bl_space_type = 'VIEW_3D'
    # this variable tells us where in that view it will be drawn
    bl_region_type = 'UI'
    # this variable is a label/name that is displayed to the user
    bl_label = 'Custom Tool Shelf'
    # this context variable tells when it will be displayed, edit mode, object mode etc
    bl_context = 'objectmode'
    # category is esentially the main UI element, the panels inside it are
    # collapsible dropdown menus drawn under a category
    # you can add your own name, or an existing one and it will be drawn accordingly
    bl_category = 'View'

    # now we define a draw method, in it we can tell what elements we want to draw
    # in this new space we created, buttons, toggles etc.
    def draw(self, context):
        # shorten the self.layout to just layout for convenience
        layout = self.layout
        layout.operator('text.init_msfs_scenery_project_operator', text='Initialize the MSFS scenery project')
        # add multiple items on the same line, like a column layout, from left to right
        subrow = layout.row(align=True)
        # the property will be drawn next to it on the right, as an adjustible slider thing
        # subrow.prop(context.scene.custom_props, 'float_slider')
        # add a label to the UI
        layout.label(text="v Testing layout, does nothing bellow this v")
        # add a new row with multiple elements in a column
        subrow = layout.row(align=True)
        # add a toggle
        # subrow.prop(context.scene.custom_props, 'bool_toggle')
        # add an int slider
        # subrow.prop(context.scene.custom_props, 'int_slider')
        # add a custom text field in the usual layout
        layout.prop(context.scene.custom_props, 'project_name')
        # NOTE: for more layout things see the types.UILayout in the documentation


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


bl_info = {
    "name": "Ui test addon",
    "category": "tests"
}

classes = (
    CustomPropertyGroup,
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


def unregister():
    del bpy.types.Scene.custom_props
    for cls in classes:
        bpy.utils.unregister_class(cls)


# a quick line to autorun the script from the text editor when we hit 'run script'
if __name__ == '__main__':
    register()
