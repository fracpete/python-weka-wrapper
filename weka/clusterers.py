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
import os
import sys
import getopt
import core.jvm as jvm
from core.classes import WekaObject
from core.classes import OptionHandler
from core.converters import Loader

class Clusterer(OptionHandler):
    """
    Wrapper class for clusterers.
    """
    
    def __init__(self, classname):
        """ Initializes the specified clusterer. """
        jobject = Clusterer.new_instance(classname)
        self._enforce_type(jobject, "weka.clusterers.Clusterer")
        super(Clusterer, self).__init__(jobject)
        
    def build_clusterer(self, data):
        """ Builds the clusterer with the data. """
        javabridge.call(self.jobject, "buildClusterer", "(Lweka/core/Instances;)V", data.jobject)
        
    def cluster_instance(self, inst):
        """ Peforms a prediction. """
        return javabridge.call(self.jobject, "clusterInstance", "(Lweka/core/Instance;)V", data.jobject)


class ClusterEvaluation(WekaObject):
    """
    Evaluation class for clusterers. 
    """
    
    def __init__(self):
        """ Initializes a ClusterEvaluation object. """
        super(ClusterEvaluation, self).__init__(ClusterEvaluation.new_instance("weka.clusterers.ClusterEvaluation"))
        
    @classmethod
    def evaluateClusterer(self, clusterer, args):
        return javabridge.static_call("Lweka/clusterers/ClusterEvaluation;", "evaluateClusterer", "(Lweka/clusterers/Clusterer;[Ljava/lang/String;)Ljava/lang/String;", clusterer.jobject, args)

def main(args):
    """
    Runs a filter from the command-line. Calls JVM start/stop automatically.
    Options:
        -j jar1[:jar2...]
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

    usage = "Usage: weka.clusterers -l jar1[" + os.pathsep + "jar2...] -t train [-T test] [-d output model file] [-l input model file] [-p attribute range] [-x num folds] [-s seed] [-c classindex] [-g graph file] clusterer classname [clusterer options]"
    optlist, args = getopt.getopt(args, "j:t:T:d:l:p:x:s:c:g:")
    if len(args) == 0:
        raise Exception("No clusterer classname provided!\n" + usage)
    for opt in optlist:
        if opt[0] == "-h":
            print(usage)
            return
        
    jars    = []
    params  = []
    train   = None
    for opt in optlist:
        if opt[0] == "-j":
            jars = opt[1].split(os.pathsep)
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
        elif opt[0] == "-x":
            params.append(opt[0])
            params.append(opt[1])
        elif opt[0] == "-g":
            params.append(opt[0])
            params.append(opt[1])
    
    # check parameters
    if train == None:
        raise Exception("No train file provided ('-t ...')!")
        
    jvm.start(jars)
    try:
        clusterer = Clusterer(args[0])
        args = args[1:]
        if len(args) > 0:
            clusterer.set_options(args)
        print(ClusterEvaluation.evaluateClusterer(clusterer, params))
    except Exception, e:
        print(e)
    finally:
        jvm.stop()

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception, e:
        print(e)
