Pypi
====

Preparation:
* increment version in `setup.py`
* increment versions in `doc/source/conf.py`

Commands for releasing on pypi.org:

<pre>
  python setup.py clean
  python setup.py sdist upload
  python setup.py build_sphinx
  python setup.py upload_sphinx
</pre>

Requirements:
* Sphinx-PyPI-upload: `easy_install sphinx-pypi-upload`


Github
======

Steps:
* start new release (version: `vX.Y.Z`)
* enter release notes, i.e., significant changes since last release
* upload `python-weka-wrapper-X.Y.Z.tar.gz` previously generated with `setyp.py`
* publish


MLOSS
=====

Steps:
* login
* goto project page https://mloss.org/software/view/548/
* click on `Update project`
* update `Version` and `Download URL`
* re-use release notes from Github release in `Changes since last revision`
* save
