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

from msfs_project.object import MsfsObject
from utils import backup_file


class MsfsShape(MsfsObject):
    dbf_file_name: str
    shp_file_name: str
    shx_file_name: str

    def __init__(self, folder, name, definition_file, dbf_file_name, shp_file_name, shx_file_name):
        super().__init__(folder, name, definition_file)
        self.dbf_file_name = dbf_file_name
        self.shp_file_name = shp_file_name
        self.shx_file_name = shx_file_name

    def backup_files(self, backup_path, dry_mode=False, pbar=None):
        backup_file(backup_path, self.folder, self.dbf_file_name, dry_mode=dry_mode, pbar=pbar)
        backup_file(backup_path, self.folder, self.shp_file_name, dry_mode=dry_mode, pbar=pbar)
        backup_file(backup_path, self.folder, self.shx_file_name, dry_mode=dry_mode, pbar=pbar)
        self.backup_file(backup_path, dry_mode=dry_mode, pbar=pbar)
