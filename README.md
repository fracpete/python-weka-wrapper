# python-weka-wrapper

Python wrapper for Weka (http://www.cs.waikato.ac.nz/~ml/weka/) 
using javabridge (https://pypi.python.org/pypi/javabridge).

Requirements:

* Python
 * javabridge (>= 1.0.1)
 * matplotlib (>= 1.7.0)
 * pygraphviz (>= 1.2)
 * PIL (>= 1.1.0)
 * numpy
* JDK 1.6+

Included:
* Weka (3.7.11)

The Python libraries you can either install using `pip install <name>` or use pre-built packages available for
your platform.

For Ubuntu this could look as follows:
<pre>
$ sudo apt-get install python-numpy python-imaging python-matplotlib python-pygraphviz
$ sudo pip install javabridge
</pre>

A build environment is required to build libraries, like `javabridge`, from source. For Ubuntu that would
be the `build-essential` meta-package and Xcode for Mac OSX.

## Code examples
See **python/wekaexamples** for example code on the various APIs.
Also, check out the sphinx documentation in **doc**.

## Command-line examples

### Data generators

Artifical data can be generated using one of Weka's data generators, e.g., the `Agrawal` classification generator:

<pre>
python weka/datagenerators.py \
    -o /tmp/out.arff \
    weka.datagenerators.classifiers.classification.Agrawal
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
    -t /my/datasets/iris.arff \
    weka.associations.Apriori -N 9 -I
</pre>
