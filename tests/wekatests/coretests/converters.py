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

# converters.py
# Copyright (C) 2014 Fracpete (pythonwekawrapper at gmail dot com)

import unittest
import os
import weka.core.jvm as jvm
import weka.core.converters as converters
import wekatests.tests.weka_test as weka_test


class TestConverters(weka_test.WekaTest):

    def test_loader_for_file(self):
        """
        Tests the loader_for_file method.
        """
        fname = "/some/where/anneal.arff"
        loader = converters.loader_for_file(fname)
        self.assertEqual("weka.core.converters.ArffLoader", loader.classname, msg="Class differs:  " + fname)
        fname = "/some/where/anneal.arff.gz"
        loader = converters.loader_for_file(fname)
        self.assertEqual("weka.core.converters.ArffLoader", loader.classname, msg="Class differs: " + fname)
        fname = "/some/where/anneal.csv"
        loader = converters.loader_for_file(fname)
        self.assertEqual("weka.core.converters.CSVLoader", loader.classname, msg="Class differs: " + fname)

    def test_saver_for_file(self):
        """
        Tests the saver_for_file method.
        """
        fname = "/some/where/anneal.arff"
        loader = converters.saver_for_file(fname)
        self.assertEqual("weka.core.converters.ArffSaver", loader.classname, msg="Class differs:  " + fname)
        fname = "/some/where/anneal.arff.gz"
        loader = converters.saver_for_file(fname)
        self.assertEqual("weka.core.converters.ArffSaver", loader.classname, msg="Class differs: " + fname)
        fname = "/some/where/anneal.csv"
        loader = converters.saver_for_file(fname)
        self.assertEqual("weka.core.converters.CSVSaver", loader.classname, msg="Class differs: " + fname)

    def test_arff_loader(self):
        """
        Tests the Loader class using an ArffLoader.
        """
        loader = converters.Loader(classname="weka.core.converters.ArffLoader")
        data = loader.load_file(self.datadir() + os.sep + "anneal.arff")
        self.assertIsNotNone(data)
        self.assertEqual(898, data.num_instances, msg="Number of instances differs!")

    def test_incremental_arff_loader(self):
        """
        Tests the Loader class using an incremental ArffLoader.
        """
        loader = converters.Loader(classname="weka.core.converters.ArffLoader")
        data = loader.load_file(self.datadir() + os.sep + "anneal.arff", incremental=True)
        self.assertIsNotNone(data)
        count = 0
        for inst in loader:
            count += 1
        self.assertEqual(898, count, msg="Number of instances differs!")

    def test_arff_saver(self):
        """
        Tests the Saver class using an ArffSaver.
        """
        loader = converters.Loader(classname="weka.core.converters.ArffLoader")
        data = loader.load_file(self.datadir() + os.sep + "anneal.arff")
        self.assertIsNotNone(data)
        outfile = self.tempfile("out.arff")
        self.delfile(outfile)
        saver = converters.Saver(classname="weka.core.converters.ArffSaver")
        saver.save_file(data, outfile)
        self.assertTrue(os.path.exists(outfile), "File does not exist: " + outfile)
        self.delfile(outfile)


def suite():
    """
    Returns the test suite.
    :return: the test suite
    :rtype: unittest.TestSuite
    """
    return unittest.TestLoader().loadTestsFromTestCase(TestConverters)


if __name__ == '__main__':
    jvm.start()
    unittest.TextTestRunner().run(suite())
    jvm.stop()
