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


import uuid
import logging
import re


class Actor(object):
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
        self._name = __name__
        self._parent = None
        self._full_name = None
        self._logger = None
        self._help = {}
        self._options = self.fix_options({})
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
        return self.__name__ + "(options=" + str(self.options) + ")"

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
        return self._options

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
            bname = re.sub(r'-[0-9]+$', '', name)
            names = []
            for actor in self.parent.actors:
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
            while parent is not None:
                fn = parent.name.replace(".", "\\.") + "." + fn
                parent = parent.parent
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
        if "skip" not in options:
            options["skip"] = False
        if "skip" not in self.help:
            self.help["skip"] = "The name of the actor to use in the flow."
        return options

    @property
    def options(self):
        """
        Obtains the currently set options of the actor.
        :return: the options
        :rtype: dict
        """
        return self._options

    @options.setter
    def options(self, options):
        """
        Sets the options of the actor.
        :param options: the options
        :type options: dict
        """
        self._options = self.fix_options(options)

    @property
    def help(self):
        """
        Obtains the help information per option for this actor.
        :return: the help
        :rtype: dict
        """
        return self._help

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
        if self.options["skip"]:
            return None

        result = self.pre_execute()
        if result is None:
            result = self.do_execute()
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
        result.append(self.__name__)
        result.append(re.sub(r'.', '=', self.__name__))
        result.append("")
        result.append(self.description())
        result.append("")
        opts = self.options.keys()
        opts.sort()
        for opt in opts:
            result.append(opt)
            helpstr = self.help[opt]
            if helpstr is None:
                helpstr = "-missing help-"
            result.append("\t" + helpstr)
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

    def __init__(self):
        """
        Initializes the actor.
        """
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

    def __init__(self):
        """
        Initializes the actor.
        """
        self._output = None

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
