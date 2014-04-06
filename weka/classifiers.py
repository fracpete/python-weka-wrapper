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

# classifiers.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import javabridge
import core.jvm as jvm
import core.classes as classes
from core.classes import OptionHandler
from core.converters import Loader

class Classifier(OptionHandler):
    """
    Wrapper class for classifiers.
    """
    
    def __init__(self, classname):
        """ Initializes the specified classifier. """
        jobject = Classifier.new_instance(classname)
        self._enforce_type(jobject, "weka.classifiers.Classifier")
        super(Classifier, self).__init__(jobject)
        
    def build_classifier(self, data):
        """ Builds the classifier with the data. """
        javabridge.call(self.jobject, "buildClassifier", "(Lweka/core/Instances;)V", data.jobject)
        
    def classify_instance(self, inst):
        """ Peforms a prediction. """
        return javabridge.call(self.jobject, "classifyInstance", "(Lweka/core/Instance;)V", data.jobject)
        
    def distribution_for_instance(self, inst):
        """ Peforms a prediction, returning the class distribution. """
        pred = javabridge.call(self.jobject, "distributionForInstance", "(Lweka/core/Instance;)V", data.jobject)
        return jvm.ENV.get_double_array_elements(pred)

if __name__ == "__main__":
    # only for testing
    jvm.start(["/home/fracpete/development/waikato/projects/weka-HEAD/dist/weka.jar"])
    try:
        cl     = Classifier("weka.classifiers.trees.J48")
        loader = Loader("weka.core.converters.ArffLoader")
        data   = loader.loadFile("/home/fracpete/development/waikato/datasets/uci/nominal/iris.arff")
        data.set_class_index(data.num_attributes() - 1)
        cl.build_classifier(data)
        print(cl)
    except Exception, e:
        print(e)
    finally:
        jvm.stop()
