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
import wekatests.coretests.capabilities
import wekatests.coretests.classes
import wekatests.coretests.converters
import wekatests.coretests.dataset
import wekatests.coretests.serialization
import wekatests.coretests.types
import wekatests.coretests.utils
import wekatests.coretests.version


"""
Executes all available tests for `weka.core`.
Add additional test suites to the `suite()` method.
"""


def suite():
    """
    Returns the test suite.
    :return: the test suite
    :rtype: unittest.TestSuite
    """
    suite = unittest.TestSuite()
    suite.addTests(wekatests.coretests.capabilities.suite())
    suite.addTests(wekatests.coretests.classes.suite())
    suite.addTests(wekatests.coretests.converters.suite())
    suite.addTests(wekatests.coretests.dataset.suite())
    suite.addTests(wekatests.coretests.serialization.suite())
    suite.addTests(wekatests.coretests.types.suite())
    suite.addTests(wekatests.coretests.utils.suite())
    suite.addTests(wekatests.coretests.version.suite())
    return suite


if __name__ == '__main__':
    jvm.start()
    unittest.TextTestRunner().run(suite())
    jvm.stop()
