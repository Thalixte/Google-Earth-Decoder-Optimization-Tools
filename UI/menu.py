# import the bpy module to access blender API
import os

import bpy
from bpy import context
from bpy.props import IntProperty, StringProperty, EnumProperty, BoolProperty, FloatProperty
from bpy.types import Menu
from bpy_extras.io_utils import ImportHelper
from bpy_types import Operator
from constants import CLEAR_CONSOLE_CMD, PNG_TEXTURE_FORMAT, JPG_TEXTURE_FORMAT
from scripts.init_msfs_scenery_project_script import init_msfs_scenery_project
from scripts.optimize_scenery_script import optimize_scenery
from scripts.update_min_size_values_script import update_min_size_values
from utils import Settings, get_sources_path, open_console

settings = Settings(get_sources_path())
updatedSettingsPropertyGroup = None

TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX = "target_min_size_value_"
SPLIT_LABEL_FACTOR = 0.4
MAX_PHOTOGRAMMETRY_LOD = 23


def reload_topbar_menu():
    try:
        if hasattr(bpy.types.TOPBAR_MT_editor_menus.draw, "_draw_funcs"):
            for f in bpy.types.TOPBAR_MT_editor_menus.draw._draw_funcs:
                if not repr(f).startswith("<function TOPBAR_MT_editor_menus.draw"):
                    bpy.types.TOPBAR_MT_editor_menus.draw._draw_funcs.remove(f)
    except AttributeError:
        pass


def invoke_current_operator():
    eval("bpy.ops." + context.scene.panel_props.current_operator + "(\"INVOKE_DEFAULT\")")


def projects_path_updated(self, context):
    settings.projects_path = self.projects_path_readonly = self.projects_path
    panel_props = context.scene.panel_props
    context.window.cursor_warp(panel_props.first_mouse_x, panel_props.first_mouse_y)
    invoke_current_operator()


def project_path_updated(self, context):
    settings.projects_path = self.projects_path = os.path.dirname(os.path.dirname(self.project_path)) + os.path.sep
    settings.project_name = self.project_name = os.path.relpath(self.project_path, start=self.projects_path)


def project_name_updated(self, context):
    settings.project_name = self.project_name
    settings.project_path = os.path.join(settings.projects_path, settings.project_name)


def author_name_updated(self, context):
    settings.author_name = self.author_name


def bake_textures_enabled_updated(self, context):
    settings.bake_textures_enabled_updated = self.bake_textures_enabled_updated


def output_texture_format_updated(self, context):
    settings.output_texture_format = self.output_texture_format


def backup_enabled_updated(self, context):
    settings.backup_enabled = self.backup_enabled


def lat_correction_updated(self, context):
    settings.lat_correction = "{:.9f}".format(float(str(self.lat_correction))).rstrip("0").rstrip(".")


def lon_correction_updated(self, context):
    settings.lon_correction = "{:.9f}".format(float(str(self.lon_correction))).rstrip("0").rstrip(".")


def target_min_size_value_updated(self, context):
    idx = 0
    prev_value = -1
    for name in self.__annotations__.keys():
        if TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX in name:
            cur_value = int(eval("self." + name))
            cur_value = prev_value if cur_value < prev_value else cur_value
            self[name] = cur_value
            settings.target_min_size_values[idx] = str(cur_value)
            prev_value = int(settings.target_min_size_values[idx])
            idx = idx+1


def build_package_enabled_updated(self, context):
    settings.build_package_enabled = self.build_package_enabled


def msfs_build_exe_path_updated(self, context):
    settings.msfs_build_exe_path = self.msfs_build_exe_path_readonly = self.msfs_build_exe_path
    invoke_current_operator()


def msfs_steam_version_updated(self, context):
    settings.msfs_steam_version = self.msfs_steam_version


def compressonator_exe_path_updated(self, context):
    settings.compressonator_exe_path = self.compressonator_exe_path_readonly = self.compressonator_exe_path
    invoke_current_operator()


def python_reload_modules_updated(self, context):
    settings.reload_modules = self.python_reload_modules


