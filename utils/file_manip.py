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

######################################################
# File manipulation methods
###################################################### 
def line_prepender(filename, line):
    with open(filename, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip("\r\n") + "\n" + content)


######################################################
# File replacement methods
###################################################### 
def replace_in_file(file, text, replacement):
    updated_file = open(file, "rt")
    data = updated_file.read()
    data = data.replace(text, replacement)
    updated_file.close()
    updated_file = open(file, "wt")
    updated_file.write(data)
    updated_file.close()


##########################################################################
# function to pretty print the XML code
##########################################################################
def pretty_print(element, level=0):
    # Function taken from elementTree site:
    # http://effbot.org/zone/element-lib.htm#prettyprint

    indent = "\n" + level * "  "
    if len(element):
        if not element.text or not element.text.strip():
            element.text = indent + "  "

        if not element.tail or not element.tail.strip():
            element.tail = indent

        for element in element:
            pretty_print(element, level + 1)

        if not element.tail or not element.tail.strip():
            element.tail = indent

    else:
        if level and (not element.tail or not element.tail.strip()):
            element.tail = indent

    return element
