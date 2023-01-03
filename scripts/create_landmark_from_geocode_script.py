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
from pathlib import Path

import osmnx as ox
import logging as lg

from utils import Settings, get_sources_path, reload_modules, print_title, isolated_print, load_gdf_from_geocode

settings = Settings(get_sources_path())

# reload modules if the option is enabled in the optimization_tools.ini file
reload_modules(settings)

import os
import warnings
from shapely.errors import ShapelyDeprecationWarning

warnings.simplefilter(action="ignore", category=UserWarning, append=True)
warnings.simplefilter(action="ignore", category=FutureWarning, append=True)
warnings.simplefilter(action="ignore", category=DeprecationWarning, append=True)
warnings.simplefilter(action="ignore", category=ShapelyDeprecationWarning, append=True)

from constants import *
from utils import check_configuration, ScriptError, build_package, pr_bg_green, pr_bg_red, pr_bg_orange
from msfs_project import MsfsProject


def create_landmark_from_geocode(script_settings):
    try:
        isolated_print(EOL)
        geocode_gdf = load_gdf_from_geocode(script_settings.geocode, check_geocode=True)

        if geocode_gdf.empty:
            geocode_gdf = load_gdf_from_geocode(WAY_OSM_PREFIX + script_settings.geocode, by_osmid=True, check_geocode=True)

        if geocode_gdf.empty:
            geocode_gdf = load_gdf_from_geocode(RELATION_OSM_PREFIX + script_settings.geocode, by_osmid=True, check_geocode=True)

        if geocode_gdf.empty:
            geocode_gdf = load_gdf_from_geocode(NODE_OSM_PREFIX + script_settings.geocode, by_osmid=True, check_geocode=True)

        if not geocode_gdf.empty:
            lat = [0, 0.0]
            lon = [0, 0.0]

            if LAT_OSM_KEY in geocode_gdf:
                lat = geocode_gdf[LAT_OSM_KEY]
            if LON_OSM_KEY in geocode_gdf:
                lon = geocode_gdf[LON_OSM_KEY]

            # instantiate the msfsProject and create the necessary resources if it does not exist
            msfs_project = MsfsProject(script_settings.projects_path, script_settings.project_name, script_settings.definition_file, script_settings.author_name, script_settings.sources_path)

            check_configuration(script_settings, msfs_project)

            if script_settings.backup_enabled:
                msfs_project.backup(Path(os.path.abspath(__file__)).stem.replace(SCRIPT_PREFIX, str()), all_files=False)

            isolated_print(EOL)
            print_title("CREATE LANDMARK FROM GEOCODE")
            msfs_project.create_landmark_from_geocode(script_settings, lat, lon)

            if script_settings.add_lights:
                print_title("ADD LIGHTS TO GEOCODE")
                msfs_project.add_lights_to_geocode(script_settings)

            if script_settings.build_package_enabled:
                build_package(msfs_project, script_settings)
        else:
            pr_bg_orange("Geocode (" + script_settings.geocode + ") not found in OSM data" + EOL + CEND)

        pr_bg_green("Script correctly applied" + constants.CEND)

    except ScriptError as ex:
        error_report = "".join(ex.value)
        isolated_print(constants.EOL + error_report)
        pr_bg_red("Script aborted" + constants.CEND)
    except RuntimeError as ex:
        isolated_print(constants.EOL + str(ex))
        pr_bg_red("Script aborted" + constants.CEND)


##################################################################
#                        Main process
##################################################################


if __name__ == "__main__":
    create_landmark_from_geocode(settings)
