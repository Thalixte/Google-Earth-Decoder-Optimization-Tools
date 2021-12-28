# import the bpy module to access blender API
from time import sleep

import os

import bpy
from bpy import context
from bpy.props import IntProperty, StringProperty, EnumProperty
from bpy.types import Menu
from bpy_extras.io_utils import ImportHelper
from bpy_types import Operator
from constants import CLEAR_CONSOLE_CMD, PNG_TEXTURE_FORMAT, JPG_TEXTURE_FORMAT
from utils import exec_script_from_menu, Settings, get_sources_path

settings = Settings(get_sources_path())


def reload_topbar_menu():
    try:
        if hasattr(bpy.types.TOPBAR_MT_editor_menus.draw, "_draw_funcs"):
            for f in bpy.types.TOPBAR_MT_editor_menus.draw._draw_funcs:
                if not repr(f).startswith("<function TOPBAR_MT_editor_menus.draw"):
                    bpy.types.TOPBAR_MT_editor_menus.draw._draw_funcs.remove(f)
    except AttributeError:
        pass


def invoke_current_operator(refresh=False):
    import ctypes

    if refresh:
        VK_ESCAPE = 0x1B
        ctypes.windll.user32.keybd_event(VK_ESCAPE)
        sleep(0.2)

    eval("bpy.ops." + context.scene.panel_props.current_operator + "(\"INVOKE_DEFAULT\")")


def projects_path_updated(self, context):
    setting_props = context.scene.setting_props
    settings.projects_path_readonly = settings.projects_path = setting_props.projects_path
    panel_props = context.scene.panel_props
    context.window.cursor_warp(panel_props.first_mouse_x, panel_props.first_mouse_y)
    invoke_current_operator(refresh=False)


def project_path_updated(self, context):
    setting_props = context.scene.setting_props
    settings.projects_path = setting_props.projects_path = os.path.dirname(os.path.dirname(setting_props.project_path)) + os.path.sep
    settings.project_name = setting_props.project_name = os.path.relpath(setting_props.project_path, start=setting_props.projects_path)


def project_name_updated(self, context):
    setting_props = context.scene.setting_props
    settings.project_name = setting_props.project_name
    settings.project_path = os.path.join(settings.projects_path, settings.project_name)


def author_name_updated(self, context):
    settings.author_name = context.scene.setting_props.author_name


def bake_textures_enabled_updated(self, context):
    settings.bake_textures_enabled_updated = context.scene.setting_props.bake_textures_enabled_updated


def output_texture_format_updated(self, context):
    settings.output_texture_format = context.scene.setting_props.output_texture_format


def backup_enabled_updated(self, context):
    settings.backup_enabled = context.scene.setting_props.backup_enabled


def lat_correction_updated(self, context):
    settings.lat_correction = "{:.9f}".format(float(str(context.scene.setting_props.lat_correction))).rstrip("0").rstrip(".")


def lon_correction_updated(self, context):
    settings.lon_correction = "{:.9f}".format(float(str(context.scene.setting_props.lon_correction))).rstrip("0").rstrip(".")


def setting_sections_updated(self, context):
    panel_props = context.scene.panel_props
    panel_props.current_section = panel_props.setting_sections


class TOPBAR_MT_google_earth_optimization_menus(Menu):
    os.system(CLEAR_CONSOLE_CMD)
    bl_idname = "TOPBAR_MT_google_earth_optimization_menus"
    bl_label = ""

    def draw(self, _context):
        layout = self.layout
        layout.menu(TOPBAR_MT_google_earth_optimization_menu.bl_idname)


class TOPBAR_MT_google_earth_optimization_menu(Menu):
    bl_idname = "TOPBAR_MT_google_earth_optimization_menu"
    bl_label = "Google Earth Optimization Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator(OT_InitMsfsSceneryPanel.bl_idname)
        layout.separator()
        layout.operator(OT_OptimizeSceneryPanel.bl_idname)


