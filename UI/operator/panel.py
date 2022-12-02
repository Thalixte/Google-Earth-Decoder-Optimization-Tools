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

from bpy_types import Operator
from constants import MAX_PHOTOGRAMMETRY_LOD, PROJECT_INI_SECTION, TILE_INI_SECTION, LODS_INI_SECTION, OSM_INI_SECTION, GEOCODE_INI_SECTION, COMPRESSONATOR_INI_SECTION, BUILD_INI_SECTION, MERGE_INI_SECTION, BACKUP_INI_SECTION, NONE_ICON, FILE_FOLDER_ICON, FILE_REFRESH_ICON, FILE_TICK_ICON, INFO_ICON, ADD_ICON, REMOVE_ICON
from .operator import OT_ProjectPathOperator, OT_MsfsBuildExePathOperator, OT_CompressonatorExePathOperator, OT_ReloadSettingsOperator, \
    OT_SaveSettingsOperator, OT_ProjectsPathOperator, OT_ProjectPathToMergeOperator, OT_addLodOperator, OT_removeLowerLodOperator, OT_openSettingsFileOperator
from .tools import reload_setting_props


class PanelOperator(Operator):
    id_name = str()
    starting_section = str()

    SPLIT_LABEL_FACTOR = 0.4

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
            reload_setting_props(context)
            panel_props.current_operator_class_name = type(self).__name__
            panel_props.current_operator = self.id_name
            panel_props.setting_sections = self.starting_section
            panel_props.current_section = panel_props.setting_sections
            panel_props.first_mouse_x = event.mouse_x
            panel_props.first_mouse_y = context.window.height - 60
            context.window.cursor_warp(panel_props.first_mouse_x, panel_props.first_mouse_y)
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
        col.operator(OT_ProjectPathOperator.bl_idname, icon=FILE_FOLDER_ICON)
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "projects_path_readonly", "Path of the project", enabled=False)
        col.separator(factor=2.0)
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "project_name", "Project name", enabled=False)
        col.separator(factor=2.0)
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "definition_file", "Xml definition file", enabled=False)
        col.separator(factor=2.0)
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "author_name", "Author of the project")
        col.separator(factor=2.0)
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "bake_textures_enabled", "Bake textures enabled")
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "output_texture_format", "Output texture format")
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "nb_parallel_blender_tasks", "Number of parallel Blender tasks")
        col.separator()
        self.draw_footer(context, self.layout, self.operator_name)

    def draw_merge_panel(self, context):
        split = self.draw_setting_sections_panel(context)
        col = self.draw_header(split)
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "project_path_readonly", "Path of the final msfs scenery project", enabled=False)
        col.separator()
        col.separator(factor=3.0)
        col.operator(OT_ProjectPathToMergeOperator.bl_idname, icon=FILE_FOLDER_ICON)
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "project_path_to_merge_readonly", "Path of the project to merge into the final one", enabled=False)
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "definition_file_to_merge", "Xml definition file of the project to merge into the final one", enabled=False)
        col.separator()
        self.draw_footer(context, self.layout, self.operator_name)

    def draw_tile_panel(self, context):
        split = self.draw_setting_sections_panel(context)
        col = self.draw_header(split)
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "lat_correction", "Latitude correction", slider=True)
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "lon_correction", "Longitude correction", slider=True)
        self.draw_footer(context, self.layout, self.operator_name)

    def draw_lods_panel(self, context):
        split = self.draw_setting_sections_panel(context)
        col = self.draw_header(split)
        col.separator()
        lod_actions_split = col.split(factor=0.75, align=True)
        lod_actions_col = lod_actions_split.split(factor=0.3, align=True)
        lod_actions_col.operator(OT_addLodOperator.bl_idname, icon=ADD_ICON)
        lod_actions_col = lod_actions_split.column()
        lod_actions_col.operator(OT_removeLowerLodOperator.bl_idname, icon=REMOVE_ICON)
        col.separator()

        for idx, min_size_value in enumerate(context.scene.settings.target_min_size_values):
            reverse_idx = (len(context.scene.settings.target_min_size_values) - 1) - idx
            cur_lod = MAX_PHOTOGRAMMETRY_LOD - reverse_idx
            self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "target_min_size_value_" + str(cur_lod), "Min size values for the lod " + str(cur_lod), slider=True)
            col.separator()

        self.draw_footer(context, self.layout, self.operator_name)

    def draw_automatic_build_panel(self, context):
        split = self.draw_setting_sections_panel(context)
        col = self.draw_header(split)
        col.separator()
        col.operator(OT_MsfsBuildExePathOperator.bl_idname, icon=FILE_FOLDER_ICON)
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "msfs_build_exe_path_readonly", "MSFS build exe path", enabled=False)
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "build_package_enabled", "Build package enabled")
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "msfs_steam_version", "Msfs Steam version")
        self.draw_footer(context, self.layout, self.operator_name)

    def draw_openstreetmap_panel(self, context):
        split = self.draw_setting_sections_panel(context)
        col = self.draw_header(split)
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "airport_city", "Airport city")
        col.separator()
        # self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "exclude_ground", "Exclude ground 3d data")
        # col.separator()
        # self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "exclude_nature_reserve", "Exclude nature reserves 3d data")
        # col.separator()
        # self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "exclude_parks", "Exclude parks 3d data")
        # col.separator()
        if self.operator_name is "wm.generate_height_data" or self.operator_name is "wm.prepare_3d_data":
            self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "height_adjustment", "Height data adjustment (in meters)")
            col.separator()
            self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "high_precision", "High precision height data generation")
            col.separator()
        self.draw_footer(context, self.layout, self.operator_name)

    def draw_geocode_panel(self, context):
        split = self.draw_setting_sections_panel(context)
        col = self.draw_header(split)
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "geocode", "Geocode")
        col.separator()
        if self.operator_name is not "wm.create_landmark_from_geocode":
            self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "geocode_margin", "Geocode margin")
            col.separator()
            self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "preserve_roads", "Preserve roads")
            col.separator()
            self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "preserve_buildings", "Preserve buildings")
            col.separator()
        if self.operator_name is "wm.create_landmark_from_geocode":
            self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "landmark_type", "Landmark type")
            col.separator()
            self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "landmark_offset", "Landmark offset")
            col.separator()
        self.draw_footer(context, self.layout, self.operator_name)

    def draw_python_panel(self, context):
        split = self.draw_setting_sections_panel(context)
        col = self.draw_header(split)
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "python_reload_modules", "Reload python modules (for dev purpose)")
        col.separator()
        self.draw_footer(context, self.layout, self.operator_name)

    def draw_compressonator_panel(self, context):
        split = self.draw_setting_sections_panel(context)
        col = self.draw_header(split)
        col.separator()
        col.operator(OT_CompressonatorExePathOperator.bl_idname, icon=FILE_FOLDER_ICON)
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "compressonator_exe_path_readonly", "Compressonator bin exe path", enabled=False)
        self.draw_footer(context, self.layout, self.operator_name)

    def draw_backup_panel(self, context):
        split = self.draw_setting_sections_panel(context)
        col = self.draw_header(split)
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "backup_enabled", "Backup enabled")
        col.separator()
        self.draw_footer(context, self.layout, self.operator_name)

    @staticmethod
    def draw_header(layout):
        col = layout.column()
        header_box = col.box()
        header_split = header_box.split(factor=0.18)
        header_split.operator(OT_ReloadSettingsOperator.bl_idname, icon=FILE_REFRESH_ICON)
        header_col = header_split.split(factor=0.25, align=True)
        header_col.separator()
        header_col.operator(OT_openSettingsFileOperator.bl_idname, icon=FILE_FOLDER_ICON)
        header_col.separator()
        header_col.operator(OT_SaveSettingsOperator.bl_idname, icon=FILE_TICK_ICON)
        col.separator()
        box = col.box()
        return box.column(align=True)

    @staticmethod
    def draw_splitted_prop(context, layout, split_factor, property_key, property_name, slider=False, enabled=True, icon=NONE_ICON):
        split = layout.split(factor=split_factor, align=True)
        split.label(text=property_name)
        col = split.column(align=True)
        if not enabled:
            col.enabled = False
        col.prop(context.scene.setting_props, property_key, slider=slider, text=str(), icon=icon)

    @staticmethod
    def display_config_sections(context, layout):
        box = layout.box()
        col = box.column(align=True)
        col.scale_x = 1.3
        col.scale_y = 1.3
        col.prop(context.scene.panel_props, "setting_sections", expand=True)
        col.separator(factor=14.0)

    def draw_footer(self, context, layout, operator_name):
        description_block = layout.box()
        self.__label_multiline(
            description_block,
            self.operator_description.splitlines(),
            icon=INFO_ICON
        )
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

    @staticmethod
    def __label_multiline(layout, text_lines, icon=NONE_ICON):
        first_line = True
        for text_line in text_lines:
            icon = icon if first_line else NONE_ICON
            layout.label(text=text_line, icon=icon)
            first_line = False


