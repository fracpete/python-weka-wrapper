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

# filters.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import os
import weka.core.jvm as jvm
import wekaexamples.helper as helper
from weka.core.converters import Loader
from weka.filters import Filter, MultiFilter


def main():
    """
    Just runs some example code.
    """

    # load a dataset
    iris = helper.get_data_dir() + os.sep + "iris.arff"
    helper.print_info("Loading dataset: " + iris)
    loader = Loader("weka.core.converters.ArffLoader")
    data = loader.load_file(iris)

    # remove class attribute
    helper.print_info("Removing class attribute")
    remove = Filter(classname="weka.filters.unsupervised.attribute.Remove", options=["-R", "last"])
    remove.set_inputformat(data)
    filtered = remove.filter(data)

    # use MultiFilter
    helper.print_info("Use MultiFilter")
    remove = Filter(classname="weka.filters.unsupervised.attribute.Remove", options=["-R", "first"])
    std = Filter(classname="weka.filters.unsupervised.attribute.Standardize")
    multi = MultiFilter()
    multi.set_filters([remove, std])
    multi.set_inputformat(data)
    filtered_multi = multi.filter(data)

    # output datasets
    helper.print_title("Input")
    print(data)
    helper.print_title("Output")
    print(filtered)
    helper.print_title("Output (MultiFilter)")
    print(filtered_multi)

if __name__ == "__main__":
    try:
        jvm.start()
        main()
    except Exception, e:
        print(e)
    finally:
        jvm.stop()
