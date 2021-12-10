import sys
import os


def isolated_print(*args, **kwargs):
    sys.stdout = sys.__stdout__
    print(*args, **kwargs)
    sys.stdout = open(os.devnull, 'w')
