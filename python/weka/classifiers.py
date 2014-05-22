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
import getopt
import weka.core.jvm as jvm
import weka.core.utils as wutils
import weka.core.types as arrays
from numpy import *
from weka.core.classes import JavaObject
from weka.core.classes import OptionHandler
from weka.core.classes import Random
from weka.core.capabilities import Capabilities
from weka.core.dataset import Instances, Instance, Attribute
from weka.filters import Filter

# logging setup
logger = logging.getLogger("weka.classifiers")


class Classifier(OptionHandler):
    """
    Wrapper class for classifiers.
    """

    def __init__(self, classname=None, jobject=None, options=None):
        """
        Initializes the specified classifier using either the classname or the supplied JB_Object.
        :param classname: the classname of the classifier
        :type classname: str
        :param jobject: the JB_Object to use
        :type jobject: JB_Object
        :param options: the list of commandline options to set
        :type options: list
        """
        if jobject is None:
            jobject = Classifier.new_instance(classname)
        self.enforce_type(jobject, "weka.classifiers.Classifier")
        self.is_updateable = self.check_type(jobject, "weka.classifiers.UpdateableClassifier")
        self.is_drawable = self.check_type(jobject, "weka.core.Drawable")
        super(Classifier, self).__init__(jobject=jobject, options=options)

    def get_capabilities(self):
        """
        Returns the capabilities of the classifier.
        :return: the capabilities
        :rtype: Capabilities
        """
        return Capabilities(javabridge.call(self.jobject, "getCapabilities", "()Lweka/core/Capabilities;"))

    def build_classifier(self, data):
        """
        Builds the classifier with the data.
        :param data: the data to train the classifier with
        :type data: Instances
        """
        javabridge.call(self.jobject, "buildClassifier", "(Lweka/core/Instances;)V", data.jobject)

    def update_classifier(self, inst):
        """
        Updates the classifier with the instance.
        :param inst: the Instance to update the classifier with
        :type inst: Instance
        """
        if self.is_updateable:
            javabridge.call(self.jobject, "updateClassifier", "(Lweka/core/Instance;)V", inst.jobject)
        else:
            logger.critical(wutils.get_classname(self.jobject) + " is not updateable!")

    def classify_instance(self, inst):
        """
        Peforms a prediction.
        :param inst: the Instance to get a prediction for
        :type inst: Instance
        :return: the classification (either regression value or 0-based label index)
        :rtype: float
        """
        return javabridge.call(self.jobject, "classifyInstance", "(Lweka/core/Instance;)D", inst.jobject)

    def distribution_for_instance(self, inst):
        """
        Peforms a prediction, returning the class distribution.
        :param inst: the Instance to get the class distribution for
        :type inst: Instance
        :return: the class distribution array
        :rtype: ndarray
        """
        pred = javabridge.call(self.jobject, "distributionForInstance", "(Lweka/core/Instance;)[D", inst.jobject)
        return javabridge.get_env().get_double_array_elements(pred)

    def graph_type(self):
        """
        Returns the graph type if classifier implements weka.core.Drawable, otherwise -1.
        :return: the type
        :rtype: int
        """
        if self.is_drawable:
            return javabridge.call(self.jobject, "graphType", "()I")
        else:
            return -1

    def graph(self):
        """
        Returns the graph if classifier implements weka.core.Drawable, otherwise None.
        :return: the generated graph string
        :rtype: str
        """
        if self.is_drawable:
            return javabridge.call(self.jobject, "graph", "()Ljava/lang/String;")
        else:
            return None

    @classmethod
    def make_copy(cls, classifier):
        """
        Creates a copy of the classifier.
        :param classifier: the classifier to copy
        :type classifier: Classifier
        :return: the copy of the classifier
        :rtype: Classifier
        """
        return Classifier(
            jobject=javabridge.static_call(
                "weka/classifiers/AbstractClassifier", "makeCopy",
                "(Lweka/classifiers/Classifier;)Lweka/classifiers/Classifier;", classifier.jobject))


class SingleClassifierEnhancer(Classifier):
    """
    Wrapper class for classifiers that use a single base classifier.
    """

    def __init__(self, classname=None, jobject=None, options=None):
        """
        Initializes the specified classifier using either the classname or the supplied JB_Object.
        :param classname: the classname of the classifier
        :type classname: str
        :param jobject: the JB_Object to use
        :type jobject: JB_Object
        :param options: the list of commandline options to set
        :type options: list
        """
        if jobject is None:
            jobject = Classifier.new_instance(classname)
        self.enforce_type(jobject, "weka.classifiers.SingleClassifierEnhancer")
        super(SingleClassifierEnhancer, self).__init__(classname=classname, jobject=jobject, options=options)

    def set_classifier(self, classifier):
        """
        Sets the base classifier.
        :param classifier: the base classifier to use
        """
        javabridge.call(self.jobject, "setClassifier", "(Lweka/classifiers/Classifier;)V", classifier.jobject)

    def get_classifier(self):
        """
        Returns the base classifier.
        :rtype: Classifier
        """
        return Classifier(javabridge.call(self.jobject, "getClassifier", "()Lweka/classifiers/Classifier;"))


