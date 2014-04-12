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

import javabridge
import logging
import os
import sys
import getopt
import numpy
import weka.core.jvm as jvm
import weka.core.utils as utils
import weka.core.arrays as arrays
from weka.core.classes import JavaObject
from weka.core.classes import OptionHandler

# logging setup
logger = logging.getLogger("weka.classifiers")


class Classifier(OptionHandler):
    """
    Wrapper class for classifiers.
    """

    def __init__(self, classname):
        """
        Initializes the specified classifier.
        :param classname: the classname of the classifier
        """
        jobject = Classifier.new_instance(classname)
        self.enforce_type(jobject, "weka.classifiers.Classifier")
        super(Classifier, self).__init__(jobject)

    def build_classifier(self, data):
        """
        Builds the classifier with the data.
        :param data: the data to train the classifier with
        """
        javabridge.call(self.jobject, "buildClassifier", "(Lweka/core/Instances;)V", data.jobject)

    def classify_instance(self, inst):
        """
        Peforms a prediction.
        :param inst: the Instance to get a prediction for
        :rtype: float
        """
        return javabridge.call(self.jobject, "classifyInstance", "(Lweka/core/Instance;)D", inst.jobject)

    def distribution_for_instance(self, inst):
        """
        Peforms a prediction, returning the class distribution.
        :param inst: the Instance to get the class distribution for
        :rtype: float[]
        """
        pred = javabridge.call(self.jobject, "distributionForInstance", "(Lweka/core/Instance;)[D", inst.jobject)
        return jvm.ENV.get_float_array_elements(pred)


class Evaluation(JavaObject):
    """
    Evaluation class for classifiers.
    """

    def __init__(self, data):
        """
        Initializes an Evaluation object.
        :param data: the data to use to initialize the priors with
        """
        jobject = javabridge.make_instance(
            "weka/classifiers/EvaluationWrapper", "(Lweka/core/Instances;)V", data.jobject)
        jobject = javabridge.call(jobject, "getEvaluation", "()Lweka/classifiers/Evaluation;")
        super(Evaluation, self).__init__(jobject)

    def crossvalidate_model(self, classifier, data, num_folds, random):
        """
        Crossvalidates the model using the specified data, number of folds and random number generator wrapper.
        :param classifier: the classifier to cross-validate
        :param data: the data to evaluate on
        :param num_folds: the number of folds
        :param random: the random number generator to use
        """
        javabridge.call(
            self.jobject, "crossValidateModel",
            "(Lweka/classifiers/Classifier;Lweka/core/Instances;ILjava/util/Random;[Ljava/lang/Object;)V",
            classifier.jobject, data.jobject, num_folds, random.jobject, [])

    def to_summary(self, title=None):
        """
        Generates a summary.
        :param title: optional title
        :rtype: str
        """
        if title is None:
            return javabridge.call(self.jobject, "toSummaryString", "()Ljava/lang/String;")
        else:
            return javabridge.call(self.jobject, "toSummaryString", "(Ljava/lang/String;)Ljava/lang/String;", title)

    def to_class_details(self, title=None):
        """
        Generates the class details.
        :param title: optional title
        :rtype: str
        """
        if title is None:
            return javabridge.call(self.jobject, "toClassDetailsString", "()Ljava/lang/String;")
        else:
            return javabridge.call(self.jobject, "toClassDetailsString", "(Ljava/lang/String;)Ljava/lang/String;", title)

    def to_matrix(self, title=None):
        """
        Generates the confusion matrix.
        :param title: optional title
        :rtype: str
        """
        if title is None:
            return javabridge.call(self.jobject, "toMatrixString", "()Ljava/lang/String;")
        else:
            return javabridge.call(self.jobject, "toMatrixString", "(Ljava/lang/String;)Ljava/lang/String;", title)

    def area_under_prc(self, class_index):
        """
        Returns the area under precision recall curve.
        :param class_index: the 0-based index of the class label
        :rtype: float
        """
        return javabridge.call(self.jobject, "areaUnderPRC", "(I)D", class_index)

    def area_under_roc(self, class_index):
        """
        Returns the area under receiver operators characteristics curve.
        :param class_index: the 0-based index of the class label
        :rtype: float
        """
        return javabridge.call(self.jobject, "areaUnderROC", "(I)D", class_index)

    def avg_cost(self):
        """
        Returns the average cost.
        :rtype: float
        """
        return javabridge.call(self.jobject, "avgCost", "()D")

    def confusion_matrix(self):
        """
        Returns the confusion matrix.
        :rtype: float[][]
        """
        return arrays.double_matrix_to_list(javabridge.call(self.jobject, "confusionMatrix", "()[[D"))

    def correct(self):
        """
        Returns the correct count (nominal classes).
        :rtype: float
        """
        return javabridge.call(self.jobject, "correct", "()D")

    def incorrect(self):
        """
        Returns the incorrect count (nominal classes).
        :rtype: float
        """
        return javabridge.call(self.jobject, "incorrect", "()D")

    def unclassified(self):
        """
        Returns the unclassified count.
        :rtype: float
        """
        return javabridge.call(self.jobject, "unclassified", "()D")

    def percent_correct(self):
        """
        Returns the percent correct (nominal classes).
        :rtype: float
        """
        return javabridge.call(self.jobject, "pctCorrect", "()D")

    def percent_incorrect(self):
        """
        Returns the percent incorrect (nominal classes).
        :rtype: float
        """
        return javabridge.call(self.jobject, "pctIncorrect", "()D")

    def percent_unclassified(self):
        """
        Returns the percent unclassified.
        :rtype: float
        """
        return javabridge.call(self.jobject, "pctUnclassified", "()D")

    def correlation_coefficient(self):
        """
        Returns the correlation coefficient (numeric classes).
        :rtype: float
        """
        return javabridge.call(self.jobject, "correlationCoefficient", "()D")

    def coverage_of_test_cases_by_predicted_regions(self):
        """
        Returns the coverage of the test cases by the predicted regions at the confidence level
        specified when evaluation was performed..
        :rtype: float
        """
        return javabridge.call(self.jobject, "coverageOfTestCasesByPredictedRegions", "()D")

    def error_rate(self):
        """
        Returns the error rate (numeric classes).
        :rtype: float
        """
        return javabridge.call(self.jobject, "errorRate", "()D")

    def false_negative_rate(self, class_index):
        """
        Returns the false negative rate.
        :param class_index: the 0-based index of the class label
        :rtype: float
        """
        return javabridge.call(self.jobject, "falseNegativeRate", "(I)D", class_index)

    def false_positive_rate(self, class_index):
        """
        Returns the false positive rate.
        :param class_index: the 0-based index of the class label
        :rtype: float
        """
        return javabridge.call(self.jobject, "falsePositiveRate", "(I)D", class_index)

    def f_measure(self, class_index):
        """
        Returns the f measure.
        :param class_index: the 0-based index of the class label
        :rtype: float
        """
        return javabridge.call(self.jobject, "fMeasure", "(I)D", class_index)

    @classmethod
    def evaluate_model(cls, classifier, args):
        """
        Evaluates the classifier with the given options.
        :rtype : str
        :param classifier: the classifier instance to use
        :param args: the command-line arguments to use
        """
        return javabridge.static_call(
            "Lweka/classifiers/Evaluation;", "evaluateModel",
            "(Lweka/classifiers/Classifier;[Ljava/lang/String;)Ljava/lang/String;",
            classifier.jobject, args)


