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

# runner.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import getopt
import javabridge
import os
import sys
import jvm
from classes import WekaObject
from classes import OptionHandler

def execute(args):
    """
    Runs a Weka class from the command-line. Calls start/stop automatically.
    Use "-l jar1:..." to build the classpath (use ";" instead on Windows)
    The first argument after "-l classpath" is the classname of the Weka class
    to execute, all others following are considered
    """

    optlist, args = getopt.getopt(args, "l:")
    if len(args) == 0:
        raise Exception("No classname provided!")
        
    jars = []
    for opt in optlist:
        if opt[0] == "-l":
            jars = opt[1].split(os.pathsep)
    jvm.start(jars)
    try:
        jo   = javabridge.make_instance(args[0].replace(".", "/"), "()V")
        print(" ".join(args))
        args = args[1:]
        if len(args) == 0:
            o = WekaObject(jo)
            print(str(o))
        else:
            o = OptionHandler(jo)
            o.set_options(args)
            print(str(o))
    except Exception, e:
        print(e)
    finally:
        jvm.stop()

if __name__ == "__main__":
    execute(sys.argv[1:])
