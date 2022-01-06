from bpy_types import Operator
from constants import MAX_PHOTOGRAMMETRY_LOD
from utils import isolated_print
from .operator import OT_ProjectPathOperator, OT_MsfsBuildExePathOperator, OT_CompressonatorExePathOperator, OT_ReloadSettingsOperator, \
                        OT_SaveSettingsOperator, OT_ProjectsPathOperator


class PanelOperator(Operator):
    id_name = str()
    starting_section = str()

    SPLIT_LABEL_FACTOR = 0.4

    def test(self):
        isolated_print("test_called")

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
        if panel_props.invocation_type != "INVOKE_SCREEN":
            panel_props.current_operator = self.id_name
            panel_props.setting_sections = self.starting_section
            panel_props.current_section = panel_props.setting_sections
            if panel_props.first_mouse_x < 0 and panel_props.first_mouse_y < 0:
                panel_props.first_mouse_x = event.mouse_x
                panel_props.first_mouse_y = event.mouse_y
                # context.window.cursor_warp(context.window.width / 2, (context.window.height / 2) + 60)
        panel_props.invocation_type = "INVOKE_DEFAULT"
        context.window_manager.invoke_props_dialog(self, width=1024)


class SettingsOperator(PanelOperator):
    operator_name = str()
    id_name = "wm.settings_operator"
    bl_idname = id_name
    bl_options = {"REGISTER", "UNDO"}

    def draw(self, context):
        eval("self.draw_" + context.scene.panel_props.current_section.lower() + "_panel(context)")

    def draw_setting_sections_panel(self, context):
        layout = self.layout
        box = layout.box()
        split = box.split(factor=self.SPLIT_LABEL_FACTOR, align=True)
        self.display_config_sections(context, split)
        return split

    def draw_project_panel(self, context):
        split = self.draw_setting_sections_panel(context)
        col = self.draw_header(split)
        col.separator()
        col.operator(OT_ProjectPathOperator.bl_idname)
        row = col.row()
        row.enabled = False
        self.draw_splitted_prop(context, row, self.SPLIT_LABEL_FACTOR, "projects_path_readonly", "Path of the project")
        col.separator()
        col.separator()
        row = col.row()
        row.enabled = False
        self.draw_splitted_prop(context, row, self.SPLIT_LABEL_FACTOR, "project_name", "Project name")
        col.separator()
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "bake_textures_enabled", "Bake textures enabled")
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "output_texture_format", "Output texture format")
        col.separator(factor=3.0)
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "backup_enabled", "Backup enabled")
        self.draw_footer(self.layout, self.operator_name)

    def draw_tile_panel(self, context):
        split = self.draw_setting_sections_panel(context)
        col = self.draw_header(split)
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "lat_correction", "Latitude correction", slider=True)
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "lon_correction", "Longitude correction", slider=True)
        self.draw_footer(self.layout, self.operator_name)

    def draw_lods_panel(self, context):
        split = self.draw_setting_sections_panel(context)
        col = self.draw_header(split)
        col.separator()

        for idx, min_size_value in enumerate(context.scene.settings.target_min_size_values):
            reverse_idx = (len(context.scene.settings.target_min_size_values) - 1) - idx
            cur_lod = MAX_PHOTOGRAMMETRY_LOD - reverse_idx
            self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "target_min_size_value_" + str(cur_lod), "Min size values for the lod " + str(cur_lod), slider=True)
            col.separator()

        self.draw_footer(self.layout, self.operator_name)

    def draw_msfs_sdk_panel(self, context):
        split = self.draw_setting_sections_panel(context)
        col = self.draw_header(split)
        col.separator()
        col.operator(OT_MsfsBuildExePathOperator.bl_idname)
        row = col.row()
        row.enabled = False
        self.draw_splitted_prop(context, row, self.SPLIT_LABEL_FACTOR, "msfs_build_exe_path_readonly", "MSFS build exe path")
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "build_package_enabled", "Build package enabled")
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "msfs_steam_version", "Msfs Steam version")
        self.draw_footer(self.layout, self.operator_name)

    def draw_python_panel(self, context):
        split = self.draw_setting_sections_panel(context)
        col = self.draw_header(split)
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "python_reload_modules", "Reload python modules (for dev purpose)")
        col.separator()
        self.draw_footer(self.layout, self.operator_name)

    def draw_compressonator_panel(self, context):
        split = self.draw_setting_sections_panel(context)
        col = self.draw_header(split)
        col.separator()
        col.operator(OT_CompressonatorExePathOperator.bl_idname)
        row = col.row()
        row.enabled = False
        self.draw_splitted_prop(context, row, self.SPLIT_LABEL_FACTOR, "compressonator_exe_path_readonly", "Compressonator bin exe path")
        self.draw_footer(self.layout, self.operator_name)

    @staticmethod
    def draw_header(layout):
        col = layout.column()
        header_box = col.box()
        header_split = header_box.split(factor=0.75, align=True)
        header_col = header_split.split(factor=0.3, align=True)
        header_col.operator(OT_ReloadSettingsOperator.bl_idname)
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
    def display_config_sections(context, layout):
        box = layout.box()
        col = box.column(align=True)
        col.scale_x = 1.3
        col.scale_y = 1.3
        col.prop(context.scene.panel_props, "setting_sections", expand=True)
        col.separator(factor=14.0)

    @staticmethod
    def draw_footer(layout, operator_name):
        layout.separator()
        box = layout.box()
        box.separator(factor=3.0)
        col = box.column(align=True)
        col.scale_x = 2.0
        col.scale_y = 2.0
        col.alert = True
        col.operator(operator_name)
        col.alert = False
        box.separator(factor=3.0)
        layout.separator(factor=3.0)

    def execute(self, context):
        return {'FINISHED'}


class OT_InitMsfsSceneryPanel(SettingsOperator):
    operator_name = "wm.init_msfs_scenery_project"
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
        super().draw_footer(col, self.operator_name)


class OT_OptimizeSceneryPanel(SettingsOperator):
    operator_name = "wm.optimize_msfs_scenery"
    id_name = "wm.optimize_scenery_panel"
    bl_idname = id_name
    bl_label = "Optimize an existing MSFS scenery"
    starting_section = "PROJECT"


class OT_UpdateMinSizeValuesPanel(SettingsOperator):
    operator_name = "wm.update_min_size_values"
    id_name = "wm.update_min_size_values_panel"
    bl_idname = id_name
    bl_label = "Update LOD min size values for each tile of the project"
    starting_section = "LODS"


class OT_CompressBuiltPackagePanel(SettingsOperator):
    operator_name = "wm.compress_built_package"
    id_name = "wm.compress_built_package_panel"
    bl_idname = id_name
    bl_label = "Optimize the built package by compressing the texture files"
    starting_section = "COMPRESSONATOR"
