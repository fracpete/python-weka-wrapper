# python-weka-wrapper

Python wrapper for the Java machine learning workbench [Weka](http://www.cs.waikato.ac.nz/~ml/weka/)
using the [javabridge](https://pypi.python.org/pypi/javabridge) library.

Requirements:

* Python 2.7 (does not work with Python 3)
 * javabridge (>= 1.0.11)
 * matplotlib (optional)
 * pygraphviz (optional)
 * PIL (optional)
* Oracle JDK 1.6+

Uses:
* Weka (3.7.12)

## Installation

Detailed instructions and links to videos on installing the library are located
[here](http://pythonhosted.org/python-weka-wrapper/install.html).

Please note, that you need a build environment to compile some libraries from source.

## Forum

You can post questions, patches or enhancement requests in the following Google Group:

https://groups.google.com/forum/#!forum/python-weka-wrapper

## Code examples
See [python-weka-wrapper-examples](https://github.com/fracpete/python-weka-wrapper-examples)
repository for example code on the various APIs. Also, check out the sphinx
documentation in the **doc** directory. You can generate HTML documentation
using the `make html` command in the **doc** directory.

Available online documentation:
* [Full documentation](http://pythonhosted.org/python-weka-wrapper/)
* Shortcuts
 * [Command-line](http://pythonhosted.org/python-weka-wrapper/commandline.html)
 * [API](http://pythonhosted.org/python-weka-wrapper/api.html)
 * [Examples](http://pythonhosted.org/python-weka-wrapper/examples.html)

## Command-line examples

Below are some examples of command-line use of the library. You can find these also
on [PyPi](http://pythonhosted.org/python-weka-wrapper/commandline.html).

### Data generators

Artifical data can be generated using one of Weka's data generators, e.g., the `Agrawal` classification generator:

<pre>
python weka/datagenerators.py \
    weka.datagenerators.classifiers.classification.Agrawal \
    -o /tmp/out.arff
</pre>

### Filters

Filtering a single ARFF dataset, removing the last attribute using the `Remove` filter:

<pre>
python weka/filters.py \
    -i /my/datasets/iris.arff \
    -o /tmp/out.arff \
    -c last \
    weka.filters.unsupervised.attribute.Remove \
    -R last
</pre>

### Classifiers

Example on how to cross-validate a `J48` classifier (with confidence factor 0.3) on the iris UCI dataset:

<pre>
python weka/classifiers.py \
    -t /my/datasets/iris.arff \
    -c last \
    weka.classifiers.trees.J48
    -C 0.3
</pre>

### Clusterers

Example on how to perform classes-to-clusters evaluation for `SimpleKMeans` (with 3 clusters) using the iris UCI dataset:

<pre>
python weka/clusterers.py \
    -t /my/datasets/iris.arff \
    -c last \
    weka.clusterers.SimpleKMeans
    -N 3
</pre>

### Attribute selection

You can perform attribute selection using `BestFirst` as search algorithm and `CfsSubsetEval` as evaluator as follows:

<pre>
python weka/attribute_selection.py \
    -i /my/datasets/iris.arff \
    -x 5 \
    -n 42 \
    -s "weka.attributeSelection.BestFirst -D 1 -N 5"
    weka.attributeSelection.CfsSubsetEval \
    -P 1 \
    -E 1
</pre>

### Associator

Associators, like `Apriori`, can be run like this:

<pre>
python weka/associators.py \
    -t /my/datasets/lung-cancer.arff \
    weka.associations.Apriori -N 9 -I
</pre>
