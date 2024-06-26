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

import bpy
import ctypes
import msvcrt
import subprocess

from ctypes import wintypes, windll

from constants import CLEAR_CONSOLE_CMD, EOL, CEND
from utils.isolated_print import isolated_print

KERNEL32_LIB = "kernel32"
USER32_LIB = "user32"
SW_HIDE = 0
SW_MAXIMIZE = 3
SW_SHOW = 5
MAX_LINES = 9999
CONSOLE_CMD = "CONOUT$"
CONSOLE_TYPE = "CONSOLE"
TITLE_LENGTH = 100
TITLE_FILL_CHAR = "-"

kernel32 = ctypes.WinDLL(KERNEL32_LIB, use_last_error=True)
user32 = ctypes.WinDLL(USER32_LIB, use_last_error=True)


def open_console():
    # clear the system console
    os.system(CLEAR_CONSOLE_CMD)

    kernel32.GetConsoleWindow.restype = wintypes.HWND
    kernel32.GetLargestConsoleWindowSize.restype = wintypes._COORD
    kernel32.GetLargestConsoleWindowSize.argtypes = (wintypes.HANDLE,)
    user32.ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)

    get_console_window = windll.kernel32.GetConsoleWindow
    show_window = windll.user32.ShowWindow
    switch_to_this_window = windll.user32.SwitchToThisWindow
    is_window_visible = windll.user32.IsWindowVisible
    hwnd = get_console_window()

    try:
        # force system console toggle to ensure the new console window will not be closable
        bpy.ops.wm.console_toggle()
    except:
        pass

    if is_window_visible(hwnd):
        show_window(hwnd, SW_HIDE)
        switch_to_this_window(hwnd, True)  # display on Top
    else:
        show_window(hwnd, SW_SHOW)
        switch_to_this_window(hwnd, True)  # display on Top

    maximize_console(MAX_LINES)


def maximize_console(lines=None):
    fd = os.open(CONSOLE_CMD, os.O_RDWR)

    try:
        hCon = msvcrt.get_osfhandle(fd)
        max_size = kernel32.GetLargestConsoleWindowSize(hCon)
        if max_size.X == 0 and max_size.Y == 0:
            raise ctypes.WinError(ctypes.get_last_error())
        cols = max_size.X
    finally:
        os.close(fd)

    hwnd = kernel32.GetConsoleWindow()
    if cols and hwnd:
        lines = max_size.Y if lines is None else max(min(lines, MAX_LINES), max_size.Y)
        subprocess.check_call("mode.com con cols={} lines={}".format(cols, lines))
        subprocess.check_call("mode.com con cp select=65001")
        user32.ShowWindow(hwnd, SW_MAXIMIZE)


def print_title(title):
    isolated_print(CEND + TITLE_FILL_CHAR*TITLE_LENGTH)
    title = " " + title + " "
    isolated_print(title.upper().center(TITLE_LENGTH, TITLE_FILL_CHAR))
    isolated_print(TITLE_FILL_CHAR*TITLE_LENGTH, EOL)
