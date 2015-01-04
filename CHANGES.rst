Changelog
=========

0.2.1 (2015-01-05)
------------------

- added unit testing framework
- added method `refresh_cache()` to `weka/core/packages.py` to allow user to refresh local cache
- method `get_classname` in `weka.core.utils` now handles Python objects and class objects as well
- added convenience method `get_jclass` to `weka.core.utils` to instantiate a Java class
- added a `JavaArray` wrapper for  `arrays, which allows getting/setting elements and iterating
- added property `classname` to class `JavaObject` for easy access to classname of underlying object
- added class method `parse_matlab` for parsing Matlab matrix strings to `CostMatrix` class
- `predictions` method of `Evaluation` class now return `None` if predictions are discarded
- `Associator.get_capabilities()` method is now a property: `Associator.capabilities`
- added wrapper classes for Java enums: `weka.core.classes.Enum`
- fixed retrieval of `sumSq` in `Stats` class (used by `AttributeStats`)
- fixed `cluster_instance` method in `Clusterer` class
- fixed `filter` and `clusterer` properties in clusterer classes (`SingleClustererEnhancer`, `FilteredClusterer`)
- added `crossvalidate_model` method to `ClusterEvaluation`
- added `get_prc` method to `plot/classifiers.py` for calculating the area under the precision-recall curve
- `Filter.filter` method now handles list of `Instances` objects as well, applying the filter sequentially
  to all the datasets (allows generation of compatible train/test sets)


0.2.0 (2014-12-22)
------------------

NB: This release is not backwards compatible!

- requires `JavaBridge` 1.0.9 at least
- moved from Java-like get/set (`getIndex()` and `setIndex(int)`) to nicer Python properties
- using Python properties (also only read-only ones) wherevere possible
- added `weka.core.version` for accessing the Weka version currently in use
- added `jwrapper` and `jclasswrapper` methods to `JavaObject` class (the mother of all objects in python-weka-wrapper)
  to allow generic access to an object's methods: http://pythonhosted.org//javabridge/highlevel.html#wrapping-java-objects-using-reflection
- added convenience methods `class_is_last()` and `class_is_first()` to `weka.core.Instances` class
- added convenience methods `delete_last_attribute()` and `delete_first_attribute()` to `weka.core.Instances` class


0.1.17 (2014-12-18)
-------------------

- fixed `setup.py` to download Weka 3.7.12 instead of 3.7.11 (this time correct URL)


0.1.16 (2014-12-18)
-------------------

- fixed `setup.py` to download Weka 3.7.12 instead of 3.7.11


0.1.15 (2014-12-18)
-------------------

- fixed `Instance.set_value` method: https://github.com/fracpete/python-weka-wrapper/issues/24
- added sub-section `From source` to section on installing the library
- upgraded to Weka 3.7.12


0.1.14 (2014-12-16)
-------------------

- fixed `setup.py` to include the jars again when using eggs (via `include_package_data` etc)
- added detailed instructions for installing the library


0.1.13 (2014-11-01)
-------------------

- added `get_class` method to `weka.core.utils` which returns the Python class object associated
  with the classname in dot-notation
- `from_commandline` method in `weka.core.utils` now takes an optional `classname` argument, which is
  the classname (in dot-notation) of the wrapper class to return - instead of the generic `OptionHandler`
- added `Kernel` and `KernelClassifier` convenience classes to better handle kernel based classifiers


0.1.12 (2014-10-17)
-------------------

- added `create_string` class method to the `Attribute` class for creating a string attribute
- ROC/PRC curves can now consist of multiple plots (ie multiple class labels)
- switched command-line option handling from `getopt` to `argparse`
- fixed Instance.get_dataset(self) method
- added iterators for: rows/attributes in dataset, values in dataset row
- incremental loaders can be iterated now


0.1.11 (2014-09-22)
-------------------

- moved `wekaexamples` module to separate github project: https://github.com/fracpete/python-weka-wrapper-examples
- added `stratify`, `train_cv` and `test_cv` methods to the `Instances` class
- fixed `to_summary` method of the Evaluation class: failed when providing a custom title


0.1.10 (2014-08-29)
-------------------

- fixed adding custom classpath using `jvm.start(class_path=[...])`


0.1.9 (2014-08-18)
------------------

- added static methods to Instances class: `summary`, `merge_instances`, `append_instances`
- added methods to Instances class: `delete_with_missing`, `equal_headers`


0.1.8 (2014-06-26)
------------------

- fixed installer: `MANIFEST.in` now includes `CHANGES.rst` and `DESCRIPTION.rst` as well


0.1.7 (2014-06-26)
------------------

- fixed `weka/plot/dataset.py` imports to avoid error when testing for matplotlib availability

- `Instance.create_instance` (`weka/core/dataset.py`) now accepts Python list and Numpy array


0.1.6 (2014-05-29)
------------------

- added troubleshooting section for Mac OSX to documentation

- recompiled helper jars with 1.6 rather than 1.7 to make it work on Mac OSX

- added link to Google Group


0.1.5 (2014-05-23)
------------------

- added CostMatrix support in the classifier evaluation

- fixed various retrievals of double arrays (accessed them incorrectly
  as float arrays), like `distributionForInstance` for a classifier

- Instances object can now retrieve all (internal) values of an
  attribute/column as numpy array

- added plotting of cluster assignments to `weka.plot.clusterers`

- fixed `weka.core.utils.from_commandline` method

- fixed `weka.classifiers.PredictionOutput` (get/set_header methods)

- predictions can be turned into an `Instances` object now using
  `weka.classifiers.predictions_to_instances`


0.1.4 (2014-05-19)
------------------

- dependencies for plotting are now optional (pygraphviz, PIL, matplotlib)

- plots now support custom titles


0.1.3 (2014-05-17)
------------------

- improved documentation

- added PRC curve plot

- aligned to PEP8 style guidelines

- fixed variety of little bugs (not so commonly used methods)

- fixed lib directory reference in make files for Java helper classes


0.1.2 (2014-05-13)
------------------

- added matrix plot

- added scatter plot for two attributes

- fixes in constructors of classes

- added `MultiFilter` convenience class

- predictions (of classifiers) can now be collected and output using
  the `PredictionOutput` class

- added support for attribute statistics


0.1.1 (2014-05-02)
------------------

- constructors now take list of commandline options as well

- added Weka package support (list/install/uninstall)

- ROC plotting for classifiers

- improved code documentation

- added more examples

- added more datasets

- using javabridge 1.0.1 now


0.1.0 (2014-04-27)
------------------

- Initial release of Python wrapper for Weka, no GUI.