class OT_InitMsfsSceneryPanel(SettingsOperator):
    operator_name = "wm.init_msfs_scenery_project"
    id_name = "wm.init_msfs_scenery_project_panel"
    bl_idname = id_name
    bl_label = "1. Initialize a new MSFS scenery project"
    operator_description = """This script creates the MSFS structure of a scenery project, if it does not already exist.
        Once created, you can copy the result of the Google Earth decoder Output folder into the PackageSources folder of the newly created project. 
        You can also create the structure, then in the Google Earth Decoder tool, point the Output folder to the PackageSources folder of the project.
        The structure is the same as the one provided in the SimpleScenery project of the MSFS SDK samples"""
    starting_section = PROJECT_INI_SECTION
    displayed_sections = [
        PROJECT_INI_SECTION,
    ]

    def draw(self, context):
        layout = self.layout
        col = self.draw_header(layout)
        box = col.box()
        col = box.column()
        col.operator(OT_ProjectsPathOperator.bl_idname, icon=FILE_FOLDER_ICON)
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "projects_path_readonly", "Path of the project", enabled=False)
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "project_name", "Name of the project to initialize")
        col.separator()
        self.draw_splitted_prop(context, col, self.SPLIT_LABEL_FACTOR, "author_name", "Author of the project")
        col.separator()
        col.separator()
        col.separator()
        super().draw_footer(context, col, self.operator_name)


