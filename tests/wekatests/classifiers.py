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

# classifiers.py
# Copyright (C) 2014 Fracpete (pythonwekawrapper at gmail dot com)

import os
import unittest
import weka.core.jvm as jvm
import weka.core.converters as converters
import weka.classifiers as classifiers
import weka.filters as filters
import wekatests.tests.weka_test as weka_test


class TestClassifiers(weka_test.WekaTest):

    def test_instantiate_classifier(self):
        """
        Tests the instantiation of several classifier classes.
        """
        cname = "weka.classifiers.trees.J48"
        options = None
        cls = classifiers.Classifier(classname=cname, options=options)
        self.assertIsNotNone(cls, msg="Failed to instantiate: " + cname + "/" + str(options))
        self.assertEqual(cname, cls.classname, "Classnames differ!")

        cname = "weka.classifiers.trees.J48"
        options = ["-C", "0.3"]
        cls = classifiers.Classifier(classname=cname, options=options)
        self.assertIsNotNone(cls, msg="Failed to instantiate: " + cname + "/" + str(options))
        self.assertEqual(cname, cls.classname, "Classnames differ!")

        cname = "weka.classifiers.meta.FilteredClassifier"
        options = ["-W", "weka.classifiers.trees.J48", "--", "-C", "0.3"]
        cls = classifiers.SingleClassifierEnhancer(classname=cname, options=options)
        self.assertIsNotNone(cls, msg="Failed to instantiate: " + cname + "/" + str(options))
        self.assertEqual(cname, cls.classname, "Classnames differ!")
        fname = "weka.filters.unsupervised.attribute.Remove"
        flter = filters.Filter(classname=fname, options=["-R", "last"])
        cls.filter = flter
        self.assertEqual(fname, cls.filter.classname, "Classnames differ!")

        cls = classifiers.FilteredClassifier()
        self.assertIsNotNone(cls, "Failed to instantiate FilteredClassifier!")
        self.assertEqual("weka.classifiers.meta.FilteredClassifier", cls.classname, "Classnames differ!")

        cname = "weka.classifiers.functions.SMO"
        cls = classifiers.KernelClassifier(classname=cname)
        self.assertIsNotNone(cls, "Failed to instantiate KernelClassifier: " + cname)
        self.assertEqual(cname, cls.classname, "Classnames differ!")
        kname = "weka.classifiers.functions.supportVector.RBFKernel"
        kernel = classifiers.Kernel(classname=kname)
        self.assertIsNotNone(kernel, "Failed to instantiate Kernel: " + kname)
        cls.kernel = kernel
        self.assertEqual(kname, cls.kernel.classname, "Kernel classnames differ!")

        cname = "weka.classifiers.meta.Vote"
        cls = classifiers.MultipleClassifiersCombiner(classname=cname)
        self.assertIsNotNone(cls, "Failed to instantiate MultipleClassifiersCombiner: " + cname)
        self.assertEqual(cname, cls.classname, "Classnames differ!")

    def test_build_classifier(self):
        """
        Tests the build_classifier method.
        """
        # 1. nominal
        loader = converters.Loader(classname="weka.core.converters.ArffLoader")
        data = loader.load_file(self.datadir() + os.sep + "anneal.arff")
        self.assertIsNotNone(data)
        data.class_is_last()

        cname = "weka.classifiers.trees.J48"
        options = ["-C", "0.3"]
        cls = classifiers.Classifier(classname=cname, options=options)
        self.assertIsNotNone(cls, msg="Failed to instantiate: " + cname + "/" + str(options))

        cls.build_classifier(data)

        # 2. numeric
        loader = converters.Loader(classname="weka.core.converters.ArffLoader")
        data = loader.load_file(self.datadir() + os.sep + "bolts.arff")
        self.assertIsNotNone(data)
        data.class_is_last()

        cname = "weka.classifiers.functions.LinearRegression"
        options = ["-R", "0.1"]
        cls = classifiers.Classifier(classname=cname, options=options)
        self.assertIsNotNone(cls, msg="Failed to instantiate: " + cname + "/" + str(options))

        cls.build_classifier(data)

    def test_distribution_for_instance(self):
        """
        Tests the distribution_for_instance method.
        """
        # 1. nominal
        loader = converters.Loader(classname="weka.core.converters.ArffLoader")
        data = loader.load_file(self.datadir() + os.sep + "anneal.arff")
        self.assertIsNotNone(data)
        data.class_is_last()

        cname = "weka.classifiers.trees.J48"
        options = ["-C", "0.3"]
        cls = classifiers.Classifier(classname=cname, options=options)
        self.assertIsNotNone(cls, msg="Failed to instantiate: " + cname + "/" + str(options))

        cls.build_classifier(data)
        for i in range(10):
            dist = cls.distribution_for_instance(data.get_instance(i))
            self.assertIsNotNone(dist)
            self.assertEqual(6, len(dist), "Number of classes in prediction differ!")

        # 2. numeric
        loader = converters.Loader(classname="weka.core.converters.ArffLoader")
        data = loader.load_file(self.datadir() + os.sep + "bolts.arff")
        self.assertIsNotNone(data)
        data.class_is_last()

        cname = "weka.classifiers.functions.LinearRegression"
        options = ["-R", "0.1"]
        cls = classifiers.Classifier(classname=cname, options=options)
        self.assertIsNotNone(cls, msg="Failed to instantiate: " + cname + "/" + str(options))

        cls.build_classifier(data)
        for i in range(10):
            dist = cls.distribution_for_instance(data.get_instance(i))
            self.assertIsNotNone(dist)
            self.assertEqual(1, len(dist), "Number of classes in prediction should be one for numeric classifier!")

    def test_classify_instance(self):
        """
        Tests the classify_instance method.
        """
        # 1. nominal
        loader = converters.Loader(classname="weka.core.converters.ArffLoader")
        data = loader.load_file(self.datadir() + os.sep + "anneal.arff")
        self.assertIsNotNone(data)
        data.class_is_last()

        cname = "weka.classifiers.trees.J48"
        options = ["-C", "0.3"]
        cls = classifiers.Classifier(classname=cname, options=options)
        self.assertIsNotNone(cls, msg="Failed to instantiate: " + cname + "/" + str(options))

        cls.build_classifier(data)
        for i in range(10):
            pred = cls.classify_instance(data.get_instance(i))
            self.assertIsNotNone(pred)

        # 2. numeric
        loader = converters.Loader(classname="weka.core.converters.ArffLoader")
        data = loader.load_file(self.datadir() + os.sep + "bolts.arff")
        self.assertIsNotNone(data)
        data.class_is_last()

        cname = "weka.classifiers.functions.LinearRegression"
        options = ["-R", "0.1"]
        cls = classifiers.Classifier(classname=cname, options=options)
        self.assertIsNotNone(cls, msg="Failed to instantiate: " + cname + "/" + str(options))

        cls.build_classifier(data)
        for i in range(10):
            pred = cls.classify_instance(data.get_instance(i))
            self.assertIsNotNone(pred)

    def test_costmatrix(self):
        """
        Tests the CostMatrix class.
        """
        cmatrix = classifiers.CostMatrix(num_classes=3)
        self.assertEqual(3, cmatrix.num_columns, msg="# of columns differ")
        self.assertEqual(3, cmatrix.num_rows, msg="# of rows differ")

        self.assertEqual(0, cmatrix.get_element(1, 1), "cell should be initialized with 0")
        cmatrix.set_element(1, 1, 0.1)
        self.assertEqual(0.1, cmatrix.get_element(1, 1), "cell value differs")

        matrixstr = "[1.0 2.0; 3.0 4.0]"
        cmatrix = classifiers.CostMatrix.parse_matlab(matrixstr)
        self.assertEqual(matrixstr, cmatrix.to_matlab(), msg="Matrix strings differ")


def suite():
    """
    Returns the test suite.
    :return: the test suite
    :rtype: unittest.TestSuite
    """
    return unittest.TestLoader().loadTestsFromTestCase(TestClassifiers)


if __name__ == '__main__':
    jvm.start()
    unittest.TextTestRunner().run(suite())
    jvm.stop()
