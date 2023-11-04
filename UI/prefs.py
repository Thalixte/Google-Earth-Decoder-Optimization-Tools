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

import addon_utils
import bpy
from UI.common import draw_splitted_prop, ALTERNATE_SPLIT_LABEL_FACTOR, PREFS_SPLIT_LABEL_FACTOR
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty
from bpy.types import Operator, AddonPreferences
from constants import ALTERNATE_PYTHON_LIB_REPO, GDAL_LIB_PREFIX, FIONA_LIB_PREFIX, ADDON_NAME, BLENDERGIS_GITHUB_DOWNLOAD_REPO, BLENDERGIS_ADDON_RELEASE, LAND_MASS_REPO, LAND_MASS_ARCHIVE, DEFAULT_OVERPASS_API_URI
from utils.global_settings import GlobalSettings
from utils.folders import get_global_path
from utils.console import isolated_print

updatedSettingsPropertyGroup = None

bpy.types.Scene.global_settings = GlobalSettings(get_global_path())
bpy.types.Scene.project_settings = None


class GEDOT_OT_pref_show(Operator):
    bl_idname = "gedot.pref_show"
    bl_description = 'Display GEDOT addons preferences'
    bl_label = "Preferences"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        addon_utils.modules_refresh(module_cache=None)
        preferences = bpy.context.preferences
        isolated_print(ADDON_NAME)
        addon_prefs = preferences.addons[ADDON_NAME].preferences

        bpy.ops.screen.userpref_show("INVOKE_DEFAULT")
        addon_prefs.active_section = 'ADDONS'
        bpy.ops.preferences.addon_expand(module=ADDON_NAME)
        bpy.ops.preferences.addon_show(module=ADDON_NAME)
        return {'FINISHED'}


class GEDOT_PREFS(AddonPreferences):
    bl_idname = ADDON_NAME

    ########################################################################
    # MSFS package building tools
    ########################################################################

    msfs_build_exe_path: StringProperty(
        subtype="FILE_PATH",
        name="Path to the MSFS bin exe that builds the MSFS packages",
        description="Select the path to the MSFS bin exe that builds the MSFS packages",
        maxlen=1024
    )
    msfs_steam_version: BoolProperty(
        name="Msfs Steam version",
        description="Set this to true if you have the MSFS 2020 Steam version",
        default=False
    )

    ########################################################################
    # Compressonator
    ########################################################################

    compressonator_exe_path: StringProperty(
        subtype="FILE_PATH",
        name="Path to the compressonator bin exe",
        description="Select the path to the compressonator bin exe that compresses the package texture file",
        maxlen=1024,
    )

    ########################################################################
    # Overpass API
    ########################################################################

    overpass_api_uri: StringProperty(
        name="Uri of the overpass API used by Osmnx yo retrieve OSM data",
        default=DEFAULT_OVERPASS_API_URI,
        description="Set the uri of the overpass API used by Osmnx yo retrieve OSM data",
        maxlen=1024,
    )

    ########################################################################
    # GDAL and FIONA libraries installation
    ########################################################################

    alternate_python_libs_repo_url: StringProperty(
        name="Repository url",
        default=ALTERNATE_PYTHON_LIB_REPO,
        description="Define the url of the repository where the libraries are available"
    )
    gdal_library: StringProperty(
        name="GDAL library version",
        default=GDAL_LIB_PREFIX,
        description="Define the version of the GDAL library to retrieve"
    )
    fiona_library: StringProperty(
        name="FIONA library version",
        default=FIONA_LIB_PREFIX,
        description="Define the version of the FIONA library to retrieve"
    )

    ########################################################################
    # Blender GIS addon installation
    ########################################################################

    blendergis_repo_url: StringProperty(
        name="Repository url",
        default=BLENDERGIS_GITHUB_DOWNLOAD_REPO,
        description="Define the url of the github repository of the Blender GIS addon"
    )
    blendergis_release: StringProperty(
        name="Release number",
        default=BLENDERGIS_ADDON_RELEASE,
        description="Define the release number of the Blender GIS addon"
    )

    ########################################################################
    # Landmass shapefile
    ########################################################################

    landmass_repo_url: StringProperty(
        name="Repository url",
        default=LAND_MASS_REPO,
        description="Define the url of the repository where the landmass shapefile is available"
    )
    landmass_archive: StringProperty(
        name="Archive name",
        default=LAND_MASS_ARCHIVE,
        description="Define the archive name containing the landmass shapefile"
    )

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="MSFS building package tools")
        box.prop(self, "msfs_build_exe_path")
        row = box.row()
        col = row.column()
        draw_splitted_prop(self, col, PREFS_SPLIT_LABEL_FACTOR, "msfs_steam_version", "Msfs Steam version")
        row = box.row()

        box = layout.box()
        box.label(text="Overpass API")
        box.prop(self, "overpass_api_uri")
        row = box.row()

        box = layout.box()
        box.label(text="Compressonator")
        box.prop(self, "compressonator_exe_path")
        row = box.row()

        box = layout.box()
        box.label(text="GDAL and FIONA libraries")
        box.prop(self, "alternate_python_libs_repo_url")
        row = box.row()
        box.prop(self, "gdal_library")
        row = box.row()
        box.prop(self, "fiona_library")
        row = box.row()

        box = layout.box()
        box.label(text="BLENDER GIS addon")
        box.prop(self, "blendergis_repo_url")
        row = box.row()
        box.prop(self, "blendergis_release")
        row = box.row()

        box = layout.box()
        box.label(text="Landmass shapefile")
        box.prop(self, "landmass_repo_url")
        row = box.row()
        box.prop(self, "landmass_archive")
        row = box.row()


classes = (
    GEDOT_OT_pref_show,
    GEDOT_PREFS
)


def get_prefs():
    if bpy.context.preferences:
        if ADDON_NAME in bpy.context.preferences.addons:
            return bpy.context.preferences.addons[ADDON_NAME].preferences

    return None


def register():
    preferences = get_prefs()

    # update core settings according to addon prefs
    # bpy.types.Scene.global_settings.proj_engine = preferences.projEngine
    # bpy.types.Scene.global_settings.img_engine = preferences.imgEngine

    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            pass


def unregister():
    try:
        del bpy.types.Scene.project_settings
        del bpy.types.Scene.global_settings
        for cls in classes:
            bpy.utils.unregister_class(cls)
    except AttributeError:
        pass
    except ValueError:
        pass


if __name__ == "__main__":
    register()
