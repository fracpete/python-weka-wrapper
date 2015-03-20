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

# conversion.py
# Copyright (C) 2015 Fracpete (pythonwekawrapper at gmail dot com)


from weka.flow.base import Configurable


class Conversion(Configurable):
    """
    Ancestor for conversions used by the 'Convert' transformer.
    """

    def __init__(self, config=None):
        """
        Initializes the conversion.
        :param config: list of options to use
        :type config: list
        """
        super(Conversion, self).__init__(config=config)
        self._input = None
        self._output = None

    def check_input(self, obj):
        """
        Performs checks on the input object. Raises an exception if unsupported.
        :param obj: the object to check
        :type obj: object
        """
        pass

    @property
    def input(self):
        """
        Returns the current input object, None if not available.
        :return: the input object
        :rtype: object
        """
        return self._input

    @input.setter
    def input(self, obj):
        """
        Accepts the data for processing.
        :param obj: the object to process
        :type obj: object
        """
        self.check_input(obj)
        self._input = obj

    @property
    def output(self):
        """
        Returns the generated output object, None if not available.
        :return: the output object
        :rtype: object
        """
        return self._output

    def convert(self):
        """
        Performs the actual conversion.
        :return: None if successful, otherwise errors message
        :rtype: str
        """
        raise Exception("Not implemented!")


class PassThrough(Conversion):
    """
    Dummy conversion, just passes through the data.
    """

    def description(self):
        """
        Returns the description for the conversion.
        :return: the description
        :rtype: str
        """
        return "Dummy conversion, just passes through the data."

    def convert(self):
        """
        Performs the actual conversion.
        :return: None if successful, otherwise errors message
        :rtype: str
        """
        self._output = self._input
        return None
