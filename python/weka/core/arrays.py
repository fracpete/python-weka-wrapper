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

# arrays.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import logging
import weka.core.jvm as jvm
import numpy

# logging setup
logger = logging.getLogger(__name__)


def string_array_to_list(a):
    """
    Turns the Java string array into Python unicode string list.
    :param a: the string array to convert
    :type a: JB_Object
    :return: the string list
    :rtype: list
    """
    result  = []
    len     = jvm.ENV.get_array_length(a)
    wrapped = jvm.ENV.get_object_array_elements(a)
    for i in xrange(len):
        result.append(jvm.ENV.get_string(wrapped[i]))
    return result


def string_list_to_array(l):
    """
    Turns a Python unicode string list into a Java String array.
    :param l: the string list
    :type: list
    :rtype: java string array
    :return: JB_Object
    """
    result = jvm.ENV.make_object_array(len(l), jvm.ENV.find_class("java/lang/String"))
    for i in xrange(len(l)):
        jvm.ENV.set_object_array_element(result, i, jvm.ENV.new_string_utf(l[i]))
    return result


def double_matrix_to_ndarray(m):
    """
    Turns the Java matrix (2-dim array) of doubles into a numpy 2-dim array.
    :param m: the double matrix
    :type: JB_Object
    :return: Numpy array
    :rtype: numpy.darray
    """
    rows   = jvm.ENV.get_object_array_elements(m)
    num    = jvm.ENV.get_array_length(m)
    result = numpy.zeros(num * num).reshape((num, num))
    i      = 0
    for row in rows:
        elements = jvm.ENV.get_double_array_elements(row)
        n        = 0
        for element in elements:
            result[i][n] = element
            n += 1
        i += 1
    return result
