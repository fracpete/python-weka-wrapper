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
import logging


ENV = None

# logging setup
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def add_bundled_jars():
    """
     Adds the bundled jars to the JVM's classpath.
    """
    # determine lib directory with jars
    rootdir = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]
    if os.path.exists(rootdir + os.sep + "lib"):
        libdir = rootdir + os.sep + "lib"
    else:
        libdir = os.path.split(rootdir)[0] + os.sep + "lib"

    # add jars from lib directory
    for l in os.listdir(libdir):
        if l.lower().endswith(".jar") and (l.lower().find("-src.") == -1):
            javabridge.JARS.append(libdir + os.sep + l)


def add_weka_packages():
    """
    Adds the jars from all Weka packages to the JVM's classpath.
    """
    package_dir = os.path.expanduser("~" + os.sep + "wekafiles" + os.sep + "packages")
    logger.debug("package_dir=" + package_dir)
    # traverse packages
    for p in os.listdir(package_dir):
        if os.path.isdir(package_dir + os.sep + p):
            directory = package_dir + os.sep + p
            logger.debug("  directory=" + directory)
            # inspect package
            for l in os.listdir(directory):
                if l.lower().endswith(".jar"):
                    javabridge.JARS.append(directory + os.sep + l)
                if l == "lib":
                    for m in os.listdir(directory + os.sep + "lib"):
                        if m.lower().endswith(".jar"):
                            javabridge.JARS.append(directory + os.sep + "lib" + os.sep + m)


def add_system_classpath():
    """
    Adds the system's classpath to the JVM's classpath.
    """
    if not os.environ['CLASSPATH'] is None:
        parts = not os.environ['CLASSPATH'].split(os.pathsep)
        for part in parts:
            javabridge.JARS.append(part)


def start(class_path=[], bundled=True, packages=False, system_cp=False):
    """
    Initializes the javabridge connection (starts up the JVM).
    :param class_path: the additional classpath elements to add
    :param bundled: whether to add jars from the "lib" directory
    :param packages: whether to add jars from Weka packages as well
    :param system_cp: whether to add the system classpath as well
    """
    global ENV

    # add user-defined jars first
    for cp in class_path:
        logger.debug("Adding user-supplied classpath=" + class_path)
        javabridge.JARS.append(cp)

    if bundled:
        logger.debug("Adding bundled jars")
        add_bundled_jars()

    if packages:
        logger.debug("Adding Weka packages")
        add_weka_packages()

    if system_cp:
        logger.debug("Adding system classpath")
        add_system_classpath()

    logger.debug("Classpath=" + str(javabridge.JARS))

    javabridge.start_vm(run_headless=True)
    javabridge.attach()
    ENV = javabridge.get_env()


def stop():
    """ Kills the JVM. """
    global ENV
    if not ENV is None:
        ENV = None
        javabridge.kill_vm()
