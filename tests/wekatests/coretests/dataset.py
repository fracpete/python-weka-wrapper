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

# dataset.py
# Copyright (C) 2014-2015 Fracpete (pythonwekawrapper at gmail dot com)

import unittest
import weka.core.jvm as jvm
import weka.core.dataset as dataset
import weka.core.converters as converters
import wekatests.tests.weka_test as weka_test


class TestDataset(weka_test.WekaTest):

    def test_attribute(self):
        """
        Tests the Attribute class.
        """
        name = "Num"
        att = dataset.Attribute.create_numeric(name)
        self.assertIsNotNone(att, "Failed to create attribute!")
        self.assertEqual(name, att.name, "Names differ")
        self.assertTrue(att.is_numeric)

        name = "Nom"
        att = dataset.Attribute.create_nominal(name, ["A", "B", "C"])
        self.assertIsNotNone(att, "Failed to create attribute!")
        self.assertEqual(name, att.name, "Names differ")
        self.assertTrue(att.is_nominal)

        name = "Dat1"
        att = dataset.Attribute.create_date(name)
        self.assertIsNotNone(att, "Failed to create attribute!")
        self.assertEqual(name, att.name, "Names differ")
        self.assertTrue(att.is_date)

        name = "Dat2"
        att = dataset.Attribute.create_date(name, formt="yyyy-MM-dd HH:mm")
        self.assertIsNotNone(att, "Failed to create attribute!")
        self.assertEqual(name, att.name, "Names differ")
        self.assertTrue(att.is_date)

        name = "Str"
        att = dataset.Attribute.create_string(name)
        self.assertIsNotNone(att, "Failed to create attribute!")
        self.assertEqual(name, att.name, "Names differ")
        self.assertTrue(att.is_string)

    def test_attributestats(self):
        """
        Tests the AttributeStats class.
        """
        loader = converters.Loader(classname="weka.core.converters.ArffLoader")
        data = loader.load_file(self.datafile("anneal.arff"))
        self.assertIsNotNone(data, msg="Failed to load data!")

        stats = data.attribute_stats(2)
        self.assertIsNotNone(stats, msg="Failed to obtain stats!")
        self.assertEqual(8, stats.distinct_count, "distinct_count differs")
        self.assertEqual(898, stats.int_count, "int_count differs")
        self.assertEqual(0, stats.missing_count, "missing_count differs")
        self.assertEqual([86, 256, 440, 0, 51, 20, 10, 19, 16], stats.nominal_counts.tolist(), "nominal_counts differs")
        self.assertEqual([86, 256, 440, 0, 51, 20, 10, 19, 16], stats.nominal_weights.tolist(), "nominal_weights differs")
        self.assertEqual(898, stats.total_count, "total_count differs")
        self.assertEqual(0, stats.unique_count, "unique_count differs")

    def test_stats(self):
        """
        Tests the Stats class.
        """
        loader = converters.Loader(classname="weka.core.converters.ArffLoader")
        data = loader.load_file(self.datafile("anneal.arff"))
        self.assertIsNotNone(data, msg="Failed to load data!")

        stats = data.attribute_stats(3)
        numstats = stats.numeric_stats
        self.assertAlmostEqual(898, numstats.count, places=3, msg="count differs")
        self.assertAlmostEqual(70, numstats.max, places=3, msg="max differs")
        self.assertAlmostEqual(3.635, numstats.mean, places=3, msg="mean differs")
        self.assertAlmostEqual(0.0, numstats.min, places=3, msg="min differs")
        self.assertAlmostEqual(13.717, numstats.stddev, places=3, msg="stddev differs")
        self.assertAlmostEqual(3264, numstats.sum, places=3, msg="sum differs")
        self.assertAlmostEqual(180636, numstats.sumsq, places=3, msg="sumsq differs")

    def test_instance(self):
        """
        Tests the Instance class.
        """
        loader = converters.Loader(classname="weka.core.converters.ArffLoader")
        data = loader.load_file(self.datafile("anneal.ORIG.arff"))
        self.assertIsNotNone(data, msg="Failed to load data!")

        inst = data.get_instance(0)
        self.assertEqual(39, inst.num_attributes, msg="num_attributes differs")
        self.assertEqual(-1, data.class_index, msg="class_index differs")

        data.class_index = data.num_attributes - 1
        self.assertEqual(38, data.class_index, msg="class_index differs")

        data.class_is_first()
        self.assertEqual(0, data.class_index, msg="class_index differs")

        data.class_is_last()
        self.assertEqual(38, data.class_index, msg="class_index differs")

        self.assertIsNotNone(inst.dataset, msg="Dataset reference should not be None!")
        self.assertTrue(inst.has_missing(), msg="Should have missing values")
        self.assertTrue(inst.is_missing(0), msg="First value should be missing")
        self.assertFalse(inst.is_missing(1), msg="Second value should not be missing")

        self.assertEqual("C", inst.get_string_value(1), msg="string value differs")
        inst.set_string_value(1, "H")
        self.assertEqual("H", inst.get_string_value(1), msg="string value differs")

        self.assertEqual(8, inst.get_value(3), msg="numeric value differs")
        inst.set_value(3, 6.3)
        self.assertEqual(6.3, inst.get_value(3), msg="numeric value differs")

    def test_instances(self):
        """
        Tests the Instances class.
        """
        loader = converters.Loader(classname="weka.core.converters.ArffLoader")
        data = loader.load_file(self.datafile("anneal.arff"))
        self.assertIsNotNone(data, msg="Failed to load data!")

        count = 0
        for i in data:
            count += 1
        self.assertEqual(898, count, msg="Number of rows differs!")

        count = 0
        for i in data.attributes():
            count += 1
        self.assertEqual(39, count, msg="Number of attributes differs!")

        self.assertEqual(898, data.num_instances, msg="num_instances differs")
        self.assertEqual(39, data.num_attributes, msg="num_attributes differs")
        self.assertEqual(-1, data.class_index, msg="class_index differs")

        data.class_index = data.num_attributes - 1
        self.assertEqual(38, data.class_index, msg="class_index differs")

        data.class_is_first()
        self.assertEqual(0, data.class_index, msg="class_index differs")

        data.class_is_last()
        self.assertEqual(38, data.class_index, msg="class_index differs")

        att = data.attribute(0)
        self.assertIsNotNone(att, msg="Attribute should not be None!")
        self.assertEqual("family", att.name, msg="attribute name differs")

        name = "steel"
        att = data.attribute_by_name(name)
        self.assertIsNotNone(att, msg="Attribute should not be None!")
        self.assertEqual(name, att.name, msg="attribute name differs")
        self.assertEqual(2, att.index, msg="attribute index differs")

        data.delete_attribute(2)
        self.assertEqual(38, data.num_attributes, msg="num_attributes differs")
        name = "steel"
        att = data.attribute_by_name(name)
        self.assertIsNone(att, msg="Attribute should be None!")

        data.delete(3)
        self.assertEqual(897, data.num_instances, msg="num_instances differs")


def suite():
    """
    Returns the test suite.
    :return: the test suite
    :rtype: unittest.TestSuite
    """
    return unittest.TestLoader().loadTestsFromTestCase(TestDataset)


if __name__ == '__main__':
    jvm.start()
    unittest.TextTestRunner().run(suite())
    jvm.stop()
