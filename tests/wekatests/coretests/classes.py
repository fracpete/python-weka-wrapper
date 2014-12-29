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

# classes.py
# Copyright (C) 2014 Fracpete (pythonwekawrapper at gmail dot com)

import unittest
import weka.core.jvm as jvm
import weka.core.classes as classes
import wekatests.tests.weka_test as weka_test


class TestClasses(weka_test.WekaTest):

    def test_singleindex(self):
        """
        Tests the SingleIndex class.
        """
        index = classes.SingleIndex()
        self.assertEquals("", index.single_index)

        index = classes.SingleIndex(index="first")
        index.upper(10)
        self.assertEquals("first", index.single_index)
        self.assertEquals(0, index.index())

        index = classes.SingleIndex(index="2")
        index.upper(10)
        self.assertEquals("2", index.single_index)
        self.assertEquals(1, index.index())

    def test_range(self):
        """
        Tests the Range class.
        """
        rang = classes.Range()
        self.assertEquals("", rang.ranges)

        rang = classes.Range(ranges="first")
        rang.upper(10)
        self.assertEquals("first", rang.ranges)
        self.assertEquals([0], rang.selection())

        rang = classes.Range(ranges="2")
        rang.upper(10)
        self.assertEquals("2", rang.ranges)
        self.assertEquals([1], rang.selection())

        rang = classes.Range(ranges="2-5,7")
        rang.upper(10)
        self.assertEquals("2-5,7", rang.ranges)
        self.assertItemsEqual([1, 2, 3, 4, 6], rang.selection())


def suite():
    """
    Returns the test suite.
    :return: the test suite
    :rtype: unittest.TestSuite
    """
    return unittest.TestLoader().loadTestsFromTestCase(TestClasses)


if __name__ == '__main__':
    jvm.start()
    unittest.TextTestRunner().run(suite())
    jvm.stop()
