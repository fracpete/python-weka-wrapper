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

# source.py
# Copyright (C) 2015 Fracpete (pythonwekawrapper at gmail dot com)


import os
import re
from weka.flow.base import Actor, OutputProducer, Token
from weka.core.database import InstanceQuery


class Source(OutputProducer, Actor):
    """
    The ancestor for all sources.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the source.
        :param name: the name of the source
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(Source, self).__init__(name=name, options=options)
        super(OutputProducer, self).__init__()


class Start(Source):
    """
    Outputs a None token for triggering other actors.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the transformer.
        :param name: the name of the transformer
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(Start, self).__init__(name=name, options=options)

    def description(self):
        """
        Returns a description of the actor.
        :return: the description
        :rtype: str
        """
        return "Outputs a None token for triggering other actors."

    def do_execute(self):
        """
        The actual execution of the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        self._output.append(Token(None))
        return None


class FileSupplier(Source):
    """
    Outputs a fixed list of files.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the transformer.
        :param name: the name of the transformer
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(FileSupplier, self).__init__(name=name, options=options)

    def description(self):
        """
        Returns a description of the actor.
        :return: the description
        :rtype: str
        """
        return "Outputs a fixed list of files."

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.
        :return: the info, None if not available
        :rtype: str
        """
        return "files: " + str(len(self.options["files"]))

    def fix_options(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.
        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(FileSupplier, self).fix_options(options)

        opt = "files"
        if opt not in options:
            options[opt] = []
        if opt not in self.help:
            self.help[opt] = "The files to output (list of string)."

        return options

    def do_execute(self):
        """
        The actual execution of the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        for f in self.resolve_option("files"):
            self._output.append(Token(f))
        return None


