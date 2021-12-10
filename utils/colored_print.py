from constants import *
from utils.isolated_print import isolated_print


######################################################
# colored print methods
######################################################

def pr_red(skk): isolated_print(CRED, format(skk), CEND)


def pr_green(skk): isolated_print(CGREEN, format(skk), CEND)


def pr_ko_red(skk): isolated_print("-", format(skk), BOLD + CRED, KO, CEND)


def pr_ko_orange(skk): isolated_print("-", format(skk), BOLD + CORANGE, KO, CEND)


def pr_ok_green(skk): isolated_print("-", format(skk), BOLD + CGREEN, OK, CEND)


def pr_bg_red(skk): isolated_print(CREDBG, format(skk), CEND)


def pr_bg_green(skk): isolated_print(CGREENBG, format(skk), CEND)
