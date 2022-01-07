import os

import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty
from constants import TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX, PNG_TEXTURE_FORMAT, JPG_TEXTURE_FORMAT, MAX_PHOTOGRAMMETRY_LOD


class SettingsPropertyGroup(bpy.types.PropertyGroup):

    def projects_path_updated(self, context):
        context.scene.settings.projects_path = self.projects_path_readonly = self.projects_path

    def project_path_updated(self, context):
        context.scene.settings.projects_path = self.projects_path = self.projects_path_readonly = os.path.dirname(os.path.dirname(self.project_path)) + os.path.sep
        context.scene.settings.project_name = self.project_name = os.path.relpath(self.project_path, start=self.projects_path)

    def project_name_updated(self, context):
        context.scene.settings.project_name = self.project_name
        context.scene.settings.project_path = os.path.join(context.scene.settings.projects_path, context.scene.settings.project_name)

    def author_name_updated(self, context):
        context.scene.settings.author_name = self.author_name

    def bake_textures_enabled_updated(self, context):
        context.scene.settings.bake_textures_enabled_updated = self.bake_textures_enabled

    def output_texture_format_updated(self, context):
        context.scene.settings.output_texture_format = self.output_texture_format

    def backup_enabled_updated(self, context):
        context.scene.settings.backup_enabled = self.backup_enabled

    def lat_correction_updated(self, context):
        context.scene.settings.lat_correction = "{:.9f}".format(float(str(self.lat_correction))).rstrip("0").rstrip(".")

    def lon_correction_updated(self, context):
        context.scene.settings.lon_correction = "{:.9f}".format(float(str(self.lon_correction))).rstrip("0").rstrip(".")

    def target_min_size_value_updated(self, context):
        prev_value = -1
        for idx, min_size_value in enumerate(bpy.types.Scene.settings.target_min_size_values):
            reverse_idx = (len(bpy.types.Scene.settings.target_min_size_values) - 1) - idx
            cur_lod = MAX_PHOTOGRAMMETRY_LOD - reverse_idx
            name = TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX + str(cur_lod)
            cur_value = int(eval("self." + name))
            cur_value = prev_value if cur_value < prev_value else cur_value
            self[name] = cur_value
            context.scene.settings.target_min_size_values[idx] = str(cur_value)
            prev_value = int(context.scene.settings.target_min_size_values[idx])

    def build_package_enabled_updated(self, context):
        context.scene.settings.build_package_enabled = self.build_package_enabled

    def msfs_build_exe_path_updated(self, context):
        context.scene.settings.msfs_build_exe_path = self.msfs_build_exe_path_readonly = self.msfs_build_exe_path

    def msfs_steam_version_updated(self, context):
        context.scene.settings.msfs_steam_version = self.msfs_steam_version

    def compressonator_exe_path_updated(self, context):
        context.scene.settings.compressonator_exe_path = self.compressonator_exe_path_readonly = self.compressonator_exe_path

    def python_reload_modules_updated(self, context):
        context.scene.settings.reload_modules = self.python_reload_modules

    projects_path: bpy.props.StringProperty(
        subtype="DIR_PATH",
        name="Path of the projects",
        description="Select the path containing all your MSFS scenery projects",
        maxlen=1024,
        default=bpy.types.Scene.settings.projects_path,
        update=projects_path_updated
    )
    projects_path_readonly: bpy.props.StringProperty(
        name="Path of the projects",
        description="Select the path containing all your MSFS scenery projects",
        default=bpy.types.Scene.settings.projects_path
    )
    project_name: StringProperty(
        name="Project name",
        description="name of the project to initialize",
        default=bpy.types.Scene.settings.project_name,
        maxlen=256,
        update=project_name_updated
    )
    project_path: StringProperty(
        subtype="DIR_PATH",
        name="Path of the project",
        description="Select the path containing the MSFS scenery project",
        maxlen=1024,
        default=os.path.join(bpy.types.Scene.settings.projects_path, bpy.types.Scene.settings.project_name),
        update=project_path_updated
    )
    author_name: StringProperty(
        name="Author name",
        description="author of the msfs scenery project",
        default=bpy.types.Scene.settings.author_name,
        maxlen=256,
        update=author_name_updated
    )
    bake_textures_enabled: BoolProperty(
        name="Bake textures enabled",
        description="Reduce the number of texture files (Lily Texture Packer addon is necessary https://gumroad.com/l/DFExj)",
        default=bpy.types.Scene.settings.bake_textures_enabled,
        update=bake_textures_enabled_updated,
    )
    output_texture_format: EnumProperty(
        name="Output texture format",
        description="output format of the texture files (jpg or png) used by the photogrammetry tiles",
        items=[
            (PNG_TEXTURE_FORMAT, PNG_TEXTURE_FORMAT, str()),
            (JPG_TEXTURE_FORMAT, JPG_TEXTURE_FORMAT, str()),
        ],
        default=bpy.types.Scene.settings.output_texture_format,
        update=output_texture_format_updated,

    )
    backup_enabled: BoolProperty(
        name="Backup enabled",
        description="Enable the backup of the project files before processing",
        default=bpy.types.Scene.settings.backup_enabled,
        update=backup_enabled_updated,
    )
    lat_correction: FloatProperty(
        name="Latitude correction",
        description="Set the latitude correction for positioning the tiles",
        soft_min=-0.1,
        soft_max=0.1,
        step=1,
        precision=6,
        default=float(bpy.types.Scene.settings.lat_correction),
        update=lat_correction_updated,
    )
    lon_correction: FloatProperty(
        name="Longitude correction",
        description="Set the longitude correction for positioning the tiles",
        soft_min=-0.1,
        soft_max=0.1,
        step=1,
        precision=6,
        default=float(bpy.types.Scene.settings.lon_correction),
        update=lon_correction_updated,
    )
    build_package_enabled: BoolProperty(
        name="Build package enabled",
        description="Enable the package compilation when the script has finished",
        default=bpy.types.Scene.settings.build_package_enabled,
        update=build_package_enabled_updated,
    )
    msfs_build_exe_path: StringProperty(
        subtype="FILE_PATH",
        name="Path to the MSFS bin exe that builds the MSFS packages",
        description="Select the path to the MSFS bin exe that builds the MSFS packages",
        maxlen=1024,
        default=bpy.types.Scene.settings.msfs_build_exe_path,
        update=msfs_build_exe_path_updated
    )
    msfs_build_exe_path_readonly: StringProperty(
        name="Path to the MSFS bin exe that builds the MSFS packages",
        description="Select the path to the MSFS bin exe that builds the MSFS packages",
        default=bpy.types.Scene.settings.msfs_build_exe_path
    )
    msfs_steam_version: BoolProperty(
        name="Msfs Steam version",
        description="Set this to true if you have the MSFS 2020 Steam version",
        default=bpy.types.Scene.settings.msfs_steam_version,
        update=msfs_steam_version_updated,
    )
    compressonator_exe_path: StringProperty(
        subtype="FILE_PATH",
        name="Path to the compressonator bin exe that compresses the package texture files",
        description="Select the path to the compressonator bin exe that compresses the package texture file",
        maxlen=1024,
        default=bpy.types.Scene.settings.compressonator_exe_path,
        update=compressonator_exe_path_updated
    )
    compressonator_exe_path_readonly: StringProperty(
        name="Path to the compressonator bin exe that compresses the package texture files",
        description="Select the path to the compressonator bin exe that compresses the package texture file",
        default=bpy.types.Scene.settings.compressonator_exe_path,
    )
    python_reload_modules: BoolProperty(
        name="Reload python modules (for dev purpose)",
        description="Set this to true if you want to reload python modules (mainly for dev purpose)",
        default=bpy.types.Scene.settings.reload_modules,
        update=python_reload_modules_updated,
    )
