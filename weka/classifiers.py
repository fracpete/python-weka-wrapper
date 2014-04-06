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
from core.classes import OptionHandler

class Classifier(OptionHandler):
    """
    Wrapper class for classifiers.
    """
    
    def __init__(self, classname):
        """ Initializes the specified classifier. """
        jo = javabridge.make_instance(classname.replace(".", "/"), "()V")
        super(Classifier, self).__init__(jo)
        if not javabridge.is_instance_of(self.jobject, "Lweka/classifiers/Classifier;"):
            raise TypeError("Classifier does not implement weka.classifiers.Classifier!")
        
    def build_classifier(self, data):
        """ Builds the classifier with the data. """
        # TODO
        
    def classify_instance(self, inst):
        """ Peforms a prediction. """
        # TODO
        
    def distribution_for_instance(self, inst):
        """ Peforms a prediction, returning the class distribution. """
        # TODO

if __name__ == "__main__":
    # only for testing
    jvm.start(["/home/fracpete/development/waikato/projects/weka-HEAD/dist/weka.jar"])
    try:
        cl = Classifier("weka.classifiers.trees.J48")
        print(cl)
    except Exception, e:
        print(e)
    finally:
        jvm.stop()
