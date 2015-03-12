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
import weka.core.utils as utils


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
        opt = "incremental"
        if opt not in options:
            options[opt] = False
        if opt not in self.help:
            self.help[opt] = "Whether to load the dataset incrementally (bool)."

        opt = "use_custom_loader"
        if opt not in options:
            options[opt] = False
        if opt not in self.help:
            self.help[opt] = "Whether to use a custom loader."

        opt = "custom_loader"
        if opt not in options:
            options[opt] = converters.Loader(classname="weka.core.converters.ArffLoader")
        if opt not in self.help:
            self.help[opt] = "The custom loader to use."

        return super(LoadDataset, self).fix_options(options)

    def to_options(self, k, v):
        """
        Hook method that allows conversion of individual options.
        :param k: the key of the option
        :type k: str
        :param v: the value
        :type v: object
        :return: the potentially processed value
        :rtype: object
        """
        if k == "custom_loader":
            return utils.to_commandline(v)
        return super(LoadDataset, self).to_options(k, v)

    def from_options(self, k, v):
        """
        Hook method that allows converting values from the dictionary
        :param k: the key in the dictionary
        :type k: str
        :param v: the value
        :type v: object
        :return: the potentially parsed value
        :rtype: object
        """
        if k == "custom_loader":
            return utils.from_commandline(v, converters.Loader)
        return super(LoadDataset, self).from_options(k, v)

    def check_input(self, token):
        """
        Performs checks on the input token. Raises an exception if unsupported.
        :param token: the token to check
        :type token: Token
        """
        if isinstance(token.payload, str):
            return
        raise Exception("Unhandled class: " + utils.get_classname(token.payload))

    def do_execute(self):
        """
        The actual execution of the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        fname = str(self.input.payload)
        if not os.path.exists(fname):
            return "File '" + fname + "' does not exist!"
        if not os.path.isfile(fname):
            return "Location '" + fname + "' is not a file!"
        if self.resolve_option("use_custom_loader"):
            self._loader = self.resolve_option("custom_loader")
        else:
            self._loader = converters.loader_for_file(fname)
        dataset = self._loader.load_file(fname, incremental=self.resolve_option("incremental"))
        if not self.resolve_option("incremental"):
            self._output.append(Token(dataset))
        else:
            self._iterator = self._loader.__iter__()
        return None

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


class SetStorageValue(Transformer):
    """
    Store the payload of the current token in internal storage using the specified name.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the transformer.
        :param name: the name of the transformer
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(SetStorageValue, self).__init__(name=name, options=options)

    def description(self):
        """
        Returns a description of the actor.
        :return: the description
        :rtype: str
        """
        return "Store the payload of the current token in internal storage using the specified name."

    def fix_options(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.
        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(SetStorageValue, self).fix_options(options)

        opt = "storage_name"
        if opt not in options:
            options[opt] = "unknown"
        if opt not in self.help:
            self.help[opt] = "The storage value name for storing the payload under (string)."

        return options

    def do_execute(self):
        """
        The actual execution of the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        if self.storagehandler is None:
            return "No storage handler available!"
        self.storagehandler.storage[self.resolve_option("storage_name")] = self.input.payload
        self._output.append(self.input)
        return None


class DeleteStorageValue(Transformer):
    """
    Deletes the specified value from internal storage.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the transformer.
        :param name: the name of the transformer
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(DeleteStorageValue, self).__init__(name=name, options=options)

    def description(self):
        """
        Returns a description of the actor.
        :return: the description
        :rtype: str
        """
        return "Deletes the specified value from internal storage."

    def fix_options(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.
        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(DeleteStorageValue, self).fix_options(options)

        opt = "storage_name"
        if opt not in options:
            options[opt] = "unknown"
        if opt not in self.help:
            self.help[opt] = "The name of the storage value to delete (string)."

        return options

    def do_execute(self):
        """
        The actual execution of the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        if self.storagehandler is None:
            return "No storage handler available!"
        self.storagehandler.storage.pop(self.resolve_option("storage_name"), None)
        self._output.append(self.input)
        return None