class FilteredClassifier(SingleClassifierEnhancer):
    """
    Wrapper class for the filtered classifier.
    """

    def __init__(self, jobject=None, options=None):
        """
        Initializes the specified classifier using either the classname or the supplied JB_Object.
        :param jobject: the JB_Object to use
        :type jobject: JB_Object
        :param options: the list of commandline options to set
        :type options: list
        """
        classname = "weka.classifiers.meta.FilteredClassifier"
        if jobject is None:
            jobject = Classifier.new_instance(classname)
        else:
            self.enforce_type(jobject, classname)
        super(FilteredClassifier, self).__init__(jobject=jobject, options=options)

    def set_filter(self, filtr):
        """
        Sets the filter.
        :param filtr: the filter to use
        :type filtr: Filter
        """
        javabridge.call(self.jobject, "setFilter", "(Lweka/filters/Filter;)V", filtr.jobject)

    def get_filter(self):
        """
        Returns the filter.
        :return: the filter in use
        :rtype: Filter
        """
        return Filter(javabridge.call(self.jobject, "getFilter", "()Lweka/filters/Filter;"))


class MultipleClassifiersCombiner(Classifier):
    """
    Wrapper class for classifiers that use a multiple base classifiers.
    """

    def __init__(self, classname=None, jobject=None, options=None):
        """
        Initializes the specified classifier using either the classname or the supplied JB_Object.
        :param classname: the classname of the classifier
        :type classname: str
        :param jobject: the JB_Object to use
        :type jobject: JB_Object
        :param options: list of commandline options
        :type options: list
        """
        if jobject is None:
            jobject = Classifier.new_instance(classname)
        self.enforce_type(jobject, "weka.classifiers.MultipleClassifiersCombiner")
        super(MultipleClassifiersCombiner, self).__init__(classname=classname, jobject=jobject, options=options)

    def set_classifiers(self, classifiers):
        """
        Sets the base classifiers.
        :param classifiers: the list of base classifiers to use
        :type classifiers: list
        """
        obj = []
        for classifier in classifiers:
            obj.append(classifier.jobject)
        javabridge.call(self.jobject, "setClassifiers", "([Lweka/classifiers/Classifier;)V", obj)

    def get_classifiers(self):
        """
        Returns the list of base classifiers.
        :return: the classifier list
        :rtype: list
        """
        objects = javabridge.get_env().get_object_array_elements(
            javabridge.call(self.jobject, "getClassifiers", "()[Lweka/classifiers/Classifier;"))
        result = []
        for obj in objects:
            result.append(Classifier(jobject=obj))
        return result


class Prediction(JavaObject):
    """
    Wrapper class for a prediction.
    """

    def __init__(self, jobject):
        """
        Initializes the wrapper.
        :param jobject: the prediction to wrap
        :type jobject: JB_Object
        """
        self.enforce_type(jobject, "weka.classifiers.evaluation.Prediction")
        super(Prediction, self).__init__(jobject)

    def actual(self):
        """
        Returns the actual value.
        :return: the actual value (internal representation)
        :rtype: float
        """
        return javabridge.call(self.jobject, "actual", "()D")

    def predicted(self):
        """
        Returns the predicted value.
        :return: the predicted value (internal representation)
        :rtype: float
        """
        return javabridge.call(self.jobject, "predicted", "()D")

    def weight(self):
        """
        Returns the weight.
        :return: the weight of the Instance that was used
        :rtype: float
        """
        return javabridge.call(self.jobject, "weight", "()D")


class NominalPrediction(Prediction):
    """
    Wrapper class for a nominal prediction.
    """

    def __init__(self, jobject):
        """
        Initializes the wrapper.
        :param jobject: the prediction to wrap
        :type jobject: JB_Object
        """
        self.enforce_type(jobject, "weka.classifiers.evaluation.NominalPrediction")
        super(NominalPrediction, self).__init__(jobject)

    def distribution(self):
        """
        Returns the class distribution.
        :return: the class distribution list
        :rtype: ndarray
        """
        return javabridge.get_env().get_double_array_elements(javabridge.call(self.jobject, "distribution", "()[D"))

    def margin(self):
        """
        Returns the margin.
        :return: the margin
        :rtype: float
        """
        return javabridge.call(self.jobject, "margin", "()D")


class NumericPrediction(Prediction):
    """
    Wrapper class for a numeric prediction.
    """

    def __init__(self, jobject):
        """
        Initializes the wrapper.
        :param jobject: the prediction to wrap
        :type jobject: JB_Object
        """
        self.enforce_type(jobject, "weka.classifiers.evaluation.NumericPrediction")
        super(NumericPrediction, self).__init__(jobject)

    def error(self):
        """
        Returns the error.
        :return: the error
        :rtype: float
        """
        return javabridge.call(self.jobject, "error", "()D")

    def prediction_intervals(self):
        """
        Returns the prediction intervals.
        :return: the intervals
        :rtype: ndarray
        """
        return arrays.double_matrix_to_ndarray(javabridge.call(self.jobject, "predictionIntervals", "()[[D"))


