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
from weka.flow.base import InputConsumer, OutputProducer, Token
from weka.flow.container import ModelContainer
import weka.core.converters as converters
from weka.core.dataset import Instance, Instances
import weka.core.utils as utils
from weka.classifiers import Classifier
from weka.clusterers import Clusterer


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

    def post_execute(self):
        """
        Gets executed after the actual execution.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = super(Transformer, self).post_execute()
        if result is None:
            self._input = None
        return result


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

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.
        :return: the info, None if not available
        :rtype: str
        """
        return "incremental: " + str(self.resolve_option("incremental")) \
               + ", custom: " + str(self.resolve_option("use_custom_loader")) \
               + ", loader: " + utils.to_commandline(self.resolve_option("custom_loader"))

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
        if token is None:
            raise Exception(self.full_name + ": No token provided!")
        if isinstance(token.payload, str):
            return
        raise Exception(self.full_name + ": Unhandled class: " + utils.get_classname(token.payload))

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
        dataset = self._loader.load_file(fname, incremental=bool(self.resolve_option("incremental")))
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

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.
        :return: the info, None if not available
        :rtype: str
        """
        return "name: " + str(self.resolve_option("storage_name"))

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

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.
        :return: the info, None if not available
        :rtype: str
        """
        return "name: " + str(self.resolve_option("storage_name"))

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


class MathExpression(Transformer):
    """
    Calculates a mathematical expression. The captial letter X in the expression gets replaced by
    the value of the current token passing through. Uses the 'eval(str)' method for the calculation,
    therefore mathematical functions can be accessed using the 'math' library, e.g., '1 + math.sin(X)'.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the transformer.
        :param name: the name of the transformer
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(MathExpression, self).__init__(name=name, options=options)

    def description(self):
        """
        Returns a description of the actor.
        :return: the description
        :rtype: str
        """
        return \
            "Calculates a mathematical expression. The captial letter X in the expression gets replaced by "\
            + "the value of the current token passing through. Uses the 'eval(str)' method for the calculation, "\
            + "therefore mathematical functions can be accessed using the 'math' library, e.g., '1 + math.sin(X)'."

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.
        :return: the info, None if not available
        :rtype: str
        """
        return "expression: " + str(self.resolve_option("expression"))

    def fix_options(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.
        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(MathExpression, self).fix_options(options)

        opt = "expression"
        if opt not in options:
            options[opt] = "X"
        if opt not in self.help:
            self.help[opt] = "The mathematical expression to evaluate (string)."

        return options

    def do_execute(self):
        """
        The actual execution of the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        expr = self.resolve_option("expression")
        expr = expr.replace("X", str(self.input.payload))
        self._output.append(Token(eval(expr)))
        return None


class ClassSelector(Transformer):
    """
    Sets/unsets the class index of a dataset.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the transformer.
        :param name: the name of the transformer
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(ClassSelector, self).__init__(name=name, options=options)

    def description(self):
        """
        Returns a description of the actor.
        :return: the description
        :rtype: str
        """
        return "Sets/unsets the class index of a dataset."

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.
        :return: the info, None if not available
        :rtype: str
        """

        return "index: " + str(self.resolve_option("index"))

    def fix_options(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.
        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(ClassSelector, self).fix_options(options)

        opt = "index"
        if opt not in options:
            options[opt] = "last"
        if opt not in self.help:
            self.help[opt] = "The class index (1-based number); 'first' and 'last' are accepted as well (string)."

        opt = "unset"
        if opt not in options:
            options[opt] = False
        if opt not in self.help:
            self.help[opt] = "Whether to unset the class index (bool)."

        return options

    def do_execute(self):
        """
        The actual execution of the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        data = self.input.payload
        index = str(self.resolve_option("index"))
        unset = bool(self.resolve_option("unset"))
        if unset:
            data.no_class()
        else:
            if index == "first":
                data.class_is_first()
            elif index == "last":
                data.class_is_last()
            else:
                data.class_index = int(index) - 1
        self._output.append(Token(data))
        return None


class TrainClassifier(Transformer):
    """
    Trains the classifier on the incoming dataset and forwards a ModelContainer with the trained
    model and the dataset header.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the transformer.
        :param name: the name of the transformer
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(TrainClassifier, self).__init__(name=name, options=options)

    def description(self):
        """
        Returns a description of the actor.
        :return: the description
        :rtype: str
        """
        return \
            "Trains the classifier on the incoming dataset and forwards a ModelContainer with the trained " \
            + "model and the dataset header."

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.
        :return: the info, None if not available
        :rtype: str
        """
        return "classifier: " + utils.to_commandline(self.resolve_option("classifier"))

    def fix_options(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.
        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(TrainClassifier, self).fix_options(options)

        opt = "classifier"
        if opt not in options:
            options[opt] = Classifier(classname="weka.classifiers.rules.ZeroR")
        if opt not in self.help:
            self.help[opt] = "The classifier to train (Classifier)."

        return options

    def check_input(self, token):
        """
        Performs checks on the input token. Raises an exception if unsupported.
        :param token: the token to check
        :type token: Token
        """
        if isinstance(token.payload, Instances):
            return
        if isinstance(token.payload, Instance):
            return
        raise Exception(self.full_name + ": Unhandled data type: " + str(token.payload.__class__.__name__))

    def do_execute(self):
        """
        The actual execution of the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        # TODO incremental classifiers
        data = self.input.payload
        cls = self.resolve_option("classifier")
        cls = Classifier.make_copy(cls)
        cls.build_classifier(data)
        cont = ModelContainer(model=cls, header=Instances.template_instances(data))
        self._output.append(Token(cont))
        return None


class TrainClusterer(Transformer):
    """
    Trains the clusterer on the incoming dataset and forwards a ModelContainer with the trained
    model and the dataset header.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the transformer.
        :param name: the name of the transformer
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(TrainClusterer, self).__init__(name=name, options=options)

    def description(self):
        """
        Returns a description of the actor.
        :return: the description
        :rtype: str
        """
        return \
            "Trains the clusterer on the incoming dataset and forwards a ModelContainer with the trained " \
            + "model and the dataset header."

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.
        :return: the info, None if not available
        :rtype: str
        """
        return "clusterer: " + utils.to_commandline(self.resolve_option("clusterer"))

    def fix_options(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.
        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(TrainClusterer, self).fix_options(options)

        opt = "clusterer"
        if opt not in options:
            options[opt] = Clusterer(classname="weka.clusterers.SimpleKMeans")
        if opt not in self.help:
            self.help[opt] = "The clusterer to train (Clusterer)."

        return options

    def check_input(self, token):
        """
        Performs checks on the input token. Raises an exception if unsupported.
        :param token: the token to check
        :type token: Token
        """
        if isinstance(token.payload, Instances):
            return
        if isinstance(token.payload, Instance):
            return
        raise Exception(self.full_name + ": Unhandled data type: " + str(token.payload.__class__.__name__))

    def do_execute(self):
        """
        The actual execution of the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        # TODO incremental clusterers
        data = self.input.payload
        cls = self.resolve_option("clusterer")
        cls = Clusterer.make_copy(cls)
        cls.build_clusterer(data)
        cont = ModelContainer(model=cls, header=Instances.template_instances(data))
        self._output.append(Token(cont))
        return None
