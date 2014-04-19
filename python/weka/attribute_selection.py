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

# attribute_selection.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import javabridge
import logging
import os
import sys
import getopt
import weka.core.jvm as jvm
import weka.core.utils as utils
import weka.core.arrays as arrays
from weka.core.classes import JavaObject
from weka.core.classes import OptionHandler
from weka.core.classes import Random
from weka.core.capabilities import Capabilities
from weka.core.dataset import Instances
from weka.filters import Filter

# logging setup
logger = logging.getLogger("weka.attribute_selection")


class ASSearch(OptionHandler):
    """
    Wrapper class for attribute selection search algorithm.
    """

    def __init__(self, classname=None, jobject=None):
        """
        Initializes the specified search algorithm using either the classname or the supplied JB_Object.
        :param classname: the classname of the search algorithms
        :param jobject: the JB_Object to use
        """
        if jobject is None:
            jobject = ASSearch.new_instance(classname)
        if classname is None:
            classname = utils.get_classname(jobject)
        self.classname = classname
        self.enforce_type(jobject, "weka.attributeSelection.ASSearch")
        super(ASSearch, self).__init__(jobject)

    def search(self, evaluation, data):
        """
        Performs the search and returns the indices of the selected attributes.
        :param evaluation: the evaluation algorithm to use
        :param data: the data to use
        :rtype: ndarray
        """
        array = javabridge.call(
            self.jobject, "search", "(Lweka/attributeSelection/ASEvaluation;Lweka/core/Instances;)[I",
            evaluation.jobject, data.jobject)
        if array is None:
            return None
        else:
            jvm.ENV.get_int_array_elements(array)


class ASEvaluation(OptionHandler):
    """
    Wrapper class for attribute selection evaluation algorithm.
    """

    def __init__(self, classname=None, jobject=None):
        """
        Initializes the specified search algorithm using either the classname or the supplied JB_Object.
        :param classname: the classname of the search algorithms
        :param jobject: the JB_Object to use
        """
        if jobject is None:
            jobject = ASEvaluation.new_instance(classname)
        if classname is None:
            classname = utils.get_classname(jobject)
        self.classname = classname
        self.enforce_type(jobject, "weka.attributeSelection.ASEvaluation")
        super(ASEvaluation, self).__init__(jobject)

    def get_capabilities(self):
        """
        Returns the capabilities of the classifier.
        :rtype: Capabilities
        """
        return Capabilities(javabridge.call(self.jobject, "getCapabilities", "()Lweka/core/Capabilities;"))

    def build_evaluator(self, data):
        """
        Builds the evaluator with the data.
        :param data: the data to use
        """
        javabridge.call(self.jobject, "buildEvaluator", "(Lweka/core/Instances;)V", data.jobject)

    def post_process(self, indices):
        """
        Post-processes the evaluator with the selected attribute indices.
        :param indices: the attribute indices list to use
        :rtype: ndarray
        """
        array = javabridge.call(self.jobject, "postProcess", "([I)[I", indices)
        if array is None:
            return None
        else:
            return jvm.ENV.get_int_array_elements(array)


class AttributeSelection(JavaObject):
    """
    Performs attribute selection using search and evaluation algorithms.
    """
    pass
