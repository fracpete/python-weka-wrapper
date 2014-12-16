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
# Copyright (C) 2014 Fracpete (pythonwekawrapper at gmail dot com)

import javabridge
import logging
import os
import sys
import argparse
import weka.core.jvm as jvm
import weka.core.utils as utils
from weka.core.classes import JavaObject
from weka.core.classes import OptionHandler
from weka.core.capabilities import Capabilities
from weka.filters import Filter

# logging setup
logger = logging.getLogger("weka.clusterers")


class Clusterer(OptionHandler):
    """
    Wrapper class for clusterers.
    """

    def __init__(self, classname=None, jobject=None, options=None):
        """
        Initializes the specified clusterer using either the classname or the supplied JB_Object.
        :param classname: the classname of the clusterer
        :type classname: str
        :param jobject: the JB_Object to use
        :type jobject: JB_Object
        :param options: the list of commandline options to use
        :type options: list
        """
        if jobject is None:
            jobject = Clusterer.new_instance(classname)
        self.is_updateable = self.check_type(jobject, "weka.clusterers.UpdateableClusterer")
        self.is_drawable = self.check_type(jobject, "weka.core.Drawable")
        self.enforce_type(jobject, "weka.clusterers.Clusterer")
        super(Clusterer, self).__init__(jobject=jobject, options=options)

    def get_capabilities(self):
        """
        Returns the capabilities of the clusterer.
        :return: the capabilities
        :rtype: Capabilities
        """
        return Capabilities(javabridge.call(self.jobject, "getCapabilities", "()Lweka/core/Capabilities;"))

    def build_clusterer(self, data):
        """
        Builds the clusterer with the data.
        :param data: the data to use for training the clusterer
        :type data: Instances
        """
        javabridge.call(self.jobject, "buildClusterer", "(Lweka/core/Instances;)V", data.jobject)

    def update_clusterer(self, inst):
        """
        Updates the clusterer with the instance.
        :param inst: the Instance to update the clusterer with
        :type inst: Instance
        """
        if self.is_updateable:
            javabridge.call(self.jobject, "updateClusterer", "(Lweka/core/Instance;)V", inst.jobject)
        else:
            logger.critical(utils.get_classname(self.jobject) + " is not updateable!")

    def update_finished(self):
        """
        Signals the clusterer that updating with new data has finished.
        """
        if self.is_updateable:
            javabridge.call(self.jobject, "updateFinished", "()V")
        else:
            logger.critical(utils.get_classname(self.jobject) + " is not updateable!")

    def cluster_instance(self, inst):
        """
        Peforms a prediction.
        :param inst: the instance to determine the cluster for
        :type inst: Instance
        :return: the clustering result
        :rtype: float
        """
        return javabridge.call(self.jobject, "clusterInstance", "(Lweka/core/Instance;)D", inst.jobject)

    def distribution_for_instance(self, inst):
        """
        Peforms a prediction, returning the cluster distribution.
        :param inst: the Instance to get the cluster distribution for
        :type inst: Instance
        :return: the cluster distribution
        :rtype: float[]
        """
        pred = javabridge.call(self.jobject, "distributionForInstance", "(Lweka/core/Instance;)[D", inst.jobject)
        return javabridge.get_env().get_double_array_elements(pred)

    def number_of_clusters(self):
        """
        Returns the number of clusters found.
        :return: the number fo clusters
        :rtype: int
        """
        return javabridge.call(self.jobject, "numberOfClusters", "()I")

    def graph_type(self):
        """
        Returns the graph type if classifier implements weka.core.Drawable, otherwise -1.
        :return: the type
        :rtype: int
        """
        if self.is_drawable:
            return javabridge.call(self.jobject, "graphType", "()I")
        else:
            return -1

    def graph(self):
        """
        Returns the graph if classifier implements weka.core.Drawable, otherwise None.
        :return: the graph or None if not available
        :rtype: str
        """
        if self.is_drawable:
            return javabridge.call(self.jobject, "graph", "()Ljava/lang/String;")
        else:
            return None


