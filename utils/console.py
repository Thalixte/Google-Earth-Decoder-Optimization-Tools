import os

import bpy
import ctypes
import msvcrt
import subprocess

from bpy import context
from ctypes import wintypes, windll

import builtins as __builtin__

from constants import CLEAR_CONSOLE_CMD

KERNEL32_LIB = "kernel32"
USER32_LIB = "user32"
SW_HIDE = 0
SW_MAXIMIZE = 3
SW_SHOW = 5
MAX_LINES = 9999
CONSOLE_CMD = "CONOUT$"
CONSOLE_TYPE = "CONSOLE"

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

    maximize_console()


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
        if lines is None:
            lines = max_size.Y
        else:
            lines = max(min(lines, MAX_LINES), max_size.Y)
        subprocess.check_call("mode.com con cols={} lines={}".format(cols, lines))
        user32.ShowWindow(hwnd, SW_MAXIMIZE)


def console_print(*args, **kwargs):
    if bpy.context.screen:
        for a in bpy.context.screen.areas:
            if a.type == CONSOLE_TYPE:
                c = {}
                c["area"] = a
                c["space_data"] = a.spaces.active
                c["region"] = a.regions[-1]
                c["window"] = context.window
                c["screen"] = context.screen
                s = " ".join([str(arg) for arg in args])
                for line in s.split("\n"):
                    bpy.ops.console.scrollback_append(c, text=line)


def print(*args, **kwargs):
    console_print(*args, **kwargs)  # to py consoles
    __builtin__.print(*args, **kwargs)  # to system console