class CostMatrix(JavaObject):
    """
    Class for storing and manipulating a misclassification cost matrix. The element at position i,j in the matrix
    is the penalty for classifying an instance of class j as class i. Cost values can be fixed or computed on a
    per-instance basis (cost sensitive evaluation only) from the value of an attribute or an expression involving
    attribute(s).
    """

    def __init__(self, matrx=None, num_classes=None):
        """
        Initializes the matrix object.
        :param matrx: the matrix to copy
        :type matrx: CostMatrix or ndarray
        :param num_classes: the number of classes
        :type num_classes: int
        """
        if not matrx is None:
            if isinstance(matrx, CostMatrix):
                jobject = javabridge.make_instance(
                    "weka/classifiers/CostMatrix", "(Lweka/classifiers/CostMatrix;)V", matrx.jobject)
                super(CostMatrix, self).__init__(jobject)
            elif isinstance(matrx, ndarray):
                shp = matrx.shape
                if len(shp) != 2:
                    raise Exception("Numpy array must be a 2-dimensional array!")
                rows, cols = shp
                if rows == cols:
                    cmatrix = CostMatrix(num_classes=rows)
                    for r in xrange(rows):
                        for c in xrange(cols):
                            cmatrix.set_element(r, c, matrx[r][c])
                    super(CostMatrix, self).__init__(cmatrix.jobject)
                else:
                    raise Exception("Numpy array must be a square matrix!")
            else:
                raise Exception("Matrix must be either a CostMatrix or a 2-dimensional numpy array: " + str(type(matrx)))
        elif not num_classes is None:
            jobject = javabridge.make_instance(
                "weka/classifiers/CostMatrix", "(I)V", num_classes)
            super(CostMatrix, self).__init__(jobject)
        else:
            raise Exception("Either matrix or number of classes must be provided!")

    def apply_cost_matrix(self, data, rnd):
        """
        Applies the cost matrix to the data.
        :param data: the data to apply to
        :type data: Instances
        :param rnd: the random number generator
        :type rnd: Random
        """
        return Instances(
            javabridge.call(
                self.jobject, "applyCostMatrix", "(Lweka/core/Instances;Ljava/util/Random;)Lweka/core/Instances;",
                data.jobject, rnd.jobject))

    def expected_costs(self, class_probs, inst=None):
        """
        Calculates the expected misclassification cost for each possible class value, given class probability
        estimates.
        :param class_probs: the class probabilities
        :type class_probs: ndarray
        :return: the calculated costs
        :rtype: ndarray
        """
        if inst is None:
            costs = javabridge.call(
                self.jobject, "expectedCosts", "([D)[D", javabridge.get_env().make_double_array(class_probs))
            return javabridge.get_env().get_double_array_elements(costs)
        else:
            costs = javabridge.call(
                self.jobject, "expectedCosts", "([DLweka/core/Instance;)[D",
                javabridge.get_env().make_double_array(class_probs), inst.jobject)
            return javabridge.get_env().get_double_array_elements(costs)

    def get_cell(self, row, col):
        """
        Returns the JB_Object at the specified location.
        :param row: the 0-based index of the row
        :type row: int
        :param col: the 0-based index of the column
        :type col: int
        :return: the object in that cell
        :rtype: JB_Object
        """
        return javabridge.call(
            self.jobject, "getCell", "(II)Ljava/lang/Object;", row, col)

    def set_cell(self, row, col, obj):
        """
        Sets the JB_Object at the specified location. Automatically unwraps JavaObject.
        :param row: the 0-based index of the row
        :type row: int
        :param col: the 0-based index of the column
        :type col: int
        :param obj: the object for that cell
        :type obj: object
        """
        if isinstance(obj, JavaObject):
            obj = obj.jobject
        javabridge.call(
            self.jobject, "setCell", "(IILjava/lang/Object;)V", row, col, obj)

    def get_element(self, row, col, inst=None):
        """
        Returns the value at the specified location.
        :param row: the 0-based index of the row
        :type row: int
        :param col: the 0-based index of the column
        :type col: int
        :param inst: the Instace
        :type inst: Instance
        :return: the value in that cell
        :rtype: float
        """
        if inst is None:
            return javabridge.call(
                self.jobject, "getElement", "(II)D", row, col)
        else:
            return javabridge.call(
                self.jobject, "getElement", "(IILweka/core/Instance;)D", row, col, inst.jobject)

    def set_element(self, row, col, value):
        """
        Sets the float value at the specified location.
        :param row: the 0-based index of the row
        :type row: int
        :param col: the 0-based index of the column
        :type col: int
        :param value: the float value for that cell
        :type value: float
        """
        javabridge.call(
            self.jobject, "setElement", "(IID)V", row, col, value)

    def get_max_cost(self, class_value, inst=None):
        """
        Gets the maximum cost for a particular class value.
        :param class_value: the class value to get the maximum cost for
        :type class_value: int
        :param inst: the Instance
        :type inst: Instance
        :return: the cost
        :rtype: float
        """
        if inst is None:
            return javabridge.call(
                self.jobject, "getMaxCost", "(I)D", class_value)
        else:
            return javabridge.call(
                self.jobject, "getElement", "(ILweka/core/Instance;)D", class_value, inst.jobject)

    def initialize(self):
        """
        Initializes the matrix.
        """
        javabridge.call(self.jobject, "initialize", "()V")

    def normalize(self):
        """
        Normalizes the matrix.
        """
        javabridge.call(self.jobject, "normalize", "()V")

    def num_columns(self):
        """
        Returns the number of columns.
        :return: the number of columns
        :rtype: int
        """
        return javabridge.call(self.jobject, "numColumns", "()I")

    def num_rows(self):
        """
        Returns the number of rows.
        :return: the number of rows
        :rtype: int
        """
        return javabridge.call(self.jobject, "numRows", "()I")

    def size(self):
        """
        Returns the number of rows/columns.
        :return: the number of rows/columns
        :rtype: int
        """
        return javabridge.call(self.jobject, "size", "()I")

    def to_matlab(self):
        """
        Returns the matrix in Matlab format.
        :return: the matrix as Matlab formatted string
        :rtype: str
        """
        return javabridge.call(self.jobject, "toMatlab", "()Ljava/lang/String;")


