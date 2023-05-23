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
from constants import NONE_ICON

SPLIT_LABEL_FACTOR = 0.4
ALTERNATE_SPLIT_LABEL_FACTOR = 0.975
PREFS_SPLIT_LABEL_FACTOR = 0.245

def draw_splitted_prop(props, layout, split_factor, property_key, property_name, slider=False, enabled=True, expand=False, toggle=False, icon_only=False, emboss=True, icon=NONE_ICON):
    split = layout.split(factor=split_factor, align=True)
    split.label(text=property_name)
    col = split.column(align=True)
    if not enabled:
        col.enabled = False
    col.prop(props, property_key, slider=slider, expand=expand, toggle=toggle, icon_only=icon_only, emboss=emboss, text=str(), icon=icon)