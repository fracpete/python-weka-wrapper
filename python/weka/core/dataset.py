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
import logging
import weka.core.jvm as jvm
from weka.core.classes import JavaObject

# logging setup
logger = logging.getLogger(__name__)


class Instances(JavaObject):
    """
    Wrapper class for weka.core.Instances.
    """
    
    def __init__(self, jobject):
        """
        Initializes the weka.core.Instances wrapper.
        :param jobject: the weka.core.Instances object to wrap
        """
        self.enforce_type(jobject, "weka.core.Instances")
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
        :param index: the 0-based index of the attribute
        :rtype: Attribute
        """
        return Attribute(javabridge.call(self.jobject, "attribute", "(I)Lweka/core/Attribute;"))

    def get_attribute_by_name(self, name):
        """
        Returns the specified attribute, None if not found.
        :param name: the name of the attribute
        :rtype: Attribute
        """
        att = javabridge.call(self.jobject, "attribute", "(Ljava/lang/String;)Lweka/core/Attribute;", name)
        if att is None:
            return None
        else:
            return Attribute(att)

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

    def delete_attribute(self, index):
        """
        Deletes an attribute at the given position.
        :param index: the 0-based index of the attribute to remove
        """
        javabridge.call(self.jobject, "deleteAttributeAt", "(I)V", index)

    def delete_attribute_type(self, type):
        """
        Deletes all attributes of the given type in the dataset.
        :param type: the attribute type to remove, see weka.core.Attribute Javadoc
        """
        javabridge.call(self.jobject, "deleteAttributeType", "(I)V", type)

    def compactify(self):
        """
        Compactifies the set of instances.
        """
        javabridge.call(self.jobject, "compactify", "()V")

    def sort(self, index):
        """
        Sorts the dataset using the specified attribute index.
        :param index: the index of the attribute
        """
        javabridge.call(self.jobject, "sort", "(I)V", index)

    @classmethod
    def copy_instances(cls, dataset):
        """
        Creates a copy of the Instances.
        :param dataset: the original dataset
        :rtype: Instances
        """
        return Instances(
            javabridge.make_instance(
                "weka/core/Instances", "(Lweka/core/Instances;)V", dataset.jobject))

    @classmethod
    def template_instances(cls, dataset, capacity=0):
        """
        Uses the Instances as template to create an empty dataset.
        :param dataset: the original dataset
        :param capacity: how many data rows to reserve initially (see compactify)
        :rtype: Instances
        """
        return Instances(
            javabridge.make_instance(
                "weka/core/Instances", "(Lweka/core/Instances;I)V", dataset.jobject, capacity))

    @classmethod
    def create_instances(cls, name, atts, capacity):
        """
        Creates a new Instances.
        :param name: the relation name
        :param atts: the list of attributes to use for the dataset
        :param capacity: how many data rows to reserve initially (see compactify)
        :rtype: Instances
        """
        attributes = []
        for att in atts:
            attributes.append(att.jobject)
        return Instances(
            javabridge.make_instance(
                "weka/core/Instances", "(Ljava/lang/String;Ljava/util/ArrayList;I)V",
                name, javabridge.make_list(attributes), capacity))


class Instance(JavaObject):
    """
    Wrapper class for weka.core.Instance.
    """
    
    def __init__(self, jobject):
        """
        Initializes the weka.core.Instance wrapper.
        :param jobject: the weka.core.Instance object to initialize with
        """
        self.enforce_type(jobject, "weka.core.Instance")
        super(Instance, self).__init__(jobject)

    def set_dataset(self, dataset):
        """
        Sets the dataset that this instance belongs to (for attribute information).
        :param dataset: the dataset this instance belongs to.
        """
        javabridge.call(self.jobject, "setDataset", "(Lweka/core/Instances;)V", dataset.jobject)

    def get_dataset(self):
        """
        Returns the dataset that this instance belongs to.
        :rtype: Instances
        """
        return Instances(javabridge.call(self.jobject, "dataset", "()Lweka/core/Instances"))

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

    def get_values(self):
        """
        Returns the internal values of this instance.
        :rtype: ndarray
        """
        return jvm.ENV.get_double_array_elements(javabridge.call(self.jobject, "toDoubleArray", "()[D"))

    @classmethod
    def create_instance(cls, values, classname="weka.core.DenseInstance", weight=1.0):
        """
        Creates a new instance.
        :param values: the double values (internal format) to use (numpy array)
        :param classname: the classname of the instance (eg weka.core.DenseInstance).
        :param weight: the weight of the instance
        """
        jni_classname = classname.replace(".", "/")
        return Instance(javabridge.make_instance(jni_classname, "(D[D)V", weight, jvm.ENV.make_double_array(values)))


class Attribute(JavaObject):
    """
    Wrapper class for weka.core.Attribute.
    """
    
    def __init__(self, jobject):
        """ Initializes the weka.core.Attribute wrapper. """
        self.enforce_type(jobject, "weka.core.Attribute")
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

    def parse_date(self, s):
        """
        Parses the date string and returns the internal format value.
        :param s: the date string
        :rtype: float
        """
        return javabridge.call(self.jobject, "parseDate", "(Ljava/lang/String;)D", s)

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

    @classmethod
    def create_numeric(cls, name):
        """
        Creates a numeric attribute.
        :param name: the name of the attribute
        """
        return Attribute(
            javabridge.make_instance(
                "weka/core/Attribute", "(Ljava/lang/String;)V", name))

    @classmethod
    def create_date(cls, name, format="yyyy-MM-dd'T'HH:mm:ss"):
        """
        Creates a date attribute.
        :param name: the name of the attribute
        :param format: the date format, see Javadoc for java.text.SimpleDateFormat
        """
        return Attribute(
            javabridge.make_instance(
                "weka/core/Attribute", "(Ljava/lang/String;Ljava/lang/String;)V", name, format))

    @classmethod
    def create_nominal(cls, name, labels):
        """
        Creates a date attribute.
        :param name: the name of the attribute
        :param labels: the list of string labels to use
        """
        return Attribute(
            javabridge.make_instance(
                "weka/core/Attribute", "(Ljava/lang/String;Ljava/util/List;)V", name, javabridge.make_list(labels)))
