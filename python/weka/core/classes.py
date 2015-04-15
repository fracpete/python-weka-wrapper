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
# Copyright (C) 2014-2015 Fracpete (pythonwekawrapper at gmail dot com)

import inspect
import json
import logging
import re
import types
import javabridge
from javabridge import JWrapper, JClassWrapper
from javabridge.jutil import JavaException
from weka.core import types as arrays


def get_class(classname):
    """
    Returns the class object associated with the dot-notation classname.
    Taken from here: http://stackoverflow.com/a/452981
    :param classname: the classname
    :type classname: str
    :return: the class object
    :rtype: object
    """
    parts = classname.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


def get_jclass(classname):
    """
    Returns the Java class object associated with the dot-notation classname.
    :param classname: the classname
    :type classname: str
    :return: the class object
    :rtype: JB_Object
    """
    return javabridge.class_for_name(classname=classname)


def get_classname(obj):
    """
    Returns the classname of the JB_Object, Python class or object.
    :param obj: the java object or Python class/object to get the classname for
    :type obj: object
    :return: the classname
    :rtype: str
    """
    if isinstance(obj, javabridge.JB_Object):
        cls = javabridge.call(obj, "getClass", "()Ljava/lang/Class;")
        return javabridge.call(cls, "getName", "()Ljava/lang/String;")
    elif inspect.isclass(obj):
        return obj.__module__ + "." + obj.__name__
    else:
        return get_classname(obj.__class__)


class Stoppable(object):
    """
    Classes that can be stopped.
    """

    def is_stopped(self):
        """
        Returns whether the object has been stopped.
        :return: whether stopped
        :rtype: bool
        """
        raise Exception("Not implemented!")

    def stop_execution(self):
        """
        Triggers the stopping of the object.
        """
        raise Exception("Not implemented!")


