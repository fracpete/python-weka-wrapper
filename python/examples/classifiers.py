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
    iris = helper.get_data_dir() + os.sep + "iris.arff"
    helper.print_info("Loading dataset: " + iris)
    loader = Loader("weka.core.converters.ArffLoader")
    data = loader.load_file(iris)
    data.set_class_index(data.num_attributes() - 1)

    # build a classifier and output model
    helper.print_title("Training J48 classifier")
    classifier = Classifier("weka.classifiers.trees.J48")
    classifier.set_options(["-C", "0.3"])
    classifier.build_classifier(data)
    print(str(classifier))

    # cross-validate classifier
    helper.print_title("Cross-validating SMO")
    classifier = Classifier("weka.classifiers.functions.SMO")
    classifier.set_options(["-M"])
    evaluation = Evaluation(data)
    evaluation.crossvalidate_model(classifier, data, 10, Random(42))
    print(evaluation.to_summary_string())


if __name__ == "__main__":
    try:
        jvm.start()
        main()
    except Exception, e:
        print(e)
    finally:
        jvm.stop()
