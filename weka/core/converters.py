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

# converters.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import javabridge
import jvm
from classes import OptionHandler
from dataset import Instances

class Loader(OptionHandler):
    """
    Wrapper class for Loaders.
    """
    
    def __init__(self, classname):
        """ Initializes the specified loader. """
        jobject = Loader.new_instance(classname)
        self._enforce_type(jobject, "weka.core.converters.Loader")
        super(Loader, self).__init__(jobject)

    def loadFile(self, file):
        """ Loads the specified file and returns the Instances object. """
        self._enforce_type(self.jobject, "weka.core.converters.FileSourcedConverter")
        if not javabridge.is_instance_of(file, "Ljava/io/File;"):
            file = javabridge.make_instance("Ljava/io/File;", "(Ljava/lang/String;)V", jvm.ENV.new_string_utf(str(file)))
        javabridge.call(self.jobject, "reset", "()V")
        javabridge.call(self.jobject, "setFile", "(Ljava/io/File;)V", file)
        return Instances(javabridge.call(self.jobject, "getDataSet", "()Lweka/core/Instances;"))
        
    def loadURL(self, url):
        """ Loads the specified URL and returns the Instances object. """
        self._enforce_type(self.jobject, "weka.core.converters.URLSourcedLoader")
        javabridge.call(self.jobject, "reset", "()V")
        javabridge.call(self.jobject, "setURL", "(Ljava/lang/String;)V", str(url))
        return Instances(javabridge.call(self.jobject, "getDataSet", "()Lweka/core/Instances;"))


class Saver(OptionHandler):
    """
    Wrapper class for Savers.
    """
    
    def __init__(self, classname):
        """ Initializes the specified saver. """
        jobject = Saver.new_instance(classname)
        self._enforce_type(jobject, "weka.core.converters.Saver")
        super(Saver, self).__init__(jobject)

    def saveFile(self, data, file):
        """ Saves the Instances object in the specified fil. """
        self._enforce_type(self.jobject, "weka.core.converters.FileSourcedConverter")
        if not javabridge.is_instance_of(file, "Ljava/io/File;"):
            file = javabridge.make_instance("Ljava/io/File;", "(Ljava/lang/String;)V", jvm.ENV.new_string_utf(str(file)))
        javabridge.call(self.jobject, "setFile", "(Ljava/io/File;)V", file)
        javabridge.call(self.jobject, "setInstances", "(Lweka/core/Instances;)V", data.jobject)
        javabridge.call(self.jobject, "writeBatch", "()V")
