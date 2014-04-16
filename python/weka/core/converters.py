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
import weka.core.jvm as jvm
from weka.core.classes import OptionHandler
from weka.core.capabilities import Capabilities
from weka.core.dataset import Instances


class Loader(OptionHandler):
    """
    Wrapper class for Loaders.
    """
    
    def __init__(self, classname="weka.core.converters.ArffLoader"):
        """
        Initializes the specified loader.
        :param classname: the classname of the loader
        """
        jobject = Loader.new_instance(classname)
        self.enforce_type(jobject, "weka.core.converters.Loader")
        super(Loader, self).__init__(jobject)

    def load_file(self, dfile):
        """
        Loads the specified file and returns the Instances object.
        :param dfile: the file to load
        """
        self.enforce_type(self.jobject, "weka.core.converters.FileSourcedConverter")
        if not javabridge.is_instance_of(dfile, "Ljava/io/File;"):
            dfile = javabridge.make_instance("Ljava/io/File;", "(Ljava/lang/String;)V", jvm.ENV.new_string_utf(str(dfile)))
        javabridge.call(self.jobject, "reset", "()V")
        javabridge.call(self.jobject, "setFile", "(Ljava/io/File;)V", dfile)
        return Instances(javabridge.call(self.jobject, "getDataSet", "()Lweka/core/Instances;"))
        
    def load_url(self, url):
        """
        Loads the specified URL and returns the Instances object.
        :param url: the URL to load the data from
        """
        self.enforce_type(self.jobject, "weka.core.converters.URLSourcedLoader")
        javabridge.call(self.jobject, "reset", "()V")
        javabridge.call(self.jobject, "setURL", "(Ljava/lang/String;)V", str(url))
        return Instances(javabridge.call(self.jobject, "getDataSet", "()Lweka/core/Instances;"))


class Saver(OptionHandler):
    """
    Wrapper class for Savers.
    """
    
    def __init__(self, classname="weka.core.converters.ArffSaver"):
        """
        Initializes the specified saver.
        :param classname: the classname of the saver
        """
        jobject = Saver.new_instance(classname)
        self.enforce_type(jobject, "weka.core.converters.Saver")
        super(Saver, self).__init__(jobject)

    def get_capabilities(self):
        """
        Returns the capabilities of the saver.
        :rtype: Capabilities
        """
        return Capabilities(javabridge.call(self.jobject, "getCapabilities", "()Lweka/core/Capabilities;"))

    def save_file(self, data, dfile):
        """
        Saves the Instances object in the specified file.
        :param data: the data to save
        :param dfile: the file to save the data to
        """
        self.enforce_type(self.jobject, "weka.core.converters.FileSourcedConverter")
        if not javabridge.is_instance_of(dfile, "Ljava/io/File;"):
            dfile = javabridge.make_instance("Ljava/io/File;", "(Ljava/lang/String;)V", jvm.ENV.new_string_utf(str(dfile)))
        javabridge.call(self.jobject, "setFile", "(Ljava/io/File;)V", dfile)
        javabridge.call(self.jobject, "setInstances", "(Lweka/core/Instances;)V", data.jobject)
        javabridge.call(self.jobject, "writeBatch", "()V")
