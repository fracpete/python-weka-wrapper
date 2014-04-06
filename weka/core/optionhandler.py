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

# optionhandler.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import os
import javabridge
import arrays
import runner
from wekaobject import WekaObject

class OptionHandler(WekaObject):
    """
    Ancestor for option-handling classes. 
    Classes must implement the weka.core.OptionHandler interface.
    """
    
    def __init__(self, jobject):
        """ Initializes the wrapper with the specified Java object. """
        super(OptionHandler, self).__init__(jobject)
        if not javabridge.is_instance_of(jobject, "Lweka/core/OptionHandler;"):
            raise TypeError("Object does not implement weka.core.OptionHandler!")
        
    def global_info(self):
        """ Returns the globalInfo() result, None if not available. """
        try:
            return javabridge.call(self.jobject, "globalInfo", "()Ljava/lang/String;")
        except:
            return None
        
    def set_options(self, options):
        """ Sets the command-line options (as list). """
        javabridge.call(self.jobject, "setOptions", "([Ljava/lang/String;)V", Arrays.string_list_to_array(options))
                                                       
    def get_options(self):
        """ Obtains the currently set options as list. """
        return Arrays.string_array_to_list(javabridge.call(self.jobject, "getOptions", "()[Ljava/lang/String;"))
                                                       
    def __str__(self):
        """ Obtains the currently set options as list. """
        return javabridge.to_string(self.jobject)

#if __name__ == "__main__":
#    Runner.start(["/home/fracpete/development/waikato/projects/weka-HEAD/dist/weka.jar"])
#    try:
#        jo = javabridge.make_instance("weka/classifiers/trees/J48", "()V")
#        o = OptionHandler(jo)
#        print(o.get_options())
#        o.set_options(["-C", "0.5"])
#        print(o.get_options())
#        print(str(o))
#        print(o.global_info())
#    finally:
#        Runner.stop()
