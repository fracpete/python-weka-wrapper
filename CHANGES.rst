Changelog
=========

0.3.1 (2015-04-23)
------------------

- added `get_tags` class method to `Tags` method for easier instantiation of Tag arrays
- added `find` method to `Tags` class to locate `Tag` object that matches the string
- fixed `__getitem__` and `__setitem__` methods of the `Tags` class
- added `GridSearch` meta-classifier with convenience properties to module `weka.classifiers`
- added `SetupGenerator` and various parameter classes to `weka.core.classes`
- added `MultiSearch` meta-classifier with convenience properties to module `weka.classifiers`
- added `quote`/`unquote` and `backquote`/`unbackquote` methods to `weka.core.classes` module
- added `main` method to `weka.core.classes` for operations on options: join, split, code
- added support for option handling to `weka.core.classes` module


0.3.0 (2015-04-15)
------------------

- added method `ndarray_to_instances` to `weka.converters` module for converting Numpy 2-dimensional array into `Instances` object
- added method `plot_learning_curve` to `weka.plot.classifiers` module for creating learning curves for multiple classifiers for a specific metric
- added plotting of experiments with `plot_experiment` methid in `weka.plot.experiments` module
- `Instance.create_instance` method now takes list of tuples (index, internal float value) when generating sparse instances
- added `weka.core.database` module for loading data from a database
- added `make_copy` class method to `Clusterer` class
- added `make_copy` class method to `Associator` class
- added `make_copy` class method to `Filter` class
- added `make_copy` class method to `DataGenerator` class
- most classes (like Classifier and Filter) now have a default classname value in the constructor
- added `TextDirectoryLoader` class to `weka.core.converters`
- moved all methods from `weka.core.utils` to `weka.core.classes`
- fixed `Attribute.index_of` method for determining label index
- fixed `Attribute.add_string_value` method (used incorrect JNI parameter)
- `create_instance` and `create_sparse_instance` methods of class `Instance` now ensure that list values are float
- added `to_help` method to `OptionHandler` class which outputs a help string generated from the base class's
  `globalInfo` and `listOptions` methods
- fixed `test_model` method of `Evaluation` class when supplying a `PredictionOutput` object (previously generated `No dataset structure provided!` exception)
- added `batch_finished` method to `Filter` class for incremental filtering
- added `line_plot` method to `weka.plot.dataset` module for plotting dataset using internal format (one line plot per instance)
- added `is_serializable` property to `JavaObject` class
- added `has_class` convenience property to `Instance` class
- added `__repr__` method to `JavaObject` classes (simply calls `toString()` method)
- added `Stemmer` class in module `weka.core.stemmers`
- added `Stopwords` class in module `weka.core.stopwords`
- added `Tokenizer` class in module `weka.core.tokenizers`
- added `StringToWordVector` filter class in module `weka.filters`
- added simple workflow engine (see documentation on *Flow*)


0.2.2 (2015-01-05)
------------------

- added convenience methods `no_class` (to unset class) and `has_class` (class set?) to `Instances` class
- switched to using faster method objects for methods `classify_instance`/`distribution_for_instance` in `Classifier` class
- switched to using faster method objects for methods `cluster_instance`/`distribution_for_instance` in `Clusterer` class
- switched to using faster method objects for methods `class_index`, `is_missing`, `get/set_value`, `get/set_string_value`, `weight` in `Instance` class
- switched to using faster method objects for methods `input`, `output`, `outputformat` in `Filter` class
- switched to using faster method objects for methods `attribute`, `attribute_by_name`, `num_attributes`, `num_instances`,
  `class_index`, `class_attribute`, `set_instance`, `get_instance`, `add_instance` in `Instances` class


0.2.1 (2015-01-05)
------------------

- added unit testing framework
- added method `refresh_cache()` to `weka/core/packages.py` to allow user to refresh local cache
- method `get_classname` in `weka.core.utils` now handles Python objects and class objects as well
- added convenience method `get_jclass` to `weka.core.utils` to instantiate a Java class
- added a `JavaArray` wrapper for  `arrays`, which allows getting/setting elements and iterating
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
