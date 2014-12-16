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

# test_utils.py
# Copyright (C) 2014 Fracpete (pythonwekawrapper at gmail dot com)

import unittest
import weka.core.jvm as jvm
import weka.core.utils as utils
import tests.weka.tests.weka_test as weka_test


class TestUtils(weka_test.WekaTest):

    def test_split_options(self):
        self.assertEquals(0, len(utils.split_options("")))
        self.assertEquals(2, len(utils.split_options("-t /some/where/test.arff")))

    def test_join_options(self):
        self.assertEquals("", str(utils.join_options([])))
        self.assertEquals("-t /some/where/test.arff", str(utils.join_options(["-t", "/some/where/test.arff"])))

if __name__ == '__main__':
    jvm.start()
    unittest.main()
    jvm.stop()
