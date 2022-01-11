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
import os

from constants import ENCODING


def load_json_file(json_file_path):
    if not os.path.isfile(json_file_path):
        return False

    file = open(json_file_path, encoding=ENCODING)

    try:
        data = json.load(file)
    except:
        data = False
    finally:
        file.close()

    return data


def save_json_file(json_file_path, data):
    if not os.path.isfile(json_file_path):
        return False

    with open(json_file_path, "w") as file:
        file.seek(0)
        json.dump(data, file, indent=4, ensure_ascii=True)
