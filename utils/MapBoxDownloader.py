#!/usr/bin/python
# GoogleMapDownloader.py 
# Created by Hayden Eskriett [http://eskriett.com]
#
# A script which when given a longitude, latitude and zoom level downloads a
# high resolution google map
# Find the associated blog post at: http://blog.eskriett.com/2013/07/19/downloading-google-maps/

import os
import math
from urllib.request import urlretrieve

from PIL import Image


class MapBoxDownloader:
    """
        A class which generates high resolution google maps images given
        a longitude, latitude and zoom level
    """

    def __init__(self, lat, lng, zoom=12):
        """
            GoogleMapDownloader Constructor

            Args:
                lat:    The latitude of the location required
                lng:    The longitude of the location required
                zoom:   The zoom level of the location required, ranges from 0 - 23
                        defaults to 12
        """
        self._lat = lat
        self._lng = lng
        self._zoom = zoom

    def get_xy(self):
        """
            Generates an X,Y tile coordinate based on the latitude, longitude 
            and zoom level

            Returns:    An X,Y tile coordinate
        """

        tile_size = 256

        # Use a left shift to get the power of 2
        # i.e. a zoom level of 2 will have 2^2 = 4 tiles
        numTiles = 1 << self._zoom

        # Find the x_point given the longitude
        point_x = (tile_size / 2 + self._lng * tile_size / 360.0) * numTiles // tile_size

        # Convert the latitude to radians and take the sine
        sin_y = math.sin(self._lat * (math.pi / 180.0))

        # Calulate the y coorindate
        point_y = ((tile_size / 2) + 0.5 * math.log((1 + sin_y) / (1 - sin_y)) * -(tile_size / (2 * math.pi))) * numTiles // tile_size

        return int(point_x), int(point_y)

    def generate_image(self, **kwargs):
        """
            Generates an image by stitching a number of google map tiles together.
            
            Args:
                start_x:        The top-left x-tile coordinate
                start_y:        The top-left y-tile coordinate
                tile_width:     The number of tiles wide the image should be -
                                defaults to 1
                tile_height:    The number of tiles high the image should be -
                                defaults to 1
                target_folder:  The folder where temporary downloadable image is stored -
                                defaults to None
            Returns:
                A high-resolution Goole Map image.
        """

        start_x = kwargs.get('start_x', None)
        start_y = kwargs.get('start_y', None)
        tile_width = kwargs.get('tile_width', 2)
        tile_height = kwargs.get('tile_height', 3)
        target_folder = kwargs.get('target_folder', None)

        # Check that we have x and y tile coordinates
        if start_x is None or start_y is None:
            start_x, start_y = self.get_xy()

        # Determine the size of the image
        width, height = 256 * tile_width, 256 * tile_height

        # Create a new image of the required size
        map_img = Image.new('RGB', (width, height))

        url = 'https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/' + str(self._lat) + ',' + str(self._lng) + ',' + str(self._zoom) + '/' + str(256 * tile_width) + 'x' + str(256 * tile_height) + '?access_token=pk.eyJ1IjoiZ2Vkb3QiLCJhIjoiY2xneGN4dnp2MDBwcDNlcWZhcDI4cmZhYyJ9.0V0zSjQazVmBEnHLua8_WA&attribution=false&logo=false'

        current_tile = '0-0'

        if target_folder is not None:
            current_tile = os.path.join(target_folder, current_tile)

        urlretrieve(url, current_tile)

        im = Image.open(current_tile)
        map_img.paste(im, (0, 0))

        os.remove(current_tile)

        return map_img
