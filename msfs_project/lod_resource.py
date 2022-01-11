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

from utils import backup_file


class MsfsLodResource:
    model_file_path: str
    folder: str
    file: str

    def __init__(self, model_file_path, folder, file):
        self.model_file_path = model_file_path
        self.folder = folder
        self.file = file

    def backup_file(self, backup_path, dry_mode=False, pbar=None):
        backup_file(backup_path, self.folder, self.file, dry_mode=dry_mode, pbar=pbar)

    def remove_file(self):
        file_path = os.path.join(self.folder, self.file)
        if os.path.isfile(file_path):
            os.remove(os.path.join(file_path))
            print(self.file, "removed")
