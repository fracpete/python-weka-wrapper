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

import javabridge
import logging
import os
import sys
import getopt
import weka.core.jvm as jvm
import weka.core.utils as utils
import weka.core.converters as converters
from weka.core.classes import OptionHandler
from weka.core.capabilities import Capabilities

# logging setup
logger = logging.getLogger("weka.associations")


class Associator(OptionHandler):
    """
    Wrapper class for associators.
    """

    def __init__(self, classname=None, jobject=None, options=None):
        """
        Initializes the specified associator using either the classname or the supplied JB_Object.
        :param classname: the classname of the associator
        :type classname: str
        :param jobject: the JB_Object to use
        :type jobject: JB_Object
        :param options: the list of commandline options to set
        :type options: list
        """
        if jobject is None:
            jobject = Associator.new_instance(classname)
        self.enforce_type(jobject, "weka.associations.Associator")
        super(Associator, self).__init__(jobject=jobject, options=options)

    def get_capabilities(self):
        """
        Returns the capabilities of the associator.
        :return: the capabilities
        :rtype: Capabilities
        """
        return Capabilities(javabridge.call(self.jobject, "getCapabilities", "()Lweka/core/Capabilities;"))

    def build_associations(self, data):
        """
        Builds the associator with the data.
        :param data: the data to train the associator with
        :type data: Instances
        """
        javabridge.call(self.jobject, "buildAssociations", "(Lweka/core/Instances;)V", data.jobject)


def main(args):
    """
    Runs a associator from the command-line. Calls JVM start/stop automatically.
    Options:
        [-j jar1[:jar2...]]
        [-X max heap size]
        -t train
        associator classname
        [associator options]
    """

    usage = "Usage: weka.associators [-j jar1[" + os.pathsep + "jar2...]] [-X max heap size] -t train [-T test] " \
            + "associator classname [associator options]"

    optlist, optargs = getopt.getopt(args, "j:X:t:h")
    if len(optargs) == 0:
        raise Exception("No associator classname provided!\n" + usage)
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

    # check parameters
    if train is None:
        raise Exception("No train file provided ('-t ...')!")

    jvm.start(jars, max_heap_size=heap, packages=True)

    logger.debug("Commandline: " + utils.join_options(args))

    try:
        associator = Associator(classname=optargs[0])
        optargs = optargs[1:]
        if len(optargs) > 0:
            associator.set_options(optargs)
        loader = converters.loader_for_file(train)
        data = loader.load_file(train)
        associator.build_associations(data)
        print(str(associator))
    except Exception, e:
        print(e)
    finally:
        jvm.stop()

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception, ex:
        print(ex)
