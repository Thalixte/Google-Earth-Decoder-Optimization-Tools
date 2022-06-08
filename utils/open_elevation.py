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
import json
from collections import defaultdict

import requests

from constants import GEOMETRY_OSM_COLUMN
from utils import isolated_print

OPEN_ELEVATION_ELEV_URI = "https://api.open-elevation.com/api/v1/lookup"
LOCATIONS_KEY = "locations"
LONGITUDE_KEY = "longitude"
LATITUDE_KEY = "latitude"
ACCEPT_HEADER_KEY = "Accept"
ACCEPT_HEADER_VALUE = "application/json"
CONTENT_TYPE_HEADER_KEY = "Content-Type"
CONTENT_TYPE_HEADER_VALUE = "application/json"


def retrieve_height_data(coords, geoid_height):
    post_data = {LOCATIONS_KEY: []}
    headers = {ACCEPT_HEADER_KEY: ACCEPT_HEADER_VALUE, CONTENT_TYPE_HEADER_KEY: CONTENT_TYPE_HEADER_VALUE}
    json_result = {}
    match = defaultdict(dict)
    results = defaultdict(dict)

    for index, row in coords.iterrows():
        x = row["x"]
        y = row["y"]
        point = row[GEOMETRY_OSM_COLUMN]
        lat = point[0]
        lon = point[1]
        coord = {LATITUDE_KEY : lat, LONGITUDE_KEY: lon}
        post_data[LOCATIONS_KEY].append(coord)
        match[(lat, lon)] = (x, y)

    post_data = json.dumps(post_data).replace("'", "\"")

    try:
        response = requests.post(OPEN_ELEVATION_ELEV_URI, data=post_data, headers=headers)
        response.raise_for_status()
        json_result = json.loads(response.text)
    except requests.exceptions.HTTPError as error:
        isolated_print(error)
    except requests.exceptions.TooManyRedirects as error:
        isolated_print(error)
    except requests.ConnectionError as error:
        isolated_print(error)
    except requests.Timeout as error:
        isolated_print(error)

    if "results" in json_result:
        height_data = json_result["results"]
        for data in height_data:
            lat = data["latitude"]
            lon = data["longitude"]
            height = data["elevation"] + geoid_height

            if (lat, lon) in match:
                x = match[(lat, lon)][0]
                y = match[(lat, lon)][1]
                results[y][x] = height

    return results
