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

# clusterers.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import os
import weka.core.jvm as jvm
import wekaexamples.helper as helper
from weka.core.converters import Loader
from weka.clusterers import Clusterer, FilteredClusterer, ClusterEvaluation
from weka.filters import Filter
import weka.plot.graph as plg
import weka.plot.clusterers as plc


def main():
    """
    Just runs some example code.
    """

    # load a dataset
    iris_file = helper.get_data_dir() + os.sep + "iris.arff"
    helper.print_info("Loading dataset: " + iris_file)
    loader = Loader("weka.core.converters.ArffLoader")
    data = loader.load_file(iris_file)

    # remove class attribute
    helper.print_info("Removing class attribute")
    remove = Filter(classname="weka.filters.unsupervised.attribute.Remove", options=["-R", "last"])
    remove.set_inputformat(data)
    data = remove.filter(data)

    # build a clusterer and output model
    helper.print_title("Training SimpleKMeans clusterer")
    clusterer = Clusterer(classname="weka.clusterers.SimpleKMeans", options=["-N", "3"])
    clusterer.build_clusterer(data)
    print(clusterer)
    helper.print_info("Evaluating on data")
    evaluation = ClusterEvaluation()
    evaluation.set_model(clusterer)
    evaluation.test_model(data)
    print("# clusters: " + str(evaluation.get_num_clusters()))
    print("log likelihood: " + str(evaluation.get_log_likelihood()))
    print("cluster assignments:\n" + str(evaluation.get_cluster_assignments()))
    plc.plot_cluster_assignments(evaluation, data, inst_no=True)

    # using a filtered clusterer
    helper.print_title("Filtered clusterer")
    loader = Loader("weka.core.converters.ArffLoader")
    data = loader.load_file(iris_file)
    clusterer = Clusterer(classname="weka.clusterers.SimpleKMeans", options=["-N", "3"])
    remove = Filter(classname="weka.filters.unsupervised.attribute.Remove", options=["-R", "last"])
    fclusterer = FilteredClusterer()
    fclusterer.set_clusterer(clusterer)
    fclusterer.set_filter(remove)
    fclusterer.build_clusterer(data)
    print(fclusterer)

    # load a dataset incrementally and build clusterer incrementally
    helper.print_title("Incremental clusterer")
    loader = Loader("weka.core.converters.ArffLoader")
    iris_inc = loader.load_file(iris_file, incremental=True)
    clusterer = Clusterer("weka.clusterers.Cobweb")
    remove = Filter(classname="weka.filters.unsupervised.attribute.Remove", options=["-R", "last"])
    remove.set_inputformat(iris_inc)
    iris_filtered = remove.get_outputformat()
    clusterer.build_clusterer(iris_filtered)
    while True:
        inst = loader.next_instance(iris_filtered)
        if inst is None:
            break
        remove.input(inst)
        inst_filtered = remove.output()
        clusterer.update_clusterer(inst_filtered)
    clusterer.update_finished()
    print(clusterer.to_commandline())
    print(clusterer)
    print(clusterer.graph())
    plg.plot_dot_graph(clusterer.graph())


if __name__ == "__main__":
    try:
        jvm.start()
        main()
    except Exception, e:
        print(e)
    finally:
        jvm.stop()
