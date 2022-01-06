import bpy
from bpy import context
from bpy.props import IntProperty
from bpy.types import Menu
from constants import CLEAR_CONSOLE_CMD, MAX_PHOTOGRAMMETRY_LOD
from utils import Settings, get_sources_path

updatedSettingsPropertyGroup = None

bpy.types.Scene.settings = Settings(get_sources_path())

from .operator.tools import *
from .operator import SettingsPropertyGroup, PanelPropertyGroup, OT_ProjectPathOperator, OT_ProjectsPathOperator, OT_MsfsBuildExePathOperator, \
                        OT_CompressonatorExePathOperator, OT_InitMsfsSceneryProjectOperator, OT_OptimizeMsfsSceneryOperator, OT_UpdateMinSizeValuesOperator, \
                        OT_CompressBuiltPackageOperator, OT_SaveSettingsOperator, OT_ReloadSettingsOperator, OT_InitMsfsSceneryPanel, OT_OptimizeSceneryPanel, \
                        OT_UpdateMinSizeValuesPanel, OT_CompressBuiltPackagePanel


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
        layout.separator()
        layout.operator(OT_CompressBuiltPackagePanel.bl_idname)


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
    OT_CompressBuiltPackageOperator,
    OT_SaveSettingsOperator,
    OT_ReloadSettingsOperator,
    OT_InitMsfsSceneryPanel,
    OT_OptimizeSceneryPanel,
    OT_UpdateMinSizeValuesPanel,
    OT_CompressBuiltPackagePanel,
)


def register():
    reload_topbar_menu()

    for idx, min_size_value in enumerate(context.scene.settings.target_min_size_values):
        reverse_idx = (len(context.scene.settings.target_min_size_values) - 1) - idx
        cur_lod = MAX_PHOTOGRAMMETRY_LOD - reverse_idx
        SettingsPropertyGroup.__annotations__[TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX + str(cur_lod)] = (IntProperty, {
            "name": TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX + str(cur_lod),
            "description": "set the min size value for the lod " + str(cur_lod),
            "default": int(min_size_value),
            "soft_min": 0,
            "soft_max": 100,
            "step": 1,
            "update": SettingsPropertyGroup.target_min_size_value_updated,
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
    del bpy.types.Scene.settings
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
