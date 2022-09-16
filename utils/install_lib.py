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
import site
import subprocess
import sys
import tempfile
from zipfile import ZipFile

import requests
from glob import glob1
from importlib import import_module

import bpy

######################################################
# Python lib installation
######################################################

from os.path import normpath, join, dirname

from constants import ALTERNATE_PYTHON_LIB_REPO, WIN64_SUFFIX, WIN32_SUFFIX, WHL_FILE_EXT, ZIP_FILE_EXT, TXT_FILE_EXT
from utils.script_errors import ScriptError

PIP_LIB = "pip"
WILDCARD = "*"
CHUNK_SIZE = 1048576


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


def install_alternate_python_lib(lib_prefix):
    is_64bits = sys.maxsize > 2 ** 32
    whl_file_name = lib_prefix + "-cp" + sys.winver.replace(".", str()) + "-cp" + sys.winver.replace(".", str()) + "-" + (WIN64_SUFFIX if is_64bits else WIN32_SUFFIX) + WHL_FILE_EXT
    whl_file = os.path.join(tempfile.gettempdir(), whl_file_name)
    download_file(ALTERNATE_PYTHON_LIB_REPO + whl_file_name, whl_file)
    install_python_lib(whl_file)
    if os.path.isfile(whl_file):
        os.remove(whl_file)


def install_shapefile_resource(repo, archive, dest):
    tmp_file = os.path.join(tempfile.gettempdir(), archive)
    download_file(repo + archive, tmp_file)
    with ZipFile(tmp_file) as zip_file:
        namelist = zip_file.namelist()
        for file in namelist:
            filename = os.path.basename(file)

            # skip directories
            if not filename:
                continue

            # skip txt files
            if filename.endswith(TXT_FILE_EXT):
                continue

            source = zip_file.open(file)
            target = open(os.path.join(dest, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)

    if os.path.isfile(tmp_file):
        os.remove(tmp_file)


def is_installed(python_lib_path, lib):
    return os.path.isdir(os.path.join(python_lib_path, lib)) or len(glob1(python_lib_path, lib + WILDCARD)) > 0 or os.path.isdir(os.path.join(site.USER_SITE, lib)) or len(glob1(site.USER_SITE, lib + WILDCARD)) > 0


def download_file(url, dest):
    from utils.progress_bar import ProgressBar
    # use a context manager to make an HTTP request and file
    with requests.get(url, stream=True) as r:
        with open(dest, 'wb') as file:
            # Get the total size, in bytes, from the response header
            total_size = int(r.headers.get('Content-Length'))
            # Define the size of the chunk to iterate over (Mb)
            # iterate over every chunk and calculate % of total
            pbar = ProgressBar(list())
            pbar.length = 100
            for i, chunk in enumerate(r.iter_content(chunk_size=CHUNK_SIZE)):
                # calculate current percentage
                c = i * CHUNK_SIZE / total_size * 100
                file.write(chunk)
                pbar.update("downloading %s" % url, progress=round(c, 4))

    pbar.update("downloading %s" % url, progress=100)
