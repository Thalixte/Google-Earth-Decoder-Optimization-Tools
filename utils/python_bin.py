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
import sys

from utils.script_errors import ScriptError

PIP_BIN = "python.exe"


def get_python_bin_path():
    # path to other python folders
    python_bin_missing_msg = "python interpreter not found on your system"
    python_exe = os.path.join(sys.prefix, 'bin', PIP_BIN)

    if python_exe is None:
        raise ScriptError(python_bin_missing_msg)

    return python_exe
