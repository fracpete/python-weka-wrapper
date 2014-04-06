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

import javabridge
import os
import sys
import getopt
import core.jvm as jvm
import core.classes as classes
from core.classes import OptionHandler
from core.converters import Loader
from core.converters import Saver
from core.dataset import Instances
from core.dataset import Instance

class Filter(OptionHandler):
    """
    Wrapper class for filters.
    """
    
    def __init__(self, classname):
        """ Initializes the specified filter. """
        jobject = Filter.new_instance(classname)
        self._enforce_type(jobject, "weka.filters.Filter")
        super(Filter, self).__init__(jobject)
        
    def set_inputformat(self, data):
        """ Sets the input format. """
        return javabridge.call(self.jobject, "setInputFormat", "(Lweka/core/Instances;)Z", data.jobject)
        
    def input(self, inst):
        """ Inputs the Instance. """
        return javabridge.call(self.jobject, "input", "(Lweka/core/Instance;)Z", inst.jobject)
        
    def output(self):
        """ Outputs the filtered Instance. """
        return Instance(javabridge.call(self.jobject, "output", "()Lweka/core/Instance;"))
        
    def filter(self, data):
        """ Filters the dataset. """
        return Instances(javabridge.static_call("Lweka/filters/Filter;", "useFilter", "(Lweka/core/Instances;Lweka/filters/Filter;)Lweka/core/Instances;", data.jobject, self.jobject))

def main(args):
    """
    Runs a filter from the command-line. Calls JVM start/stop automatically.
    Use "-l jar1:..." to build the classpath (use ";" instead on Windows)
    The first argument after "-l classpath" is the classname of the Weka 
    filter class to execute, all others following are considered options
    """

    usage = "Usage: weka.filters -l jar1[" + os.pathsep + "jar2...] -i input1 -o output1 [-r input2 -s output2] [-c classindex] filterclass [filter options]"
    optlist, args = getopt.getopt(args, "l:i:o:r:s:c:h")
    if len(args) == 0:
        raise Exception("No filter classname provided!\n" + usage)
    for opt in optlist:
        if opt[0] == "-h":
            print(usage)
            return
        
    jars    = []
    input1  = None
    output1 = None
    input2  = None
    output2 = None
    cls     = "-1"
    for opt in optlist:
        if opt[0] == "-l":
            jars = opt[1].split(os.pathsep)
        elif opt[0] == "-i":
            input1 = opt[1]
        elif opt[0] == "-o":
            output1 = opt[1]
        elif opt[0] == "-r":
            input2 = opt[1]
        elif opt[0] == "-s":
            output2 = opt[1]
        elif opt[0] == "-c":
            cls = opt[1]
    
    # check parameters
    if input1 == None:
        raise Exception("No input file provided ('-i ...')!")
    if output1 == None:
        raise Exception("No output file provided ('-o ...')!")
    if input2 != None and output2 == None:
        raise Exception("No 2nd output file provided ('-s ...')!")
        
    jvm.start(jars)
    try:
        filter = Filter(args[0])
        args = args[1:]
        if len(args) > 0:
            filter.set_options(args)
        loader = Loader("weka.core.converters.ArffLoader")
        in1 = loader.loadFile(input1)
        if str(cls) == "first":
            cls = "0"
        if str(cls) == "last":
            cls = str(in1.num_attributes() - 1)
        in1.set_class_index(int(cls))
        filter.set_inputformat(in1)
        out1 = filter.filter(in1)
        saver = Saver("weka.core.converters.ArffSaver")
        saver.saveFile(out1, output1)
        if input2 != None:
            in2 = loader.loadFile(input2)
            in2.set_class_index(int(cls))
            out2 = filter.filter(in2)
            saver.saveFile(out2, output2)
    except Exception, e:
        print(e)
    finally:
        jvm.stop()

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception, e:
        print(e)
