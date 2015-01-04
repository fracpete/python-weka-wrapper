Changelog
=========

0.2.2 (????-??-??)
------------------

- ...


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


Older releases
--------------

https://github.com/fracpete/python-weka-wrapper/blob/7fd0bba3c74277313eb463e338c1a7e117a1ea22/CHANGES.rst
