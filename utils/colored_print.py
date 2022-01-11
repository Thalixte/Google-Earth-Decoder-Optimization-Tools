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
