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

# clusterers.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import javabridge
import core.jvm as jvm
from core.classes import OptionHandler

class Clusterer(OptionHandler):
    """
    Wrapper class for clusterers.
    """
    
    def __init__(self, classname):
        """ Initializes the specified clusterer. """
        jo = javabridge.make_instance(classname.replace(".", "/"), "()V")
        super(Clusterer, self).__init__(jo)
        if not javabridge.is_instance_of(self.jobject, "Lweka/clusterers/Clusterer;"):
            raise TypeError("Clusterer does not implement weka.clusterers.Clusterer!")
        
    def build_clusterer(self, data):
        """ Builds the clusterer with the data. """
        # TODO
        
    def cluster_instance(self, inst):
        """ Peforms a prediction. """
        # TODO

if __name__ == "__main__":
    # only for testing
    jvm.start(["/home/fracpete/development/waikato/projects/weka-HEAD/dist/weka.jar"])
    try:
        cl = Clusterer("weka.clusterers.SimpleKMeans")
        print(cl)
    except Exception, e:
        print(e)
    finally:
        jvm.stop()