class Evaluation(JavaObject):
    """
    Evaluation class for classifiers.
    """

    def __init__(self, data, cost_matrix=None):
        """
        Initializes an Evaluation object.
        :param data: the data to use to initialize the priors with
        :type data: Instances
        :param cost_matrix: the cost matrix to use for initializing
        :type cost_matrix: CostMatrix
        """
        if cost_matrix is None:
            jobject = javabridge.make_instance(
                "weka/classifiers/EvaluationWrapper", "(Lweka/core/Instances;)V",
                data.jobject)
        else:
            jobject = javabridge.make_instance(
                "weka/classifiers/EvaluationWrapper", "(Lweka/core/Instances;Lweka/classifiers/CostMatrix;)V",
                data.jobject, cost_matrix.jobject)
        self.wrapper = jobject
        jobject = javabridge.call(jobject, "getEvaluation", "()Lweka/classifiers/Evaluation;")
        super(Evaluation, self).__init__(jobject)

    def crossvalidate_model(self, classifier, data, num_folds, rnd, output=None):
        """
        Crossvalidates the model using the specified data, number of folds and random number generator wrapper.
        :param classifier: the classifier to cross-validate
        :type classifier: Classifier
        :param data: the data to evaluate on
        :type data: Instances
        :param num_folds: the number of folds
        :type num_folds: int
        :param rnd: the random number generator to use
        :type rnd: Random
        :param output: the output generator to use
        :type output: PredictionOutput
        """
        if output is None:
            generator = []
        else:
            generator = [output.jobject]
        javabridge.call(
            self.jobject, "crossValidateModel",
            "(Lweka/classifiers/Classifier;Lweka/core/Instances;ILjava/util/Random;[Ljava/lang/Object;)V",
            classifier.jobject, data.jobject, num_folds, rnd.jobject, generator)

    def evaluate_train_test_split(self, classifier, data, percentage, rnd, output=None):
        """
        Splits the data into train and test, builds the classifier with the training data and
        evaluates it against the test set.
        :param classifier: the classifier to cross-validate
        :type classifier: Classifier
        :param data: the data to evaluate on
        :type data: Instances
        :param percentage: the percentage split to use (amount to use for training)
        :type percentage: double
        :param rnd: the random number generator to use, if None the order gets preserved
        :type rnd: Random
        :param output: the output generator to use
        :type output: PredictionOutput
        """
        if not rnd is None:
            data.randomize(rnd)
        train_size = int(round(data.num_instances() * percentage / 100))
        test_size = data.num_instances() - train_size
        train_inst = Instances.copy_instances(data, 0, train_size)
        test_inst = Instances.copy_instances(data, train_size, test_size)
        cls = Classifier.make_copy(classifier)
        cls.build_classifier(train_inst)
        self.test_model(cls, test_inst, output=output)

    def test_model(self, classifier, data, output=None):
        """
        Evaluates the built model using the specified test data and returns the classifications.
        :param classifier: the trained classifier to evaluate
        :type classifier: Classifier
        :param data: the data to evaluate on
        :type data: Instances
        :param output: the output generator to use
        :type output: PredictionOutput
        :return: the classifications
        :rtype: ndarray
        """
        if output is None:
            generator = []
        else:
            generator = [output.jobject]
        cls = javabridge.call(
            self.jobject, "evaluateModel",
            "(Lweka/classifiers/Classifier;Lweka/core/Instances;[Ljava/lang/Object;)[D",
            classifier.jobject, data.jobject, generator)
        if cls is None:
            return None
        else:
            return javabridge.get_env().get_double_array_elements(cls)

    def test_model_once(self, classifier, inst):
        """
        Evaluates the built model using the specified test instance and returns the classification.
        :param classifier: the classifier to cross-validate
        :type classifier: Classifier
        :param inst: the Instance to evaluate on
        :type inst: Instances
        :return: the classification
        :rtype: float
        """
        return javabridge.call(
            self.jobject, "evaluateModelOnce",
            "(Lweka/classifiers/Classifier;Lweka/core/Instance;)D",
            classifier.jobject, inst.jobject)

    def to_summary(self, title=None):
        """
        Generates a summary.
        :param title: optional title
        :type title: str
        :return: the summary
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
        :type title: str
        :return: the details
        :rtype: str
        """
        if title is None:
            return javabridge.call(
                self.jobject, "toClassDetailsString", "()Ljava/lang/String;")
        else:
            return javabridge.call(
                self.jobject, "toClassDetailsString", "(Ljava/lang/String;)Ljava/lang/String;", title)

    def to_matrix(self, title=None):
        """
        Generates the confusion matrix.
        :param title: optional title
        :type title: str
        :return: the matrix
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
        :type class_index: int
        :return: the area
        :rtype: float
        """
        return javabridge.call(self.jobject, "areaUnderPRC", "(I)D", class_index)

    def weighted_area_under_prc(self):
        """
        Returns the weighted area under precision recall curve.
        :return: the weighted area
        :rtype: float
        """
        return javabridge.call(self.jobject, "weightedAreaUnderPRC", "()D")

    def area_under_roc(self, class_index):
        """
        Returns the area under receiver operators characteristics curve.
        :param class_index: the 0-based index of the class label
        :type class_index: int
        :return: the area
        :rtype: float
        """
        return javabridge.call(self.jobject, "areaUnderROC", "(I)D", class_index)

    def weighted_area_under_roc(self):
        """
        Returns the weighted area under receiver operator characteristic curve.
        :return: the weighted area
        :rtype: float
        """
        return javabridge.call(self.jobject, "weightedAreaUnderROC", "()D")

    def avg_cost(self):
        """
        Returns the average cost.
        :return: the cost
        :rtype: float
        """
        return javabridge.call(self.jobject, "avgCost", "()D")

    def total_cost(self):
        """
        Returns the total cost.
        :return: the cost
        :rtype: float
        """
        return javabridge.call(self.jobject, "totalCost", "()D")

    def confusion_matrix(self):
        """
        Returns the confusion matrix.
        :return: the matrix
        :rtype: ndarray
        """
        return arrays.double_matrix_to_ndarray(javabridge.call(self.jobject, "confusionMatrix", "()[[D"))

    def correct(self):
        """
        Returns the correct count (nominal classes).
        :return: the count
        :rtype: float
        """
        return javabridge.call(self.jobject, "correct", "()D")

    def incorrect(self):
        """
        Returns the incorrect count (nominal classes).
        :return: the count
        :rtype: float
        """
        return javabridge.call(self.jobject, "incorrect", "()D")

    def unclassified(self):
        """
        Returns the unclassified count.
        :return: the count
        :rtype: float
        """
        return javabridge.call(self.jobject, "unclassified", "()D")

    def num_instances(self):
        """
        Returns the number of instances that had a known class value.
        :return: the number of instances
        :rtype: float
        """
        return javabridge.call(self.jobject, "numInstances", "()D")

    def percent_correct(self):
        """
        Returns the percent correct (nominal classes).
        :return: the percentage
        :rtype: float
        """
        return javabridge.call(self.jobject, "pctCorrect", "()D")

    def percent_incorrect(self):
        """
        Returns the percent incorrect (nominal classes).
        :return: the percentage
        :rtype: float
        """
        return javabridge.call(self.jobject, "pctIncorrect", "()D")

    def percent_unclassified(self):
        """
        Returns the percent unclassified.
        :return: the percentage
        :rtype: float
        """
        return javabridge.call(self.jobject, "pctUnclassified", "()D")

    def correlation_coefficient(self):
        """
        Returns the correlation coefficient (numeric classes).
        :return: the coefficient
        :rtype: float
        """
        return javabridge.call(self.jobject, "correlationCoefficient", "()D")

    def matthews_correlation_coefficient(self, class_index):
        """
        Returns the Matthews correlation coefficient (nominal classes).
        :param class_index: the 0-based index of the class label
        :type class_index: int
        :return: the coefficient
        :rtype: float
        """
        return javabridge.call(self.jobject, "matthewsCorrelationCoefficient", "(I)D", class_index)

    def weighted_matthews_correlation(self):
        """
        Returns the weighted Matthews correlation (nominal classes).
        :return: the correlation
        :rtype: float
        """
        return javabridge.call(self.jobject, "weightedMatthewsCorrelation", "()D")

    def coverage_of_test_cases_by_predicted_regions(self):
        """
        Returns the coverage of the test cases by the predicted regions at the confidence level
        specified when evaluation was performed.
        :return: the coverage
        :rtype: float
        """
        return javabridge.call(self.jobject, "coverageOfTestCasesByPredictedRegions", "()D")

    def size_of_predicted_regions(self):
        """
        Returns  the average size of the predicted regions, relative to the range of the target in the
        training data, at the confidence level specified when evaluation was performed.
        :return:the size of the regions
        :rtype: float
        """
        return javabridge.call(self.jobject, "sizeOfPredictedRegions", "()D")

    def error_rate(self):
        """
        Returns the error rate (numeric classes).
        :return: the rate
        :rtype: float
        """
        return javabridge.call(self.jobject, "errorRate", "()D")

    def mean_absolute_error(self):
        """
        Returns the mean absolute error.
        :return: the error
        :rtype: float
        """
        return javabridge.call(self.jobject, "meanAbsoluteError", "()D")

    def relative_absolute_error(self):
        """
        Returns the relative absolute error.
        :return: the error
        :rtype: float
        """
        return javabridge.call(self.jobject, "relativeAbsoluteError", "()D")

    def root_mean_squared_error(self):
        """
        Returns the root mean squared error.
        :return: the error
        :rtype: float
        """
        return javabridge.call(self.jobject, "rootMeanSquaredError", "()D")

    def root_relative_squared_error(self):
        """
        Returns the root relative squared error.
        :return: the error
        :rtype: float
        """
        return javabridge.call(self.jobject, "rootRelativeSquaredError", "()D")

    def root_mean_prior_squared_error(self):
        """
        Returns the root mean prior squared error.
        :return: the error
        :rtype: float
        """
        return javabridge.call(self.jobject, "rootMeanPriorSquaredError", "()D")

    def mean_prior_absolute_error(self):
        """
        Returns the mean prior absolute error.
        :return: the error
        :rtype: float
        """
        return javabridge.call(self.jobject, "meanPriorAbsoluteError", "()D")

    def false_negative_rate(self, class_index):
        """
        Returns the false negative rate.
        :param class_index: the 0-based index of the class label
        :type class_index: int
        :return: the rate
        :rtype: float
        """
        return javabridge.call(self.jobject, "falseNegativeRate", "(I)D", class_index)

    def weighted_false_negative_rate(self):
        """
        Returns the weighted false negative rate.
        :return: the rate
        :rtype: float
        """
        return javabridge.call(self.jobject, "weightedFalseNegativeRate", "()D")

    def false_positive_rate(self, class_index):
        """
        Returns the false positive rate.
        :param class_index: the 0-based index of the class label
        :type class_index: int
        :return: the rate
        :rtype: float
        """
        return javabridge.call(self.jobject, "falsePositiveRate", "(I)D", class_index)

    def weighted_false_positive_rate(self):
        """
        Returns the weighted false positive rate.
        :return: the rate
        :rtype: float
        """
        return javabridge.call(self.jobject, "weightedFalsePositiveRate", "()D")

    def num_false_negatives(self, class_index):
        """
        Returns the number of false negatives.
        :param class_index: the 0-based index of the class label
        :type class_index: int
        :return: the count
        :rtype: float
        """
        return javabridge.call(self.jobject, "numFalseNegatives", "(I)D", class_index)

    def true_negative_rate(self, class_index):
        """
        Returns the true negative rate.
        :param class_index: the 0-based index of the class label
        :type class_index: int
        :return: the rate
        :rtype: float
        """
        return javabridge.call(self.jobject, "trueNegativeRate", "(I)D", class_index)

    def weighted_true_negative_rate(self):
        """
        Returns the weighted true negative rate.
        :return: the rate
        :rtype: float
        """
        return javabridge.call(self.jobject, "weightedTrueNegativeRate", "()D")

    def num_true_negatives(self, class_index):
        """
        Returns the number of true negatives.
        :param class_index: the 0-based index of the class label
        :type class_index: int
        :return: the count
        :rtype: float
        """
        return javabridge.call(self.jobject, "numTrueNegatives", "(I)D", class_index)

    def num_false_positives(self, class_index):
        """
        Returns the number of false positives.
        :param class_index: the 0-based index of the class label
        :type class_index: int
        :return: the count
        :rtype: float
        """
        return javabridge.call(self.jobject, "numFalsePositives", "(I)D", class_index)

    def true_positive_rate(self, class_index):
        """
        Returns the true positive rate.
        :param class_index: the 0-based index of the class label
        :type class_index: int
        :return: the rate
        :rtype: float
        """
        return javabridge.call(self.jobject, "truePositiveRate", "(I)D", class_index)

    def weighted_true_positive_rate(self):
        """
        Returns the weighted true positive rate.
        :return: the rate
        :rtype: float
        """
        return javabridge.call(self.jobject, "weightedTruePositiveRate", "()D")

    def num_true_positives(self, class_index):
        """
        Returns the number of true positives.
        :param class_index: the 0-based index of the class label
        :type class_index: int
        :return: the count
        :rtype: float
        """
        return javabridge.call(self.jobject, "numTruePositives", "(I)D", class_index)

    def f_measure(self, class_index):
        """
        Returns the f measure.
        :param class_index: the 0-based index of the class label
        :type class_index: int
        :return: the measure
        :rtype: float
        """
        return javabridge.call(self.jobject, "fMeasure", "(I)D", class_index)

    def weighted_f_measure(self):
        """
        Returns the weighted f measure.
        :return: the measure
        :rtype: float
        """
        return javabridge.call(self.jobject, "weightedFMeasure", "()D")

    def unweighted_macro_f_measure(self):
        """
        Returns the unweighted macro-averaged F-measure.
        :return: the measure
        :rtype: float
        """
        return javabridge.call(self.jobject, "unweightedMacroFmeasure", "()D")

    def unweighted_micro_f_measure(self):
        """
        Returns the unweighted micro-averaged F-measure.
        :return: the measure
        :rtype: float
        """
        return javabridge.call(self.jobject, "unweightedMicroFmeasure", "()D")

    def precision(self, class_index):
        """
        Returns the precision.
        :param class_index: the 0-based index of the class label
        :type class_index: int
        :return: the precision
        :rtype: float
        """
        return javabridge.call(self.jobject, "precision", "(I)D", class_index)

    def weighted_precision(self):
        """
        Returns the weighted precision.
        :return: the precision
        :rtype: float
        """
        return javabridge.call(self.jobject, "weightedPrecision", "()D")

    def recall(self, class_index):
        """
        Returns the recall.
        :param class_index: the 0-based index of the class label
        :type class_index: int
        :return: the recall
        :rtype: float
        """
        return javabridge.call(self.jobject, "recall", "(I)D", class_index)

    def weighted_recall(self):
        """
        Returns the weighted recall.
        :return: the recall
        :rtype: float
        """
        return javabridge.call(self.jobject, "weightedRecall", "()D")

    def kappa(self):
        """
        Returns kappa.
        :return: kappa
        :rtype: float
        """
        return javabridge.call(self.jobject, "kappa", "()D")

    def kb_information(self):
        """
        Returns KB information.
        :return: the information
        :rtype: float
        """
        return javabridge.call(self.jobject, "KBInformation", "()D")

    def kb_mean_information(self):
        """
        Returns KB mean information.
        :return: the information
        :rtype: float
        """
        return javabridge.call(self.jobject, "KBMeanInformation", "()D")

    def kb_relative_information(self):
        """
        Returns KB relative information.
        :return: the information
        :rtype: float
        """
        return javabridge.call(self.jobject, "KBRelativeInformation", "()D")

    def sf_entropy_gain(self):
        """
        Returns the total SF, which is the null model entropy minus the scheme entropy.
        :return: the gain
        :rtype: float
        """
        return javabridge.call(self.jobject, "SFEntropyGain", "()D")

    def sf_mean_entropy_gain(self):
        """
        Returns the SF per instance, which is the null model entropy minus the scheme entropy, per instance.
        :return: the gain
        :rtype: float
        """
        return javabridge.call(self.jobject, "SFMeanEntropyGain", "()D")

    def sf_mean_prior_entropy(self):
        """
        Returns the entropy per instance for the null model.
        :return: the entropy
        :rtype: float
        """
        return javabridge.call(self.jobject, "SFMeanPriorEntropy", "()D")

    def sf_mean_scheme_entropy(self):
        """
        Returns the entropy per instance for the scheme.
        :return: the entropy
        :rtype: float
        """
        return javabridge.call(self.jobject, "SFMeanSchemeEntropy", "()D")

    def set_class_priors(self, data):
        """
        Sets the class priors derived from the dataset.
        :param data: the dataset to derive the priors from
        :type data: Instances
        """
        return javabridge.call(self.jobject, "setClassPriors", "(Lweka/core/Instances;)V", data)

    def get_class_priors(self):
        """
        Returns the class priors.
        :return: the priors
        :rtype: ndarray
        """
        return javabridge.get_env().get_double_array_elements(javabridge.call(self.jobject, "getClassPriors", "()[D"))

    def header(self):
        """
        Returns the header format.
        :return: the header format
        :rtype: Instances
        """
        return Instances(javabridge.call(self.jobject, "getHeader", "()Lweka/core/Instances;"))

    def set_discard_predictions(self, discard):
        """
        Sets whether to discard predictions (saves memory).
        :param discard: True if to discard predictions
        :type discard: bool
        """
        javabridge.call(self.jobject, "setDiscardPredictions", "(Z)V", discard)

    def get_discard_predictions(self):
        """
        Returns whether to discard predictions (saves memory).
        :return: True if to discard
        :rtype: bool
        """
        return javabridge.call(self.jobject, "getDiscardPredictions", "()Z")

    def predictions(self):
        """
        Returns the predictions.
        :return: the predictions
        :rtype: list
        """
        preds = javabridge.get_collection_wrapper(
            javabridge.call(self.jobject, "predictions", "()Ljava/util/ArrayList;"))
        result = []
        for pred in preds:
            if javabridge.is_instance_of(pred, "weka/classifiers/evaluation/NominalPrediction"):
                result.append(NominalPrediction(pred))
            elif javabridge.is_instance_of(pred, "weka/classifiers/evaluation/NumericPrediction"):
                result.append(NumericPrediction(pred))
            else:
                result.append(Prediction(pred))
        return result

    @classmethod
    def evaluate_model(cls, classifier, args):
        """
        Evaluates the classifier with the given options.
        :param classifier: the classifier instance to use
        :type classifier: Classifier
        :param args: the command-line arguments to use
        :type args: list
        :return: the evaluation string
        :rtype : str
        """
        return javabridge.static_call(
            "Lweka/classifiers/Evaluation;", "evaluateModel",
            "(Lweka/classifiers/Classifier;[Ljava/lang/String;)Ljava/lang/String;",
            classifier.jobject, args)


