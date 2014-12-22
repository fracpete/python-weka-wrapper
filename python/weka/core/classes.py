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
# Copyright (C) 2014 Fracpete (pythonwekawrapper at gmail dot com)

import types
import javabridge
from javabridge import JWrapper, JClassWrapper
from javabridge.jutil import JavaException


class JavaObject(object):
    """
    Basic Java object.
    """
    
    def __init__(self, jobject):
        """
        Initializes the wrapper with the specified Java object.
        :param jobject: the Java object to wrap
        :type jobject: JB_Object
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

    def __unicode__(self):
        """
        Just calls the toString() method.
        :rtype: str
        """
        return javabridge.to_string(self.jobject)

    def set_property(self, path, jobject):
        """
        Attempts to set the value (jobject, a Java object) of the provided (bean) property path.
        :param path: the property path, e.g., "filter" for a setFilter(...)/getFilter() method pair
        :type path: str
        :param jobject: the Java object to set; if instance of JavaObject class, the jobject member is
        automatically used
        :type jobject: JB_Object
        """
        # unwrap?
        if isinstance(jobject, JavaObject):
            jobject = jobject.jobject

        javabridge.static_call(
            "Lweka/core/PropertyPath;", "setValue",
            "(Ljava/lang/Object;Ljava/lang/String;Ljava/lang/Object;)V",
            self.jobject, path, jobject)

    def get_property(self, path):
        """
        Attempts to get the value (jobject, a Java object) of the provided (bean) property path.
        :param path: the property path, e.g., "filter" for a setFilter(...)/getFilter() method pair
        :type path: str
        :return the wrapped Java object
        :rtype: JavaObject
        """
        return JavaObject(javabridge.static_call(
            "Lweka/core/PropertyPath;", "getValue",
            "(Ljava/lang/Object;Ljava/lang/String;)Ljava/lang/Object;",
            self.jobject, path))

    def jwrapper(self):
        """
        Returns a JWrapper instance of the encapsulated Java object, giving access to methods
        using dot notation.
        http://pythonhosted.org//javabridge/highlevel.html#wrapping-java-objects-using-reflection
        :return: the wrapper
        :rtype: JWrapper
        """
        return JWrapper(self.jobject)

    def jclasswrapper(self):
        """
        Returns a JClassWrapper instance of the class for the encapsulated Java object, giving
        access to the class methods using dot notation.
        http://pythonhosted.org//javabridge/highlevel.html#wrapping-java-objects-using-reflection
        :return: the wrapper
        :rtype: JClassWrapper
        """
        return JClassWrapper(javabridge.call(self.jobject, "getClass", "()Ljava/lang/Class;"))

    @classmethod
    def check_type(cls, jobject, intf_or_class, jni_intf_or_class=None):
        """
        Returns whether the object implements the specified interface or is a subclass. 
        E.g.: self._check_type('weka.core.OptionHandler', 'Lweka/core/OptionHandler;') 
        or self._check_type('weka.core.converters.AbstractFileLoader')
        :param jobject: the Java object to check
        :type jobject: JB_Object
        :param intf_or_class: the classname in Java notation (eg "weka.core.Instance")
        :type intf_or_class: str
        :param jni_intf_or_class: the classname in JNI notation (eg "Lweka/core/Instance;")
        :type jni_intf_or_class: str
        :return: whether object implements interface or is subclass
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
        :type jobject: JB_Object
        :param intf_or_class: the classname in Java notation (eg "weka.core.Instance")
        :type intf_or_class: str
        :param jni_intf_or_class: the classname in JNI notation (eg "Lweka/core/Instance;")
        :type jni_intf_or_class: str
        """
        if not cls.check_type(jobject, intf_or_class, jni_intf_or_class):
            raise TypeError("Object does not implement or subclass " + intf_or_class + "!")

    @classmethod
    def new_instance(cls, classname, jni_classname=None):
        """
        Creates a new object from the given classname using the default constructor, None in case of error.
        :param classname: the classname in Java notation (eg "weka.core.Instance")
        :type classname: str
        :param jni_classname: the classname in JNI notation (eg "Lweka/core/Instance;")
        :type jni_classname: str
        :return: the Java object
        :rtype: JB_Object
        """
        if jni_classname is None:
            jni_classname = classname.replace(".", "/")
        try:
            return javabridge.make_instance(jni_classname, "()V")
        except JavaException, e:
            print("Failed to instantiate " + classname + "/" + jni_classname + ": " + str(e))
            return None


class Random(JavaObject):
    """
    Wrapper for the java.util.Random class.
    """

    def __init__(self, seed):
        """
        The seed value.
        :param seed: the seed value
        :type seed: int
        """
        super(Random, self).__init__(javabridge.make_instance("Ljava/util/Random;", "(J)V", seed))

    def next_int(self, n=None):
        """
        Next random integer. if n is provided, then between 0 and n-1.
        :param n: the upper limit (minus 1) for the random integer
        :type n: int
        :return: the next random integer
        :rtype: int
        """
        if n is None:
            return javabridge.call(self.jobject, "nextInt", "()I")
        else:
            return javabridge.call(self.jobject, "nextInt", "(I)I", n)

    def next_double(self):
        """
        Next random double.
        :return: the next random double
        :rtype: double
        """
        return javabridge.call(self.jobject, "nextDouble", "()D")


class OptionHandler(JavaObject):
    """
    Ancestor for option-handling classes. 
    Classes should implement the weka.core.OptionHandler interface to have any effect.
    """
    
    def __init__(self, jobject, options=None):
        """
        Initializes the wrapper with the specified Java object.
        :param jobject: the java object to wrap
        :type jobject: JB_Object
        :param options: the options to set
        :type options: list
        """
        super(OptionHandler, self).__init__(jobject)
        self.is_optionhandler = OptionHandler.check_type(jobject, "weka.core.OptionHandler")
        if (not options is None) and (len(options) > 0):
            self.options = options
        
    def global_info(self):
        """
        Returns the globalInfo() result, None if not available.
        :rtypes: str
        """
        try:
            return javabridge.call(self.jobject, "globalInfo", "()Ljava/lang/String;")
        except JavaException:
            return None

    @property
    def options(self):
        """
        Obtains the currently set options as list.
        :return: the list of options
        :rtype: list
        """
        if self.is_optionhandler:
            return types.string_array_to_list(javabridge.call(self.jobject, "getOptions", "()[Ljava/lang/String;"))
        else:
            return []

    @options.setter
    def options(self, options):
        """
        Sets the command-line options (as list).
        :param options: the list of command-line options to set
        :type options: list
        """
        if self.is_optionhandler:
            javabridge.call(self.jobject, "setOptions", "([Ljava/lang/String;)V", types.string_list_to_array(options))

    def to_commandline(self):
        """
        Generates a commandline string from the JavaObject instance.
        :return: the commandline string
        :rtype: str
        """
        return javabridge.static_call(
            "Lweka/core/Utils;", "toCommandLine",
            "(Ljava/lang/Object;)Ljava/lang/String;",
            self.jobject)

    def __str__(self):
        """
        Calls the toString() method of the java object.
        :return: the result of the toString() method
        :rtype: str
        """
        return javabridge.to_string(self.jobject)


class SingleIndex(JavaObject):
    """
    Wrapper for a Weka SingleIndex object.
    """

    def __init__(self, jobject=None, index=None):
        """
        Initializes the wrapper with the specified Java object or string index.
        :param jobject: the java object to wrap
        :type jobject: JB_Object
        :param index: the string index to use
        :type index: str
        """
        if jobject is None:
            if index is None:
                jobject = javabridge.make_instance("weka/core/SingleIndex", "()V")
            else:
                jobject = javabridge.make_instance("weka/core/SingleIndex", "(Ljava/lang/String;)V", index)
        else:
            self.enforce_type(jobject, "weka.core.SingleIndex")
        super(SingleIndex, self).__init__(jobject)

    def upper(self, upper):
        """
        Sets the upper limit.
        :param upper: the upper limit
        :type upper: int
        """
        javabridge.call(self.jobject, "setUpper", "(I)V", upper)

    def index(self):
        """
        Returns the integer index.
        :return: the 0-based integer index
        :rtype: int
        """
        return javabridge.call(self.jobject, "getIndex", "()I")

    @property
    def single_index(self):
        """
        Returns the string index.
        :return: the 1-based string index
        :rtype: str
        """
        return javabridge.call(self.jobject, "getSingleIndex", "()Ljava/lang/String;")

    @single_index.setter
    def single_index(self, index):
        """
        Sets the string index.
        :param index: the 1-based string index
        ::type index: str
        """
        javabridge.call(self.jobject, "setSingleIndex", "(Ljava/lang/String;)V", index)


class Range(JavaObject):
    """
    Wrapper for a Weka Range object.
    """

    def __init__(self, jobject=None, ranges=None):
        """
        Initializes the wrapper with the specified Java object or string range.
        :param jobject: the java object to wrap
        :type jobject: JB_Object
        :param ranges: the string range to use
        :type ranges: str
        """
        if jobject is None:
            if ranges is None:
                jobject = javabridge.make_instance("weka/core/Range", "()V")
            else:
                jobject = javabridge.make_instance("weka/core/Range", "(Ljava/lang/String;)V", ranges)
        else:
            self.enforce_type(jobject, "weka.core.Range")
        super(Range, self).__init__(jobject)

    def upper(self, upper):
        """
        Sets the upper limit.
        :param upper: the upper limit
        :type upper: int
        """
        javabridge.call(self.jobject, "setUpper", "(I)V", upper)

    def selection(self):
        """
        Returns the selection list.
        :return: the list of 0-based integer indices
        :rtype: list
        """
        return javabridge.get_env().get_int_array_elements(javabridge.call(self.jobject, "getSelection", "()[I"))

    @property
    def ranges(self):
        """
        Returns the string range.
        :return: the string range of 1-based indices
        :rtype: str
        """
        return javabridge.call(self.jobject, "getRanges", "()Ljava/lang/String;")

    @ranges.setter
    def ranges(self, rng):
        """
        Sets the string range.
        :param rng: the range to set
        :type rng: str
        """
        javabridge.call(self.jobject, "setRanges", "(Ljava/lang/String;)V", rng)

    @property
    def invert(self):
        """
        Returns whether the range is inverted.
        :return: true if inverted
        :rtype: bool
        """
        return javabridge.call(self.jobject, "getInvert", "()Z")

    @invert.setter
    def invert(self, invert):
        """
        Sets the invert state.
        :param invert: whether to invert or not
        :type invert: bool
        """
        javabridge.call(self.jobject, "setInvert", "(Z)V", invert)


class Tag(JavaObject):
    """
    Wrapper for the weka.core.Tag class.
    """

    def __init__(self, jobject=None, ident=None, ident_str="", readable="", uppercase=True):
        """
        :param jobject: the java object to wrap
        :type jobject: JB_Object
        :param ident: the ID integer associated with the tag
        :type ident: int
        :param ident_str: the ID string associated with the tag (case-insensitive)
        :type ident_str: str
        :param readable: the text of the tag
        :type readable: str
        :param uppercase: whether to uppercase the id string
        :type uppercase: bool
        """
        if jobject is None:
            jobject = javabridge.make_instance(
                "weka/core/Tag", "(ILjava/lang/String;Ljava/lang/String;Z)V",
                ident, ident_str, readable, uppercase)
        else:
            self.enforce_type(jobject, "weka.core.Tag")
        super(Tag, self).__init__(jobject)

    @property
    def ident(self):
        """
        Returns the current integer ID of the tag.
        :return: the integer ID
        :rtype: int
        """
        return javabridge.call(self.jobject, "getID", "()I")

    @ident.setter
    def ident(self, value):
        """
        Sets the integer ID of the tag.
        :param value: the new ID
        :type value: int
        """
        javabridge.call(self.jobject, "setID", "(I)V", value)

    @property
    def identstr(self):
        """
        Returns the current ID string.
        :return: the ID string
        :rtype: str
        """
        return javabridge.call(self.jobject, "getIDStr", "()Ljava/lang/String;")

    @identstr.setter
    def identstr(self, value):
        """
        Sets the ID string.
        :param value: the new ID string
        :type value: str
        """
        javabridge.call(self.jobject, "setIDStr", "(Ljava/lang/String;)V", value)

    @property
    def readable(self):
        """
        Returns the 'human readable' string.
        :return: the readable string
        :rtype: str
        """
        return javabridge.call(self.jobject, "getReadable", "()Ljava/lang/String;")

    @readable.setter
    def readable(self, value):
        """
        Sets the 'human readable' string.
        :param value: the new readable string
        :type value: str
        """
        javabridge.call(self.jobject, "setReadable", "(Ljava/lang/String;)V", value)


class SelectedTag(JavaObject):
    """
    Wrapper for the weka.core.SelectedTag class.
    """

    def __init__(self, jobject=None, tag_id=None, tag_text=None, tags=None):
        """
        Initializes the wrapper with the specified Java object or tags and either tag_id or tag_text.
        :param jobject: the java object to wrap
        :type jobject: JB_Object
        :param tag_id: the integer associated with the tag
        :type tag_id: int
        :param tag_text: the text associated with the tag
        :type tag_text: str
        :param tags: list of Tag objects
        :type tags: list
        """
        if jobject is None:
            if tag_id is None:
                jobject = javabridge.make_instance(
                    "weka/core/SelectedTag", "(Ljava/lang/String;I])V", tag_text, tags)
            else:
                jobject = javabridge.make_instance(
                    "weka/core/SelectedTag", "(II])V", tag_id, tags)
        else:
            self.enforce_type(jobject, "weka.core.SelectedTag")
        super(SelectedTag, self).__init__(jobject)

    @property
    def selected(self):
        """
        Returns the selected tag.
        :return: the tag
        :rtype: Tag
        """
        return Tag(javabridge.call(self.jobject, "getSelectedTag", "()Lweka/core/Tag;"))

    @property
    def tags(self):
        """
        Returns the associated tags.
        :return: the list of Tag objects
        :rtype: list
        """
        result = []
        a = javabridge.call(self.jobject, "getTags", "()Lweka/core/Tag;]")
        length = javabridge.get_env().get_array_length(a)
        wrapped = javabridge.get_env().get_object_array_elements(a)
        for i in xrange(length):
            result.append(Tag(javabridge.get_env().get_string(wrapped[i])))
        return result
