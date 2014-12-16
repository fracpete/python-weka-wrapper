Installation
============

The following sections should help you install the library on your machine.

Some of the instructions are based on the *CellProfiler*
`instructions <https://github.com/CellProfiler/python-javabridge/blob/master/docs/installation.rst>`_, the guys
behind the *javabridge* library.

However, if you should encounter problems or if you would like to submit improvements
on the instructions below, please use the following mailing list:

https://groups.google.com/forum/#!forum/python-weka-wrapper


Debian/Ubuntu
-------------

First, you need to be able to compile C/C++ code:

.. code-block:: bash

   $ sudo apt-get install build-essential

Now, you can install the various packages that `python-weka-wrapper` requires, which are available from the repositories:

.. code-block:: bash

   $ sudo apt-get install python-numpy python-imaging python-matplotlib python-pygraphviz


Finally, you can use `pip` to install the Python packages that are not available in the repositories:

.. code-block:: bash

   $ sudo pip install javabridge
   $ sudo pip install python-weka-wrapper


Other Linux distributions
-------------------------

See `these <http://docs.python-guide.org/en/latest/starting/install/linux/>`_ general instructions
for installing Python on Linux. Also, you need to be able to compile C/C++ code on your machine.

We need to install the following Python packages, preferably through your package manager (e.g., `yum`):

* numpy
* PIL
* matplotlib
* pygraphviz

Once these libraries are installed, we can use `pip` to install the remaining Python packages:

.. code-block:: bash

   $ sudo pip install javabridge
   $ sudo pip install python-weka-wrapper


Mac OSX
-------

Please following `these <http://docs.python-guide.org/en/latest/starting/install/osx/>`_
general instructions for installing Python.

You also need to install *Xcode* in order to compile C/C++ code and an *Oracle JDK 1.7.x*.

You need to install the following Python packages:

* numpy
* PIL
* matplotlib
* pygraphviz

Once these libraries are installed, we can use `pip` to install the remaining Python packages:

.. code-block:: bash

   $ pip install javabridge
   $ pip install python-weka-wrapper


Windows
-------

**Please note:** You need to make sure that the *bitness* of your environment is consistent.
I.e., if you install a 32-bit version of Python, you need to install a 32-bit JDK and 32-bit numpy
(or all of them are 64-bit).

Perform the following steps:

* install an `Oracle JDK (1.7.x) <http://www.oracle.com/technetwork/java/javase/downloads/>`_
* install `Python <www.python.org/downloads>`_, make sure you check `Add python.exe to path` during the installation
* add the Python scripts directory to your `PATH` environment variable, e.g., `C:\\Python27\\Scripts`
* install `numpy 1.8.x <http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy>`_
* install `.Net 4.0 <http://go.microsoft.com/fwlink/?LinkID=187668>`_
* install `Windows SDK 7.1 <http://www.microsoft.com/download/details.aspx?id=8279>`_
* install `pip` with these steps:
 * download from `here <https://bootstrap.pypa.io/get-pip.py>`_
 * install using `python get-pip.py`
* open Windows SDK command prompt (**not** the regular command prompt!) and install `javabridge` and `python-weka-wrapper`

  .. code-block:: bat

     set MSSdk=1
     set DISTUTILS_USE_SDK=1
     pip install javabridge
     pip install python-weka-wrapper

Now you can run `python-weka-wrapper` using the regular command-prompt as well.
