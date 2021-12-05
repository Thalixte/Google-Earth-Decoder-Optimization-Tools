##################################################################
# Octant methods
##################################################################

import os
from collections import namedtuple

octant_dict = {
    '0': (0, 0, 0),
    '1': (1, 0, 0),
    '2': (0, 1, 0),
    '3': (1, 1, 0),
    '4': (0, 0, 1),
    '5': (1, 0, 1),
    '6': (0, 1, 1),
    '7': (1, 1, 1),
}

LatLon = namedtuple('LatLon', ['lat', 'lon'])


class LatLonBox(namedtuple('LatLonBox', ['north', 'south', 'west', 'east'])):
    @property
    def mid_point(self):
        n, s, w, e = tuple(self)
        return LatLon((n + s) / 2, (w + e) / 2)

    @property
    def bl_point(self):
        n, s, w, e = tuple(self)
        return LatLon(s, w)

    def get_child(self, octant):
        try:
            oct_x, oct_y, oct_z = octant_dict[octant]
        except KeyError:
            raise ValueError("invalid octant value")

        n, s, w, e = tuple(self)

        if oct_y == 0:
            n = self.mid_point.lat
        elif oct_y == 1:
            s = self.mid_point.lat
        else:
            raise ValueError

        if n == 90 or s == -90:
            return LatLonBox(n, s, w, e)

        if oct_x == 0:
            e = self.mid_point.lon
        elif oct_x == 1:
            w = self.mid_point.lon
        else:
            raise ValueError

        return LatLonBox(n, s, w, e)


first_latlonbox_dict = {
    '02': LatLonBox(0, -90, -180, -90),
    '03': LatLonBox(0, -90, -90, 0),
    '12': LatLonBox(0, -90, 0, 90),
    '13': LatLonBox(0, -90, 90, 180),
    '20': LatLonBox(90, 0, -180, -90),
    '21': LatLonBox(90, 0, -90, 0),
    '30': LatLonBox(90, 0, 0, 90),
    '31': LatLonBox(90, 0, 90, 180),
}


#######################****************###########################

def get_position_from_file_name(file_name):
    pos = tuple([0, 0])

    try:
        latlonbox = first_latlonbox_dict[file_name[0:2]]
    except KeyError as e:
        return pos

    for octant in file_name[2:]:
        latlonbox = latlonbox.get_child(octant)

    return tuple(latlonbox.bl_point)


def is_octant(file_name):
    try:
        first_latlonbox_dict[file_name[0:2]]
    except KeyError as e:
        return False

    return True