def setting_sections_updated(self, context):
    self.current_section = self.setting_sections


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
        layout.separator()
        layout.operator(OT_UpdateMinSizeValuesPanel.bl_idname)


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
    bake_textures_enabled: BoolProperty(
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
    backup_enabled: BoolProperty(
        name="Backup enabled",
        description="Enable the backup of the project files before processing",
        default=settings.backup_enabled,
        update=backup_enabled_updated,
    )
    lat_correction: FloatProperty(
        name="Latitude correction",
        description="Set the latitude correction for positioning the tiles",
        soft_min=-0.1,
        soft_max=0.1,
        step=1,
        precision=6,
        default=float(settings.lat_correction),
        update=lat_correction_updated,
    )
    lon_correction: FloatProperty(
        name="Longitude correction",
        description="Set the longitude correction for positioning the tiles",
        soft_min=-0.1,
        soft_max=0.1,
        step=1,
        precision=6,
        default=float(settings.lon_correction),
        update=lon_correction_updated,
    )
    build_package_enabled: BoolProperty(
        name="Build package enabled",
        description="Enable the package compilation when the script has finished",
        default=settings.build_package_enabled,
        update=build_package_enabled_updated,
    )
    msfs_build_exe_path: StringProperty(
        subtype="FILE_PATH",
        name="Path to the MSFS bin exe that builds the MSFS packages",
        description="Select the path to the MSFS bin exe that builds the MSFS packages",
        maxlen=1024,
        default=settings.msfs_build_exe_path,
        update=msfs_build_exe_path_updated
    )
    msfs_build_exe_path_readonly: StringProperty(
        name="Path to the MSFS bin exe that builds the MSFS packages",
        description="Select the path to the MSFS bin exe that builds the MSFS packages",
        default=settings.msfs_build_exe_path
    )
    msfs_steam_version: BoolProperty(
        name="Msfs Steam version",
        description="Set this to true if you have the MSFS 2020 Steam version",
        default=settings.msfs_steam_version,
        update=msfs_steam_version_updated,
    )
    compressonator_exe_path: StringProperty(
        subtype="FILE_PATH",
        name="Path to the compressonator bin exe that compresses the package texture files",
        description="Select the path to the compressonator bin exe that compresses the package texture file",
        maxlen=1024,
        default=settings.compressonator_exe_path,
        update=compressonator_exe_path_updated
    )
    compressonator_exe_path_readonly: StringProperty(
        name="Path to the compressonator bin exe that compresses the package texture files",
        description="Select the path to the compressonator bin exe that compresses the package texture file",
        default=settings.compressonator_exe_path,
    )
    python_reload_modules: BoolProperty(
        name="Reload python modules (for dev purpose)",
        description="Set this to true if you want to reload python modules (mainly for dev purpose)",
        default=settings.reload_modules,
        update=python_reload_modules_updated,
    )


class PanelPropertyGroup(bpy.types.PropertyGroup):
    current_operator: StringProperty(default=str())
    current_section: StringProperty(default=str())
    first_mouse_x: IntProperty(default=0)
    first_mouse_y: IntProperty(default=0)
    setting_sections: EnumProperty(items=settings.sections, default="PROJECT", update=setting_sections_updated)


class PanelOperator(Operator):
    id_name = str()
    previous_operator = str()
    starting_section = str()

    def check(self, context):
        return True

    def invoke(self, context, event):
        self.__save_operator_context(context, event)
        return {"RUNNING_MODAL"}

    @classmethod
    def poll(cls, context):
        return True

    def __save_operator_context(self, context, event):
        panel_props = context.scene.panel_props
        panel_props.current_operator = self.id_name
        panel_props.setting_sections = self.starting_section if panel_props.current_operator != self.previous_operator else panel_props.setting_sections
        panel_props.current_section = panel_props.setting_sections
        self.previous_operator = panel_props.current_operator
        if panel_props.first_mouse_x == 0 and panel_props.first_mouse_y == 0:
            panel_props.first_mouse_x = event.mouse_x
            panel_props.first_mouse_y = event.mouse_y
            # context.window.cursor_warp(context.window.width / 2, (context.window.height / 2) + 60)
        context.window_manager.invoke_props_dialog(self, width=1024)


class SettingsOperator(PanelOperator):
    operator_name = str()
    id_name = "wm.settings_operator"
    bl_idname = id_name
    bl_options = {"REGISTER", "UNDO"}

    def draw(self, context):
        eval("self.draw_" + context.scene.panel_props.current_section.lower() + "_panel(context)")

    def draw_setting_sections_panel(self):
        layout = self.layout
        box = layout.box()
        split = box.split(factor=SPLIT_LABEL_FACTOR, align=True)
        self.__display_config_sections(split)
        return split

    def draw_project_panel(self, context):
        split = self.draw_setting_sections_panel()
        col = self.draw_header(split)
        col.separator()
        col.operator(OT_ProjectPathOperator.bl_idname)
        row = col.row()
        row.enabled = False
        self.draw_splitted_prop(context, row, SPLIT_LABEL_FACTOR, "projects_path_readonly", "Path of the project")
        col.separator()
        col.separator()
        row = col.row()
        row.enabled = False
        self.draw_splitted_prop(context, row, SPLIT_LABEL_FACTOR, "project_name", "Project name")
        col.separator()
        col.separator()
        self.draw_splitted_prop(context, col, SPLIT_LABEL_FACTOR, "bake_textures_enabled", "Bake textures enabled")
        col.separator()
        self.draw_splitted_prop(context, col, SPLIT_LABEL_FACTOR, "output_texture_format", "Output texture format")
        col.separator(factor=3.0)
        self.draw_splitted_prop(context, col, SPLIT_LABEL_FACTOR, "backup_enabled", "Backup enabled")
        self.__draw_footer(col, self.operator_name)

    def draw_tile_panel(self, context):
        split = self.draw_setting_sections_panel()
        col = self.draw_header(split)
        col.separator()
        self.draw_splitted_prop(context, col, SPLIT_LABEL_FACTOR, "lat_correction", "Latitude correction", slider=True)
        col.separator()
        self.draw_splitted_prop(context, col, SPLIT_LABEL_FACTOR, "lon_correction", "Longitude correction", slider=True)
        self.__draw_footer(col, self.operator_name)

    def draw_lods_panel(self, context):
        split = self.draw_setting_sections_panel()
        col = self.draw_header(split)
        col.separator()

        for idx, min_size_value in enumerate(settings.target_min_size_values):
            reverse_idx = (len(settings.target_min_size_values) - 1) - idx
            cur_lod = MAX_PHOTOGRAMMETRY_LOD - reverse_idx
            self.draw_splitted_prop(context, col, SPLIT_LABEL_FACTOR, "target_min_size_value_" + str(cur_lod), "Min size values for the lod " + str(cur_lod), slider=True)
            col.separator()

        self.__draw_footer(col, self.operator_name)

    def draw_msfs_sdk_panel(self, context):
        split = self.draw_setting_sections_panel()
        col = self.draw_header(split)
        col.separator()
        col.operator(OT_MsfsBuildExePathOperator.bl_idname)
        row = col.row()
        row.enabled = False
        self.draw_splitted_prop(context, row, SPLIT_LABEL_FACTOR, "msfs_build_exe_path_readonly", "MSFS build exe path")
        col.separator()
        self.draw_splitted_prop(context, col, SPLIT_LABEL_FACTOR, "build_package_enabled", "Build package enabled")
        col.separator()
        self.draw_splitted_prop(context, col, SPLIT_LABEL_FACTOR, "msfs_steam_version", "Msfs Steam version")
        self.__draw_footer(col, self.operator_name)

    def draw_python_panel(self, context):
        split = self.draw_setting_sections_panel()
        col = self.draw_header(split)
        col.separator()
        self.draw_splitted_prop(context, col, SPLIT_LABEL_FACTOR, "python_reload_modules", "Reload python modules (for dev purpose)")
        col.separator()
        self.__draw_footer(col, self.operator_name)

    def draw_compressonator_panel(self, context):
        split = self.draw_setting_sections_panel()
        col = self.draw_header(split)
        col.separator()
        col.operator(OT_CompressonatorExePathOperator.bl_idname)
        row = col.row()
        row.enabled = False
        self.draw_splitted_prop(context, row, SPLIT_LABEL_FACTOR, "compressonator_exe_path_readonly", "Compressonator bin exe path")
        self.__draw_footer(col, self.operator_name)

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

    @staticmethod
    def __draw_footer(layout, operator_name):
        layout.separator(factor=10.0)
        layout.operator(operator_name)
        layout.separator(factor=10.0)

    def execute(self, context):
        return {'FINISHED'}


class OT_InitMsfsSceneryPanel(SettingsOperator):
    id_name = "wm.init_msfs_scenery_project_panel"
    bl_idname = id_name
    bl_label = "Initialize a new MSFS project scenery"

    def draw(self, context):
        layout = self.layout
        setting_props = context.scene.setting_props
        box = layout.box()
        col = box.column()
        col.operator(OT_ProjectsPathOperator.bl_idname)
        row = col.row()
        row.enabled = False
        row.prop(setting_props, "projects_path_readonly")
        col.separator()
        col.separator()
        col.prop(setting_props, "project_name")
        col.separator()
        col.prop(setting_props, "author_name")
        col.separator()
        col.separator()
        col.separator()
        col.separator()
        col.operator(OT_InitMsfsSceneryProjectOperator.bl_idname)
        col.separator()
        col.separator()


class OT_OptimizeSceneryPanel(SettingsOperator):
    operator_name = "wm.optimize_msfs_scenery"
    id_name = "wm.optimize_scenery_panel"
    bl_idname = id_name
    bl_label = "Optimize an existing MSFS scenery"
    starting_section = "PROJECT"

    def execute(self, context):
        return {'FINISHED'}


class OT_UpdateMinSizeValuesPanel(SettingsOperator):
    operator_name = "wm.update_min_size_values"
    id_name = "wm.update_min_size_values_panel"
    bl_idname = id_name
    bl_label = "Update LOD min size values for each tile of the project"
    starting_section = "LODS"

    def invoke(self, context, event):
        context.scene.panel_props.current_section = "LODS"
        super().invoke(context, event)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        return {'FINISHED'}


class FileBrowserOperator(Operator, ImportHelper):
    def draw(self, context):
        space = context.space_data
        params = space.params
        params.display_size = "NORMAL"


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


class OT_MsfsBuildExePathOperator(FileBrowserOperator):
    bl_idname = "wm.msfs_build_exe_path_operator"
    bl_label = "Path to the MSFS bin exe that builds the MSFS packages..."

    filter_glob: StringProperty(
        default="*.exe",
        options={"HIDDEN"},
    )

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def draw(self, context):
        super().draw(context)

    def execute(self, context):
        context.scene.setting_props.msfs_build_exe_path = self.filepath
        return {'FINISHED'}

    def invoke(self, context, event):
        self.filepath = context.scene.setting_props.msfs_build_exe_path
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class OT_CompressonatorExePathOperator(FileBrowserOperator):
    bl_idname = "wm.compressonator_exe_path_operator"
    bl_label = "Path to the compressonator bin exe that compresses the package texture files..."

    filter_glob: StringProperty(
        default="*.exe",
        options={"HIDDEN"},
    )

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def draw(self, context):
        super().draw(context)

    def execute(self, context):
        context.scene.setting_props.compressonator_exe_path = self.filepath
        return {'FINISHED'}

    def invoke(self, context, event):
        self.filepath = context.scene.setting_props.compressonator_exe_path
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class OT_InitMsfsSceneryProjectOperator(Operator):
    bl_idname = "wm.init_msfs_scenery_project"
    bl_label = "Initialize a new MSFS project scenery..."

    def execute(self, context):
        # clear and open the system console
        open_console()
        init_msfs_scenery_project(settings)
        return {'FINISHED'}


class OT_OptimizeMsfsSceneryOperator(Operator):
    bl_idname = "wm.optimize_msfs_scenery"
    bl_label = "Optimize an existing MSFS scenery..."

    def execute(self, context):
        # clear and open the system console
        open_console()
        optimize_scenery(settings)
        return {'FINISHED'}


class OT_UpdateMinSizeValuesOperator(Operator):
    bl_idname = "wm.update_min_size_values"
    bl_label = "Update LOD min size values for each tile of the project..."

    def execute(self, context):
        # clear and open the system console
        open_console()
        update_min_size_values(settings)
        return {'FINISHED'}


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
    PanelPropertyGroup,
    updatedSettingsPropertyGroup,
    OT_ProjectPathOperator,
    OT_ProjectsPathOperator,
    OT_MsfsBuildExePathOperator,
    OT_CompressonatorExePathOperator,
    OT_InitMsfsSceneryProjectOperator,
    OT_OptimizeMsfsSceneryOperator,
    OT_UpdateMinSizeValuesOperator,
    OT_SaveSettingsOperator,
    OT_InitMsfsSceneryPanel,
    OT_OptimizeSceneryPanel,
    OT_UpdateMinSizeValuesPanel,
)


def register():
    reload_topbar_menu()
    for idx, min_size_value in enumerate(settings.target_min_size_values):
        reverse_idx = (len(settings.target_min_size_values) - 1) - idx
        cur_lod = MAX_PHOTOGRAMMETRY_LOD - reverse_idx
        SettingsPropertyGroup.__annotations__[TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX + str(cur_lod)] = (IntProperty, {
            "name": TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX + str(cur_lod),
            "description": "set the min size value for the lod " + str(cur_lod),
            "default": int(min_size_value),
            "soft_min": 0,
            "soft_max": 100,
            "step": 1,
            "update": target_min_size_value_updated,
        })

    data = {
        'bl_label': "updatedSettingsPropertyGroup",
        'bl_idname': "wm.updatedSettingsPropertyGroup",
        '__annotations__': SettingsPropertyGroup.__annotations__
    }

    updatedSettingsPropertyGroup = type("newSettingsPropertyGroup", (bpy.types.PropertyGroup,), data)
    bpy.utils.register_class(updatedSettingsPropertyGroup)

    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            pass

    try:
        bpy.types.Scene.setting_props = bpy.props.PointerProperty(type=updatedSettingsPropertyGroup)
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
