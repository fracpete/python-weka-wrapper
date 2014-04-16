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

# classes.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import arrays
import javabridge
from javabridge.jutil import JavaException


class JavaObject(object):
    """ Basic Java object. """
    
    def __init__(self, jobject):
        """
        Initializes the wrapper with the specified Java object.
        :param jobject: the Java object to wrap
        """
        if jobject is None:
            raise Exception("No Java object supplied!")
        self.jobject = jobject

    def __str__(self):
        """
        Just calls the toString() method.
        :rtype: str
        """
        return javabridge.to_string(self.jobject)

    def set_property(self, path, jobject):
        """
        Attempts to set the value (jobject, a Java object) of the provided (bean) property path.
        :param path: the property path, e.g., "filter" for a setFilter(...)/getFilter() method pair
        :param jobject: the Java object to set
        """
        javabridge.static_call(
            "Lweka/core/PropertyPath;", "setValue",
            "(Ljava/lang/Object;Ljava/lang/String;Ljava/lang/Object;)V",
            self.jobject, path, jobject)

    def get_property(self, path):
        """
        Attempts to get the value (jobject, a Java object) of the provided (bean) property path.
        :param path: the property path, e.g., "filter" for a setFilter(...)/getFilter() method pair
        :rtype: JavaObject
        """
        return JavaObject(javabridge.static_call(
            "Lweka/core/PropertyPath;", "getValue",
            "(Ljava/lang/Object;Ljava/lang/String;)Ljava/lang/Object;",
            self.jobject, path))

    @classmethod
    def check_type(cls, jobject, intf_or_class, jni_intf_or_class=None):
        """
        Returns whether the object implements the specified interface or is a subclass. 
        E.g.: self._check_type('weka.core.OptionHandler', 'Lweka/core/OptionHandler;') 
        or self._check_type('weka.core.converters.AbstractFileLoader')
        :param jobject: the Java object to check
        :param intf_or_class: the classname in Java notation (eg "weka.core.Instance")
        :param jni_intf_or_class: the classname in JNI notation (eg "Lweka/core/Instance;")
        :rtype: bool
        """
        if jni_intf_or_class is None:
            jni_intf_or_class = "L" + intf_or_class.replace(".", "/") + ";"
        return javabridge.is_instance_of(jobject, jni_intf_or_class)
        
    @classmethod
    def enforce_type(cls, jobject, intf_or_class, jni_intf_or_class=None):
        """
        Raises an exception if the object does not implement the specified interface or is not a subclass. 
        E.g.: self._enforce_type('weka.core.OptionHandler', 'Lweka/core/OptionHandler;') 
        or self._enforce_type('weka.core.converters.AbstractFileLoader')
        :param jobject: the Java object to check
        :param intf_or_class: the classname in Java notation (eg "weka.core.Instance")
        :param jni_intf_or_class: the classname in JNI notation (eg "Lweka/core/Instance;")
        """
        if not cls.check_type(jobject, intf_or_class, jni_intf_or_class):
            raise TypeError("Object does not implement or subclass " + intf_or_class + "!")

    @classmethod
    def new_instance(cls, classname, jni_classname=None):
        """
        Creates a new object from the given classname using the default constructor, None in case of error.
        :param classname: the classname in Java notation (eg "weka.core.Instance")
        :param jni_classname: the classname in JNI notation (eg "Lweka/core/Instance;")
        :rtype: object
        """
        if jni_classname is None:
            jni_classname = classname.replace(".", "/")
        try:
            return javabridge.make_instance(jni_classname, "()V")
        except JavaException, e:
            print("Failed to instantiate " + classname + "/" + jni_classname + ": " + e)
            return None


class Capability(JavaObject):
    """ Wrapper for a Capability. """

    def __init__(self, jobject):
        """
        Initializes the wrapper with the specified Capability object.
        :param jobject: the Capability object to wrap
        """
        Capability.enforce_type(jobject, "weka.core.Capabilities$Capability")
        super(Capability, self).__init__(jobject)

    @classmethod
    def parse(cls, s):
        """
        Tries to instantiate a Capability object from the string representation.
        :param s: the string representing a Capability
        """
        return Capability(
            javabridge.static_call(
                "weka/core/Capabilities$Capability", "valueOf",
                "(Ljava/lang/String;)Lweka/core/Capabilities$Capability;", s))


