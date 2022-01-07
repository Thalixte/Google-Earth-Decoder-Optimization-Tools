import bpy
from bpy.types import Menu
from utils import Settings, get_sources_path

updatedSettingsPropertyGroup = None

bpy.types.Scene.settings = Settings(get_sources_path())

from .operator.tools import *
from .operator import PanelPropertyGroup, OT_ProjectPathOperator, OT_ProjectsPathOperator, OT_MsfsBuildExePathOperator, \
    OT_CompressonatorExePathOperator, OT_InitMsfsSceneryProjectOperator, OT_OptimizeMsfsSceneryOperator, OT_UpdateTilesPositionOperator, \
    OT_UpdateMinSizeValuesOperator, OT_CompressBuiltPackageOperator, OT_SaveSettingsOperator, OT_ReloadSettingsOperator, OT_InitMsfsSceneryPanel, \
    OT_OptimizeSceneryPanel, OT_UpdateTilesPositionPanel, OT_UpdateMinSizeValuesPanel, OT_CompressBuiltPackagePanel


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
        layout.operator(OT_UpdateTilesPositionPanel.bl_idname)
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
    OT_UpdateTilesPositionOperator,
    OT_UpdateMinSizeValuesOperator,
    OT_CompressBuiltPackageOperator,
    OT_SaveSettingsOperator,
    OT_ReloadSettingsOperator,
    OT_InitMsfsSceneryPanel,
    OT_OptimizeSceneryPanel,
    OT_UpdateTilesPositionPanel,
    OT_UpdateMinSizeValuesPanel,
    OT_CompressBuiltPackagePanel,
)


def register():
    reload_topbar_menu()

    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            pass

    try:
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
