# python-weka-wrapper

Python wrapper for Weka (http://www.cs.waikato.ac.nz/~ml/weka/) 
using javabridge (https://pypi.python.org/pypi/javabridge).

Requirements:

* javabridge (>= 1.0.0)
* matplotlib (>= 1.7.0)
* pygraphviz (>= 1.2)
* PIL (>= 1.1.0)
* numpy

Included:
* Weka (3.7.10)

## Code examples
See **python/examples** for example code on the various APIs.

## Command-line examples

### Classifiers

Example on how to cross-validate a `J48` classifier (with confidence factor 0.3) on the iris UCI dataset:

<pre>
weka.classifiers \
    -t /my/datasets/iris.arff \
    -c last \
    weka.classifiers.trees.J48
    -C 0.3
</pre>

### Clusterers

Example on how to perform classes-to-clusters evaluation for `SimpleKMeans` (with 3 clusters) using the iris UCI dataset:

<pre>
weka.clusterers \
    -t /my/datasets/iris.arff \
    -c last \
    weka.clusterers.SimpleKMeans
    -N 3
</pre>

### Filters

Filtering a single ARFF dataset, removing the last attribute using the `Remove` filter:

<pre>
weka.filters \
    -i /my/datasets/iris.arff \
    -o /tmp/out.arff \
    -c last \
    weka.filters.unsupervised.attribute.Remove \
    -R last
</pre>

### Data generators

Artifical data can be generated using one of Weka's data generators, e.g., the `Agrawal` classification generator:

<pre>
weka.datagenerators \
    -o /tmp/out.arff \
    weka.datagenerators.classifiers.classification.Agrawal
</pre>

### Associator

Associators, like `Apriori`, can be run like this:

<pre>
weka.associators \
    -t /my/datasets/iris.arff \
    weka.associations.Apriori -N 9 -I
</pre>

### Attribute selection

You can perform attribute selection using `BestFirst` as search algorithm and `CfsSubsetEval` as evaluator as follows:

<pre>
weka.attribute_selection \
    -i /my/datasets/iris.arff \
    -x 5 \
    -n 42 \
    -s "weka.attributeSelection.BestFirst -D 1 -N 5"
    weka.attributeSelection.CfsSubsetEval \
    -P 1 \
    -E 1
</pre>