class Configurable(object):
    """
    The ancestor for all actors.
    """

    def __init__(self, config=None):
        """
        Initializes the object.
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        self._logger = None
        self._help = {}
        self._config = self.fix_config({})
        if config is not None:
            self.config = config

    def __repr__(self):
        """
        Returns Python code for instantiating the object.
        :return: the representation
        :rtype: str
        """
        return \
            self.__class__.__module__ + "." + self.__class__.__name__ \
            + "(config=" + str(self.config) + ")"

    def description(self):
        """
        Returns a description of the object.
        :return: the description
        :rtype: str
        """
        raise Exception("Not implemented!")

    def fix_config(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.
        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        return options

    @property
    def config(self):
        """
        Obtains the currently set options of the actor.
        :return: the options
        :rtype: dict
        """
        return self._config

    @config.setter
    def config(self, options):
        """
        Sets the options of the actor.
        :param options: the options
        :type options: dict
        """
        self._config = self.fix_config(options)

    def to_config(self, k, v):
        """
        Hook method that allows conversion of individual options.
        :param k: the key of the option
        :type k: str
        :param v: the value
        :type v: object
        :return: the potentially processed value
        :rtype: object
        """
        if isinstance(v, Configurable):
            return v.to_config_dict()
        return v

    def to_config_dict(self):
        """
        Returns a dictionary of its options.
        :return: the options as dictionary
        :rtype: dict
        """
        result = {}
        result["class"] = get_classname(self)
        options = self.config.copy()
        result["options"] = {}
        for k in options.keys():
            result["options"][k] = self.to_config(k, options[k])
        return result

    def from_config(self, k, v):
        """
        Hook method that allows converting values from the dictionary
        :param k: the key in the dictionary
        :type k: str
        :param v: the value
        :type v: object
        :return: the potentially parsed value
        :rtype: object
        """
        if isinstance(v, dict):
            if "class" in v:
                cls = get_class(v["class"])
                obj = cls()
                if isinstance(obj, Configurable) and "options" in v:
                    obj.from_config_dict(v["options"])
                    return obj
                if isinstance(obj, OptionHandler) and ("jclass" in v):
                    jcls = v["jclass"]
                    jopt = None
                    if "joptions" in v:
                        jopt = split_options(v["joptions"])
                    return cls(classname=jcls, options=jopt)
        return v

    def from_config_dict(self, d):
        """
        Restores the object from the given options dictionary.
        :param d: the dictionary to use for restoring the options
        :type d: dict
        """
        for k in d.keys():
            if k in self.config:
                self.config[k] = self.from_config(k, d[k])
            elif k == "class":
                self = self.from_config(k, d[k])
            d.pop(k, None)

    @property
    def json(self):
        """
        Returns the options as JSON.
        :return: the object as string
        :rtype: str
        """
        return json.dumps(self.to_config_dict(), sort_keys=True, indent=2, separators=(',', ': '))

    @json.setter
    def json(self, s):
        """
        Restores the object from the given JSON.
        :param s: the JSON string to parse
        :type s: str
        """
        self.from_config_dict(json.loads(s))

    def new_logger(self):
        """
        Returns a new logger instance.
        :return: the logger instance
        :rtype: logger
        """
        return logging.getLogger(get_classname(self))

    @property
    def logger(self):
        """
        Returns the logger object.
        :return: the logger
        :rtype: logger
        """
        if self._logger is None:
            self._logger = self.new_logger()
        return self._logger

    @property
    def help(self):
        """
        Obtains the help information per option for this actor.
        :return: the help
        :rtype: dict
        """
        return self._help

    def generate_help(self):
        """
        Generates a help string for this actor.
        :return: the help string
        :rtype: str
        """
        result = []
        result.append(self.__class__.__name__)
        result.append(re.sub(r'.', '=', self.__class__.__name__))
        result.append("")
        result.append("DESCRIPTION")
        result.append(self.description())
        result.append("")
        result.append("OPTIONS")
        opts = self.config.keys()
        opts.sort()
        for opt in opts:
            result.append(opt)
            helpstr = self.help[opt]
            if helpstr is None:
                helpstr = "-missing help-"
            result.append("\t" + helpstr)
            result.append("")
        return '\n'.join(result)

    def print_help(self):
        """
        Prints a help string for this actor to stdout.
        """
        print(self.generate_help())


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

    def __repr__(self):
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

    @property
    def classname(self):
        """
        Returns the Java classname in dot-notation.
        :return: the Java classname
        :rtype: str
        """
        cls = javabridge.call(self.jobject, "getClass", "()Ljava/lang/Class;")
        return javabridge.call(cls, "getName", "()Ljava/lang/String;")

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

    @property
    def jclass(self):
        """
        Returns the Java class object of the underlying Java object.
        :return: the Java class
        :rtype: JB_Object
        """
        return javabridge.call(self.jobject, "getClass", "()Ljava/lang/Class;")

    @property
    def jwrapper(self):
        """
        Returns a JWrapper instance of the encapsulated Java object, giving access to methods
        using dot notation.
        http://pythonhosted.org//javabridge/highlevel.html#wrapping-java-objects-using-reflection
        :return: the wrapper
        :rtype: JWrapper
        """
        return JWrapper(self.jobject)

    @property
    def jclasswrapper(self):
        """
        Returns a JClassWrapper instance of the class for the encapsulated Java object, giving
        access to the class methods using dot notation.
        http://pythonhosted.org//javabridge/highlevel.html#wrapping-java-objects-using-reflection
        :return: the wrapper
        :rtype: JClassWrapper
        """
        return JClassWrapper(javabridge.call(self.jobject, "getClass", "()Ljava/lang/Class;"))

    @property
    def is_serializable(self):
        """
        Returns true if the object is serialiable.
        :return: true if serializable
        :rtype: bool
        """
        return JavaObject.check_type(self.jobject, "java.io.Serializable")

    @classmethod
    def check_type(cls, jobject, intf_or_class, jni_intf_or_class=None):
        """
        Returns whether the object implements the specified interface or is a subclass. 
        E.g.: self._check_type('weka.core.OptionHandler', 'Lweka/core/OptionHandler;') 
        or self._check_type('weka.core.converters.AbstractFileLoader')
        :param jobject: the Java object to check
        :type jobject: JB_Object
        :param intf_or_class: the classname in Java notation (eg "weka.core.DenseInstance;")
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
        :param intf_or_class: the classname in Java notation (eg "weka.core.DenseInstance")
        :type intf_or_class: str
        :param jni_intf_or_class: the classname in JNI notation (eg "Lweka/core/DenseInstance;")
        :type jni_intf_or_class: str
        """
        if not cls.check_type(jobject, intf_or_class, jni_intf_or_class):
            raise TypeError("Object does not implement or subclass " + intf_or_class + ": " + get_classname(jobject))

    @classmethod
    def new_instance(cls, classname, jni_classname=None):
        """
        Creates a new object from the given classname using the default constructor, None in case of error.
        :param classname: the classname in Java notation (eg "weka.core.DenseInstance")
        :type classname: str
        :param jni_classname: the classname in JNI notation (eg "Lweka/core/DenseInstance;")
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


