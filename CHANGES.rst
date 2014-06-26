Changelog
=========

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
