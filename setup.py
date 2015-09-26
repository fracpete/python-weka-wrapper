# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# setup.py
# Copyright (C) 2014-2015 Fracpete (pythonwekawrapper at gmail dot com)

import os
from setuptools import setup
from urllib2 import urlopen, URLError, HTTPError


def download_file(url, outfile):
    """
    Downloads the file associated with the URL and saves it to the specified output file.
    Taken from here: http://stackoverflow.com/a/4028894
    :param url: the URL to download
    :type url: str
    :param outfile: the name of the output file
    :type outfile: str
    :returns: whether the download was successful
    :rtype: bool
    """
    try:
        # Open the url
        f = urlopen(url)
        print("Downloading '" + url + "' to '" + outfile + "'")
        # Open our local file for writing
        with open(outfile, "wb") as local_file:
            local_file.write(f.read())
    # handle errors
    except HTTPError, e:
        print("HTTP Error: " + str(e.code) + " " + url)
        return False
    except URLError, e:
        print("URL Error: " + str(e.reason) + " " + url)
        return False
    return True


def download_weka():
    """
    Downloads the monolithic Weka jar from sourceforget.net if nececssary.
    """
    url = "https://sourceforge.net/projects/weka/files/weka-3-7/3.7.13/weka-3-7-13-monolithic.jar/download"
    outfile = os.path.join(os.path.dirname(__file__), "python", "weka", "lib", "weka.jar")
    if not os.path.exists(outfile):
        if not download_file(url, outfile):
            print("Failed to download Weka jar '" + url + "' to '" + outfile + "'!")
        else:
            print("Download of Weka jar successful!")


def ext_modules():
    """
    Initiates Weka jar download.
    """
    download_weka()


def _read(f):
    """
    Reads in the content of the file.
    :param f: the file to read
    :type f: str
    :return: the content
    :rtype: str
    """
    return open(f, 'rb').read()


setup(
    name="python-weka-wrapper",
    description="Python wrapper for the Weka Machine Learning Workbench",
    long_description=(
        _read('DESCRIPTION.rst') + b'\n' +
        _read('CHANGES.rst')).decode('utf-8'),
    url="https://github.com/fracpete/python-weka-wrapper",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Programming Language :: Python',
    ],
    license='GNU General Public License version 3.0 (GPLv3)',
    package_dir={
        '': 'python'
    },
    packages=[
        "weka",
        "weka.core",
        "weka.flow",
        "weka.plot"
    ],
    package_data={
        "weka": ["lib/*.jar"],
    },
    include_package_data=True,
    version="0.3.3",
    author='Peter "fracpete" Reutemann',
    author_email='pythonwekawrapper at gmail dot com',
    install_requires=[
        "javabridge>=1.0.11",
        "numpy"
    ],
    extras_require={
        'plots': ["matplotlib"],
        'graphs': ["pygraphviz", "PIL"],
    },
    ext_modules=ext_modules(),
)
