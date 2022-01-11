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

# constants
CEND = "\033[0m"
BOLD = "\033[01m"
CRED = "\033[31m"
CGREEN = "\033[32m"
CORANGE = "\033[38;5;214m"
CREDBG = "\033[41m"
CGREENBG = "\033[6;30;42m"
OK = "OK"
KO = "KO"
EOL = "\n"
INI_FILE = "optimization_tools.ini"
MSFS_BUILD_EXE="fspackagetool.exe"
EARTH_RADIUS = 6371010

PNG_TEXTURE_FORMAT = "png"
JPG_TEXTURE_FORMAT = "jpg"

POS_FILE_EXT = ".pos"
XML_FILE_EXT = ".xml"
GLTF_FILE_EXT = ".gltf"
BIN_FILE_EXT = ".bin"
DBF_FILE_EXT = ".dbf"
SHP_FILE_EXT = ".shp"
SHX_FILE_EXT = ".shx"
PNG_FILE_EXT = "." + PNG_TEXTURE_FORMAT
JPG_FILE_EXT = "." + JPG_TEXTURE_FORMAT

POS_FILE_PATTERN = "*" + POS_FILE_EXT
XML_FILE_PATTERN = "*" + XML_FILE_EXT
GLTF_FILE_PATTERN = "*" + GLTF_FILE_EXT
BIN_FILE_PATTERN = "*" + BIN_FILE_EXT
DBF_FILE_PATTERN = "*" + DBF_FILE_EXT
SHP_FILE_PATTERN = "*" + SHP_FILE_EXT
SHX_FILE_PATTERN = "*" + SHX_FILE_EXT
JPG_FILE_PATTERN = "*" + JPG_FILE_EXT
PNG_FILE_PATTERN = "*" + PNG_FILE_EXT

ENCODING = "utf-8"

XML_HEADER = '<?xml version="1.0"?>'

CLEAR_CONSOLE_CMD = "cls"

PYTHON_COMPIL_OPTION = "exec"

CONSTANTS_FOLDER = "constants"
UTILS_FOLDER = "utils"
SCRIPT_FOLDER = "scripts"
UI_FOLDER = "UI"

SCRIPT_PREFIX = "_script"

RESOURCE_FOLDER = "resource"
TEMPLATES_FOLDER = RESOURCE_FOLDER + "\\" + "templates"
THUMBNAIL_FOLDER = RESOURCE_FOLDER + "\\" + "thumbnail"

BUSINESS_JSON_TEMPLATE = "Business.json"
PACKAGE_DEFINITIONS_TEMPLATE = "package-definition.xml"
PROJECT_DEFINITION_TEMPLATE = "project-definition.xml"
THUMBNAIL_PICTURE_TEMPLATE = "Thumbnail.jpg"

PROJECT_DEFINITION_TEMPLATE_PATH = TEMPLATES_FOLDER + "\\" + PROJECT_DEFINITION_TEMPLATE
BUSINESS_JSON_TEMPLATE_PATH = TEMPLATES_FOLDER + "\\" + BUSINESS_JSON_TEMPLATE
PACKAGE_DEFINITIONS_TEMPLATE_PATH = TEMPLATES_FOLDER + "\\" + PACKAGE_DEFINITIONS_TEMPLATE
THUMBNAIL_PICTURE_TEMPLATE_PATH = THUMBNAIL_FOLDER + "\\" + THUMBNAIL_PICTURE_TEMPLATE

LILY_TEXTURE_PACKER_ADDON = "LilyTexturePacker"

MAX_PHOTOGRAMMETRY_LOD = 23

TARGET_MIN_SIZE_VALUE_PROPERTY_PREFIX = "target_min_size_value_"

PROJECT_INI_SECTION = "PROJECT"
MERGE_INI_SECTION = "MERGE"
TILE_INI_SECTION = "TILE"
LODS_INI_SECTION = "LODS"
MSFS_SDK_INI_SECTION = "MSFS_SDK"
COMPRESSONATOR_INI_SECTION = "COMPRESSONATOR"
BACKUP_INI_SECTION = "BACKUP"
PYTHON_INI_SECTION = "PYTHON"

NONE_ICON = "NONE"
FILE_FOLDER_ICON="FILE_FOLDER"
FILE_TICK_ICON = "FILE_TICK"
FILE_REFRESH_ICON = "FILE_REFRESH"
INFO_ICON = "INFO"
