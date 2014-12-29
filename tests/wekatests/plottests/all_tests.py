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

# all_tests.py
# Copyright (C) 2014 Fracpete (pythonwekawrapper at gmail dot com)

import unittest
import weka.core.jvm as jvm
import wekatests.plottests.classifiers
import wekatests.plottests.clusterers
import wekatests.plottests.dataset
import wekatests.plottests.graph


"""
Executes all available tests for `weka.plot`.
Add additional test suites to the `suite()` method.
"""


def suite():
    """
    Returns the test suite.
    :return: the test suite
    :rtype: unittest.TestSuite
    """
    suite = unittest.TestSuite()
    suite.addTests(wekatests.plottests.classifiers.suite())
    suite.addTests(wekatests.plottests.clusterers.suite())
    suite.addTests(wekatests.plottests.dataset.suite())
    suite.addTests(wekatests.plottests.graph.suite())
    return suite


if __name__ == '__main__':
    jvm.start()
    unittest.TextTestRunner().run(suite())
    jvm.stop()