class SettingsPropertyGroup(bpy.types.PropertyGroup):
    projects_path: bpy.props.StringProperty(
        subtype="DIR_PATH",
        name="Path of the projects",
        description="Select the path containing all your MSFS scenery projects",
        maxlen=1024,
        default=settings.projects_path,
        update=projects_path_updated
    )
    projects_path_readonly: bpy.props.StringProperty(
        name="Path of the projects",
        description="Select the path containing all your MSFS scenery projects",
        maxlen=1024,
        default=settings.projects_path
    )
    project_name: StringProperty(
        name="Project name",
        description="name of the project to initialize",
        default=settings.project_name,
        maxlen=256,
        update=project_name_updated
    )
    project_path: StringProperty(
        subtype="DIR_PATH",
        name="Path of the project",
        description="Select the path containing the MSFS scenery project",
        maxlen=1024,
        default=os.path.join(settings.projects_path, settings.project_name),
        update=project_path_updated
    )
    author_name: StringProperty(
        name="Author name",
        description="author of the msfs scenery project",
        default=settings.author_name,
        maxlen=256,
        update=author_name_updated
    )
    bake_textures_enabled: bpy.props.BoolProperty(
        name="Bake textures enabled",
        description="Reduce the number of texture files (Lily Texture Packer addon is necessary https://gumroad.com/l/DFExj)",
        default=settings.bake_textures_enabled,
        update=bake_textures_enabled_updated,
    )
    output_texture_format: EnumProperty(
        name="Output texture format",
        description="output format of the texture files (jpg or png) used by the photogrammetry tiles",
        items=[
                (PNG_TEXTURE_FORMAT, PNG_TEXTURE_FORMAT, str()),
                (JPG_TEXTURE_FORMAT, JPG_TEXTURE_FORMAT, str()),
        ],
        default=settings.output_texture_format,
        update=output_texture_format_updated,

    )
    backup_enabled: bpy.props.BoolProperty(
        name="Backup enabled",
        description="Enable the backup of the project files before processing",
        default=settings.backup_enabled,
        update=backup_enabled_updated,
    )
    lat_correction: bpy.props.FloatProperty(
        name="Latitude correction",
        description="Set the latitude correction for positioning the tiles",
        soft_min=-0.1,
        soft_max=0.1,
        step=1,
        precision=6,
        default=float(settings.lat_correction),
        update=lat_correction_updated,
    )
    lon_correction: bpy.props.FloatProperty(
        name="Longitude correction",
        description="Set the longitude correction for positioning the tiles",
        soft_min=-0.1,
        soft_max=0.1,
        step=1,
        precision=6,
        default=float(settings.lon_correction),
        update=lon_correction_updated,
    )


class PanelPropertyGroup(bpy.types.PropertyGroup):
    current_operator: StringProperty(default=str())
    current_section: StringProperty(default=str())
    first_mouse_x: IntProperty(default=0)
    first_mouse_y: IntProperty(default=0)
    setting_sections: EnumProperty(items=settings.sections, default="PROJECT", update=setting_sections_updated)


class PanelOperator(Operator):
    def check(self, context):
        return True

    def invoke(self, context, event):
        self.__save_operator_context(context, event)
        return {"RUNNING_MODAL"}

    def execute(self, context, script_file):
        exec_script_from_menu(os.path.join(settings.sources_path, script_file))
        return {"FINISHED"}

    @classmethod
    def poll(cls, context):
        return True

    def __save_operator_context(self, context, event):
        panel_props = context.scene.panel_props
        panel_props.current_operator = self.id_name
        panel_props.current_section = panel_props.setting_sections
        if panel_props.first_mouse_x == 0 and panel_props.first_mouse_y == 0:
            panel_props.first_mouse_x = event.mouse_x
            panel_props.first_mouse_y = event.mouse_y
            # context.window.cursor_warp(context.window.width / 2, (context.window.height / 2) + 60)
        context.window_manager.invoke_props_dialog(self, width=1024)


class SettingsOperator(PanelOperator):
    bl_options = {"REGISTER", "UNDO"}

    def draw_setting_sections_panel(self):
        layout = self.layout
        box = layout.box()
        split = box.split(factor=0.2, align=True)
        self.__display_config_sections(split)
        return split

    @staticmethod
    def draw_header(layout):
        col = layout.column()
        header_box = col.box()
        header_split = header_box.split(factor=0.8, align=True)
        header_split.column()
        header_col = header_split.column()
        header_col.operator(OT_SaveSettingsOperator.bl_idname)
        col.separator()
        box = col.box()
        return box.column(align=True)

    @staticmethod
    def draw_splitted_prop(context, layout, split_factor, property_key, property_name, slider=False):
        split = layout.split(factor=split_factor, align=True)
        split.label(text=property_name)
        split.prop(context.scene.setting_props, property_key, slider=slider, text=str())

    @staticmethod
    def __display_config_sections(layout):
        box = layout.box()
        col = box.column(align=True)
        col.scale_x = 1.3
        col.scale_y = 1.3
        col.prop(context.scene.panel_props, "setting_sections", expand=True)


class OT_InitMsfsSceneryPanel(SettingsOperator):
    id_name = "wm.init_msfs_scenery_project_panel"
    bl_idname = id_name
    bl_label = "Initialize a new MSFS project scenery"

    def draw(self, context):
        layout = self.layout
        setting_props = context.scene.setting_props
        box = layout.box()
        col = box.column()
        col.operator(OT_ProjectsPathOperator)
        row = col.row()
        row.enabled = False
        row.prop(setting_props, "projects_path")
        col.separator()
        col.separator()
        col.prop(setting_props, "project_name")
        col.separator()
        col.prop(setting_props, "author_name")

    def execute(self, context):
        return super().execute(context, "init_msfs_scenery_project.py")