class JavaArrayIterator(object):
    """
    Iterator for elements in a Java array.
    """
    def __init__(self, data):
        """
        :param data: the Java array to iterate over
        :type data: JavaArray
        """
        self.data = data
        self.index = 0
        self.length = len(data)

    def __iter__(self):
        """
        Returns itself.
        """
        return self

    def next(self):
        """
        Returns the next element from the array.
        :return: the next array element object, wrapped as JavaObject if not null
        :rtype: JavaObject or None
        """
        if self.index < self.length:
            index = self.index
            self.index += 1
            return self.data[index]
        else:
            raise StopIteration()


class JavaArray(JavaObject):
    """
    Convenience wrapper around Java arrays.
    """

    def __init__(self, jobject):
        """
        Initializes the wrapper with the specified Java object.
        :param jobject: the java array object to wrap
        :type jobject: JB_Object
        """
        super(JavaArray, self).__init__(jobject)
        c = self.jclass
        if not javabridge.call(c, "isArray", "()Z"):
            raise Exception("Not an array!")

    def __len__(self):
        """
        Returns the length of the array.
        :return: the array length
        :rtype: int
        """
        return javabridge.get_env().get_array_length(self.jobject)

    def __getitem__(self, key):
        """
        Returns the specified element in the array wrapped in a JavaObject.
        :param key: the index of the element to retrieve
        :type key: int
        :return: the element or None if element is null
        :rtype; JavaObject
        """
        if not isinstance(key, (int, long)):
            raise Exception("Key must be an integer!")
        element = javabridge.static_call(
            "Ljava/lang/reflect/Array;", "get", "(Ljava/lang/Object;I)Ljava/lang/Object;",
            self.jobject, key)
        if element is None:
            return None
        return JavaObject(element)

    def __setitem__(self, key, value):
        """
        Sets the specified element in the array.
        :param key: the index of the element to set
        :type key: int
        :param value: the object to set (JavaObject or JB_Object)
        """
        if isinstance(value, JavaObject):
            obj = value.jobject
        else:
            obj = value
        if not isinstance(key, (int, long)):
            raise Exception("Key must be an integer!")
        javabridge.static_call(
            "Ljava/lang/reflect/Array;", "set", "(Ljava/lang/Object;ILjava/lang/Object;)V",
            self.jobject, key, obj)

    def __delitem__(self, key):
        """
        Not implemented, raises an exception.
        """
        raise Exception("Cannot delete item from array!")

    def __iter__(self):
        """
        Returns an iterator over the elements.
        :return: the iterator
        :rtype: JavaArrayIterator
        """
        return JavaArrayIterator(self)

    @classmethod
    def new_instance(cls, classname, length):
        """
        Creates a new array with the given classname and length; initial values are null.
        :param classname: the classname in Java notation (eg "weka.core.DenseInstance")
        :type classname: str
        :param length: the length of the array
        :type length: int
        :return: the Java array
        :rtype: JB_Object
        """
        return javabridge.static_call(
            "Ljava/lang/reflect/Array;",
            "newInstance",
            "(Ljava/lang/Class;I)Ljava/lang/Object;",
            javabridge.class_for_name(classname=classname), length)


