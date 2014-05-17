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
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import os
import tempfile
import weka.core.jvm as jvm
import weka.core.converters as converters
import wekaexamples.helper as helper
from weka.classifiers import Classifier
from weka.experiments import SimpleCrossValidationExperiment, SimpleRandomSplitExperiment, Tester, ResultMatrix


def main():
    """
    Just runs some example code.
    """

    print(helper.get_data_dir())

    # cross-validation + classification
    helper.print_title("Experiment: Cross-validation + classification")
    datasets = [helper.get_data_dir() + os.sep + "iris.arff", helper.get_data_dir() + os.sep + "anneal.arff"]
    classifiers = [Classifier("weka.classifiers.rules.ZeroR"), Classifier("weka.classifiers.trees.J48")]
    outfile = tempfile.gettempdir() + os.sep + "results-cv.arff"
    exp = SimpleCrossValidationExperiment(
        classification=True,
        runs=10,
        folds=10,
        datasets=datasets,
        classifiers=classifiers,
        result=outfile)
    exp.setup()
    exp.run()

    # evaluate
    loader = converters.loader_for_file(outfile)
    data = loader.load_file(outfile)
    matrix = ResultMatrix("weka.experiment.ResultMatrixPlainText")
    tester = Tester("weka.experiment.PairedCorrectedTTester")
    tester.set_resultmatrix(matrix)
    comparison_col = data.get_attribute_by_name("Percent_correct").get_index()
    tester.set_instances(data)
    print(tester.header(comparison_col))
    print(tester.multi_resultset_full(0, comparison_col))

    # random split + regression
    helper.print_title("Experiment: Random split + regression")
    datasets = [helper.get_data_dir() + os.sep + "bolts.arff", helper.get_data_dir() + os.sep + "bodyfat.arff"]
    classifiers = [
        Classifier("weka.classifiers.rules.ZeroR"),
        Classifier("weka.classifiers.functions.LinearRegression")
    ]
    outfile = tempfile.gettempdir() + os.sep + "results-rs.arff"
    exp = SimpleRandomSplitExperiment(
        classification=False,
        runs=10,
        percentage=66.6,
        preserve_order=False,
        datasets=datasets,
        classifiers=classifiers,
        result=outfile)
    exp.setup()
    exp.run()

    # evaluate
    loader = converters.loader_for_file(outfile)
    data = loader.load_file(outfile)
    matrix = ResultMatrix("weka.experiment.ResultMatrixPlainText")
    tester = Tester("weka.experiment.PairedCorrectedTTester")
    tester.set_resultmatrix(matrix)
    comparison_col = data.get_attribute_by_name("Correlation_coefficient").get_index()
    tester.set_instances(data)
    print(tester.header(comparison_col))
    print(tester.multi_resultset_full(0, comparison_col))

if __name__ == "__main__":
    try:
        jvm.start()
        main()
    except Exception, e:
        print(e)
    finally:
        jvm.stop()