def main(args):
    """
    Runs a classifier from the command-line. Calls JVM start/stop automatically.
    Options:
        -j jar1[:jar2...]
        -t train
        [-T test]
        [-c classindex]
        [-d output model file]
        [-l input model file]
        [-x num folds]
        [-s seed]
        [-v # no stats for training]
        [-o # only stats, no model]
        [-i # information-retrieval stats per class]
        [-k # information-theoretic stats]
        [-m cost matrix file]
        [-g graph file]
        classifier classname
        [classifier options]
    """

    usage = "Usage: weka.classifiers -j jar1[" + os.pathsep + "jar2...] -t train [-T test] [-c classindex] " \
            + "[-d output model file] [-l input model file] [-x num folds] [-s seed] [-v # no stats for training] " \
            + "[-o # only stats, no model] [-i # information-retrieval stats per class] " \
            + "-kl # information-theoretic stats] [-m cost matrix file] [-g graph file] " \
            + "classifier classname [classifier options]"

    optlist, optargs = getopt.getopt(args, "j:t:T:c:d:l:x:s:voikm:g:")
    if len(optargs) == 0:
        raise Exception("No classifier classname provided!\n" + usage)
    for opt in optlist:
        if opt[0] == "-h":
            print(usage)
            return

    jars   = []
    params = []
    train  = None
    for opt in optlist:
        if opt[0] == "-j":
            jars = opt[1].split(os.pathsep)
        elif opt[0] == "-t":
            params.append(opt[0])
            params.append(opt[1])
            train = opt[1]
        elif opt[0] == "-T":
            params.append(opt[0])
            params.append(opt[1])
        elif opt[0] == "-d":
            params.append(opt[0])
            params.append(opt[1])
        elif opt[0] == "-l":
            params.append(opt[0])
            params.append(opt[1])
        elif opt[0] == "-x":
            params.append(opt[0])
            params.append(opt[1])
        elif opt[0] == "-s":
            params.append(opt[0])
            params.append(opt[1])
        elif opt[0] == "-v":
            params.append(opt[0])
        elif opt[0] == "-o":
            params.append(opt[0])
        elif opt[0] == "-i":
            params.append(opt[0])
        elif opt[0] == "-k":
            params.append(opt[0])
        elif opt[0] == "-m":
            params.append(opt[0])
            params.append(opt[1])
        elif opt[0] == "-g":
            params.append(opt[0])
            params.append(opt[1])

    # check parameters
    if train is None:
        raise Exception("No train file provided ('-t ...')!")

    jvm.start(jars)

    logger.debug("Commandline: " + utils.join_options(args))

    try:
        classifier = Classifier(optargs[0])
        optargs = optargs[1:]
        if len(optargs) > 0:
            classifier.set_options(optargs)
        print(Evaluation.evaluate_model(classifier, params))
        # data = Loader("weka.core.converters.ArffLoader").load_file(train)
        # data.set_class_index(data.num_attributes() - 1)
        # evl = Evaluation(data)
        # rnd = Random(1)
        # evl.crossvalidate_model(classifier, data, 10, rnd)
        # print(evl.get_percent_correct())
    except Exception, e:
        print(e)
    finally:
        jvm.stop()

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception, e:
        print(e)
