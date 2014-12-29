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
import wekatests.associations
import wekatests.attribute_selection
import wekatests.classifiers
import wekatests.clusterers
import wekatests.datagenerators
import wekatests.experiments
import wekatests.filters
import wekatests.coretests.all_tests
import wekatests.plottests.all_tests


"""
Executes all available tests.
Add additional test suites to the `suite()` method.
"""


def suite():
    """
    Returns the test suite.
    :return: the test suite
    :rtype: unittest.TestSuite
    """
    suite = unittest.TestSuite()
    suite.addTests(wekatests.associations.suite())
    suite.addTests(wekatests.attribute_selection.suite())
    suite.addTests(wekatests.classifiers.suite())
    suite.addTests(wekatests.clusterers.suite())
    suite.addTests(wekatests.datagenerators.suite())
    suite.addTests(wekatests.experiments.suite())
    suite.addTests(wekatests.filters.suite())
    suite.addTests(wekatests.coretests.all_tests.suite())
    suite.addTests(wekatests.plottests.all_tests.suite())
    return suite


if __name__ == '__main__':
    jvm.start()
    unittest.TextTestRunner().run(suite())
    jvm.stop()
