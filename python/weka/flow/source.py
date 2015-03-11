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


from weka.flow.base import Actor, OutputProducer


class Source(Actor, OutputProducer):
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
        super(Actor, self).__init__(name=name, options=options)
        super(OutputProducer, self).__init__()
