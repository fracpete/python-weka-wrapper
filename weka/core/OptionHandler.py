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

# OptionHandler.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import javabridge

class OptionHandler:
    """
    Ancestor for option-handling classes. 
    must implement the weka.core.OptionHandler interface.
    """
    
    def __init__(self, jobject)
        """ Initializes the wrapper with the specified Java object. """
        javabridge.is_instance_of(jobject, "Lweka/core/OptionHandler;")
        self.jobject = jobject

if __name__ == "__main__":
    jo = javabridge.make_instance("weka/classifiers/trees/J48", "()V")
    o = OptionHandler(jo)
