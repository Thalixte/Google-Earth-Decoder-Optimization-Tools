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
import site
import subprocess
import sys
import urllib3
from glob import glob1
from importlib import import_module

import bpy

######################################################
# Python lib installation
######################################################

from os.path import normpath, join, dirname
from utils.script_errors import ScriptError

PIP_LIB = "pip"
WILDCARD = "*"


def install_python_lib(lib, install_pip=False):
    # path to other python folders
    python_missing_msg = "python interpreter not found on your system"
    error_msg = "pip and " + lib + " installation failed in blender lib folder. Please consider running this script as an administrator"
    python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')

    # python lib path fallback
    if not hasattr(bpy.app, "binary_path_python") or bpy.app.binary_path_python is None:
        python_lib_path = normpath(join(dirname(sys.executable), '..', '..', 'python\\lib'))
    else:
        # path to blender python lib folders
        python_lib_path = normpath(join(dirname(bpy.app.binary_path_python), '..', '..', 'python\\lib'))

    if python_lib_path is None:
        raise ScriptError(python_missing_msg)

    if is_installed(python_lib_path, PIP_LIB) and is_installed(python_lib_path, lib):
        print(PIP_LIB, "and", lib, "correctly installed in blender lib folder")
        return True

    try:
        if install_pip:
            # install or upgrade pip
            subprocess.check_call([sys.executable, "-m", "ensurepip"], shell=True)
            subprocess.check_call([python_exe, "-m", PIP_LIB, "--disable-pip-version-check", "install", "--upgrade", PIP_LIB, "--user", "--no-warn-script-location"], shell=True)
            globals()[PIP_LIB] = import_module(PIP_LIB)

        # install required packages
        subprocess.run([python_exe, "-m", PIP_LIB, "--disable-pip-version-check", "install", "--upgrade", lib, "--user", "--no-warn-script-location"], shell=True)
    except:
        raise ScriptError(error_msg)

    if is_installed(python_lib_path, PIP_LIB) and is_installed(python_lib_path, lib):
        print(PIP_LIB, "and", lib, "correctly installed in blender lib folder")
        return True

    return True


def is_installed(python_lib_path, lib):
    return os.path.isdir(os.path.join(python_lib_path, lib)) or len(glob1(python_lib_path, lib + WILDCARD)) > 0 or os.path.isdir(os.path.join(site.USER_SITE, lib)) or len(glob1(site.USER_SITE, lib + WILDCARD)) > 0


def download_whl_file(url, dest):
    urllib3.disable_warnings()
    with urllib3.PoolManager() as http:
        r = http.request('GET', url)
        with open(dest, 'wb') as fout:
            fout.write(r.data)