class ListFiles(Source):
    """
    Source that list files in a directory.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the transformer.
        :param name: the name of the transformer
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(ListFiles, self).__init__(name=name, options=options)

    def description(self):
        """
        Returns a description of the actor.
        :return: the description
        :rtype: str
        """
        return "Source that list files in a directory."

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.
        :return: the info, None if not available
        :rtype: str
        """
        return "dir: " + str(self.options["dir"]) \
               + ", files: " + str(self.options["list_files"]) \
               + ", dirs: " + str(self.resolve_option("list_dirs")) \
               + ", recursive: " + str(self.options["recursive"])

    def fix_options(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.
        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(ListFiles, self).fix_options(options)

        opt = "dir"
        if opt not in options:
            options[opt] = "."
        if opt not in self.help:
            self.help[opt] = "The directory to search (string)."

        opt = "recursive"
        if opt not in options:
            options[opt] = False
        if opt not in self.help:
            self.help[opt] = "Whether to search recursively (bool)."

        opt = "list_files"
        if opt not in options:
            options[opt] = True
        if opt not in self.help:
            self.help[opt] = "Whether to include files (bool)."

        opt = "list_dirs"
        if opt not in options:
            options[opt] = False
        if opt not in self.help:
            self.help[opt] = "Whether to include directories (bool)."

        opt = "regexp"
        if opt not in options:
            options[opt] = ".*"
        if opt not in self.help:
            self.help[opt] = "The regular expression that files/dirs must match (string)."

        return options

    def _list(self, path, collected):
        """
        Lists all the files/dirs in directory that match the pattern.
        :param path: the directory to search
        :type path: str
        :param collected: the files/dirs collected so far (full path)
        :type collected: list
        :return: None if successful, error otherwise
        :rtype: str
        """
        list_files = self.resolve_option("list_files")
        list_dirs = self.resolve_option("list_dirs")
        recursive = self.resolve_option("recursive")
        spattern = str(self.resolve_option("regexp"))
        pattern = None
        if (spattern is not None) and (spattern != ".*"):
            pattern = re.compile(spattern)

        try:
            items = os.listdir(path)
            for item in items:
                fp = path + os.sep + item
                if list_files and os.path.isfile(fp):
                    if (pattern is None) or pattern.match(item):
                        collected.append(fp)
                if list_dirs and os.path.isdir(fp):
                    if (pattern is None) or pattern.match(item):
                        collected.append(fp)
                if recursive and os.path.isdir(fp):
                    self._list(fp, collected)
        except Exception, e:
            return "Error listing '" + path + "': " + str(e)

    def do_execute(self):
        """
        The actual execution of the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        directory = str(self.resolve_option("dir"))
        if not os.path.exists(directory):
            return "Directory '" + directory + "' does not exist!"
        if not os.path.isdir(directory):
            return "Location '" + directory + "' is not a directory!"
        collected = []
        result = self._list(directory, collected)
        if result is None:
            for c in collected:
                self._output.append(Token(c))
        return result


class GetStorageValue(Source):
    """
    Outputs the specified value from storage.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the transformer.
        :param name: the name of the transformer
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(GetStorageValue, self).__init__(name=name, options=options)

    def description(self):
        """
        Returns a description of the actor.
        :return: the description
        :rtype: str
        """
        return "Outputs the specified value from storage."

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.
        :return: the info, None if not available
        :rtype: str
        """
        return "name: " + str(self.options["storage_name"])

    def fix_options(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.
        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(GetStorageValue, self).fix_options(options)

        opt = "storage_name"
        if opt not in options:
            options[opt] = "unknown"
        if opt not in self.help:
            self.help[opt] = "The name of the storage value to retrieve (string)."

        return options

    def do_execute(self):
        """
        The actual execution of the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        if self.storagehandler is None:
            return "No storage handler available!"
        sname = str(self.resolve_option("storage_name"))
        if sname not in self.storagehandler.storage:
            return "No storage item called '" + sname + "' present!"
        self._output.append(self.storagehandler.storage[sname])
        return None


class ForLoop(Source):
    """
    Outputs integers using the specified min, max and step.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the transformer.
        :param name: the name of the transformer
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(ForLoop, self).__init__(name=name, options=options)

    def description(self):
        """
        Returns a description of the actor.
        :return: the description
        :rtype: str
        """
        return "Outputs integers using the specified min, max and step."

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.
        :return: the info, None if not available
        :rtype: str
        """
        return "min: " + str(self.options["min"]) \
               + ", max: " + str(self.options["max"]) \
               + ", step: " + str(self.options["step"])

    def fix_options(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.
        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(ForLoop, self).fix_options(options)

        opt = "min"
        if opt not in options:
            options[opt] = 1
        if opt not in self.help:
            self.help[opt] = "The minimum for the loop (included, int)."

        opt = "max"
        if opt not in options:
            options[opt] = 10
        if opt not in self.help:
            self.help[opt] = "The maximum for the loop (included, int)."

        opt = "step"
        if opt not in options:
            options[opt] = 1
        if opt not in self.help:
            self.help[opt] = "The step size (int)."

        return options

    def do_execute(self):
        """
        The actual execution of the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        for i in xrange(
                int(self.resolve_option("min")),
                int(self.resolve_option("max")) + 1,
                int(self.resolve_option("step"))):
            self._output.append(Token(i))
        return None


class LoadDatabase(Source):
    """
    Loads a dataset from the database.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the source.
        :param name: the name of the source
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(LoadDatabase, self).__init__(name=name, options=options)
        self._loader = None
        self._iterator = None

    def description(self):
        """
        Returns a description of the actor.
        :return: the description
        :rtype: str
        """
        return "Loads a dataset from a database using a supplied SQL query."

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.
        :return: the info, None if not available
        :rtype: str
        """
        return "url: " + str(self.options["db_url"]) \
               + ", query: " + str(self.options["query"])

    def fix_options(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.
        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        opt = "db_url"
        if opt not in options:
            options[opt] = "jdbc:mysql://somehost:3306/somedatabase"
        if opt not in self.help:
            self.help[opt] = "The JDBC database URL to connect to (str)."

        opt = "user"
        if opt not in options:
            options[opt] = "user"
        if opt not in self.help:
            self.help[opt] = "The database user to use for connecting (str)."

        opt = "password"
        if opt not in options:
            options[opt] = "secret"
        if opt not in self.help:
            self.help[opt] = "The password for the database user (str)."

        opt = "query"
        if opt not in options:
            options[opt] = "SELECT * FROM table"
        if opt not in self.help:
            self.help[opt] = "The SQL query for generating the dataset (str)."

        opt = "sparse"
        if opt not in options:
            options[opt] = False
        if opt not in self.help:
            self.help[opt] = "Whether to return the data in sparse format (bool)."

        opt = "custom_props"
        if opt not in options:
            options[opt] = ""
        if opt not in self.help:
            self.help[opt] = "Custom properties filename (str)."

        return super(LoadDatabase, self).fix_options(options)

    def do_execute(self):
        """
        The actual execution of the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        iquery = InstanceQuery()
        iquery.db_url = str(self.resolve_option("db_url"))
        iquery.user = str(self.resolve_option("user"))
        iquery.password = str(self.resolve_option("password"))
        props = str(self.resolve_option("custom_props"))
        if (len(props) > 0) and os.path.isfile(props):
            iquery.custom_properties = props
        iquery.query = str(self.resolve_option("query"))
        data = iquery.retrieve_instances()
        self._output.append(Token(data))
        return None
