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
import shutil


def backup_file(backup_path, folder, file, dry_mode=False, pbar=None):
    file_path = os.path.join(folder, file)
    backup_file_path = get_backup_file_path(backup_path, folder, file)
    previous_path = str()

    if not dry_mode:
        for path in os.path.dirname(backup_file_path).split(os.sep):
            # ensure that the folders already exist prior to backup the files
            path = os.path.join(previous_path, path)
            if not os.path.isdir(path):
                os.mkdir(os.path.abspath(path))
            previous_path = path + os.sep

    if os.path.isfile(file_path):
        if not os.path.isfile(backup_file_path):
            if not dry_mode:
                shutil.copyfile(file_path, backup_file_path)
            if not pbar is None:
                if dry_mode:
                    pbar.range+=1
                else:
                    pbar.update("%s" % file)


def get_backup_file_path(backup_path, folder, file):
    root_path = os.path.commonpath([backup_path, folder])
    return os.path.join(root_path, os.path.relpath(backup_path, root_path), os.path.relpath(os.path.join(folder, file), root_path))

