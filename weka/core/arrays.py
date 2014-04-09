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

import jvm

def string_array_to_list(array):
    """
    Turns the Java string array into Python unicode string list.
    :param array: the string array to convert
    :rtype: list
    """
    result  = []
    len     = jvm.ENV.get_array_length(array)
    wrapped = jvm.ENV.get_object_array_elements(array)
    for i in xrange(len):
        result.append(jvm.ENV.get_string(wrapped[i]))
    return result


def string_list_to_array(list):
    """
    Turns a Python unicode string list into a Java String array.
    :param list: the string list
    :rtype: java string array
    """
    result = jvm.ENV.make_object_array(len(list), jvm.ENV.find_class("java/lang/String"))
    for i in xrange(len(list)):
        jvm.ENV.set_object_array_element(result, i, jvm.ENV.new_string_utf(list[i]))
    return result
