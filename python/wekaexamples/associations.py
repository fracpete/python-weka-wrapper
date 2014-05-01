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

# associations.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import os
import weka.core.jvm as jvm
import wekaexamples.helper as helper
from weka.core.converters import Loader
from weka.associations import Associator


def main():
    """
    Just runs some example code.
    """

    # load a dataset
    vote_file = helper.get_data_dir() + os.sep + "vote.arff"
    helper.print_info("Loading dataset: " + vote_file)
    loader = Loader("weka.core.converters.ArffLoader")
    vote_data = loader.load_file(vote_file)
    vote_data.set_class_index(vote_data.num_attributes() - 1)

    # train and output associator
    associator = Associator(classname="weka.associations.Apriori", options=["-N", "9", "-I"])
    associator.build_associations(vote_data)
    print(associator)

if __name__ == "__main__":
    try:
        jvm.start()
        main()
    except Exception, e:
        print(e)
    finally:
        jvm.stop()
