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

# filters.py
# Copyright (C) 2014 Fracpete (pythonwekawrapper at gmail dot com)

import unittest
import weka.core.jvm as jvm
import weka.core.converters as converters
import weka.filters as filters
import wekatests.tests.weka_test as weka_test


class TestFilters(weka_test.WekaTest):

    def test_capabilities(self):
        """
        Tests the capabilities.
        """
        cname = "weka.classifiers.trees.J48"
        options = None
        flter = filters.Filter(classname="weka.filters.unsupervised.attribute.Remove", options=["-R", "1,3"])
        self.assertIsNotNone(flter, msg="Failed to instantiate: " + cname + "/" + str(options))

        caps = flter.capabilities
        self.assertIsNotNone(caps, msg="Capabilities are None!")

    def test_batch_filtering(self):
        """
        Tests the Filter.filter method.
        """
        loader = converters.Loader(classname="weka.core.converters.ArffLoader")
        data = loader.load_file(self.datafile("anneal.arff"))
        self.assertIsNotNone(data)

        flter = filters.Filter(classname="weka.filters.unsupervised.attribute.Remove", options=["-R", "1,3"])
        flter.inputformat(data)
        filtered = flter.filter(data)
        self.assertEqual(data.num_attributes - 2, filtered.num_attributes, msg="Number of attributes differ")
        self.assertEqual(data.num_instances, filtered.num_instances, msg="Number of instances differ")

        # multple files
        data = loader.load_file(self.datafile("reutersTop10Randomized_1perc_shortened-train.arff"))
        self.assertIsNotNone(data)
        data2 = loader.load_file(self.datafile("reutersTop10Randomized_1perc_shortened-test.arff"))
        self.assertIsNotNone(data2)

        flter = filters.Filter(classname="weka.filters.unsupervised.attribute.StringToWordVector")
        flter.inputformat(data)
        filtered = flter.filter([data, data2])
        print(filtered[0])
        print(filtered[1])
        self.assertIsNone(filtered[0].equal_headers(filtered[1]), msg="Headers should be compatible")

    def test_incremental_filtering(self):
        """
        Tests the Filter.input/output methods.
        """
        loader = converters.Loader(classname="weka.core.converters.ArffLoader")
        data = loader.load_file(self.datafile("anneal.arff"))
        self.assertIsNotNone(data)

        flter = filters.Filter(classname="weka.filters.unsupervised.attribute.Remove", options=["-R", "1,3"])
        flter.inputformat(data)
        filtered = flter.outputformat()

        for inst in data:
            flter.input(inst)
            finst = flter.output()
            filtered.add_instance(finst)

        self.assertEqual(data.num_attributes - 2, filtered.num_attributes, msg="Number of attributes differ")
        self.assertEqual(data.num_instances, filtered.num_instances, msg="Number of instances differ")

def suite():
    """
    Returns the test suite.
    :return: the test suite
    :rtype: unittest.TestSuite
    """
    return unittest.TestLoader().loadTestsFromTestCase(TestFilters)


if __name__ == '__main__':
    jvm.start()
    unittest.TextTestRunner().run(suite())
    jvm.stop()
