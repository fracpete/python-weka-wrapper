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

# experiments.py
# Copyright (C) 2014-2015 Fracpete (pythonwekawrapper at gmail dot com)

import unittest
import weka.core.jvm as jvm
import weka.core.converters as converters
import weka.experiments as experiments
import weka.classifiers as classifiers
import wekatests.tests.weka_test as weka_test


class TestExperiments(weka_test.WekaTest):

    def test_crossvalidation_classification(self):
        """
        Tests cross-validated classification.
        """
        datasets = [self.datafile("iris.arff"), self.datafile("anneal.arff")]
        cls = [
            classifiers.Classifier("weka.classifiers.rules.ZeroR"),
            classifiers.Classifier("weka.classifiers.trees.J48")]
        outfile = self.tempfile("results-cv.arff")
        exp = experiments.SimpleCrossValidationExperiment(
            classification=True,
            runs=10,
            folds=10,
            datasets=datasets,
            classifiers=cls,
            result=outfile)
        self.assertIsNotNone(exp, msg="Failed to instantiate!")
        exp.setup()
        exp.run()

        # evaluate
        loader = converters.loader_for_file(outfile)
        data = loader.load_file(outfile)
        self.assertIsNotNone(data, msg="Failed to load data: " + outfile)

        matrix = experiments.ResultMatrix("weka.experiment.ResultMatrixPlainText")
        self.assertIsNotNone(matrix, msg="Failed to instantiate!")

        tester = experiments.Tester("weka.experiment.PairedCorrectedTTester")
        self.assertIsNotNone(tester, msg="Failed to instantiate!")

        tester.resultmatrix = matrix
        comparison_col = data.attribute_by_name("Percent_correct").index
        tester.instances = data
        self.assertGreater(len(tester.header(comparison_col)), 0, msg="Generated no header")
        self.assertGreater(len(tester.multi_resultset_full(0, comparison_col)), 0, msg="Generated no result")

    def test_randomsplit_regression(self):
        """
        Tests random split on regression.
        """
        datasets = [self.datafile("bolts.arff"), self.datafile("bodyfat.arff")]
        cls = [
            classifiers.Classifier("weka.classifiers.rules.ZeroR"),
            classifiers.Classifier("weka.classifiers.functions.LinearRegression")
        ]
        outfile = self.tempfile("results-rs.arff")
        exp = experiments.SimpleRandomSplitExperiment(
            classification=False,
            runs=10,
            percentage=66.6,
            preserve_order=False,
            datasets=datasets,
            classifiers=cls,
            result=outfile)
        self.assertIsNotNone(exp, msg="Failed to instantiate!")
        exp.setup()
        exp.run()

        # evaluate
        loader = converters.loader_for_file(outfile)
        data = loader.load_file(outfile)
        self.assertIsNotNone(data, msg="Failed to load data: " + outfile)

        matrix = experiments.ResultMatrix("weka.experiment.ResultMatrixPlainText")
        self.assertIsNotNone(matrix, msg="Failed to instantiate!")

        tester = experiments.Tester("weka.experiment.PairedCorrectedTTester")
        self.assertIsNotNone(tester, msg="Failed to instantiate!")

        tester.resultmatrix = matrix
        comparison_col = data.attribute_by_name("Correlation_coefficient").index
        tester.instances = data
        self.assertGreater(len(tester.header(comparison_col)), 0, msg="Generated no header")
        self.assertGreater(len(tester.multi_resultset_full(0, comparison_col)), 0, msg="Generated no result")


def suite():
    """
    Returns the test suite.
    :return: the test suite
    :rtype: unittest.TestSuite
    """
    return unittest.TestLoader().loadTestsFromTestCase(TestExperiments)


if __name__ == '__main__':
    jvm.start()
    unittest.TextTestRunner().run(suite())
    jvm.stop()