class PredictionOutput(OptionHandler):
    """
    For collecting predictions and generating output from.
    Must be derived from weka.classifiers.evaluation.output.prediction.AbstractOutput
    """

    def __init__(self, classname=None, jobject=None, options=None):
        """
        Initializes the specified output generator using either the classname or the supplied JB_Object.
        :param classname: the classname of the generator
        :type classname: str
        :param jobject: the JB_Object to use
        :type jobject: JB_Object
        :param options: the list of commandline options to set
        :type options: list
        """
        if jobject is None:
            jobject = PredictionOutput.new_instance(classname)
        self.enforce_type(jobject, "weka.classifiers.evaluation.output.prediction.AbstractOutput")
        super(PredictionOutput, self).__init__(jobject=jobject, options=options)
        buf = javabridge.make_instance("java/lang/StringBuffer", "()V")
        javabridge.call(self.jobject, "setBuffer", "(Ljava/lang/StringBuffer;)V", buf)

    def set_header(self, data):
        """
        Sets the header format.
        :param data: The dataset format
        :type data: Instances
        """
        javabridge.call(self.jobject, "setHeader", "(Lweka/core/Instances;)V", data.jobject)

    def get_header(self):
        """
        Returns the header format.
        :return: The dataset format
        :rtype: Instances
        """
        return Instances(javabridge.call(self.jobject, "getHeader", "()Lweka/core/Instances;"))

    def print_header(self):
        """
        Prints the header to the buffer.
        """
        javabridge.call(self.jobject, "printHeader", "()V")

    def print_footer(self):
        """
        Prints the footer to the buffer.
        """
        javabridge.call(self.jobject, "printFooter", "()V")

    def print_all(self, cls, data):
        """
        Prints the header, classifications and footer to the buffer.
        :param cls: the classifier
        :type cls: Classifier
        :param data: the test data
        :type data: Instances
        """
        javabridge.call(
            self.jobject, "print", "(Lweka/classifiers/Classifier;Lweka/core/Instances;)V",
            cls.jobject, data.jobject)

    def print_classifications(self, cls, data):
        """
        Prints the classifications to the buffer.
        :param cls: the classifier
        :type cls: Classifier
        :param data: the test data
        :type data: Instances
        """
        javabridge.call(
            self.jobject, "printClassifications", "(Lweka/classifiers/Classifier;Lweka/core/Instances;)V",
            cls.jobject, data.jobject)

    def print_classification(self, cls, inst, index):
        """
        Prints the classification to the buffer.
        :param cls: the classifier
        :type cls: Classifier
        :param inst: the test instance
        :type inst: Instance
        :param index: the 0-based index of the test instance
        :type index: int
        """
        javabridge.call(
            self.jobject, "printClassification", "(Lweka/classifiers/Classifier;Lweka/core/Instance;I)V",
            cls.jobject, inst.jobject, index)

    def get_buffer_content(self):
        """
        Returns the content of the buffer as string.
        :return: The buffer content
        :rtype: str
        """
        return javabridge.to_string(javabridge.call(self.jobject, "getBuffer", "()Ljava/lang/StringBuffer;"))

    def __str__(self):
        """
        Returns the content of the buffer.
        :return: the current buffer content
        :rtype: str
        """
        return self.get_buffer_content()