class OT_OptimizeSceneryPanel(SettingsOperator):
    operator_name = "wm.optimize_msfs_scenery"
    id_name = "wm.optimize_scenery_panel"
    bl_idname = id_name
    bl_label = "2. Optimize an existing MSFS scenery project"
    operator_description = """This script optimizes an existing Google Earth Decoder scenery project (textures, Lods, CTD fix).
        If you installed and enabled the Lily Texture Packer Blender addon, and you ticked the "Bake textures enabled" checkbox in the tool menu (section PROJECT), 
        the textures of the project are merged per tile lods, which significantly reduce the number of the project files.        
        It fixes the bounding box of each tile in order for them to fit the MSFS lod management system.
        This script also adds Asobo extension tags in order to manage collisions, road traffic, and correct lightning."""
    starting_section = PROJECT_INI_SECTION
    displayed_sections = [
        PROJECT_INI_SECTION,
        TILE_INI_SECTION,
        LODS_INI_SECTION,
        BUILD_INI_SECTION,
        BACKUP_INI_SECTION,
    ]


class OT_CleanPackageFilesPanel(SettingsOperator):
    operator_name = "wm.clean_package_files"
    id_name = "wm.clean_package_files_panel"
    bl_idname = id_name
    bl_label = "6. Clean the unused files of the msfs project"
    operator_description = """This script clean the unused files of the MSFS scenery project.
        Once you removed some tiles of a project, use this script to clean the gltf, bin and texture files associated to those tiles."""
    starting_section = PROJECT_INI_SECTION
    displayed_sections = [
        PROJECT_INI_SECTION,
        BUILD_INI_SECTION,
        BACKUP_INI_SECTION,
    ]


class OT_MergeSceneriesPanel(SettingsOperator):
    operator_name = "wm.merge_sceneries"
    id_name = "wm.merge_sceneries_panel"
    bl_idname = id_name
    bl_label = "(Optional) Merge an existing MSFS scenery project into another one"
    operator_description = """Merge the tiles of a MSFS scenery project into another MSFS scenery project.
        In the MERGE section, select the project that you want to merge into the project indicated in the PROJECT section."""
    starting_section = MERGE_INI_SECTION
    displayed_sections = [
        PROJECT_INI_SECTION,
        MERGE_INI_SECTION,
        BUILD_INI_SECTION,
        BACKUP_INI_SECTION,
    ]


