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

# sink.py
# Copyright (C) 2015 Fracpete (pythonwekawrapper at gmail dot com)


from weka.flow.base import InputConsumer


class Sink(InputConsumer):
    """
    The ancestor for all sinks.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the sink.
        :param name: the name of the sink
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(Sink, self).__init__(name=name, options=options)
        super(InputConsumer, self).__init__()

    def post_execute(self):
        """
        Gets executed after the actual execution.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = super(Sink, self).post_execute()
        if result is None:
            self.input = None
        return result


class Null(Sink):
    """
    Sink that just gobbles up all the data.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the transformer.
        :param name: the name of the transformer
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(Null, self).__init__(name=name, options=options)

    def description(self):
        """
        Returns a description of the actor.
        :return: the description
        :rtype: str
        """
        return "Sink that just gobbles up all the data."

    def do_execute(self):
        """
        The actual execution of the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        return None


class Console(Sink):
    """
    Sink that outputs the payloads of the data on stdout.
    """

    def __init__(self, name=None, options=None):
        """
        Initializes the transformer.
        :param name: the name of the transformer
        :type name: str
        :param options: the dictionary with the options (str -> object).
        :type options: dict
        """
        super(Console, self).__init__(name=name, options=options)

    def description(self):
        """
        Returns a description of the actor.
        :return: the description
        :rtype: str
        """
        return "Sink that outputs the payloads of the data on stdout."

    def fix_options(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.
        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(Console, self).fix_options(options)

        opt = "prefix"
        if opt not in options:
            options[opt] = ""
        if opt not in self.help:
            self.help[opt] = "The prefix for the output (string)."

        return options

    def do_execute(self):
        """
        The actual execution of the actor.
        :return: None if successful, otherwise error message
        :rtype: str
        """
        print(self.resolve_option("prefix") + str(self.input.payload))
        return None