def predictions_to_instances(data, preds):
    """
    Turns the predictions turned into an Instances object.
    :param data: the original dataset format
    :type data: Instances
    :param preds: the predictions to convert
    :type preds: list
    :return: the predictions, None if no predictions present
    :rtype: Instances
    """
    if len(preds) == 0:
        return None

    is_numeric = isinstance(preds[0], NumericPrediction)

    # create header
    atts = []
    if is_numeric:
        atts.append(Attribute.create_numeric("index"))
        atts.append(Attribute.create_numeric("weight"))
        atts.append(Attribute.create_numeric("actual"))
        atts.append(Attribute.create_numeric("predicted"))
        atts.append(Attribute.create_numeric("error"))
    else:
        atts.append(Attribute.create_numeric("index"))
        atts.append(Attribute.create_numeric("weight"))
        atts.append(data.get_class_attribute().copy(name="actual"))
        atts.append(data.get_class_attribute().copy(name="predicted"))
        atts.append(Attribute.create_nominal("error", ["no", "yes"]))
        atts.append(Attribute.create_numeric("classification"))
        for i in xrange(data.get_class_attribute().num_values()):
            atts.append(Attribute.create_numeric("distribution-" + data.get_class_attribute().value(i)))

    result = Instances.create_instances("Predictions", atts, len(preds))

    count = 0
    for pred in preds:
        count += 1
        if is_numeric:
            values = array([count, pred.weight(), pred.actual(), pred.predicted(), pred.error()])
        else:
            if pred.actual() == pred.predicted():
                error = 0.0
            else:
                error = 1.0
            l = [count, pred.weight(), pred.actual(), pred.predicted(), error, max(pred.distribution())]
            for i in xrange(data.get_class_attribute().num_values()):
                l.append(pred.distribution()[i])
            values = array(l)
        inst = Instance.create_instance(values)
        result.add_instance(inst)

    return result


