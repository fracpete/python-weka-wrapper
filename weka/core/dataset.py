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

# dataset.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import javabridge
import core.jvm as jvm
from core.classes import WekaObject

class Instances(WekaObject):
    """
    Wrapper class for weka.core.Instances.
    """
    
    def __init__(self, jobject):
        """ Initializes the weka.core.Instances wrapper. """
        self._enforce_type(jobject, "weka.core.Instances")
        super(Instances, self).__init__(jobject)

    def num_attributes(self):
        """ Returns the number of attributes. """
        return javabridge.call(self.jobject, "numAttributes", "()I")
        
    def num_instances(self):
        """ Returns the number of instances. """
        return javabridge.call(self.jobject, "numInstances", "()I")
        
    def get_class_index(self):
        """ Returns the currently set class index (0-based). """
        return javabridge.call(self.jobject, "classIndex", "()I")
        
    def set_class_index(self, index):
        """ Sets the class index (0-based). """
        return javabridge.call(self.jobject, "setClassIndex", "(I)V", index)
        
    def get_instance(self, index):
        """ Returns the Instance object at the specified location. """
        return Instance(javabridge.call(self.jobject, "instance", "(I)Lweka/core/Instance;", index))

class Instance(WekaObject):
    """
    Wrapper class for weka.core.Instance.
    """
    
    def __init__(self, jobject):
        """ Initializes the weka.core.Instance wrapper. """
        self._enforce_type(jobject, "weka.core.Instance")
        super(Instances, self).__init__(jobject)

    def num_attributes(self):
        """ Returns the number of attributes. """
        return javabridge.call(self.jobject, "numAttributes", "()I")
        
    def get_class_index(self):
        """ Returns the currently set class index. """
        return javabridge.call(self.jobject, "classIndex", "()I")
    
    def get_value(self, index):
        """ Returns the internal value at the specified position (0-based). """
        return javabridge.call(self.jobject, "value", "(I)I", index)
    
    def set_value(self, index, value):
        """ Sets the internal value at the specified position (0-based). """
        return javabridge.call(self.jobject, "value", "(ID)V", index, value)
        
    def get_weight(self):
        """ Returns the currently set weight. """
        return javabridge.call(self.jobject, "weight", "()D")
        
    def set_weight(self, weight):
        """ Sets the weight. """
        return javabridge.call(self.jobject, "setWeight", "(D)V", weight)
        
