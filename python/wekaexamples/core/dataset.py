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
import weka.core.jvm as jvm
import wekaexamples.helper as helper
from weka.core.converters import Loader
from weka.core.dataset import Instances
from weka.core.dataset import Instance
from weka.core.dataset import Attribute
import weka.plot.dataset as pld


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
    helper.print_title("Iris summary")
    print(Instances.summary(iris_data))
    helper.print_title("Instance at #0")
    print(iris_data.get_instance(0))
    print(iris_data.get_instance(0).get_values())
    print("Attribute stats (first):\n" + str(iris_data.get_attribute_stats(0)))
    print("total count (first attribute):\n" + str(iris_data.get_attribute_stats(0).total_count()))
    print("numeric stats (first attribute):\n" + str(iris_data.get_attribute_stats(0).numeric_stats()))
    print("nominal counts (last attribute):\n"
          + str(iris_data.get_attribute_stats(iris_data.num_attributes() - 1).nominal_counts()))

    # append datasets
    helper.print_title("append datasets")
    data1 = Instances.copy_instances(iris_data, 0, 2)
    data2 = Instances.copy_instances(iris_data, 2, 2)
    print("Dataset #1:\n" + str(data1))
    print("Dataset #2:\n" + str(data2))
    msg = data1.equal_headers(data2)
    print("#1 == #2 ? " + "yes" if msg is None else msg)
    combined = Instances.append_instances(data1, data2)
    print("Combined:\n" + str(combined))

    # merge datasets
    helper.print_title("merge datasets")
    data1 = Instances.copy_instances(iris_data, 0, 2)
    data1.set_class_index(-1)
    data1.delete_attribute(1)
    data1.delete_attribute(0)
    data2 = Instances.copy_instances(iris_data, 0, 2)
    data2.set_class_index(-1)
    data2.delete_attribute(4)
    data2.delete_attribute(3)
    data2.delete_attribute(2)
    print("Dataset #1:\n" + str(data1))
    print("Dataset #2:\n" + str(data2))
    msg = data1.equal_headers(data2)
    print("#1 == #2 ? " + ("yes" if msg is None else msg))
    combined = Instances.merge_instances(data2, data1)
    print("Combined:\n" + str(combined))

    # load dataset incrementally
    iris_file = helper.get_data_dir() + os.sep + "iris.arff"
    helper.print_info("Loading dataset incrementally: " + iris_file)
    loader = Loader("weka.core.converters.ArffLoader")
    iris_data = loader.load_file(iris_file, incremental=True)
    iris_data.set_class_index(iris_data.num_attributes() - 1)
    helper.print_title("Iris dataset")
    print(iris_data)
    while True:
        inst = loader.next_instance(iris_data)
        if inst is None:
            break
        print(inst)

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
    inst = Instance.create_instance(values)
    print("Instance #1:\n" + str(inst))
    dataset.add_instance(inst)
    values = [2.71828, date_att.parse_date("2014-08-09"), float('nan')]
    inst = Instance.create_instance(values)
    dataset.add_instance(inst)
    print("Instance #2:\n" + str(inst))
    print("Dataset:\n" + str(dataset))
    dataset.delete_with_missing(2)
    print("Dataset (after delete of missing):\n" + str(dataset))

    # simple scatterplot of iris dataset: petalwidth x petallength
    iris_data = loader.load_file(iris_file)
    iris_data.set_class_index(iris_data.num_attributes() - 1)
    pld.scatter_plot(
        iris_data, iris_data.get_attribute_by_name("petalwidth").get_index(),
        iris_data.get_attribute_by_name("petallength").get_index(),
        percent=50,
        wait=False)

    # matrix plot of iris dataset
    iris_data = loader.load_file(iris_file)
    iris_data.set_class_index(iris_data.num_attributes() - 1)
    pld.matrix_plot(iris_data, percent=50, title="Matrix plot iris", wait=True)


if __name__ == "__main__":
    try:
        jvm.start()
        main()
    except Exception, e:
        print(e)
    finally:
        jvm.stop()