class OT_UpdateTilesPositionPanel(SettingsOperator):
    operator_name = "wm.update_tiles_position"
    id_name = "wm.update_tiles_position_panel"
    bl_idname = id_name
    bl_label = "Update the position of the MSFS scenery tiles"
    operator_description = """This script calculates the position of the MSFS scenery tiles.
        If you are not satisfied with the resulting positions, you can setup a latitude correction and/or a longitude correction in the TILE section."""
    starting_section = TILE_INI_SECTION
    displayed_sections = [
        PROJECT_INI_SECTION,
        TILE_INI_SECTION,
        BUILD_INI_SECTION,
        BACKUP_INI_SECTION,
    ]


class OT_UpdateMinSizeValuesPanel(SettingsOperator):
    operator_name = "wm.update_min_size_values"
    id_name = "wm.update_min_size_values_panel"
    bl_idname = id_name
    bl_label = "Update LOD min size values for each tile of the project"
    operator_description = """This script updates the LOD min size values for each tile of the project. 
        In the LODS section, you can setup each minsize value of each LOD level.
        According to the MSFS SDK documentation, the selection process is as follows: 
        starting from LoD 0, going down, the first LoD with a minSize smaller than the model's current size on screen will be selected for display. 
        The selection will also take into account forced and disabled LoDs as configured by the model options."""
    starting_section = LODS_INI_SECTION
    displayed_sections = [
        PROJECT_INI_SECTION,
        LODS_INI_SECTION,
        BUILD_INI_SECTION,
        BACKUP_INI_SECTION,
    ]


class OT_FixTilesLightningIssuesPanel(SettingsOperator):
    operator_name = "wm.fix_tiles_lightning_issues"
    id_name = "wm.fix_tiles_lightning_issues_panel"
    bl_idname = id_name
    bl_label = "Fix lightning issues on tiles at dawn or dusk"
    operator_description = """This script fixes the lightning issues on tiles at dawn or dusk.
        To do so, it adds a specific Asobo extension tag ("ASOBO_material_fake_terrain") in the gltf files corresponding to the tiles Lod levels"""
    starting_section = PROJECT_INI_SECTION
    displayed_sections = [
        PROJECT_INI_SECTION,
        BUILD_INI_SECTION,
        BACKUP_INI_SECTION,
    ]


class OT_CreateTerraformAndExclusionPolygonsPanel(SettingsOperator):
    operator_name = "wm.create_terraform_and_exclusion_polygons"
    id_name = "wm.create_terraform_and_exclusion_polygons_panel"
    bl_idname = id_name
    bl_label = "3. Create the terraform and exclusion polygons for the scenery"
    operator_description = """Create the terraform and exclusion polygons for the scenery.
        In the OPENSTREETMAP section, set the city to exclude the airport, if it exists.
        In the OPENSTREETMAP section, indicate if you want to exclude the ground 3d data (forests, woods), 
        the nature reserves, and/or the parks (can produce 3d artifacts)."""
    starting_section = OSM_INI_SECTION
    displayed_sections = [
        PROJECT_INI_SECTION,
        OSM_INI_SECTION,
        BUILD_INI_SECTION,
        BACKUP_INI_SECTION,
    ]


class OT_GenerateHeightDataPanel(SettingsOperator):
    operator_name = "wm.generate_height_data"
    id_name = "wm.generate_height_data_panel"
    bl_idname = id_name
    bl_label = "4. Generate height data based on Google Earth tiles"
    operator_description = """Generate height data based on the profile of the Google Earth tiles.
        In the OPENSTREETMAP section, you can enable high precision, by ticking the "high precision" checkbox if you want to generate 
        height data based on the highest google Earth tile lods. This can help calculating the data 
        for mountain areas but it is not suitable for city area, as it will produce noise due to building height"""
    starting_section = OSM_INI_SECTION
    displayed_sections = [
        PROJECT_INI_SECTION,
        OSM_INI_SECTION,
        BUILD_INI_SECTION,
        BACKUP_INI_SECTION,
    ]


