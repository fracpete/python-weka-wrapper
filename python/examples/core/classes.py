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

# classes.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import weka.core.jvm as jvm
import examples.helper as helper
from weka.core.classes import Capability
from weka.classifiers import Classifier


def main():
    """
    Just runs some example code.
    """

    classifier = Classifier("weka.classifiers.trees.J48")

    helper.print_title("Capabilities")
    capabilities = classifier.get_capabilities()
    print(capabilities)

    helper.print_title("Disable/Enable")
    capability = Capability.parse("UNARY_ATTRIBUTES")
    capabilities.disable(capability)
    print("Removing: " + str(capability))
    print(capabilities)


if __name__ == "__main__":
    try:
        jvm.start()
        main()
    except Exception, e:
        print(e)
    finally:
        jvm.stop()