class SingleClustererEnhancer(Clusterer):
    """
    Wrapper class for clusterers that use a single base clusterer.
    """

    def __init__(self, classname=None, jobject=None, options=None):
        """
        Initializes the specified clusterer using either the classname or the supplied JB_Object.
        :param classname: the classname of the clusterer
        :type classname: str
        :param jobject: the JB_Object to use
        :type jobject: JB_Object
        :param options: the list of commandline options to use
        :type options: list
        """
        if jobject is None:
            jobject = Clusterer.new_instance(classname)
        self.enforce_type(jobject, "weka.clusterers.SingleClustererEnhancer")
        super(SingleClustererEnhancer, self).__init__(classname=classname, jobject=jobject, options=options)

    def set_clusterer(self, clusterer):
        """
        Sets the base clusterer.
        :param clusterer: the base clusterer to use
        :type clusterer: Clusterer
        """
        javabridge.call(self.jobject, "setClusterer", "(Lweka/clusterers/Clusterer;)V", clusterer.jobject)

    def get_clusterer(self):
        """
        Returns the base clusterer.
        :return: the clusterer
        :rtype: Clusterer
        """
        return Clusterer(javabridge.call(self.jobject, "getClusterer", "()Lweka/clusterers/Clusterer;"))


class FilteredClusterer(SingleClustererEnhancer):
    """
    Wrapper class for the filtered clusterer.
    """

    def __init__(self, jobject=None, options=None):
        """
        Initializes the specified clusterer using either the classname or the supplied JB_Object.
        :param jobject: the JB_Object to use
        :type jobject: JB_Object
        :param options: the list of commandline options to use
        :type options: list
        """
        classname = "weka.clusterers.FilteredClusterer"
        if jobject is None:
            jobject = Clusterer.new_instance(classname)
        self.enforce_type(jobject, classname)
        super(FilteredClusterer, self).__init__(classname=classname, jobject=jobject, options=options)

    def set_filter(self, filtr):
        """
        Sets the filter.
        :param filtr: the filter to use
        :type filtr: Filter
        """
        javabridge.call(self.jobject, "setFilter", "(Lweka/filters/Filter;)V", filtr.jobject)

    def get_filter(self):
        """
        Returns the filter.
        :return: the filter
        :rtype: Filter
        """
        return Filter(javabridge.call(self.jobject, "getFilter", "()Lweka/filters/Filter;"))


class ClusterEvaluation(JavaObject):
    """
    Evaluation class for clusterers.
    """

    def __init__(self):
        """
        Initializes a ClusterEvaluation object.
        """
        super(ClusterEvaluation, self).__init__(ClusterEvaluation.new_instance("weka.clusterers.ClusterEvaluation"))

    def set_model(self, clusterer):
        """
        Sets the built clusterer to evaluate.
        :param clusterer: the clusterer to evaluate
        :type clusterer: Clusterer
        """
        javabridge.call(self.jobject, "setClusterer", "(Lweka/clusterers/Clusterer;)V", clusterer.jobject)

    def test_model(self, test):
        """
        Evaluates the currently set clusterer on the test set.
        :param test: the test set to use for evaluating
        :type test: Instances
        """
        javabridge.call(self.jobject, "evaluateClusterer", "(Lweka/core/Instances;)V", test.jobject)

    def get_cluster_results(self):
        """
        The cluster results as string.
        :return: the results string
        :rtype: str
        """
        return javabridge.call(self.jobject, "clusterResultsToString", "()Ljava/lang/String;")

    def get_cluster_assignments(self):
        """
        Return an array of cluster assignments corresponding to the most recent set of instances clustered.
        :return: the cluster assignments
        :rtype: ndarray
        """
        array = javabridge.call(self.jobject, "getClusterAssignments", "()[D")
        if array is None:
            return None
        else:
            return javabridge.get_env().get_double_array_elements(array)

    def get_num_clusters(self):
        """
        Returns the number of clusters.
        :return: the number of clusters
        :rtype: int
        """
        return javabridge.call(self.jobject, "getNumClusters", "()I")

    def get_log_likelihood(self):
        """
        Returns the log likelihood.
        :return: the log likelihood
        :rtype: float
        """
        return javabridge.call(self.jobject, "getLogLikelihood", "()D")

    def get_classes_to_clusters(self):
        """
        Return the array (ordered by cluster number) of minimum error class to cluster mappings..
        :return: the mappings
        :rtype: ndarray
        """
        array = javabridge.call(self.jobject, "getClassesToClusters", "()[I")
        if array is None:
            return None
        else:
            return javabridge.get_env().get_int_array_elements(array)

    @classmethod
    def evaluate_clusterer(cls, clusterer, args):
        """
        Evaluates the clusterer with the given options.
        :param clusterer: the clusterer instance to evaluate
        :type clusterer: Clusterer
        :param args: the command-line arguments
        :type args: list
        :return: the evaluation result
        :rtype: str
        """
        return javabridge.static_call(
            "Lweka/clusterers/ClusterEvaluation;", "evaluateClusterer",
            "(Lweka/clusterers/Clusterer;[Ljava/lang/String;)Ljava/lang/String;",
            clusterer.jobject, args)


