from constants import *


######################################################
# colored print methods
######################################################
def pr_red(skk): print(CRED, format(skk), CEND)


def pr_green(skk): print(CGREEN, format(skk), CEND)


def pr_ko_red(skk): print("-", format(skk), BOLD + CRED, KO, CEND)


def pr_ko_orange(skk): print("-", format(skk), BOLD + CORANGE, KO, CEND)


def pr_ok_green(skk): print("-", format(skk), BOLD + CGREEN, OK, CEND)


def pr_bg_red(skk): print(CREDBG, format(skk), CEND)


def pr_bg_green(skk): print(CGREENBG, format(skk), CEND)
