.. python-weka-wrapper documentation master file, created by
   sphinx-quickstart on Sat Apr 12 11:51:06 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

python-weka-wrapper
===================

Contents:

.. toctree::
   :maxdepth: 2

   index


Introduction
============

*python-weka-wrapper* allows you to use `Weka <http://www.cs.waikato.ac.nz/~ml/weka/>`_ from within Python.

The library uses the `javabridge <https://pypi.python.org/pypi/javabridge>`_ library for starting up,
communicating with and shutting down the Java Virtual Machine in which the Weka processes get executed.

*python-weka-wrapper* provides a thin wrapper around the basic (non-GUI) functionality of Weka.
You can automatically add all your Weka packages to the classpath. Additional jars can be added as well.

Project homepage: https://github.com/fracpete/python-weka-wrapper


Requirements
============

The library has the following requirements:

* javabridge
* pygraphviz
* matplotlib
* PIL
* JDK 1.6+


Command-line
============

From command-line, *python-weka-wrapper* behaves similar to Weka itself, i.e., the command-line.
Most of the general options are available, as well as the following:

* `-j` for adding additional jars, in the same format as the classpath for the platform.
  E.g., for Linux, `-j /some/where/a.jar:/other/place/b.jar`
* `-X` for defining the maximum heap size.
  E.g., `-X 512m` for 512 MB of heap size.

