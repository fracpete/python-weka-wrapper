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
from weka.core.classes import JavaObject


class Instances(JavaObject):
    """
    Wrapper class for weka.core.Instances.
    """
    
    def __init__(self, jobject):
        """
        Initializes the weka.core.Instances wrapper.
        :param jobject: the weka.core.Instances object to wrap
        """
        self._enforce_type(jobject, "weka.core.Instances")
        super(Instances, self).__init__(jobject)

    def get_relationname(self):
        """
        Returns the name of the dataset.
        :rtype: str
        """
        return javabridge.call(self.jobject, "relationName", "()Ljava/lang/String;")

    def num_attributes(self):
        """
        Returns the number of attributes.
        :rtype: int
        """
        return javabridge.call(self.jobject, "numAttributes", "()I")
        
    def get_attribute(self, index):
        """
        Returns the specified attribute.
        :rtype: Attribute
        """
        return Attribute(javabridge.call(self.jobject, "attribute", "(I)Lweka/core/Attribute;"))
        
    def num_instances(self):
        """
        Returns the number of instances.
        :rtype: int
        """
        return javabridge.call(self.jobject, "numInstances", "()I")
        
    def get_class_attribute(self):
        """
        Returns the currently set class attribute.
        :rtype: Attribute
        """
        return Attribute(javabridge.call(self.jobject, "classAttribute", "()Lweka/core/Attribute;"))
        
    def get_class_index(self):
        """
        Returns the currently set class index (0-based).
        :rtype: int
        """
        return javabridge.call(self.jobject, "classIndex", "()I")
        
    def set_class_index(self, index):
        """ Sets the class index (0-based). """
        return javabridge.call(self.jobject, "setClassIndex", "(I)V", index)
        
    def get_instance(self, index):
        """
        Returns the Instance object at the specified location.
        :param index: the 0-based index of the instance
        :rtype: Instance
        """
        return Instance(javabridge.call(self.jobject, "instance", "(I)Lweka/core/Instance;", index))
        
    def add_instance(self, inst, index=None):
        """
        Adds the specified instance to the dataset.
        :param inst: Instance
        :param index: the 0-based index where to add the Instance
        """
        if index is None:
            javabridge.call(self.jobject, "add", "(Lweka/core/Instance;)Z", inst.jobject)
        else:
            javabridge.call(self.jobject, "add", "(ILweka/core/Instance;)V", index, inst.jobject)
        
    def set_instance(self, index, inst):
        """
        Sets the Instance at the specified location in the dataset.
        :param index: the 0-based index of the instance to replace
        :param inst: the Instance to set
        :rtype: Instance
        """
        return Instance(javabridge.call(self.jobject, "set", "(ILweka/core/Instance;)Lweka/core/Instance;", index, inst.jobject))
            
    def delete(self, index=None):
        """
        Removes either the specified Instance or all Instance objects.
        :param index: the 0-based index of the instance to remove
        """
        if index is None:
            javabridge.call(self.jobject, "delete", "()V")
        else:
            javabridge.call(self.jobject, "delete", "(I)V", index)
            
    def sort(self, index):
        """
        Sorts the dataset using the specified attribute index.
        :param index: the index of the attribute
        """
        javabridge.call(self.jobject, "sort", "(I)V", index)


class Instance(JavaObject):
    """
    Wrapper class for weka.core.Instance.
    """
    
    def __init__(self, jobject):
        """
        Initializes the weka.core.Instance wrapper.
        :param jobject: the weka.core.Instance object to initialize with
        """
        self._enforce_type(jobject, "weka.core.Instance")
        super(Instances, self).__init__(jobject)

    def num_attributes(self):
        """
        Returns the number of attributes.
        :rtype: int
        """
        return javabridge.call(self.jobject, "numAttributes", "()I")
        
    def get_class_index(self):
        """
        Returns the currently set class index.
        :rtype: int
        """
        return javabridge.call(self.jobject, "classIndex", "()I")
    
    def get_value(self, index):
        """
        Returns the internal value at the specified position (0-based).
        :param index: the 0-based index of the inernal value
        :rtype: float
        """
        return javabridge.call(self.jobject, "value", "(I)D", index)
    
    def set_value(self, index, value):
        """
        Sets the internal value at the specified position (0-based).
        :param index: the 0-based index of the attribute
        :param value: the internal float value to set
        """
        javabridge.call(self.jobject, "value", "(ID)V", index, value)
        
    def get_weight(self):
        """
        Returns the currently set weight.
        :rtype: float
        """
        return javabridge.call(self.jobject, "weight", "()D")
        
    def set_weight(self, weight):
        """
        Sets the weight.
        :param weight: the float weight to set
        """
        javabridge.call(self.jobject, "setWeight", "(D)V", weight)
        