class OT_RemoveWaterFrom3dDataPanel(SettingsOperator):
    operator_name = "wm.remove_water_from_3d_data"
    id_name = "wm.remove_water_from_3d_data_panel"
    bl_idname = id_name
    bl_label = "Remove water from Google Earth tiles"
    operator_description = """Automatically removes water from the Google Earth tiles, based on the OpenStreetMap data.
        Optionally, in the OPENSTREETMAP section, set the city of the airport, in case you want to remove an airport."""
    starting_section = OSM_INI_SECTION
    displayed_sections = [
        PROJECT_INI_SECTION,
        OSM_INI_SECTION,
        BUILD_INI_SECTION,
    ]


class OT_RemoveForestsAndWoodsFrom3dDataPanel(SettingsOperator):
    operator_name = "wm.remove_forests_and_woods_from_3d_data"
    id_name = "wm.remove_forests_and_woods_from_3d_data_panel"
    bl_idname = id_name
    bl_label = "Remove water, forests and woods from Google Earth tiles"
    operator_description = """Automatically removes water, forests and woods from the Google Earth tiles, based on the OpenStreetMap data.
        Optionally, in the OPENSTREETMAP section, set the city of the airport, in case you want to remove an airport.
        Notice: this method can produce some visual artifacts when removing the forests, woods or parks, because of the Google Earth trees        
        which exceeds the open street map corresponding area. Those trees will be partially cut. It is the same for building that touch trees"""
    starting_section = OSM_INI_SECTION
    displayed_sections = [
        PROJECT_INI_SECTION,
        OSM_INI_SECTION,
        BUILD_INI_SECTION,
    ]


class OT_RemoveForestsWoodsAndParksFrom3dDataPanel(SettingsOperator):
    operator_name = "wm.remove_forests_woods_and_parks_from_3d_data"
    id_name = "wm.remove_forests_woods_and_parks_from_3d_data_panel"
    bl_idname = id_name
    bl_label = "Remove water, forests, woods and parks from GE tiles"
    operator_description = """Automatically removes water, forests, woods and parks from the Google Earth tiles, based on the OpenStreetMap data.
        Optionally, in the OPENSTREETMAP section, set the city of the airport, in case you want to remove an airport.
        Notice: this method can produce some visual artifacts when removing the forests, woods or parks, because of the Google Earth trees        
        which exceeds the open street map corresponding area. Those trees will be partially cut. It is the same for building that touch trees"""
    starting_section = OSM_INI_SECTION
    displayed_sections = [
        PROJECT_INI_SECTION,
        OSM_INI_SECTION,
        BUILD_INI_SECTION,
    ]


class OT_KeepOnlyBuildings3dDataPanel(SettingsOperator):
    operator_name = "wm.keep_only_buildings_3d_data"
    id_name = "wm.keep_only_buildings_3d_data_panel"
    bl_idname = id_name
    bl_label = "Keep only buildings from Google Earth tiles"
    operator_description = """Automatically removes everything, except buildings from the Google Earth tiles, based on the OpenStreetMap data.
        Optionally, in the OPENSTREETMAP section, set the city of the airport, in case you want to remove an airport.
        Notice: this method can produce some visual artifacts, and buildings that are not included in OpenStreetMap data can be removed"""
    starting_section = OSM_INI_SECTION
    displayed_sections = [
        PROJECT_INI_SECTION,
        OSM_INI_SECTION,
        BUILD_INI_SECTION,
    ]


class OT_KeepOnlyBuildingsAndRoads3dDataPanel(SettingsOperator):
    operator_name = "wm.keep_only_buildings_and_roads_3d_data"
    id_name = "wm.keep_only_buildings_and_roads_3d_data_panel"
    bl_idname = id_name
    bl_label = "5. Keep only buildings and roads from Google Earth tiles"
    operator_description = """Automatically removes everything, except buildings and roads from the Google Earth tiles, based on the OpenStreetMap data.
        Optionally, in the OPENSTREETMAP section, set the city of the airport, in case you want to remove an airport.
        Notice: this method can produce some visual artifacts, and buildings that are not included in OpenStreetMap data can be removed"""
    starting_section = OSM_INI_SECTION
    displayed_sections = [
        PROJECT_INI_SECTION,
        OSM_INI_SECTION,
        BUILD_INI_SECTION,
    ]