class Capabilities(JavaObject):
    """ Wrapper for Capabilities. """

    def __init__(self, jobject):
        """
        Initializes the wrapper with the specified Capabilities object.
        :param jobject: the Capabilities object to wrap
        """
        Capabilities.enforce_type(jobject, "weka.core.Capabilities")
        super(Capabilities, self).__init__(jobject)

    def capabilities(self):
        """
        Returns all the capabilities.
        :rtype: list
        """
        result = []
        iter   = javabridge.iterate_java(javabridge.call(self.jobject, "capabilities", "()Ljava/util/Iterator;"))
        for c in iter:
            result.append(Capability(c))
        return result

    def dependencies(self):
        """
        Returns all the dependencies.
        :rtype: list
        """
        result = []
        iter   = javabridge.iterate_java(javabridge.call(self.jobject, "dependencies", "()Ljava/util/Iterator;"))
        for c in iter:
            result.append(Capability(c))
        return result

    def enable_all(self):
        """
        Enables all capabilities.
        """
        javabridge.call(self.jobject, "enableAll", "()V")

    def enable(self, capability):
        """
        Enables the specified capability.
        """
        javabridge.call(self.jobject, "enable", "(Lweka/core/Capabilities$Capability;)V", capability.jobject)

    def disable_all(self):
        """
        Disables all capabilities.
        """
        javabridge.call(self.jobject, "disableAll", "()V")

    def disable(self, capability):
        """
        Disables the specified capability.
        """
        javabridge.call(self.jobject, "disable", "(Lweka/core/Capabilities$Capability;)V", capability.jobject)


class Random(JavaObject):
    """
    Wrapper for the java.util.Random class.
    """

    def __init__(self, seed):
        """
        The seed value.
        :param seed: the seed value
        """
        super(Random, self).__init__(javabridge.make_instance("Ljava/util/Random;", "(J)V", seed))

    def next_int(self, n=None):
        """
        Next random integer. if n is provided, then between 0 and n-1.
        :param n: the upper limit (minus 1) for the random integer
        :rtype: int
        """
        if n is None:
            return javabridge.call(self.jobject, "nextInt", "()I")
        else:
            return javabridge.call(self.jobject, "nextInt", "(I)I")

    def next_double(self):
        """
        Next random double.
        :rtype: double
        """
        return javabridge.call(self.jobject, "nextDouble", "()D")


class OptionHandler(JavaObject):
    """
    Ancestor for option-handling classes. 
    Classes should implement the weka.core.OptionHandler interface to have any effect.
    """
    
    def __init__(self, jobject):
        """
        Initializes the wrapper with the specified Java object.
        :param jobject: the java object to wrap
        """
        super(OptionHandler, self).__init__(jobject)
        self.is_optionhandler = OptionHandler.check_type(jobject, "weka.core.OptionHandler")
        
    def global_info(self):
        """
        Returns the globalInfo() result, None if not available.
        :rtypes: str
        """
        try:
            return javabridge.call(self.jobject, "globalInfo", "()Ljava/lang/String;")
        except JavaException, e:
            return None
        
    def set_options(self, options):
        """
        Sets the command-line options (as list).
        :param options: the list of command-line options to set
        """
        if self.is_optionhandler:
            javabridge.call(self.jobject, "setOptions", "([Ljava/lang/String;)V", arrays.string_list_to_array(options))
                                                       
    def get_options(self):
        """
        Obtains the currently set options as list.
        :rtype: list
        """
        if self.is_optionhandler:
            return arrays.string_array_to_list(javabridge.call(self.jobject, "getOptions", "()[Ljava/lang/String;"))
        else:
            return []
                                                       
    def __str__(self):
        """
        Obtains the currently set options as list.
        :rtype: str
        """
        return javabridge.to_string(self.jobject)
