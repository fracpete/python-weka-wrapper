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

ENV = None
DEBUG = False


def start(class_path=[]):
    """
    Initializes the javabridge connection (starts up the JVM).
    :param class_path: the additional classpath elements to add
    """
    global ENV
    global DEBUG
    for cp in class_path:
        javabridge.JARS.append(cp)
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
