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
