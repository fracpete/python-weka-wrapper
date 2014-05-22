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

import javabridge
import logging
import os
import sys
import getopt
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


def main(args):
    """
    Runs a clusterer from the command-line. Calls JVM start/stop automatically.
    Options:
        [-j jar1[:jar2...]]
        [-X max heap size]
        -t train
        [-T test]
        [-d output model file]
        [-l input model file]
        [-p attribute range]
        [-x num folds]
        [-s seed]
        [-c classindex]
        [-g graph file]
        clusterer classname
        [clusterer options]
    """

    usage = "Usage: weka.clusterers [-j jar1[" + os.pathsep + "jar2...]] [-X max heap size] " \
            + "-t train [-T test] [-d output model file] [-l input model file] " \
            + "[-p attribute range] [-x num folds] [-s seed] [-c classindex] " \
            + "[-g graph file] clusterer classname [clusterer options]"

    optlist, optargs = getopt.getopt(args, "j:X:t:T:d:l:p:x:s:c:g:h")
    if len(optargs) == 0:
        raise Exception("No clusterer classname provided!\n" + usage)
    for opt in optlist:
        if opt[0] == "-h":
            print(usage)
            return

    jars = []
    params = []
    train = None
    heap = None
    for opt in optlist:
        if opt[0] == "-j":
            jars = opt[1].split(os.pathsep)
        elif opt[0] == "-X":
            heap = opt[1]
        elif opt[0] == "-t":
            params.append(opt[0])
            params.append(opt[1])
            train = opt[1]
        elif opt[0] == "-T":
            params.append(opt[0])
            params.append(opt[1])
        elif opt[0] == "-d":
            params.append(opt[0])
            params.append(opt[1])
        elif opt[0] == "-l":
            params.append(opt[0])
            params.append(opt[1])
        elif opt[0] == "-p":
            params.append(opt[0])
            params.append(opt[1])
        elif opt[0] == "-x":
            params.append(opt[0])
            params.append(opt[1])
        elif opt[0] == "-s":
            params.append(opt[0])
            params.append(opt[1])
        elif opt[0] == "-c":
            params.append(opt[0])
            params.append(opt[1])
        elif opt[0] == "-g":
            params.append(opt[0])
            params.append(opt[1])

    # check parameters
    if train is None:
        raise Exception("No train file provided ('-t ...')!")

    jvm.start(jars, max_heap_size=heap, packages=True)

    logger.debug("Commandline: " + utils.join_options(args))

    try:
        clusterer = Clusterer(classname=optargs[0])
        optargs = optargs[1:]
        if len(optargs) > 0:
            clusterer.set_options(optargs)
        print(ClusterEvaluation.evaluate_clusterer(clusterer, params))
    except Exception, e:
        print(e)
    finally:
        jvm.stop()

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception, ex:
        print(ex)