def main(args):
    """
    Runs a classifier from the command-line. Calls JVM start/stop automatically.
    Options:
        [-j jar1[:jar2...]]
        [-X max heap size]
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

    usage = "Usage: weka.classifiers [-j jar1[" + os.pathsep + "jar2...]] [-X max heap size] -t train " \
            + "[-T test] [-c classindex] " \
            + "[-d output model file] [-l input model file] [-x num folds] [-s seed] [-v # no stats for training] " \
            + "[-o # only stats, no model] [-i # information-retrieval stats per class] " \
            + "-kl # information-theoretic stats] [-m cost matrix file] [-g graph file] " \
            + "classifier classname [classifier options]"

    optlist, optargs = getopt.getopt(args, "j:X:t:T:c:d:l:x:s:voikm:g:h")
    if len(optargs) == 0:
        raise Exception("No classifier classname provided!\n" + usage)
    for opt in optlist:
        if opt[0] == "-h":
            print(usage)
            return

    jars = []
    params = []
    train = None
    heap = None
    for opt in optlist:
        if opt[0] == "-j":
            jars = opt[1].split(os.pathsep)
        elif opt[0] == "-X":
            heap = opt[1]
        elif opt[0] == "-t":
            params.append(opt[0])
            params.append(opt[1])
            train = opt[1]
        elif opt[0] == "-T":
            params.append(opt[0])
            params.append(opt[1])
        elif opt[0] == "-c":
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

    jvm.start(jars, max_heap_size=heap, packages=True)

    logger.debug("Commandline: " + utils.join_options(args))

    try:
        classifier = Classifier(classname=optargs[0])
        optargs = optargs[1:]
        if len(optargs) > 0:
            classifier.set_options(optargs)
        print(Evaluation.evaluate_model(classifier, params))
    except Exception, e:
        print(e)
    finally:
        jvm.stop()

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception, ex:
        print(ex)
