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
# Copyright (C) 2014 Fracpete (pythonwekawrapper at gmail dot com)

import javabridge
import logging
import os
import sys
import argparse
import weka.core.jvm as jvm
import weka.core.utils as utils
from weka.core.classes import OptionHandler
from weka.core.capabilities import Capabilities
from weka.core.converters import Loader
from weka.core.converters import Saver
from weka.core.dataset import Instances
from weka.core.dataset import Instance

# logging setup
logger = logging.getLogger("weka.filters")


class Filter(OptionHandler):
    """
    Wrapper class for filters.
    """

    def __init__(self, classname=None, jobject=None, options=None):
        """
        Initializes the specified filter using either the classname or the supplied JB_Object.
        :param classname: the classname of the filter
        :type classname: str
        :param jobject: the JB_Object to use
        :type jobject: JB_Object
        :param options: the list of commandline options to set
        :type options: list
        """
        if jobject is None:
            jobject = Filter.new_instance(classname)
        self.enforce_type(jobject, "weka.filters.Filter")
        super(Filter, self).__init__(jobject=jobject, options=options)

    def get_capabilities(self):
        """
        Returns the capabilities of the filter.
        :return: the capabilities
        :rtype: Capabilities
        """
        return Capabilities(javabridge.call(self.jobject, "getCapabilities", "()Lweka/core/Capabilities;"))

    def set_inputformat(self, data):
        """
        Sets the input format.
        :param data: the data to use as input
        :type data: Instances
        """
        return javabridge.call(self.jobject, "setInputFormat", "(Lweka/core/Instances;)Z", data.jobject)

    def input(self, inst):
        """
        Inputs the Instance.
        :param inst: the instance to filter
        :type inst: Instance
        """
        return javabridge.call(self.jobject, "input", "(Lweka/core/Instance;)Z", inst.jobject)

    def get_outputformat(self):
        """
        Returns the output format.
        :return: the output format
        :rtype: Instances
        """
        inst = javabridge.call(self.jobject, "getOutputFormat", "()Lweka/core/Instances;")
        if inst is None:
            return None
        else:
            return Instances(inst)

    def output(self):
        """
        Outputs the filtered Instance.
        :return: the filtered instance
        :rtype: an Instance object
        """
        return Instance(javabridge.call(self.jobject, "output", "()Lweka/core/Instance;"))

    def filter(self, data):
        """
        Filters the dataset.
        :param data: the Instances to filter
        :type data: Instances
        :return: the filtered Instances object
        :rtype: Instances
        """
        return Instances(javabridge.static_call(
            "Lweka/filters/Filter;", "useFilter",
            "(Lweka/core/Instances;Lweka/filters/Filter;)Lweka/core/Instances;",
            data.jobject, self.jobject))


class MultiFilter(Filter):
    """
    Wrapper class for weka.filters.MultiFilter.
    """

    def __init__(self, jobject=None, options=None):
        """
        Initializes the MultiFilter instance using either creating new instance or using the supplied JB_Object.
        :param jobject: the JB_Object to use
        :type jobject: JB_Object
        :param options: list of commandline options
        :type options: list
        """
        if jobject is None:
            classname = "weka.filters.MultiFilter"
            jobject = MultiFilter.new_instance(classname)
        self.enforce_type(jobject, "weka.filters.MultiFilter")
        super(MultiFilter, self).__init__(jobject=jobject, options=options)

    def set_filters(self, filters):
        """
        Sets the base filters.
        :param filters: the list of base filters to use
        :type filters: list
        """
        obj = []
        for fltr in filters:
            obj.append(fltr.jobject)
        javabridge.call(self.jobject, "setFilters", "([Lweka/filters/Filter;)V", obj)

    def get_filters(self):
        """
        Returns the list of base filters.
        :return: the filter list
        :rtype: list
        """
        objects = javabridge.get_env().get_object_array_elements(
            javabridge.call(self.jobject, "getFilters", "()[Lweka/filters/Filter;"))
        result = []
        for obj in objects:
            result.append(Filter(jobject=obj))
        return result


def main():
    """
    Runs a filter from the command-line. Calls JVM start/stop automatically.
    Use -h to see all options.
    """
    parser = argparse.ArgumentParser(
        description='Executes a filter from the command-line. Calls JVM start/stop automatically.')
    parser.add_argument("-j", metavar="classpath", dest="classpath", help="additional classpath, jars/directories")
    parser.add_argument("-X", metavar="heap", dest="heap", help="max heap size for jvm, e.g., 512m")
    parser.add_argument("-i", metavar="input1", dest="input1", required=True, help="input file 1")
    parser.add_argument("-o", metavar="output1", dest="output1", required=True, help="output file 1")
    parser.add_argument("-r", metavar="input2", dest="input2", help="input file 2")
    parser.add_argument("-s", metavar="output2", dest="output2", help="output file 2")
    parser.add_argument("-c", metavar="classindex", default="-1", dest="classindex", help="1-based class attribute index")
    parser.add_argument("filter", help="filter classname, e.g., weka.filters.AllFilter")
    parser.add_argument("option", nargs=argparse.REMAINDER, help="additional filter options")
    parsed = parser.parse_args()
    if parsed.input2 is None and not parsed.output2 is None:
        raise Exception("No second input file provided ('-r ...')!")

    jars = []
    if not parsed.classpath is None:
        jars = parsed.classpath.split(os.pathsep)
    params = []
    if not parsed.input1 is None:
        params.extend(["-i", parsed.input1])
    if not parsed.output1 is None:
        params.extend(["-o", parsed.output1])
    if not parsed.input2 is None:
        params.extend(["-r", parsed.input2])
    if not parsed.output2 is None:
        params.extend(["-s", parsed.output2])
    if not parsed.classindex is None:
        params.extend(["-c", parsed.classindex])

    jvm.start(jars, max_heap_size=parsed.heap, packages=True)

    logger.debug("Commandline: " + utils.join_options(sys.argv[1:]))

    try:
        flter = Filter(parsed.filter)
        if len(parsed.option) > 0:
            flter.set_options(parsed.option)
        loader = Loader(classname="weka.core.converters.ArffLoader")
        in1 = loader.load_file(parsed.input1)
        cls = parsed.classindex
        if str(parsed.classindex) == "first":
            cls = "0"
        if str(parsed.classindex) == "last":
            cls = str(in1.num_attributes() - 1)
        in1.set_class_index(int(cls))
        flter.set_inputformat(in1)
        out1 = flter.filter(in1)
        saver = Saver(classname="weka.core.converters.ArffSaver")
        saver.save_file(out1, parsed.output1)
        if not parsed.input2 is None:
            in2 = loader.load_file(parsed.input2)
            in2.set_class_index(int(cls))
            out2 = flter.filter(in2)
            saver.save_file(out2, parsed.output2)
    except Exception, e:
        print(e)
    finally:
        jvm.stop()

if __name__ == "__main__":
    try:
        main()
    except Exception, ex:
        print(ex)