class Enum(JavaObject):
    """
    Wrapper for Java enums.
    """

    def __init__(self, jobject=None, enum=None, member=None):
        """
        Initializes the enum class.
        :param jobject: the Java object to wrap
        :type jobject: JB_Object
        :param enum: the enum class to instantiate (dot notation)
        :type enum: str
        :param member: the member of the enum class to instantiate
        :type member: str
        """
        if jobject is None:
            enumclass = javabridge.class_for_name(classname=enum)
            jobject = javabridge.static_call(
                "java/lang/Enum", "valueOf",
                "(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Enum;",
                enumclass, member)
        super(Enum, self).__init__(jobject)

    @property
    def name(self):
        """
        Returns the name of the enum member.
        :return: the name
        :rtype: str
        """
        return javabridge.call(self.jobject, "name", "()Ljava/lang/String;")

    @property
    def ordinal(self):
        """
        Returns the ordinal of the enum member.
        :return: the ordinal
        :rtype: int
        """
        return javabridge.call(self.jobject, "ordinal", "()I")

    @property
    def values(self):
        """
        Returns list of all enum members.
        :return: all enum members
        :rtype: list
        """
        cls = javabridge.call(self.jobject, "getClass", "()Ljava/lang/Class;")
        clsname = javabridge.call(cls, "getName", "()Ljava/lang/String;")
        l = javabridge.static_call(clsname.replace(".", "/"), "values", "()[L" + clsname.replace(".", "/") + ";")
        l = javabridge.get_env().get_object_array_elements(l)
        result = []
        for item in l:
            result.append(Enum(jobject=item))
        return result


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


class Option(JavaObject):
    """
    Wrapper for the weka.core.Option class.
    """

    def __init__(self, jobject):
        """
        Initializes the wrapper with the specified option object.
        :param jobject: the java object to wrap
        :type jobject: JB_Object
        """
        super(Option, self).__init__(jobject)
        Option.enforce_type(jobject, "weka.core.Option")

    @property
    def name(self):
        """
        Returns the name of the option.
        :return: the name
        :rtype: str
        """
        return javabridge.call(self.jobject, "name", "()Ljava/lang/String;")

    @property
    def description(self):
        """
        Returns the description of the option.
        :return: the description
        :rtype: str
        """
        return javabridge.call(self.jobject, "description", "()Ljava/lang/String;")

    @property
    def synopsis(self):
        """
        Returns the synopsis of the option.
        :return: the synopsis
        :rtype: str
        """
        return javabridge.call(self.jobject, "synopsis", "()Ljava/lang/String;")

    @property
    def num_arguments(self):
        """
        Returns the synopsis of the option.
        :return: the synopsis
        :rtype: str
        """
        return javabridge.call(self.jobject, "numArguments", "()I")


class OptionHandler(JavaObject, Configurable):
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
        if (options is not None) and (len(options) > 0):
            self.options = options
        # we have to manually instantiate some objects, since multiple inheritance doesn't call
        # Configurable constructor
        self._logger = None
        self._help = {}
        self._config = self.fix_config({})

    def global_info(self):
        """
        Returns the globalInfo() result, None if not available.
        :rtypes: str
        """
        try:
            return javabridge.call(self.jobject, "globalInfo", "()Ljava/lang/String;")
        except JavaException:
            return None

    def description(self):
        """
        Returns a description of the object.
        :return: the description
        :rtype: str
        """
        return self.global_info()

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

    def to_help(self):
        """
        Returns a string that contains the 'global_info' text and the options.
        :return: the generated help string
        :rtype: str
        """
        result = []
        result.append(self.classname)
        result.append("=" * len(self.classname))
        result.append("")
        result.append("DESCRIPTION")
        result.append("")
        result.append(self.global_info())
        result.append("")
        result.append("OPTIONS")
        result.append("")
        options = javabridge.call(self.jobject, "listOptions", "()Ljava/util/Enumeration;")
        enum = javabridge.get_enumeration_wrapper(options)
        while enum.hasMoreElements():
            opt = Option(enum.nextElement())
            result.append(opt.synopsis)
            result.append(opt.description)
            result.append("")
        return '\n'.join(result)

    def __str__(self):
        """
        Calls the toString() method of the java object.
        :return: the result of the toString() method
        :rtype: str
        """
        return javabridge.to_string(self.jobject)

    def to_config_dict(self):
        """
        Returns a dictionary of its options.
        :return: the options as dictionary
        :rtype: dict
        """
        result = super(OptionHandler, self).to_config_dict()
        result["jclass"] = get_classname(self.jobject)
        result["joptions"] = join_options(self.options)
        result.pop("options", None)
        return result


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


