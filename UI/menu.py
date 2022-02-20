#  #
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 2
#   of the License, or (at your option) any later version.
#  #
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#  #
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#  #
#
#  <pep8 compliant>

import bpy
from bpy.types import Menu
from constants import CLEAR_CONSOLE_CMD
from utils import Settings, get_sources_path

updatedSettingsPropertyGroup = None

bpy.types.Scene.settings = Settings(get_sources_path())

from .operator.tools import *
from .operator import PanelPropertyGroup, OT_ProjectPathOperator, OT_ProjectsPathOperator, OT_MsfsBuildExePathOperator, \
    OT_CompressonatorExePathOperator, OT_InitMsfsSceneryProjectOperator, OT_OptimizeMsfsSceneryOperator, OT_UpdateTilesPositionOperator, \
    OT_UpdateMinSizeValuesOperator, OT_CompressBuiltPackageOperator, OT_SaveSettingsOperator, OT_ReloadSettingsOperator, OT_InitMsfsSceneryPanel, \
    OT_OptimizeSceneryPanel, OT_UpdateTilesPositionPanel, OT_UpdateMinSizeValuesPanel, OT_CompressBuiltPackagePanel, OT_ProjectPathToMergeOperator, \
    OT_MergeSceneriesPanel, OT_MergeSceneriesOperator, OT_CleanPackageFilesOperator, OT_CleanPackageFilesPanel, OT_FixTilesLightningIssuesPanel, \
    OT_FixTilesLightningIssuesOperator, OT_addLodOperator, OT_removeLowerLodOperator, OT_openSettingsFileOperator, OT_AddTileCollidersPanel, OT_RemoveTileCollidersPanel, OT_AddTileCollidersOperator, OT_RemoveTileCollidersOperator


class TOPBAR_MT_google_earth_optimization_menus(Menu):
    os.system(CLEAR_CONSOLE_CMD)
    bl_idname = "TOPBAR_MT_google_earth_optimization_menus"
    bl_label = ""

    def draw(self, _context):
        layout = self.layout
        layout.menu(TOPBAR_MT_google_earth_optimization_menu.bl_idname)


class TOPBAR_MT_google_earth_optimization_menu(Menu):
    bl_idname = "TOPBAR_MT_google_earth_optimization_menu"
    bl_label = "Google Earth Decoder Optimization Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator(OT_InitMsfsSceneryPanel.bl_idname)
        layout.separator()
        layout.operator(OT_OptimizeSceneryPanel.bl_idname)
        layout.separator()
        layout.operator(OT_CleanPackageFilesPanel.bl_idname)
        layout.separator()
        layout.operator(OT_MergeSceneriesPanel.bl_idname)
        layout.separator()
        layout.operator(OT_UpdateTilesPositionPanel.bl_idname)
        layout.separator()
        layout.operator(OT_UpdateMinSizeValuesPanel.bl_idname)
        layout.separator()
        layout.operator(OT_FixTilesLightningIssuesPanel.bl_idname)
        layout.separator()
        layout.operator(OT_AddTileCollidersPanel.bl_idname)
        layout.separator()
        layout.operator(OT_RemoveTileCollidersPanel.bl_idname)
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
    OT_ProjectPathToMergeOperator,
    OT_MsfsBuildExePathOperator,
    OT_CompressonatorExePathOperator,
    OT_InitMsfsSceneryProjectOperator,
    OT_OptimizeMsfsSceneryOperator,
    OT_CleanPackageFilesOperator,
    OT_MergeSceneriesOperator,
    OT_UpdateTilesPositionOperator,
    OT_UpdateMinSizeValuesOperator,
    OT_FixTilesLightningIssuesOperator,
    OT_AddTileCollidersOperator,
    OT_RemoveTileCollidersOperator,
    OT_CompressBuiltPackageOperator,
    OT_openSettingsFileOperator,
    OT_addLodOperator,
    OT_removeLowerLodOperator,
    OT_SaveSettingsOperator,
    OT_ReloadSettingsOperator,
    OT_InitMsfsSceneryPanel,
    OT_OptimizeSceneryPanel,
    OT_CleanPackageFilesPanel,
    OT_MergeSceneriesPanel,
    OT_UpdateTilesPositionPanel,
    OT_UpdateMinSizeValuesPanel,
    OT_FixTilesLightningIssuesPanel,
    OT_AddTileCollidersPanel,
    OT_RemoveTileCollidersPanel,
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
    except AttributeError:
        pass
    finally:
        bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_google_earth_optimization_menus.draw)

        if not hasattr(bpy.types.Scene, "settings"):
            bpy.types.Scene.settings = Settings(get_sources_path())


def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_google_earth_optimization_menus.draw)

    try:
        del bpy.types.Scene.setting_props
        del bpy.types.Scene.panel_props
        del bpy.types.Scene.settings
        for cls in classes:
            bpy.utils.unregister_class(cls)
    except AttributeError:
        pass
    except ValueError:
        pass
    finally:
        reload_topbar_menu()


if __name__ == "__main__":
    register()