class OT_OptimizeSceneryPanel(SettingsOperator):
    id_name = "wm.optimize_scenery_panel"
    bl_idname = id_name
    bl_label = "Optimize an existing MSFS scenery"

    def execute(self, context):
        return super().execute(context, "init_msfs_scenery_project.py")

    def draw(self, context):
        eval("self.draw_" + context.scene.panel_props.current_section.lower() + "_panel(context)")

    def draw_project_panel(self, context):
        setting_props = context.scene.setting_props
        split = super().draw_setting_sections_panel()
        col = super().draw_header(split)
        col.separator()
        col.operator(OT_ProjectPathOperator.bl_idname)
        row = col.row()
        row.enabled = False
        super().draw_splitted_prop(context, row, 0.2, "projects_path_readonly", "Path of the project")
        col.separator()
        col.separator()
        row = col.row()
        row.enabled = False
        super().draw_splitted_prop(context, row, 0.2, "project_name", "Project name")
        col.separator()
        col.separator()
        super().draw_splitted_prop(context, col, 0.2, "bake_textures_enabled", "Bake textures enabled")
        col.separator()
        super().draw_splitted_prop(context, col, 0.2, "output_texture_format", "Output texture format")
        col.separator()
        col.separator()
        col.separator()
        super().draw_splitted_prop(context, col, 0.2, "backup_enabled", "Backup enabled")
        col.separator()

    def draw_tile_panel(self, context):
        setting_props = context.scene.setting_props
        split = super().draw_setting_sections_panel()
        col = super().draw_header(split)
        col.separator()
        super().draw_splitted_prop(context, col, 0.2, "lat_correction", "Latitude correction", slider=True)
        col.separator()
        super().draw_splitted_prop(context, col, 0.2, "lon_correction", "Longitude correction", slider=True)
        col.separator()

    def draw_nodejs_panel(self, context):
        setting_props = context.scene.setting_props
        split = super().draw_setting_sections_panel()
        col = super().draw_header(split)
        col.separator()
        pass

    def draw_lods_panel(self, context):
        setting_props = context.scene.setting_props
        split = super().draw_setting_sections_panel()
        col = super().draw_header(split)
        col.separator()
        pass

    def draw_msfs_sdk_panel(self, context):
        setting_props = context.scene.setting_props
        split = super().draw_setting_sections_panel()
        col = super().draw_header(context, split)
        col.separator()
        pass

    def draw_python_panel(self, context):
        setting_props = context.scene.setting_props
        split = super().draw_setting_sections_panel()
        col = super().draw_header(context, split)
        col.separator()
        pass

    def draw_compressonator_panel(self, context):
        setting_props = context.scene.setting_props
        split = super().draw_setting_sections_panel()
        col = super().draw_header(context, split)
        col.separator()
        pass


class DirectoryBrowserOperator(Operator, ImportHelper):
    def draw(self, context):
        space = context.space_data
        params = space.params
        params.use_filter = True
        params.use_filter_folder = True
        params.display_size = "NORMAL"


class OT_ProjectsPathOperator(DirectoryBrowserOperator):
    bl_idname = "wm.projects_path_operator"
    bl_label = "Path of the MSFS projects..."

    directory: bpy.props.StringProperty(subtype="DIR_PATH")

    def draw(self, context):
        super().draw(context)

    def execute(self, context):
        context.scene.setting_props.projects_path = self.directory
        return {'FINISHED'}

    def invoke(self, context, event):
        self.directory = context.scene.setting_props.projects_path
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class OT_ProjectPathOperator(DirectoryBrowserOperator):
    bl_idname = "wm.project_path_operator"
    bl_label = "Path of the MSFS project..."

    directory: bpy.props.StringProperty(subtype="DIR_PATH")

    def draw(self, context):
        super().draw(context)

    def execute(self, context):
        context.scene.setting_props.project_path = self.directory
        return {'FINISHED'}

    def invoke(self, context, event):
        self.directory = context.scene.setting_props.project_path
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class OT_SaveSettingsOperator(Operator):
    bl_idname = "wm.save_settings_operator"
    bl_label = "Save settings..."

    def execute(self, context):
        settings.save()
        return {'FINISHED'}


bl_info = {
    "name": "Ui test addon",
    "category": "tests"
}

classes = (
    TOPBAR_MT_google_earth_optimization_menus,
    TOPBAR_MT_google_earth_optimization_menu,
    SettingsPropertyGroup,
    PanelPropertyGroup,
    OT_ProjectPathOperator,
    OT_ProjectsPathOperator,
    OT_SaveSettingsOperator,
    OT_InitMsfsSceneryPanel,
    OT_OptimizeSceneryPanel
)


def register():
    reload_topbar_menu()

    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            pass

    try:
        bpy.types.Scene.setting_props = bpy.props.PointerProperty(type=SettingsPropertyGroup)
        bpy.types.Scene.panel_props = bpy.props.PointerProperty(type=PanelPropertyGroup)
        bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_google_earth_optimization_menus.draw)
    except AttributeError:
        pass


def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_google_earth_optimization_menus.draw)

    del bpy.types.Scene.setting_props
    del bpy.types.Scene.panel_props
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()