class Tags(JavaObject):
    """
    Wrapper for an array of weka.core.Tag objects.
    """

    def __init__(self, jobject=None, tags=None):
        """
        :param jobject: the Java Tag array to wrap.
        :type jobject: JB_Object
        :param tags: the list of Tag objects to use
        :type tags: list
        """
        if not tags is None:
            jarray = JavaArray(JavaArray.new_instance("weka.core.Tag", len(tags)))
            for i in range(len(tags)):
                jarray[i] = tags[i]
            jobject = jarray.jobject
        self.enforce_type(jobject, "weka.core.Tag", jni_intf_or_class="[Lweka/core/Tag;")
        super(Tags, self).__init__(jobject)
        self.array = JavaArray(self.jobject)

    def __len__(self):
        """
        Returns the number of Tag objects in the array.
        :return: the number of tag objects
        :rtype: int
        """
        return len(self.array)

    def __getitem__(self, item):
        """
        Returns the specified Tag from the array.
        :param item: the 0-based index
        :type item: int
        :return: the tag
        :rtype: Tag
        """
        return Tag(self.array[item])

    def __setitem__(self, key, value):
        """
        Not implemented.
        """
        raise Exception("Cannot set a Tag!")

    def __delitem__(self, key):
        """
        Not implemented.
        """
        raise Exception("Cannot delete a Tag!")

    def __str__(self):
        """
        Just calls the toString() method.
        :rtype: str
        """
        result = ""
        for i in xrange(len(self.array)):
            if i > 0:
                result += "|"
            result += str(self.array[i])
        return result


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
        :param tags: list of Tag objects or Tags wrapper object
        :type tags: list or Tags
        """

        if isinstance(tags, Tags):
            tobj = tags.jobject
        else:
            tobj = tags

        if jobject is None:
            if tag_id is None:
                jobject = javabridge.make_instance(
                    "weka/core/SelectedTag", "(Ljava/lang/String;[Lweka/core/Tag;)V", tag_text, tobj)
            else:
                jobject = javabridge.make_instance(
                    "weka/core/SelectedTag", "(I[Lweka/core/Tag;)V", tag_id, tobj)
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


def join_options(options):
    """
    Turns the list of options back into a single commandline string.
    :param options: the list of options to process
    :type options: list
    :return: the combined options
    :rtype: str
    """
    return javabridge.static_call(
        "Lweka/core/Utils;", "joinOptions",
        "([Ljava/lang/String;)Ljava/lang/String;",
        options)


def split_options(cmdline):
    """
    Splits the commandline into a list of options.
    :param cmdline: the commandline string to split into individual options
    :type cmdline: str
    :return: the split list of commandline options
    :rtype: list
    """
    return arrays.string_array_to_list(
        javabridge.static_call(
            "Lweka/core/Utils;", "splitOptions",
            "(Ljava/lang/String;)[Ljava/lang/String;",
            cmdline))


def to_commandline(optionhandler):
    """
    Generates a commandline string from the OptionHandler instance.
    :param optionhandler: the OptionHandler instance to turn into a commandline
    :type optionhandler: OptionHandler
    :return: the commandline string
    :rtype: str
    """
    return javabridge.static_call(
        "Lweka/core/Utils;", "toCommandLine",
        "(Ljava/lang/Object;)Ljava/lang/String;",
        optionhandler.jobject)


def from_commandline(cmdline, classname=None):
    """
    Creates an OptionHandler based on the provided commandline string.
    :param cmdline: the commandline string to use
    :type cmdline: str
    :param classname: the classname of the wrapper to return other than OptionHandler (in dot-notation)
    :type classname: str
    :return: the generated option handler instance
    :rtype: object
    """
    params = split_options(cmdline)
    cls = params[0]
    params = params[1:]
    handler = OptionHandler(jobject=javabridge.make_instance(cls.replace(".", "/"), "()V"), options=params)
    if classname is None:
        return handler
    else:
        c = get_class(classname)
        return c(jobject=handler.jobject)