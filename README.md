python-weka-wrapper
===================

Python wrapper for Weka (http://www.cs.waikato.ac.nz/~ml/weka/) 
using javabridge (https://pypi.python.org/pypi/javabridge).

Requirements:

* javabridge (>= 1.0.0)


Examples
--------

See **python/examples** for some example code.


Classifiers
-----------

Example on how to cross-validate a J48 classifier (with confidence factor 0.3)
on the iris UCI dataset:

<pre>
weka.classifiers \
    -t /my/datasets/iris.arff \
    -c last \
    weka.classifiers.trees.J48
    -C 0.3
</pre>

Clusterers
----------

Example on how to perform classes-to-clusters evaluation for SimpleKMeans (with 3 clusters)
using the iris UCI dataset:

<pre>
weka.clusterers \
    -t /my/datasets/iris.arff \
    -c last \
    weka.clusterers.SimpleKMeans
    -N 3
</pre>

Filters
-------

Filtering a single ARFF dataset, removing the last attribute using the Remove filter:

<pre>
weka.filters \
    -i /my/datasets/iris.arff \
    -o /tmp/out.arff \
    -c last \
    weka.filters.unsupervised.attribute.Remove \
    -R last
</pre>

Data generators
---------------

Artifical data can be generated using one of Weka' data generators, e.g., the Agrawal classification generator:

<pre>
weka.datagenerators \
    -o /tmp/out.arff \
    weka.datagenerators.classifiers.classification.Agrawal
</pre>
