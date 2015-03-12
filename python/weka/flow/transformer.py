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

# transformer.py
# Copyright (C) 2015 Fracpete (pythonwekawrapper at gmail dot com)


import os
from weka.flow.base import Actor, InputConsumer, OutputProducer, Token
import weka.core.converters as converters


class Transformer(InputConsumer, OutputProducer):
    """
    The ancestor for all sources.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the transformer.
        :param name: the name of the transformer
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(InputConsumer, self).__init__(name=name, options=options)
        super(OutputProducer, self).__init__(name=name, options=options)


class PassThrough(Transformer):
    """
    Dummy actor that just passes through the data.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the transformer.
        :param name: the name of the transformer
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(PassThrough, self).__init__(name=name, options=options)

    def description(self):
        """
        Returns a description of the actor.
        :return: the description
        :rtype: str
        """
        return "Dummy actor that just passes through the data."

    def do_execute(self):
        """
        The actual execution of the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        self._output.append(self.input)


class LoadDataset(Transformer):
    """
    Loads a dataset from a file.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the transformer.
        :param name: the name of the transformer
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(LoadDataset, self).__init__(name=name, options=options)
        self._loader = None
        self._iterator = None

    def description(self):
        """
        Returns a description of the actor.
        :return: the description
        :rtype: str
        """
        return "Loads a dataset from a file. Either all at once or incrementally."

    def fix_options(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.
        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        if "incremental" not in options:
            options["incremental"] = False
        if "incremental" not in self.help:
            self.help["incremental"] = "Whether to load the dataset incrementally (bool)."

        if "use_custom_loader" not in options:
            options["use_custom_loader"] = False
        if "use_custom_loader" not in self.help:
            self.help["use_custom_loader"] = "Whether to use a custom loader."

        if "custom_loader" not in options:
            options["custom_loader"] = converters.Loader(classname="weka.core.converters.ArffLoader")
        if "custom_loader" not in self.help:
            self.help["custom_loader"] = "The custom loader to use."

        return super(LoadDataset, self).fix_options(options)

    def do_execute(self):
        """
        The actual execution of the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        self._output = []
        fname = str(self.input.payload)
        if not os.path.exists(fname):
            return "File '" + fname + "' does not exist!"
        if not os.path.isfile(fname):
            return "Location '" + fname + "' is not a file!"
        if self.options["use_custom_loader"]:
            self._loader = self.options["custom_loader"]
        else:
            self._loader = converters.loader_for_file(fname)
        dataset = self._loader.load_file(fname, incremental=self.options["incremental"])
        if not self.options["incremental"]:
            self._output.append(Token(dataset))
        else:
            self._iterator = self._loader.__iter__()

    def has_output(self):
        """
        Checks whether any output tokens are present.
        :return: true if at least one output token present
        :rtype: bool
        """
        return super(LoadDataset, self).has_output() or (self._iterator is not None)

    def output(self):
        """
        Returns the next available output token.
        :return: the next token, None if none available
        :rtype: Token
        """
        if self._iterator is not None:
            try:
                inst = self._iterator.next()
                result = Token(inst)
            except Exception, e:
                self._iterator = None
                result = None
        else:
            result = super(LoadDataset, self).output()
        return result

    def stop_execution(self):
        """
        Triggers the stopping of the object.
        """
        super(LoadDataset, self).stop_execution()
        self._loader = None
        self._iterator = None

    def wrapup(self):
        """
        Finishes up after execution finishes, does not remove any graphical output.
        """
        self._loader = None
        self._iterator = None
        super(LoadDataset, self).wrapup()
