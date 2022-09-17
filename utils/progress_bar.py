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

import sys
import time

import os
import warnings
from types import GeneratorType

from constants import EOL, CRED, CORANGE, CGREEN, CEND
from utils import print_title, isolated_print

MSG_LENGTH = 160
PROGRESS_BAR_LENGTH = 50
DEFAULT_SLEEP = 0.0
DONE_PROCESS = "DONE"


class ProgressBar:
    iterable: list
    title: str
    sleep: float
    length: int
    range: int
    idx: int

    PROGRESS_BAR_COLORS = {0: CRED, 0.25: CORANGE, 0.75: CGREEN}

    def __init__(self, iterable, title=str(), sleep=DEFAULT_SLEEP, length=PROGRESS_BAR_LENGTH):
        self.iterable = iterable
        self.title = title
        self.sleep = sleep
        self.length = length
        self.idx = 0
        self.range = len(iterable) if type(iterable) is not GeneratorType else len(list(iterable))

        self.display_title()

    def display_title(self, title=str()):
        if self.range <= 0:
            return

        if title is not str():
            self.title = title
        if self.title is not str():
            print_title(self.title)

    def update(self, description=str(), progress=None, stall=False):
        if progress is None and self.range <= 0:
            return

        if not stall:
            self.idx += 1

        if progress is None:
            progress = self.idx / self.range
            block = int(round(self.length * progress))
        else:
            block = int(progress)
            progress = progress / 100

        description = DONE_PROCESS if progress >= 1 else description
        msg = self.__get_color(progress) + "\r[{0}] {1}{2}".format("\u25A0" * block + "-" * (self.length - block), str(round(progress * 100, 2)) + "%: " if progress > 0 else str(), description + CEND)

        if progress is None:
            sys.stdout.close()
        warnings.simplefilter("ignore", ResourceWarning, append=True)
        sys.stdout = sys.__stdout__
        sys.stdout.write(msg.ljust(MSG_LENGTH))
        sys.stdout.flush()
        sys.stdout = open(os.devnull, 'w')
        time.sleep(self.sleep)

        if progress >= 1:
            isolated_print(EOL)

    def __get_color(self, progress):
        for step, color in self.PROGRESS_BAR_COLORS.items(): res = color if progress >= step else res
        return res
