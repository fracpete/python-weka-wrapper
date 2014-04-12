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
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import os
import weka.core.jvm as jvm
import examples.helper as helper
from weka.core.converters import Loader
from weka.classifiers import Classifier
from weka.classifiers import Evaluation
from weka.core.classes import Random


def main():
    """
    Just runs some example code.
    """

    # load a dataset
    iris_file = helper.get_data_dir() + os.sep + "iris.arff"
    helper.print_info("Loading dataset: " + iris_file)
    loader = Loader("weka.core.converters.ArffLoader")
    iris_data = loader.load_file(iris_file)
    iris_data.set_class_index(iris_data.num_attributes() - 1)

    # build a classifier and output model
    helper.print_title("Training J48 classifier on iris")
    classifier = Classifier("weka.classifiers.trees.J48")
    classifier.set_options(["-C", "0.3"])
    classifier.build_classifier(iris_data)
    print(classifier)

    # cross-validate nominal classifier
    helper.print_title("Cross-validating SMO on iris")
    classifier = Classifier("weka.classifiers.functions.SMO")
    classifier.set_options(["-M"])
    evaluation = Evaluation(iris_data)
    evaluation.crossvalidate_model(classifier, iris_data, 10, Random(42))
    print(evaluation.to_summary())
    print(evaluation.to_class_details())
    print(evaluation.to_matrix())
    print("areaUnderPRC/0: " + str(evaluation.area_under_prc(0)))
    print("areaUnderROC/1: " + str(evaluation.area_under_roc(1)))
    print("avgCost: " + str(evaluation.avg_cost()))
    print("confusionMatrix: " + str(evaluation.confusion_matrix()))
    print("correct: " + str(evaluation.correct()))
    print("pctCorrect: " + str(evaluation.percent_correct()))
    print("incorrect: " + str(evaluation.incorrect()))
    print("pctIncorrect: " + str(evaluation.percent_incorrect()))
    print("unclassified: " + str(evaluation.unclassified()))
    print("pctUnclassified: " + str(evaluation.percent_unclassified()))
    print("coverageOfTestCasesByPredictedRegions: " + str(evaluation.coverage_of_test_cases_by_predicted_regions()))
    print("falseNegativeRate: " + str(evaluation.false_negative_rate(1)))
    print("falsePositiveRate: " + str(evaluation.false_positive_rate(1)))
    print("fMeasure: " + str(evaluation.f_measure(1)))

    # load a numeric dataset
    bolts_file = helper.get_data_dir() + os.sep + "bolts.arff"
    helper.print_info("Loading dataset: " + bolts_file)
    loader = Loader("weka.core.converters.ArffLoader")
    bolts_data = loader.load_file(bolts_file)
    bolts_data.set_class_index(bolts_data.num_attributes() - 1)

    # build a classifier and output model
    helper.print_title("Training LinearRegression on bolts")
    classifier = Classifier("weka.classifiers.functions.LinearRegression")
    classifier.set_options(["-S", "1", "-C"])
    classifier.build_classifier(bolts_data)
    print(classifier)

    # cross-validate numeric classifier
    helper.print_title("Cross-validating LinearRegression on bolts")
    classifier = Classifier("weka.classifiers.functions.LinearRegression")
    classifier.set_options(["-S", "1", "-C"])
    evaluation = Evaluation(bolts_data)
    evaluation.crossvalidate_model(classifier, bolts_data, 10, Random(42))
    print(evaluation.to_summary())
    print("correlationCoefficient: " + str(evaluation.correlation_coefficient()))
    print("errorRate: " + str(evaluation.error_rate()))


if __name__ == "__main__":
    try:
        jvm.start()
        main()
    except Exception, e:
        print(e)
    finally:
        jvm.stop()
