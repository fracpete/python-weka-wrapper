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

import os
import numpy
import weka.core.jvm as jvm
import examples.helper as helper
from weka.core.converters import Loader
from weka.core.dataset import Instances
from weka.core.dataset import Instance
from weka.core.dataset import Attribute


def main():
    """
    Just runs some example code.
    """

    # load a dataset
    iris_file = helper.get_data_dir() + os.sep + "iris.arff"
    helper.print_info("Loading dataset: " + iris_file)
    loader = Loader("weka.core.converters.ArffLoader")
    iris_data = loader.load_file(iris_file)
    iris_data.set_class_index(iris_data.num_attributes() - 1)
    helper.print_title("Iris dataset")
    print(iris_data)
    helper.print_title("Instance at #0")
    print(iris_data.get_instance(0))
    print(iris_data.get_instance(0).get_values())

    # create attributes
    helper.print_title("Creating attributes")
    num_att = Attribute.create_numeric("num")
    print("numeric: " + str(num_att))
    date_att = Attribute.create_date("dat", "yyyy-MM-dd")
    print("date: " + str(date_att))
    nom_att = Attribute.create_nominal("nom", ["label1", "label2"])
    print("nominal: " + str(nom_att))

    # create dataset
    helper.print_title("Create dataset")
    dataset = Instances.create_instances("helloworld", [num_att, date_att, nom_att], 0)
    print(str(dataset))

    # create an instance
    helper.print_title("Create and add instance")
    values = [3.1415926, date_att.parse_date("2014-04-10"), 1.0]
    inst = Instance.create_instance(numpy.array(values))
    dataset.add_instance(inst)
    print("Instance:\n" + str(inst))
    print("Dataset:\n" + str(dataset))


if __name__ == "__main__":
    try:
        jvm.start()
        main()
    except Exception, e:
        print(e)
    finally:
        jvm.stop()
