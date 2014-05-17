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

# capabilities.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import javabridge
from weka.core.classes import JavaObject
from weka.core.dataset import Attribute, Instances


class Capability(JavaObject):
    """ Wrapper for a Capability. """

    def __init__(self, jobject):
        """
        Initializes the wrapper with the specified Capability object.
        :param jobject: the Capability object to wrap
        :type jobject: JB_Object
        """
        Capability.enforce_type(jobject, "weka.core.Capabilities$Capability")
        super(Capability, self).__init__(jobject)

    @classmethod
    def parse(cls, s):
        """
        Tries to instantiate a Capability object from the string representation.
        :param s: the string representing a Capability
        :type s: str
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
        :type jobject: JB_Object
        """
        Capabilities.enforce_type(jobject, "weka.core.Capabilities")
        super(Capabilities, self).__init__(jobject)

    def capabilities(self):
        """
        Returns all the capabilities.
        :return: all capabilities
        :rtype: list
        """
        result = []
        iterator = javabridge.iterate_java(javabridge.call(self.jobject, "capabilities", "()Ljava/util/Iterator;"))
        for c in iterator:
            result.append(Capability(c))
        return result

    def get_attribute_capabilities(self):
        """
        Returns all the attribute capabilities.
        :return: attribute capabilities
        :rtype: Capabilities
        """
        return Capabilities(
            javabridge.call(self.jobject, "getAttributeCapabilities", "()Lweka/core/Capabilities;"))

    def get_class_capabilities(self):
        """
        Returns all the class capabilities.
        :return: class capabilities
        :rtype: Capabilities
        """
        return Capabilities(
            javabridge.call(self.jobject, "getClassCapabilities", "()Lweka/core/Capabilities;"))

    def get_other_capabilities(self):
        """
        Returns all other capabilities.
        :return: all other capabilities
        :rtype: Capabilities
        """
        return Capabilities(
            javabridge.call(self.jobject, "getOtherCapabilities", "()Lweka/core/Capabilities;"))

    def dependencies(self):
        """
        Returns all the dependencies.
        :return: the dependency list
        :rtype: list
        """
        result = []
        iterator = javabridge.iterate_java(javabridge.call(self.jobject, "dependencies", "()Ljava/util/Iterator;"))
        for c in iterator:
            result.append(Capability(c))
        return result

    def enable_all(self):
        """
        enables all capabilities.
        """
        javabridge.call(self.jobject, "enableAll", "()V")

    def enable_all_attributes(self):
        """
        enables all attributes.
        """
        javabridge.call(self.jobject, "enableAllAttributes", "()V")

    def enable_all_classes(self):
        """
        enables all classes.
        """
        javabridge.call(self.jobject, "enableAllClasses", "()V")

    def enable(self, capability):
        """
        enables the specified capability.
        :param capability: the capability to enable
        :type capability: Capability
        """
        javabridge.call(self.jobject, "enable", "(Lweka/core/Capabilities$Capability;)V", capability.jobject)

    def enable_all_attribute_dependencies(self):
        """
        enables all attribute dependencies.
        """
        javabridge.call(self.jobject, "enableAllAttributeDependencies", "()V")

    def enable_all_class_dependencies(self):
        """
        enables all class dependencies.
        """
        javabridge.call(self.jobject, "enableAllClassDependencies", "()V")

    def enable_dependency(self, capability):
        """
        enables the dependency of the given capability enabling NOMINAL_ATTRIBUTES also enables
        BINARY_ATTRIBUTES, UNARY_ATTRIBUTES and EMPTY_NOMINAL_ATTRIBUTES.
        :param capability: the dependency to enable
        :type capability: Capability
        """
        javabridge.call(
            self.jobject, "enableDependency", "(Lweka/core/Capabilities$Capability;)V", capability.jobject)

    def disable_all(self):
        """
        Disables all capabilities.
        """
        javabridge.call(self.jobject, "disableAll", "()V")

    def disable_all_attributes(self):
        """
        Disables all attributes.
        """
        javabridge.call(self.jobject, "disableAllAttributes", "()V")

    def disable_all_classes(self):
        """
        Disables all classes.
        """
        javabridge.call(self.jobject, "disableAllClasses", "()V")

    def disable(self, capability):
        """
        Disables the specified capability.
        :param capability: the capability to disable
        :type capability: Capability
        """
        javabridge.call(self.jobject, "disable", "(Lweka/core/Capabilities$Capability;)V", capability.jobject)

    def disable_all_attribute_dependencies(self):
        """
        Disables all attribute dependencies.
        """
        javabridge.call(self.jobject, "disableAllAttributeDependencies", "()V")

    def disable_all_class_dependencies(self):
        """
        Disables all class dependencies.
        """
        javabridge.call(self.jobject, "disableAllClassDependencies", "()V")

    def disable_dependency(self, capability):
        """
        Disables the dependency of the given capability Disabling NOMINAL_ATTRIBUTES also disables
        BINARY_ATTRIBUTES, UNARY_ATTRIBUTES and EMPTY_NOMINAL_ATTRIBUTES.
        :param capability: the dependency to disable
        :type capability: Capability
        """
        javabridge.call(
            self.jobject, "disableDependency", "(Lweka/core/Capabilities$Capability;)V", capability.jobject)

    def has_dependencies(self):
        """
        Returns whether any dependencies are set.
        :return: whether any dependecies are set
        :rtype: bool
        """
        return javabridge.call(self.jobject, "hasDependencies", "()Z")

    def has_dependency(self, capability):
        """
        Returns whether the specified dependency is set
        :param capability: the capability to check
        :type capability: Capability
        :return: whether the dependency is set
        :rtype: bool
        """
        return javabridge.call(
            self.jobject, "hasDependency", "(Lweka/core/Capabilities$Capability;)Z", capability.jobject)

    def supports(self, capabilities):
        """
        Returns true if the currently set capabilities support at least all of the capabiliites of the given
        Capabilities object (checks only the enum!)
        :param capabilities: the capabilities to check
        :type capabilities: Capabilities
        :return: whether the current capabilities support at least the specified ones
        :rtype: bool
        """
        return javabridge.call(self.jobject, "supports", "(Lweka/core/Capabilities;)Z", capabilities.jobject)

    def supports_maybe(self, capabilities):
        """
        Returns true if the currently set capabilities support (or have a dependency) at least all of the
        capabilities of the given Capabilities object (checks only the enum!)
        :param capabilities: the capabilities to check
        :type capabilities: Capabilities
        :return: whether the current capabilities (potentially) support the specified ones
        :rtype: bool
        """
        return javabridge.call(self.jobject, "supportsMaybe", "(Lweka/core/Capabilities;)Z", capabilities.jobject)

    def set_min_instances(self, minimum):
        """
        Sets the minimum number of instances that must be supported.
        :param minimum: the minimum number
        :type minimum: int
        """
        javabridge.call(self.jobject, "setMinimumNumberInstances", "(I)V", minimum)

    def get_min_instances(self):
        """
        Returns the minimum number of instances that must be supported.
        :return: the minimum number
        :rtype: int
        """
        return javabridge.call(self.jobject, "getMinimumNumberInstances", "()I")

    def test_attribute(self, att, is_class=None, fail=False):
        """
        Tests whether the attribute meets the conditions.
        :param att: the Attribute to test
        :type att: Attribute
        :param is_class: whether this attribute is the class attribute
        :type is_class: bool
        :param fail: whether to fail with an exception in case the test fails
        :type fail: bool
        :return: whether the attribute meets the conditions
        :rtype: bool
        """
        if fail:
            if is_class is None:
                return javabridge.call(
                    self.jobject, "test", "(Lweka/core/Attribute;)Z", att.jobject)
            else:
                return javabridge.call(
                    self.jobject, "test", "(Lweka/core/Attribute;Z)Z", att.jobject, is_class)
        else:
            if is_class is None:
                return javabridge.call(
                    self.jobject, "testWithFail", "(Lweka/core/Attribute;)Z", att.jobject)
            else:
                return javabridge.call(
                    self.jobject, "testWithFail", "(Lweka/core/Attribute;Z)Z", att.jobject, is_class)

    def test_instances(self, data, from_index=None, to_index=None, fail=False):
        """
        Tests whether the dataset meets the conditions.
        :param data: the Instances to test
        :type data: Instances
        :param from_index: the first attribute to include
        :type from_index: int
        :param to_index: the last attribute to include
        :type to_index: int
        :return: wether the dataset meets the requirements
        :rtype: bool
        """
        if fail:
            if (from_index is None) or (to_index is None):
                return javabridge.call(
                    self.jobject, "test", "(Lweka/core/Instances;)Z", data.jobject)
            else:
                return javabridge.call(
                    self.jobject, "test", "(Lweka/core/Instances;II)Z", data.jobject, from_index, to_index)
        else:
            if (from_index is None) or (to_index is None):
                return javabridge.call(
                    self.jobject, "testWithFail", "(Lweka/core/Instances;)Z", data.jobject)
            else:
                return javabridge.call(
                    self.jobject, "testWithFail", "(Lweka/core/Instances;II)Z", data.jobject, from_index, to_index)

    @classmethod
    def for_instances(cls, data, multi=None):
        """
        returns a Capabilities object specific for this data. The minimum number of instances is not set, the check
        for multi-instance data is optional.
        :param data: the data to generate the capabilities for
        :type data: Instances
        :param multi: whether to check the structure, too
        :type multi: bool
        :return: the generated capabilities
        :rtype: Capabilities
        """
        if multi is None:
            return Capabilities(javabridge.static_call(
                "weka/core/Capabilities", "forInstances",
                "(Lweka/core/Instances;)Lweka/core/Capabilities;", data.jobject))
        else:
            return Capabilities(javabridge.static_call(
                "weka/core/Capabilities", "forInstances",
                "(Lweka/core/Instances;Z)Lweka/core/Capabilities;", data.jobject, multi))
