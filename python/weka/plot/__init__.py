# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# __init__.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

# check whether pygraphviz is there
pygraphviz_available = False
try:
    import pygraphviz
    pygraphviz_available = True
except ImportError:
    pass

# check whether PIL is there
PIL_available = False
try:
    import PIL
    PIL_available = True
except ImportError:
    pass

# check whether matplotlib is there
matplotlib_available = False
try:
    import matplotlib
    matplotlib_available = True
except ImportError:
    pass