def main():
    """
    Runs a clusterer from the command-line. Calls JVM start/stop automatically.
    Use -h to see all options.
    """
    parser = argparse.ArgumentParser(
        description='Performs clustering from the command-line. Calls JVM start/stop automatically.')
    parser.add_argument("-j", metavar="classpath", dest="classpath", help="additional classpath, jars/directories")
    parser.add_argument("-X", metavar="heap", dest="heap", help="max heap size for jvm, e.g., 512m")
    parser.add_argument("-t", metavar="train", dest="train", required=True, help="training set file")
    parser.add_argument("-T", metavar="test", dest="test", help="test set file")
    parser.add_argument("-d", metavar="outmodel", dest="outmodel", help="model output file name")
    parser.add_argument("-l", metavar="inmodel", dest="inmodel", help="model input file name")
    parser.add_argument("-p", metavar="attributes", dest="attributes", help="attribute range")
    parser.add_argument("-x", metavar="num folds", dest="numfolds", help="number of folds")
    parser.add_argument("-s", metavar="seed", dest="seed", help="seed value for randomization")
    parser.add_argument("-c", metavar="class index", dest="classindex", help="1-based class attribute index")
    parser.add_argument("-g", metavar="graph", dest="graph", help="graph output file (if supported)")
    parser.add_argument("clusterer", help="clusterer classname, e.g., weka.clusterers.SimpleKMeans")
    parser.add_argument("option", nargs=argparse.REMAINDER, help="additional clusterer options")
    parsed = parser.parse_args()
    jars = []
    if not parsed.classpath is None:
        jars = parsed.classpath.split(os.pathsep)
    params = []
    if not parsed.train is None:
        params.extend(["-t", parsed.train])
    if not parsed.test is None:
        params.extend(["-T", parsed.test])
    if not parsed.outmodel is None:
        params.extend(["-d", parsed.outmodel])
    if not parsed.inmodel is None:
        params.extend(["-l", parsed.inmodel])
    if not parsed.attributes is None:
        params.extend(["-p", parsed.attributes])
    if not parsed.numfolds is None:
        params.extend(["-x", parsed.numfolds])
    if not parsed.seed is None:
        params.extend(["-s", parsed.seed])
    if not parsed.classindex is None:
        params.extend(["-c", parsed.classindex])
    if not parsed.graph is None:
        params.extend(["-g", parsed.graph])

    jvm.start(jars, max_heap_size=parsed.heap, packages=True)

    logger.debug("Commandline: " + utils.join_options(sys.argv[1:]))

    try:
        clusterer = Clusterer(classname=parsed.clusterer)
        if len(parsed.option) > 0:
            clusterer.set_options(parsed.option)
        print(ClusterEvaluation.evaluate_clusterer(clusterer, params))
    except Exception, e:
        print(e)
    finally:
        jvm.stop()

if __name__ == "__main__":
    try:
        main()
    except Exception, ex:
        print(ex)
