import os
import site
import subprocess
import sys
from importlib import reload, import_module

import bpy

######################################################
# Python lib installation
######################################################
from os.path import normpath, join, dirname
from utils import ScriptError

PIP_LIB = "pip"
WILDCARD = "*"


def install_python_lib(lib, install_pip=False):
    # path to other python folders
    os_python_path = os.path.expandvars(R"%USERPROFILE%\AppData\Roaming\Python")
    python_missing_meg = "python interpreter not found on your system"
    error_msg = "pip and " + lib + " installation failed in blender lib folder. Please consider running this script as an administrator"
    python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')

    # python lib path fallback
    if bpy.app.binary_path_python is None:
        python_lib_path = normpath(join(dirname(os_python_path), '..', '..', 'python\\lib'))
    else:
        # path to blender python lib folders
        python_lib_path = normpath(join(dirname(bpy.app.binary_path_python), '..', '..', 'python\\lib'))

    if python_lib_path is None:
        raise ScriptError(python_missing_meg)

    if is_installed(python_lib_path, PIP_LIB) and is_installed(python_lib_path, lib):
        print(PIP_LIB, "and", lib, "correctly installed in blender lib folder")
        return

    try:
        if install_pip:
            # install or upgrade pip
            subprocess.check_call([sys.executable, "-m", "ensurepip"], shell=True)
            subprocess.check_call(
                [python_exe, "-m", PIP_LIB, "--disable-pip-version-check", "install", "--upgrade", PIP_LIB,
                 "--user", "--no-warn-script-location"], shell=True)
            globals()[PIP_LIB] = import_module(PIP_LIB)

        # install required packages
        subprocess.run(
            [python_exe, "-m", PIP_LIB, "--disable-pip-version-check", "install", "--upgrade", lib, "--user",
             "--no-warn-script-location"], shell=True)
    except:
        raise ScriptError(error_msg)

    if is_installed(python_lib_path, PIP_LIB) and is_installed(python_lib_path, lib):
        print(PIP_LIB, "and", lib, "correctly installed in blender lib folder")


def is_installed(python_lib_path, lib):
    return os.path.isdir(os.path.join(python_lib_path, lib)) or os.path.isdir(os.path.join(site.USER_SITE, lib))
