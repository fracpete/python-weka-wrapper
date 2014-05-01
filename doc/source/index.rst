.. python-weka-wrapper documentation master file, created by
   sphinx-quickstart on Sat Apr 12 11:51:06 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introduction
============

*python-weka-wrapper* allows you to use `Weka <http://www.cs.waikato.ac.nz/~ml/weka/>`_ from within Python.

The library uses the `javabridge <https://pypi.python.org/pypi/javabridge>`_ library for starting up,
communicating with and shutting down the Java Virtual Machine in which the Weka processes get executed.

*python-weka-wrapper* provides a thin wrapper around the basic (non-GUI) functionality of Weka.
You can automatically add all your Weka packages to the classpath. Additional jars can be added as well.

Project homepage: https://github.com/fracpete/python-weka-wrapper

MLOSS project: https://mloss.org/software/view/548/


Requirements
============

The library has the following requirements:

* javabridge
* pygraphviz
* matplotlib
* PIL
* JDK 1.6+


Contents
========

.. toctree::
   :maxdepth: 2

   commandline
   api
   virtualenv
   sourcecode
   examples
