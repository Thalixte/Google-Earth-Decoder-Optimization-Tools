import sys
import time
from types import GeneratorType

from constants import EOL

PROGRESS_BAR_LENGTH = 50
DEFAULT_SLEEP = 0.0


class ProgressBar:
    iterable: list
    title: str
    sleep: float
    length: int
    range: int
    idx: int

    def __init__(self, iterable, title=str(), sleep=DEFAULT_SLEEP, length=PROGRESS_BAR_LENGTH):
        self.iterable = iterable
        self.title = title
        self.sleep = sleep
        self.length = length
        self.idx = 0
        if type(iterable) is not GeneratorType:
            self.range = len(iterable)
        else:
            self.range = len(list(iterable))

        self.display_title()

    def display_title(self, title=str()):
        if self.range <= 0:
            return

        if title is not str():
            self.title = title
        if self.title is not str():
            sys.stdout.write(self.title + EOL)
            sys.stdout.flush()

    def update(self, description=""):
        if self.range <= 0:
            return

        self.idx += 1
        progress = self.idx / self.range
        block = int(round(self.length * progress))
        if progress >= 1:
            description = " DONE"
        msg = "\r[{0}] {1}%: {2}".format("#" * block + "-" * (self.length - block), round(progress * 100, 2), description)

        sys.stdout.write(msg.ljust(140))
        sys.stdout.flush()
        time.sleep(self.sleep)

        if progress >= 1:
            print(EOL)