class OT_CreateLandmarkFromGeocodePanel(SettingsOperator):
    operator_name = "wm.create_landmark_from_geocode"
    id_name = "wm.create_landmark_from_geocode_panel"
    bl_idname = id_name
    bl_label = "Create MSFS landmark from geocode"
    operator_description = """Automatically creates MSFS landmark, based on a geocode.
        In the GEOCODE section, set the geocode for which want to create a landmark in MSFS. This geocode is in the form "location name, city"
        Example: "Buckingham Palace, London" for a POI, or "London, United Kingdom" for a city. 
        In the GEOCODE section, choose the type of landmark (POI, city).
        Optionally, in the GEOCODE section, indicates the landmark height offset to change the height of the landmark point.
        """
    starting_section = GEOCODE_INI_SECTION
    displayed_sections = [
        PROJECT_INI_SECTION,
        GEOCODE_INI_SECTION,
        BUILD_INI_SECTION,
        BACKUP_INI_SECTION,
    ]


class OT_Exclude3dDataFromGeocodePanel(SettingsOperator):
    operator_name = "wm.exclude_3d_data_from_geocode"
    id_name = "wm.exclude_3d_data_from_geocode_panel"
    bl_idname = id_name
    bl_label = "Remove a building from the Google Earth 3d data"
    operator_description = """Automatically removes a building from Google Earth 3d data, based on a geocode, or an osmid.
        In the GEOCODE section, indicates the geocode you want to remove from 3d data. This geocode is in the form "location name, city"
        Alternatively, in the GEOCODE section, you can set the osmid (Open Street Map id) you want to remove from 3d data.
        Example: "Buckingham Palace, London" for a geocode, or "5208404", which is the osmid of Buckingham Palace. 
        In the GEOCODE section, set the geocode margin (as OSM and Google Earth can have a slight difference between building position, 
        it allows you to remove a greater area to be sure to exclude completely the building).
        Optionally, in the GEOCODE section, if you want to preserve the roads next to the building to exclude (preserve roads checkbox).
        Optionally, in the GEOCODE section, if you want to preserve the buildings next to the building to exclude (preserve buildings checkbox).
        """
    starting_section = GEOCODE_INI_SECTION
    displayed_sections = [
        PROJECT_INI_SECTION,
        GEOCODE_INI_SECTION,
        BUILD_INI_SECTION,
        BACKUP_INI_SECTION,
    ]


class OT_AddTileCollidersPanel(SettingsOperator):
    operator_name = "wm.add_tile_colliders"
    id_name = "wm.add_tile_colliders_panel"
    bl_idname = id_name
    bl_label = "7. Add a collider for each tile of the project"
    operator_description = """This script adds a collider for each tile of the project. """
    starting_section = PROJECT_INI_SECTION
    displayed_sections = [
        PROJECT_INI_SECTION,
        BUILD_INI_SECTION,
        BACKUP_INI_SECTION,
    ]


class OT_RemoveTileCollidersPanel(SettingsOperator):
    operator_name = "wm.remove_tile_colliders"
    id_name = "wm.remove_tile_colliders_panel"
    bl_idname = id_name
    bl_label = "Remove the colliders for each tile of the project"
    operator_description = """This script removes the colliders for each tile of the project. """
    starting_section = PROJECT_INI_SECTION
    displayed_sections = [
        PROJECT_INI_SECTION,
        BUILD_INI_SECTION,
        BACKUP_INI_SECTION,
    ]


class OT_CompressBuiltPackagePanel(SettingsOperator):
    operator_name = "wm.compress_built_package"
    id_name = "wm.compress_built_package_panel"
    bl_idname = id_name
    bl_label = "8. Optimize the built package by compressing the texture files"
    operator_description = """This script optimizes the built package of a MSFS scenery project by compressing the DDS texture files.
        For the script to process correctly, the package must have been successfully built prior to executing the script."""
    starting_section = COMPRESSONATOR_INI_SECTION
    displayed_sections = [
        PROJECT_INI_SECTION,
        COMPRESSONATOR_INI_SECTION,
        BACKUP_INI_SECTION,
    ]
