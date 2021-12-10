import sys
import time

import os
from types import GeneratorType

from constants import EOL, CRED, CORANGE, CGREEN, CEND
from utils import print_title, isolated_print

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

    PROGRESS_BAR_COLORS = {0: CRED, 0.25: CORANGE, 0.5: CGREEN, 0.75: CGREEN, 1.0: CGREEN}

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

    def update(self, description=str()):
        if self.range <= 0:
            return

        self.idx += 1
        progress = self.idx / self.range
        block = int(round(self.length * progress))
        description = DONE_PROCESS if progress >= 1 else description
        msg = "\r[{0}] {1}%: {2}".format("\u25A0" * block + "-" * (self.length - block), round(progress * 100, 2), description + self.__get_color(progress))

        sys.stdout = sys.__stdout__
        sys.stdout.write(msg.ljust(140))
        sys.stdout.flush()
        sys.stdout = open(os.devnull, 'w')
        time.sleep(self.sleep)

        if progress >= 1:
            isolated_print(CEND, EOL)

    def __get_color(self, progress):
        for step, color in self.PROGRESS_BAR_COLORS.items(): res = color if progress >= step else res
        return res
