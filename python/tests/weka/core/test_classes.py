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

# test_classes.py
# Copyright (C) 2014 Fracpete (pythonwekawrapper at gmail dot com)

import unittest
import weka.core.jvm as jvm
import weka.core.classes as classes
import tests.weka.tests.weka_test as weka_test


class TestUtils(weka_test.WekaTest):

    def test_singleindex(self):
        """
        Tests the SingleIndex class.
        """
        index = classes.SingleIndex()
        self.assertEquals("", index.get_single_index())

        index = classes.SingleIndex(index="first")
        index.upper(10)
        self.assertEquals("first", index.get_single_index())
        self.assertEquals(0, index.index())

        index = classes.SingleIndex(index="2")
        index.upper(10)
        self.assertEquals("2", index.get_single_index())
        self.assertEquals(1, index.index())

    def test_range(self):
        """
        Tests the Range class.
        """
        rang = classes.Range()
        self.assertEquals("", rang.get_ranges())

        rang = classes.Range(ranges="first")
        rang.upper(10)
        self.assertEquals("first", rang.get_ranges())
        self.assertEquals([0], rang.selection())

        rang = classes.Range(ranges="2")
        rang.upper(10)
        self.assertEquals("2", rang.get_ranges())
        self.assertEquals([1], rang.selection())

        rang = classes.Range(ranges="2-5,7")
        rang.upper(10)
        self.assertEquals("2-5,7", rang.get_ranges())
        self.assertItemsEqual([1, 2, 3, 4, 6], rang.selection())


if __name__ == '__main__':
    jvm.start()
    unittest.main()
    jvm.stop()
