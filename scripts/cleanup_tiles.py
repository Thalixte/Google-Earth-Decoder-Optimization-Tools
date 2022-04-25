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
from osmnx.utils_geo import bbox_to_poly

from utils import Settings, get_sources_path, reload_modules, print_title, isolated_print

settings = Settings(get_sources_path())

# reload modules if the option is enabled in the optimization_tools.ini file
reload_modules(settings)

import os
import osmnx as ox
import pandas as pd
import geopandas as gpd
import warnings

from shapely.errors import ShapelyDeprecationWarning
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)

from pathlib import Path
from constants import *
from utils import check_configuration, ScriptError, build_package, pr_bg_green, pr_bg_red, install_python_lib
from msfs_project import MsfsProject


def cleanup_tiles(script_settings):
    try:
        # bbox_coords = [49.8944091796875, 49.89166259765625, 2.2576904296875, 2.26318359375]
        bbox_coords = [49.89715576171875, 49.8944091796875, 2.2576904296875, 2.26318359375]
        b = bbox_to_poly(bbox_coords[1], bbox_coords[0], bbox_coords[2], bbox_coords[3])
        bbox = gpd.GeoDataFrame(pd.DataFrame(["box"], index=[("bbox", 1)], columns=["boundary"]), crs={"init": "epsg:4326"}, geometry=[b])
        landuse = ox.geometries_from_bbox(bbox_coords[0], bbox_coords[1], bbox_coords[2], bbox_coords[3], tags={"landuse": True})
        leisure = ox.geometries_from_bbox(bbox_coords[0], bbox_coords[1], bbox_coords[2], bbox_coords[3], tags={"leisure": True})
        natural = ox.geometries_from_bbox(bbox_coords[0], bbox_coords[1], bbox_coords[2], bbox_coords[3], tags={"natural": True})
        water = ox.geometries_from_bbox(bbox_coords[0], bbox_coords[1], bbox_coords[2], bbox_coords[3], tags={"water": True})
        aeroway = ox.geometries_from_bbox(bbox_coords[0], bbox_coords[1], bbox_coords[2], bbox_coords[3], tags={"aeroway": True})

        green = landuse[landuse["landuse"].isin(["forest", "nature_reserve", "farmland", "meadow", "vineyard"])].drop(labels="nodes", axis=1)
        # ox.plot_footprints(green)
        parks = leisure[leisure["leisure"].isin(["park", "playground"])].drop(labels="nodes", axis=1)
        # ox.plot_footprints(parks)
        natural = natural[natural["natural"].isin(["wood", "woods", "water", "river", "stream", "sea", "grassland", "scrub"])].drop(labels="nodes", axis=1)
        # ox.plot_footprints(natural)
        water = water[water["water"].isin(["river", "stream", "sea", "water"])].drop(labels="nodes", axis=1)
        # ox.plot_footprints(water)
        # ox.plot_footprints(aeroway)
        isolated_print("Coordinate system:", green.crs)
        # ox.plot_footprints(green)
        export_geopandas_to_osm_xml([green, parks, natural, water], b, "exclude")
        export_geopandas_to_osm_xml([bbox], b, "bbox", [("height", 100)])

        # instantiate the msfsProject and create the necessary resources if it does not exist
        msfs_project = MsfsProject(script_settings.projects_path, script_settings.project_name, script_settings.definition_file, script_settings.author_name, script_settings.sources_path)

        check_configuration(script_settings, msfs_project)

        if script_settings.backup_enabled:
            msfs_project.backup(Path(os.path.abspath(__file__)).stem.replace(SCRIPT_PREFIX, str()))

        isolated_print(EOL)
        print_title("CLEANUP TILES")

        if script_settings.build_package_enabled:
            build_package(msfs_project, script_settings)

        pr_bg_green("Script correctly applied" + constants.CEND)

    except ScriptError as ex:
        error_report = "".join(ex.value)
        isolated_print(constants.EOL + error_report)
        pr_bg_red("Script aborted" + constants.CEND)
    except RuntimeError as ex:
        isolated_print(constants.EOL + str(ex))
        pr_bg_red("Script aborted" + constants.CEND)


import xml.etree.ElementTree as ET


def export_geopandas_to_osm_xml(geopandas_data_frames, bbox_poly, file_name, additional_tags=[]):
    osm_root = ET.Element("osm", attrib={
        "version": "0.6",
        "generator": "custom python script"
        })

    ET.SubElement(osm_root, "bounds", attrib={
        "minlat": str(bbox_poly.bounds[0]),
        "minlon": str(bbox_poly.bounds[1]),
        "maxlat": str(bbox_poly.bounds[2]),
        "maxlon": str(bbox_poly.bounds[3])})

    for geopandas_data_frame in geopandas_data_frames:
        for index, row in geopandas_data_frame.iterrows():
            i = -1
            current_way = ET.SubElement(osm_root, "way", attrib={
                "id": str(index[1]),
                "visible": "true",
                "version": "1",
                "uid": str(index[1]),
                "changeset": "false"})

            for point in row.geometry.exterior.coords:
                i = i+1
                current_node = ET.SubElement(osm_root, "node", attrib={
                    "id": str(index[1])+str(i),
                    "visible": "true",
                    "version": "1",
                    "uid": str(index[1]),
                    "lat": str(point[1]),
                    "lon": str(point[0]),
                    "changeset": "false"})

                ET.SubElement(current_way, "nd", attrib={
                    "ref": str(index[1])+str(i)})

            i = 0
            ET.SubElement(current_way, "nd", attrib={
                "ref": str(index[1])+str(i)})

            for column in geopandas_data_frame.columns:
                if column != "geometry" and str(row[column]) != "nan":
                    ET.SubElement(current_node, "tag", attrib={
                        "k": column,
                        "v": str(row[column])})

                    ET.SubElement(current_way, "tag", attrib={
                        "k": column,
                        "v": str(row[column])})

            for additional_tag in additional_tags:
                ET.SubElement(current_node, "tag", attrib={
                    "k": additional_tag[0],
                    "v": str(additional_tag[1])})

                ET.SubElement(current_way, "tag", attrib={
                    "k": additional_tag[0],
                    "v": str(additional_tag[1])})

    output_file = ET.ElementTree(element=osm_root)
    output_file.write(file_name + ".osm")
    output_file.write(file_name + ".osm.xml")

##################################################################
#                        Main process
##################################################################


if __name__ == "__main__":
    cleanup_tiles(settings)
