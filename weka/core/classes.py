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

import javabridge
import arrays
import jvm

class WekaObject(object):
    """ Basic Weka object. """
    
    def __init__(self, jobject):
        """ Initializes the wrapper with the specified Java object. """
        if jobject == None:
            raise Exception("No Java object supplied!")
        self.jobject = jobject

    def _check_type(self, jobject, intf_or_class, jni_intf_or_class = None):
        """
        Returns whether the object implements the specified interface or is a subclass. 
        E.g.: self._check_type('weka.core.OptionHandler', 'Lweka/core/OptionHandler;') 
        or self._check_type('weka.core.converters.AbstractFileLoader')
        """
        if jni_intf_or_class == None:
            jni_intf_or_class = "L" + intf_or_class.replace(".", "/") + ";"
        return javabridge.is_instance_of(jobject, jni_intf_or_class)
        
    def _enforce_type(self, jobject, intf_or_class, jni_intf_or_class = None):
        """
        Raises an exception if the object does not implement the specified interface or is not a subclass. 
        E.g.: self._enforce_type('weka.core.OptionHandler', 'Lweka/core/OptionHandler;') 
        or self._enforce_type('weka.core.converters.AbstractFileLoader')
        """
        if not self._check_type(jobject, intf_or_class, jni_intf_or_class):
            raise TypeError("Object does not implement or subclass " + intf_or_class + "!")
 
    def __str__(self):
        """ Just calls the toString() method. """
        return javabridge.to_string(self.jobject)
       
    @classmethod
    def new_instance(cls, classname, jni_classname = None):
        """ Creates a new object from the given classname using the default constructor, None in case of error. """
        if jni_classname == None:
            jni_classname = classname.replace(".", "/")
        try:
            return javabridge.make_instance(jni_classname, "()V")
        except Exception, e:
            print("Failed to instantiate " + classname + "/" + jni_classname + ": " + e)
            return None


class OptionHandler(WekaObject):
    """
    Ancestor for option-handling classes. 
    Classes should implement the weka.core.OptionHandler interface to have any effect.
    """
    
    def __init__(self, jobject):
        """ Initializes the wrapper with the specified Java object. """
        super(OptionHandler, self).__init__(jobject)
        self.is_optionhandler = self._check_type(jobject, "weka.core.OptionHandler")
        
    def global_info(self):
        """ Returns the globalInfo() result, None if not available. """
        try:
            return javabridge.call(self.jobject, "globalInfo", "()Ljava/lang/String;")
        except:
            return None
        
    def set_options(self, options):
        """ Sets the command-line options (as list). """
        if self.is_optionhandler:
            javabridge.call(self.jobject, "setOptions", "([Ljava/lang/String;)V", arrays.string_list_to_array(options))
                                                       
    def get_options(self):
        """ Obtains the currently set options as list. """
        if self.is_optionhandler:
            return arrays.string_array_to_list(javabridge.call(self.jobject, "getOptions", "()[Ljava/lang/String;"))
        else:
            return []
                                                       
    def __str__(self):
        """ Obtains the currently set options as list. """
        return javabridge.to_string(self.jobject)
