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

# jvm.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import javabridge
import os


ENV = None
DEBUG = False


def start(class_path=[]):
    """
    Initializes the javabridge connection (starts up the JVM).
    :param class_path: the additional classpath elements to add
    """
    global ENV
    global DEBUG

    # add user-defined jars first
    for cp in class_path:
        javabridge.JARS.append(cp)

    # determine lib directory with jars
    rootdir = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]
    if os.path.exists(rootdir + os.sep + "lib"):
        libdir = rootdir + os.sep + "lib"
    else:
        libdir = os.path.split(rootdir)[0] + os.sep + "lib"

    # add jars from lib directory
    for l in os.listdir(libdir):
        if l.lower().endswith(".jar"):
            javabridge.JARS.append(libdir + os.sep + l)

    if DEBUG:
        print("classpath: " + str(javabridge.JARS))

    javabridge.start_vm(run_headless=True)
    javabridge.attach()
    ENV = javabridge.get_env()


def stop():
    """ Kills the JVM. """
    global ENV
    if not ENV is None:
        ENV = None
        javabridge.kill_vm()
