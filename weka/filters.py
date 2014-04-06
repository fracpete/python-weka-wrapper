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

# filters.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import javabridge
import core.jvm as jvm
import core.classes as classes
from core.classes import OptionHandler
from core.converters import Loader
from core.dataset import Instances
from core.dataset import Instance

class Filter(OptionHandler):
    """
    Wrapper class for filters.
    """
    
    def __init__(self, classname):
        """ Initializes the specified filter. """
        jobject = Filter.new_instance(classname)
        self._enforce_type(jobject, "weka.filters.Filter")
        super(Filter, self).__init__(jobject)
        
    def set_inputformat(self, data):
        """ Sets the input format. """
        return javabridge.call(self.jobject, "setInputFormat", "(Lweka/core/Instances;)Z", data.jobject)
        
    def input(self, inst):
        """ Inputs the Instance. """
        return javabridge.call(self.jobject, "input", "(Lweka/core/Instance;)Z", inst.jobject)
        
    def output(self):
        """ Outputs the filtered Instance. """
        return Instance(javabridge.call(self.jobject, "output", "()Lweka/core/Instance;"))
        
    def filter(self, data):
        """ Filters the dataset. """
        return Instances(javabridge.static_call("Lweka/filters/Filter;", "useFilter", "(Lweka/core/Instances;Lweka/filters/Filter;)Lweka/core/Instances;", data.jobject, self.jobject))

if __name__ == "__main__":
    # only for testing
    jvm.start(["/home/fracpete/development/waikato/projects/weka-HEAD/dist/weka.jar"])
    try:
        filter = Filter("weka.filters.unsupervised.attribute.Remove")
        filter.set_options(["-R", "last"])
        loader = Loader("weka.core.converters.ArffLoader")
        data   = loader.loadFile("/home/fracpete/development/waikato/datasets/uci/nominal/iris.arff")
        data.set_class_index(data.num_attributes() - 1)
        print("class index: " + str(data.get_class_index()))
        print("class attr: " + str(data.get_class_attribute()))
        filter.set_inputformat(data)
        filtered = filter.filter(data)
        print("input:\n" + data.get_relationname() + "\n" + str(data))
        print("output:\n" + filtered.get_relationname() + "\n" + str(filtered))
    except Exception, e:
        print(e)
    finally:
        jvm.stop()
