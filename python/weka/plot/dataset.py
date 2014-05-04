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

# dataset.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import matplotlib.pyplot as plt
from weka.core.dataset import Instances


def scatter_plot(data, index_x, index_y, size=50, outfile=None, wait=True):
    """
    Plots two attributes against each other.
    TODO: click events http://matplotlib.org/examples/event_handling/data_browser.html
    :param data: the dataset
    :type data: Instances
    :param index_x: the 0-based index of the attribute on the x axis
    :type index_x: int
    :param index_y: the 0-based index of the attribute on the y axis
    :type index_y: int
    :param size: the size of the circles in point
    :type size: int
    :param outfile: the (optional) file to save the generated plot to. The extension determines the file format.
    :type outfile: str
    :param wait: whether to wait for the user to close the plot
    :type wait: bool
    """
    x = []
    y = []
    if data.get_class_index() == -1:
        c = None
    else:
        c = []
    for i in xrange(data.num_instances()):
        inst = data.get_instance(i)
        x.append(inst.get_value(index_x))
        y.append(inst.get_value(index_y))
        if not c is None:
            c.append(inst.get_value(inst.get_class_index()))
    fig, ax = plt.subplots()
    if c is None:
        ax.scatter(x, y, s=size, alpha=0.5)
    else:
        ax.scatter(x, y, c=c, s=size, alpha=0.5)
    ax.set_xlabel(data.get_attribute(index_x).get_name())
    ax.set_ylabel(data.get_attribute(index_y).get_name())
    ax.set_title("Attribute scatter plot")
    ax.plot(ax.get_xlim(), ax.get_ylim(), ls="--", c="0.3")
    ax.grid(True)
    plt.draw()
    if not outfile is None:
        plt.savefig(outfile)
    if wait:
        plt.show()