class Attribute(JavaObject):
    """
    Wrapper class for weka.core.Attribute.
    """
    
    def __init__(self, jobject):
        """ Initializes the weka.core.Attribute wrapper. """
        self._enforce_type(jobject, "weka.core.Attribute")
        super(Attribute, self).__init__(jobject)

    def get_name(self):
        """
        Returns the name of the attribute.
        :rtype: str
        """
        return javabridge.call(self.jobject, "name", "()Ljava/lang/String;")
        
    def get_index(self):
        """
        Returns the index of this attribute.
        :rtype: int
        """
        return javabridge.call(self.jobject, "index", "()I")

    def set_weight(self, weight):
        """
        Sets the weight of the attribute.
        :param weight: the weight of the attribute
        """
        javabridge.call(self.jobject, "setWeight", "(D)V")

    def get_weight(self):
        """
        Returns the weight of the attribute.
        :rtype: float
        """
        return javabridge.call(self.jobject, "weight", "()D")

    def index_of(self, label):
        """
        Returns the index of the label in this attribute.
        :param label: the string label to get the index for
        :rtype: int
        """
        return javabridge.call(self.jobject, "indexOf", "(Ljava/lang/String;)I")

    def value(self, index):
        """
        Returns the label for the index.
        :param index: the 0-based index of the label to  return
        :rtype: str
        """
        return javabridge.call(self.jobject, "value", "(I)Ljava/lang/String;")

    def get_type(self):
        """
        Returns the type of the attribute.
        :rtype: int
        """
        return javabridge.call(self.jobject, "type", "()I")

    def is_date(self):
        """
        Returns whether the attribute is a date one.
        :rtype: bool
        """
        return javabridge.call(self.jobject, "isDate", "()Z")

    def is_nominal(self):
        """
        Returns whether the attribute is a nominal one.
        :rtype: bool
        """
        return javabridge.call(self.jobject, "isNominal", "()Z")

    def is_numeric(self):
        """
        Returns whether the attribute is a numeric one.
        :rtype: bool
        """
        return javabridge.call(self.jobject, "isNumeric", "()Z")

    def is_relation_valued(self):
        """
        Returns whether the attribute is a relation valued one.
        :rtype: bool
        """
        return javabridge.call(self.jobject, "isRelationValued", "()Z")

    def is_string(self):
        """
        Returns whether the attribute is a string attribute.
        :rtype: bool
        """
        return javabridge.call(self.jobject, "isString", "()Z")

    def get_date_format(self):
        """
        Returns the format of this data attribute.
        :rtype: str
        """
        return javabridge.call(self.jobject, "getDateFormat", "()Ljava/lang/String;")

    def get_lower_numeric_bound(self):
        """
        Returns the lower numeric bound of the numeric attribute.
        :rtype: float
        """
        return javabridge.call(self.jobject, "getLowerNumericBound", "()D")

    def get_upper_numeric_bound(self):
        """
        Returns the upper numeric bound of the numeric attribute.
        :rtype: float
        """
        return javabridge.call(self.jobject, "getUpperNumericBound", "()D")

    def is_in_range(self, value):
        """
        Checks whether the value is within the bounds of the numeric attribute.
        :param value: the numeric value to check
        :rtype: bool
        """
        return javabridge.call(self.jobject, "isInRange", "(D)Z", value)

    def add_string_value(self, s):
        """
        Adds the string value, returns the index.
        :param s: the string to add
        :rtype: int
        """
        return javabridge.call(self.jobject, "addStringValue", "(S)I", s)

    def add_relation(self, instances):
        """
        Adds the relation value, returns the index.
        :param instances: the Instances object to add
        :rtype: int
        """
        return javabridge.call(self.jobject, "addRelation", "(Lweka/core/Instances;)I", instances.jobject)

    def equals(self, att):
        """
        Checks whether this attributes is the same as the provided one.
        :param att: the Attribute to check against
        :rtype: bool
        """
        return javabridge.call(self.jobject, "equals", "(Lweka/core/Attribute;)Z", att.jobject)

    def equals_msg(self, att):
        """
        Checks whether this attributes is the same as the provided one.
        Returns None if the same, otherwise error message.
        :param att: the Attribute to check against
        :rtype: str
        """
        return javabridge.call(self.jobject, "equalsMsg", "(Lweka/core/Attribute;)Ljava/lang/String;", att.jobject)
