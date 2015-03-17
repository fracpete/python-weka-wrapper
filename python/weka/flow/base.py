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

# base.py
# Copyright (C) 2015 Fracpete (pythonwekawrapper at gmail dot com)


import json
import logging
import re
import traceback
import uuid
import weka.core.utils as utils


class Stoppable(object):
    """
    Classes that can be stopped.
    """

    def is_stopped(self):
        """
        Returns whether the object has been stopped.
        :return: whether stopped
        :rtype: bool
        """
        raise Exception("Not implemented!")

    def stop_execution(self):
        """
        Triggers the stopping of the object.
        """
        raise Exception("Not implemented!")


class Actor(Stoppable):
    """
    The ancestor for all actors.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the actor.
        :param name: the name of the actor
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        self._name = self.__class__.__name__
        self._parent = None
        self._full_name = None
        self._logger = None
        self._help = {}
        self._options = self.fix_options({})
        self._stopped = False
        if options is not None:
            self.options = options
        if name is not None:
            self.name = name

    def __str__(self):
        """
        Returns a short representation of the actor's setup.
        :return: the setup
        :rtype: str
        """
        return self.full_name + ": " + str(self._options)

    def __repr__(self):
        """
        Returns Python code for instantiating the actor.
        :return: the representation
        :rtype: str
        """
        return \
            self.__class__.__module__ + "." + self.__class__.__name__ \
            + "(name=" + self.name + ", options=" + str(self.options) + ")"

    def description(self):
        """
        Returns a description of the actor.
        :return: the description
        :rtype: str
        """
        raise Exception("Not implemented!")

    @property
    def logger(self):
        """
        Returns the logger object.
        :return: the logger
        :rtype: logger
        """
        if self._logger is None:
            self._logger = logging.getLogger(self.full_name)
        return self._logger

    @property
    def name(self):
        """
        Obtains the currently set name of the actor.
        :return: the name
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of the actor.
        :param name: the name
        :type name: str
        """
        self._name = name

    def unique_name(self, name):
        """
        Generates a unique name.
        :param name: the name to check
        :type name: str
        :return: the unique name
        :rtype: str
        """
        result = name

        if self.parent is not None:
            index = self.index
            bname = re.sub(r'-[0-9]+$', '', name)
            names = []
            for idx, actor in enumerate(self.parent.actors):
                if idx != index:
                    names.append(actor.name)
            result = bname
            count = 0
            while result in names:
                count += 1
                result = bname + "-" + str(count)

        return result

    @property
    def parent(self):
        """
        Obtains the currently set parent of the actor.
        :return: the name
        :rtype: str
        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        """
        Sets the parent of the actor.
        :param parent: the parent
        :type parent: Actor
        """
        self._name = self.unique_name(self._name)
        self._full_name = None
        self._logger = None
        self._parent = parent

    @property
    def index(self):
        """
        Returns the index of this actor in its parent's list of actors.
        :return: the index, -1 if not available
        :rtype: int
        """
        if self.parent is None:
            return -1
        else:
            return self.parent.index_of(self.name)

    @property
    def full_name(self):
        """
        Obtains the full name of the actor.
        :return: the full name
        :rtype: str
        """
        if self._full_name is None:
            fn = self.name.replace(".", "\\.")
            parent = self._parent
            if parent is not None:
                fn = parent.full_name + "." + fn
            self._full_name = fn

        return self._full_name

    def fix_options(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.
        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        opt = "annotation"
        if opt not in options:
            options[opt] = None
        if opt not in self.help:
            self.help[opt] = "The (optional) annotation for this actor."

        opt = "skip"
        if opt not in options:
            options[opt] = False
        if opt not in self.help:
            self.help[opt] = "The name of the actor to use in the flow."

        return options

    @property
    def options(self):
        """
        Obtains the currently set options of the actor.
        :return: the options
        :rtype: dict
        """
        return self._options

    def resolve_option(self, name, default=None):
        """
        Resolves the option, i.e., interprets "@{...}" values and retrievs them instead from internal
        storage.
        :param name: the name of the option
        :type name: str
        :param default: the optional default value
        :type default: object
        :return: the resolved value
        :rtype: object
        """
        value = self.options[name]
        if value is None:
            return default
        elif isinstance(value, str) and value.startswith("@{") and value.endswith("}"):
            stname = value[2:len(value)-1]
            if (self.storagehandler is not None) and (stname in self.storagehandler.storage):
                return self.storagehandler.storage[stname]
            else:
                return default
        else:
            return value

    @options.setter
    def options(self, options):
        """
        Sets the options of the actor.
        :param options: the options
        :type options: dict
        """
        self._options = self.fix_options(options)

    @property
    def skip(self):
        """
        Obtains whether the actor is disabled (skipped).
        :return: True if skipped
        :rtype: bool
        """
        return self.resolve_option("skip")

    @skip.setter
    def skip(self, skip):
        """
        Sets whether the actor is skipped.
        :param skip: True if skipped
        :type skip: bool
        """
        self.options["skip"] = skip

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.
        :return: the info, None if not available
        :rtype: str
        """
        return None

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
        return v

    def to_options_dict(self):
        """
        Returns a dictionary of its options.
        :return: the options as dictionary
        :rtype: dict
        """
        result = {}
        result["name"] = self.name
        result["class"] = utils.get_classname(self)
        options = self.options.copy()
        result["options"] = {}
        for k in options.keys():
            result["options"][k] = self.to_options(k, options[k])
        return result

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
        return v

    def from_options_dict(self, d):
        """
        Restores the object from the given options dictionary.
        :param d: the dictionary to use for restoring the options
        :type d: dict
        """
        for k in d.keys():
            if k in self.options:
                self.options[k] = d[k]
            d.pop(k, None)

    @property
    def json(self):
        """
        Returns the options as JSON.
        :return: the object as string
        :rtype: str
        """
        return json.dumps(self.to_options_dict())

    @json.setter
    def json(self, s):
        """
        Restores the object from the given JSON.
        :param s: the JSON string to parse
        :type s: str
        """
        self.from_options_dict(json.loads(s))

    @property
    def help(self):
        """
        Obtains the help information per option for this actor.
        :return: the help
        :rtype: dict
        """
        return self._help

    @property
    def storagehandler(self):
        """
        Returns the storage handler available to thise actor.
        :return: the storage handler, None if not available
        """
        if isinstance(self, StorageHandler):
            return self
        elif self.parent is not None:
            return self.parent.storagehandler
        else:
            return None

    @property
    def root(self):
        """
        Returns the top-level actor.
        :return: the top-level actor
        :rtype: Actor
        """
        if self.parent is None:
            return self
        else:
            return self.parent.root

    @property
    def depth(self):
        """
        Returns the depth of this actor inside the overall flow.
        :return: the depth
        :rtype: int
        """
        if self.parent is None:
            return 0
        else:
            return self.parent.depth + 1

    def is_stopped(self):
        """
        Returns whether the object has been stopped.
        :return: whether stopped
        :rtype: bool
        """
        return self._stopped

    def stop_execution(self):
        """
        Triggers the stopping of the object.
        """
        self._stopped = True

    def setup(self):
        """
        Configures the actor before execution.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        return None

    def pre_execute(self):
        """
        Gets executed before the actual execution.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        return None

    def do_execute(self):
        """
        The actual execution of the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        raise Exception("Not implemented!")

    def post_execute(self):
        """
        Gets executed after the actual execution.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        return None

    def execute(self):
        """
        Executes the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        if self.skip:
            return None

        result = self.pre_execute()
        if result is None:
            try:
                result = self.do_execute()
            except Exception, e:
                result = traceback.format_exc()
                print(self.full_name + "\n" + result)
        if result is None:
            result = self.post_execute()
        return result

    def wrapup(self):
        """
        Finishes up after execution finishes, does not remove any graphical output.
        """
        pass

    def cleanup(self):
        """
        Destructive finishing up after execution stopped.
        """
        pass

    def generate_help(self):
        """
        Generates a help string for this actor.
        :return: the help string
        :rtype: str
        """
        result = []
        result.append(self.__class__.__name__)
        result.append(re.sub(r'.', '=', self.__class__.__name__))
        result.append("")
        result.append("DESCRIPTION")
        result.append(self.description())
        result.append("")
        result.append("OPTIONS")
        opts = self.options.keys()
        opts.sort()
        for opt in opts:
            result.append(opt)
            helpstr = self.help[opt]
            if helpstr is None:
                helpstr = "-missing help-"
            result.append("\t" + helpstr)
            result.append("")
        return '\n'.join(result)

    def print_help(self):
        """
        Prints a help string for this actor to stdout.
        """
        print(self.generate_help())


class Token(object):
    """
    Container for transporting data through the flow.
    """

    def __init__(self, payload):
        """
        Initializes the token with the given payload.
        :param payload: the payload for the token.
        :type payload: object
        """
        self._id = str(uuid.uuid4())
        self._payload = payload

    @property
    def id(self):
        """
        Obtains the ID of the token.
        :return: the ID
        :rtype: str
        """
        return self._id

    @property
    def payload(self):
        """
        Obtains the currently set payload.
        :return: the payload
        :rtype: object
        """
        return self._payload

    def __str__(self):
        """
        Returns a short representation of the token and its payload.
        """
        return self._id + ": " + str(self._payload)


class InputConsumer(Actor):
    """
    Actors that consume tokens inherit this class.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the actor.
        :param name: the name of the actor
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(InputConsumer, self).__init__(name=name, options=options)
        self._input = None

    def check_input(self, token):
        """
        Performs checks on the input token. Raises an exception if unsupported.
        :param token: the token to check
        :type token: Token
        """
        pass

    @property
    def input(self):
        """
        Returns the current input token, None if not available.
        :return: the input token
        :rtype: Token
        """
        return self._input

    @input.setter
    def input(self, token):
        """
        Accepts the data for processing.
        :param token: the token to process
        :type token: Token
        """
        self.check_input(token)
        self._input = token


class OutputProducer(Actor):
    """
    Actors that generate output tokens inherit this class.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the actor.
        :param name: the name of the actor
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(OutputProducer, self).__init__(name=name, options=options)
        self._output = None

    def pre_execute(self):
        """
        Gets executed before the actual execution.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        self._output = []
        return None

    def has_output(self):
        """
        Checks whether any output tokens are present.
        :return: true if at least one output token present
        :rtype: bool
        """
        return (self._output is not None) and (len(self._output) > 0)

    def output(self):
        """
        Returns the next available output token.
        :return: the next token, None if none available
        :rtype: Token
        """
        if (self._output is None) or (len(self._output) == 0):
            result = None
        else:
            result = self._output.pop(0)
        return result


class StorageHandler(object):
    """
    For classes that support internal storage (= dictionary).
    """

    @property
    def storage(self):
        """
        Returns the internal storage.
        :return: the internal storage
        :rtype: dict
        """
        raise Exception("Not implemented!")

    def expand(self, s):
        """
        Expands all occurrences of "@{...}" within the string with the actual values currently stored
        in internal storage.
        :param s: the string to expand
        :type s: str
        :return: the expanded string
        :rtype: str
        """
        result = s
        while result.find("@{") > -1:
            start = result.index("@{")
            end = result.index("}", start)
            name = result[start + 2:end]
            value = self.storage[name]
            if value is None:
                raise("Storage value '" + name + "' not present, failed to expand string: " + s)
            else:
                result = result[1:start] + str(value) + result[end + 1:]
        return result

    def pad(self, name):
        """
        Pads the name with "@{...}".
        :param name: the name to pad
        :type name: str
        :return: the padded name
        :rtype: str
        """
        if name.startswith("@{"):
            return name
        else:
            return "@{" + name + "}"

    def extract(self, padded):
        """
        Removes the surrounding "@{...}" from the name.
        :param padded: the padded string
        :type padded: str
        :return: the extracted name
        :rtype: str
        """
        if padded.startswith("@{") and padded.endswith("}"):
            return padded[2:len(padded)-1]
        else:
            return padded


def is_source(actor):
    """
    Checks whether the actor is a source.
    :param actor: the actor to check
    :type actor: Actor
    :return: True if the actor is a source
    :rtype: bool
    """
    return not isinstance(actor, InputConsumer) and isinstance(actor, OutputProducer)


def is_transformer(actor):
    """
    Checks whether the actor is a transformer.
    :param actor: the actor to check
    :type actor: Actor
    :return: True if the actor is a transformer
    :rtype: bool
    """
    return isinstance(actor, InputConsumer) and isinstance(actor, OutputProducer)


def is_sink(actor):
    """
    Checks whether the actor is a sink.
    :param actor: the actor to check
    :type actor: Actor
    :return: True if the actor is a sink
    :rtype: bool
    """
    return isinstance(actor, InputConsumer) and not isinstance(actor, OutputProducer)


def to_commandline(o):
    """
    Turns the object into a commandline string. However, first checks whether a string represents
    a internal value placeholder (@{...}).
    :param o: the object to turn into commandline
    :type o: object
    :return: the commandline
    :rtype: str
    """
    if isinstance(o, str) and o.startswith("@{") and o.endswith("}"):
        return o
    else:
        return utils.to_commandline(o)