The following examples are all for a Linux bash environment. Windows users have to replace
forwarding slashes `/` with backslashes `\` and place the command on a single line with the
backslashes `\` at the end of the lines removed.


Data generators
---------------

Artifical data can be generated using one of Weka's data generators, e.g., the
`Agrawal` classification generator:

.. code-block:: bash

   python weka/datagenerators.py \
       -o /tmp/out.arff \
       weka.datagenerators.classifiers.classification.Agrawal


Filters
-------

Filtering a single ARFF dataset, removing the last attribute using the `Remove` filter:

.. code-block:: bash

   python weka/filters.py \
       -i /my/datasets/iris.arff \
       -o /tmp/out.arff \
       -c last \
       weka.filters.unsupervised.attribute.Remove \
       -R last

For batch filtering, you can use the `-r` and `-s` options for the input and output
for the second file.


Classifiers
-----------

Example on how to cross-validate a `J48` classifier (with confidence factor 0.3)
on the iris UCI dataset:

.. code-block:: bash

   python weka/classifiers.py \
        -t /my/datasets/iris.arff \
        -c last \
        weka.classifiers.trees.J48
        -C 0.3


Clusterers
----------

Example on how to perform classes-to-clusters evaluation for `SimpleKMeans`
(with 3 clusters) using the iris UCI dataset:

.. code-block:: bash

   pythonn weka/clusterers.py \
       -t /my/datasets/iris.arff \
       -c last \
       weka.clusterers.SimpleKMeans
       -N 3


Attribute selection
-------------------

You can perform attribute selection using `BestFirst` as search algorithm and
`CfsSubsetEval` as evaluator as follows:

.. code-block:: bash

   python weka/attribute_selection.py \
       -i /my/datasets/iris.arff \
       -x 5 \
       -n 42 \
       -s "weka.attributeSelection.BestFirst -D 1 -N 5"
       weka.attributeSelection.CfsSubsetEval \
       -P 1 \
       -E 1


Associators
-----------

Associators, like `Apriori`, can be run like this:

.. code-block:: bash

   python weka/associators.py \
       -t /my/datasets/iris.arff \
       weka.associations.Apriori \
       -N 9 -I


Python
======

The following sections explain in more detail of how to use *python-weka-wrapper* from Python.

A lot more examples you will find in the (aptly named) `examples` module.


Java Virtual Machine
--------------------

In order to use the library, you need to manage the Java Virtual Machine (JVM).

For starting up the library, use the following code:

.. code-block:: python

   >>> import weka.core.jvm as jvm
   >>> jvm.start()

If you want to use the classpath environment variable and all currently installed Weka packages,
use the following call:

.. code-block:: python

   >>> jvm.start(system_cp=True, packages=True)

Most of the times, you will want to increase the maximum heap size available to the JVM.
The following example reserves 512 MB:

.. code-block:: python

   >>> jvm.start(max_heap_size="512m")

And, finally, in order to stop the JVM again, use the following call:

.. code-block:: python

   >>> jvm.stop()


Data generators
---------------

Artifical data can be generated using one of Weka's data generators, e.g., the
`Agrawal` classification generator:

.. code-block:: python

   >>> from weka.datagenerators import DataGenerator
   >>> generator = DataGenerator("weka.datagenerators.classifiers.classification.Agrawal")
   >>> generator.set_options(["-B", "-P", "0.05"])
   >>> DataGenerator.make_data(generator, ["-o", "/some/where/outputfile.arff"])

Or using the low-level API (outputting data to stdout):

.. code-block:: python

   >>> generator = DataGenerator("weka.datagenerators.classifiers.classification.Agrawal")
   >>> generator.set_options(["-n", "10", "-r", "agrawal"])
   >>> generator.set_dataset_format(generator.define_data_format())
   >>> print(generator.get_dataset_format())
   >>> if generator.get_single_mode_flag():
   >>>     for i in xrange(generator.get_num_examples_act()):
   >>>         print(generator.generate_example())
   >>> else:
   >>>     print(generator.generate_examples())


Loaders and Savers
------------------

You can load and save datasets of various data formats using the `Loader` and `Saver` classes.

The following example loads an ARFF file and saves it as CSV:

.. code-block:: python

   >>> from weka.core.converters import Loader, Saver
   >>> loader = Loader("weka.core.converters.ArffLoader")
   >>> data = loader.load_file("/some/where/iris.arff")
   >>> print(data)
   >>> saver = Saver("weka.core.converters.CSVSaver")
   >>> saver.save_file(data, "/some/where/iris.csv")


Filters
-------

The `Filter` class from the `weka.filters` module allows you to filter datasets, e.g.,
removing the last attribute using the `Remove` filter:

.. code-block:: python

   >>> from weka.filters import Filter
   >>> data = ...                       # previously loaded data
   >>> remove = Filter(classname="weka.filters.unsupervised.attribute.Remove")
   >>> remove.set_options(["-R", "last"])
   >>> remove.set_inputformat(data)     # let the filter know about the type of data to filter
   >>> filtered = remove.filter(data)   # filter the data
   >>> print(filtered)                  # output the filtered data

Classifiers
-----------

Here is an example on how to cross-validate a `J48` classifier (with confidence factor 0.3)
on a dataset and output the summary and some specific statistics:

.. code-block:: python

   >>> from weka.classifiers import Classifier, Evaluation
   >>> from weka.core.classes import Random
   >>> data = ...                                        # previously loaded data
   >>> data.set_class_index(data.num_attributes() - 1)   # set class attribute
   >>> classifier = Classifier("weka.classifiers.trees.J48")
   >>> classifier.set_options(["-C", "0.3"])
   >>> evaluation = Evaluation(data)                     # initialize with priors
   >>> evaluation.crossvalidate_model(classifier, iris_data, 10, Random(42))  # 10-fold CV
   >>> print(evaluation.to_summary())
   >>> print("pctCorrect: " + str(evaluation.percent_correct()))
   >>> print("incorrect: " + str(evaluation.incorrect()))


Clusterers
----------

In the following an example on how to build a `SimpleKMeans` (with 3 clusters)
using a previously loaded dataset without a class attribute:

.. code-block:: python

   >>> from weka.clusterers import Clusterer
   >>> data = ... # previously loaded dataset
   >>> clusterer = Clusterer(classname="weka.clusterers.SimpleKMeans")
   >>> clusterer.set_options(["-N", "3"])
   >>> clusterer.build_clusterer(data)
   >>> print(clusterer)


Attribute selection
-------------------

You can perform attribute selection using `BestFirst` as search algorithm and
`CfsSubsetEval` as evaluator as follows:

.. code-block:: python

   >>> from weka.attribute_selection import ASSearch, ASEvaluation, AttributeSelection
   >>> data = ...   # previously loaded dataset
   >>> search = ASSearch("weka.attributeSelection.BestFirst")
   >>> search.set_options(["-D", "1", "-N", "5"])
   >>> evaluator = ASEvaluation("weka.attributeSelection.CfsSubsetEval")
   >>> evaluator.set_options(["-P", "1", "-E", "1"])
   >>> attsel = AttributeSelection()
   >>> attsel.set_search(search)
   >>> attsel.set_evaluator(evaluator)
   >>> attsel.select_attributes(data)
   >>> print("# attributes: " + str(attsel.get_number_attributes_selected()))
   >>> print("attributes: " + str(attsel.get_selected_attributes()))
   >>> print("result string:\n" + attsel.to_results_string())


Associators
-----------

Associators, like `Apriori`, can be built and output like this:

.. code-block:: python

   >>> from weka.associations import Associator
   >>> data = ...   # previously loaded dataset
   >>> associator = Associator("weka.associations.Apriori")
   >>> associator.set_options(["-N", "9", "-I"])
   >>> associator.build_associations(data)
   >>> print(associator)


Serialization
-------------

You can easily serialize and de-serialize as well.

Here we just save a trained classifier to a file, load it again from disk and output the model:

.. code-block:: python

   >>> import weka.core.serialization as serialization
   >>> from weka.classifiers import Classifier
   >>> classifier = ...  # previously built classifier
   >>> serialization.write("/some/where/out.model", classifier)
   >>> ...
   >>> classifier2 = Classifier(jobject=serialization.read("/some/where/out.model"))
   >>> print(classifier2)

Weka usually saves the header of the dataset that was used for training as well (e.g., in order to determine
whether test data is commpatible). This is done as follows:

.. code-block:: python

   >>> import weka.core.serialization as serialization
   >>> from weka.classifiers import Classifier
   >>> from weka.core.dataset import Instances
   >>> classifier = ...  # previously built Classifier
   >>> data = ... # previously loaded/generated Instances
   >>> serialization.write_all("/some/where/out.model", [classifier, Instances.template_instances(data)])
   >>> ...
   >>> objects = serialization.read_all("/some/where/out.model")
   >>> classifier2 = Classifier(jobject=objects[0])
   >>> data2 = Instances(jobject=objects[1])
   >>> print(classifier2)
   >>> print(data2)


Experiments
-----------

Experiments, like they are run in Weka's Experimenter, can be configured and executed as well.

Here is an example for performing a cross-validated classification experiment:

.. code-block:: python

   >>> from weka.experiments import SimpleCrossValidationExperiment, SimpleRandomSplitExperiment, Tester, ResultMatrix
   >>> from weka.classifiers import Classifier
   >>> import weka.core.converters as converters
   >>> # configure experiment
   >>> datasets = ["iris.arff", "anneal.arff"]
   >>> classifiers = [Classifier("weka.classifiers.rules.ZeroR"), Classifier("weka.classifiers.trees.J48")]
   >>> outfile = "results-cv.arff"   # store results for later analysis
   >>> exp = SimpleCrossValidationExperiment(
   >>>     classification=True,
   >>>     runs=10,
   >>>     folds=10,
   >>>     datasets=datasets,
   >>>     classifiers=classifiers,
   >>>     result=outfile)
   >>> exp.setup()
   >>> exp.run()
   >>> # evaluate previous run
   >>> loader = converters.loader_for_file(outfile)
   >>> data   = loader.load_file(outfile)
   >>> matrix = ResultMatrix("weka.experiment.ResultMatrixPlainText")
   >>> tester = Tester("weka.experiment.PairedCorrectedTTester")
   >>> tester.set_resultmatrix(matrix)
   >>> comparison_col = data.get_attribute_by_name("Percent_correct").get_index()
   >>> tester.set_instances(data)
   >>> print(tester.header(comparison_col))
   >>> print(tester.multi_resultset_full(0, comparison_col))

And a setup for performing regression experiments on random splits on the datasets:

.. code-block:: python

   >>> from weka.experiments import SimpleCrossValidationExperiment, SimpleRandomSplitExperiment, Tester, ResultMatrix
   >>> from weka.classifiers import Classifier
   >>> import weka.core.converters as converters
   >>> # configure experiment
   >>> datasets = ["bolts.arff", "bodyfat.arff"]
   >>> classifiers = [Classifier("weka.classifiers.rules.ZeroR"), Classifier("weka.classifiers.functions.LinearRegression")]
   >>> outfile = "results-rs.arff"   # store results for later analysis
   >>> exp = SimpleRandomSplitExperiment(
   >>>     classification=False,
   >>>     runs=10,
   >>>     percentage=66.6,
   >>>     preserve_order=False,
   >>>     datasets=datasets,
   >>>     classifiers=classifiers,
   >>>     result=outfile)
   >>> exp.setup()
   >>> exp.run()
   >>> # evaluate previous run
   >>> loader = converters.loader_for_file(outfile)
   >>> data   = loader.load_file(outfile)
   >>> matrix = ResultMatrix("weka.experiment.ResultMatrixPlainText")
   >>> tester = Tester("weka.experiment.PairedCorrectedTTester")
   >>> tester.set_resultmatrix(matrix)
   >>> comparison_col = data.get_attribute_by_name("Correlation_coefficient").get_index()
   >>> tester.set_instances(data)
   >>> print(tester.header(comparison_col))
   >>> print(tester.multi_resultset_full(0, comparison_col))


virtualenv
==========

If you want to merely test out the library, you can do that easily in a *virtual python environment*
created with `virtualenv`.


Setup
-----

The following steps set up an evironment:

* create a directory and initialize the environment

  .. code-block:: bash

     $ mkdir pwwtest
     $ virtualenv pwwtest

* install the required packages

  .. code-block:: bash

     $ pwwtest/bin/pip install numpy
     $ pwwtest/bin/pip install PIL
     $ pwwtest/bin/pip install matplotlib
     $ pwwtest/bin/pip install pygraphviz
     $ pwwtest/bin/pip install javabridge


Troubleshooting
---------------

* You may need to install the header files for the following libraries for the compilations to succeed:

  * freetype
  * graphviz
  * png

* Before you can install `matplotlib`, you may have to upgrade your `distribute` library as follows:

  .. code-block:: bash

     $  bin/easy_install -U distribute

* On Ubuntu, follow `this post <http://www.sandersnewmedia.com/why/2012/04/16/installing-pil-virtualenv-ubuntu-1204-precise-pangolin/>`_
  to install all the required dependencies for PIL:

  .. code-block:: bash

     $ sudo apt-get build-dep python-imaging

* To enable support for PIL on Ubuntu, see
  `this post <http://www.sandersnewmedia.com/why/2012/04/16/installing-pil-virtualenv-ubuntu-1204-precise-pangolin/>`_:

  .. code-block:: bash

     $ sudo ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/
     $ sudo ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/
     $ sudo ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/


Source code
===========

The following sections explain how to obtain the source code of *python-weka-wrapper*,
generate the documentation and create an installer.


Download
--------

You can clone the *python-weka-wrapper* repository on
`github <https://github.com/fracpete/python-weka-wrapper>`_ as follows:

.. code-block:: bash

   $ git clone https://github.com/fracpete/python-weka-wrapper.git


Documentation
-------------

Change into the directory that you created when cloning the repository and use
`sphinx-doc` to generate the documentation, e.g., `html`:

.. code-block:: bash

   $ cd python-weka-wrapper/doc
   $ make html

Use the `make` command without any parameters to check what output formats are support.


Install
-------

You can install the library as follows in the previously installed virtual environment as follows:

.. code-block:: bash

   $ /some/where/pwwtest/bin/python setup.py install
