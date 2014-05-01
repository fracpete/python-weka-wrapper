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
import matplotlib.pyplot as plt
from weka.core.classes import JavaObject
from weka.core.dataset import Instances
from weka.classifiers import NumericPrediction


def plot_classifier_errors(predictions, absolute=True, max_relative_size=20, outfile=None, wait=True):
    """
    Plots the classifers for the given list of predictions.
    NB: The plot window blocks execution till closed.
    :param predictions: the predictions to plot
    :type predictions: list
    :param absolute: whether to use absolute errors as size or relative ones
    :type absolute: bool
    :param max_relative_size: the maximum size in point in case of relative mode
    :type max_relative_size: int
    :param outfile: the output file, ignored if None
    :type outfile: str
    :param wait: whether to wait for the user to close the plot
    :type wait: bool
    """
    actual    = []
    predicted = []
    error     = None
    for pred in predictions:
        actual.append(pred.actual())
        predicted.append(pred.predicted())
        if isinstance(pred, NumericPrediction):
            if error is None:
                error = []
            error.append(abs(pred.error()))
    fig, ax = plt.subplots()
    if error is None:
        ax.scatter(actual, predicted)
    else:
        if not absolute:
            min_err = min(error)
            max_err = max(error)
            factor  = (max_err  - min_err) / max_relative_size
            for i in xrange(len(error)):
                error[i] = error[i] / factor * max_relative_size
        ax.scatter(actual, predicted, s=error)
    ax.set_xlabel("actual")
    ax.set_ylabel("predicted")
    ax.set_title("Classifier errors")
    ax.plot(ax.get_xlim(), ax.get_ylim(), ls="--", c="0.3")
    ax.grid(True)
    plt.draw()
    if not outfile is None:
        plt.savefig(outfile)
    if wait:
        plt.show()


def plot_roc(evaluation, class_index=0, outfile=None, wait=True):
    """
    Plots the ROC (receiver operator characteristics) curve for the given predictions.
    :param evaluation: the evaluation to obtain the predictions from
    :type evaluation: Evaluation
    :param class_index: the 0-based index of the class-label to create the plot for
    :type class_index: int
    :param outfile: the output file, ignored if None
    :type outfile: str
    :param wait: whether to wait for the user to close the plot
    :type wait: bool
    """
    jtc = JavaObject.new_instance("weka.classifiers.evaluation.ThresholdCurve")
    pred = javabridge.call(evaluation.jobject, "predictions", "()Ljava/util/ArrayList;")
    data = Instances(javabridge.call(jtc, "getCurve", "(Ljava/util/ArrayList;I)Lweka/core/Instances;", pred, class_index))
    area = javabridge.static_call(
        "weka/classifiers/evaluation/ThresholdCurve", "getROCArea", "(Lweka/core/Instances;)D", data.jobject)
    xi   = data.get_attribute_by_name("False Positive Rate").get_index()
    yi   = data.get_attribute_by_name("True Positive Rate").get_index()
    x    = []
    y    = []
    for i in xrange(data.num_instances()):
        inst = data.get_instance(i)
        x.append(inst.get_value(xi))
        y.append(inst.get_value(yi))
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC (%0.4f)" % area)
    ax.plot(ax.get_xlim(), ax.get_ylim(), ls="--", c="0.3")
    ax.grid(True)
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.draw()
    if not outfile is None:
        plt.savefig(outfile)
    if wait:
        plt.show()
