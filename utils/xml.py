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

import os
import xml.etree.ElementTree as Et

from constants import *
from utils import pretty_print, line_prepender
from utils.string import remove_accents


class Xml:
    file_name: str
    file_path: str
    tree: object
    root: object

    ROOT_TAG = "root"

    PATTERN_SUFFIX = "']"
    PARENT_SUFFIX = "/.."
    PARENT_PATTERN_SUFFIX = PATTERN_SUFFIX + PARENT_SUFFIX

    FS_DATA_VERSION = 9.0

    def __init__(self, file_folder, file_name):
        self.file_path = os.path.join(file_folder, file_name)
        self.file_name = file_name
        if os.path.isfile(self.file_path):
            self.tree = Et.parse(self.file_path, parser=Et.XMLParser(encoding=ENCODING))
            self.root = self.tree.getroot()
        else:
            self.root = Et.Element(self.ROOT_TAG)
            self.tree = Et.ElementTree(self.root)

    def save(self):
        try:
            Et.indent(self.tree)
        except AttributeError:
            pass

        self.tree.write(self.file_path, encoding=ENCODING)
        pretty_print(element=self.root)

        line_prepender(self.file_path, XML_HEADER)

    def to_parseable(self, tree):
        t = Et.tostring(tree)
        t = t.lower().replace(b"'", b"")
        t = remove_accents(t.decode(ENCODING))
        return Et.fromstring(t)

    @staticmethod
    def remove_tags(parents, elems):
        for parent in parents:
            for elem in elems:
                parent.remove(elem)
