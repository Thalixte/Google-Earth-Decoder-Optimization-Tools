from constants import *


class ScriptError(Exception):
    value: str

    def __init__(self, value):
        self.value = CREDBG + value + CEND + EOL

    def __str__(self):
        return repr(CREDBG + self.value + CEND + EOL)
