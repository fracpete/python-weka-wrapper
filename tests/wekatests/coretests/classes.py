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
# Copyright (C) 2014-2155 Fracpete (pythonwekawrapper at gmail dot com)

import unittest
import javabridge
import weka.core.jvm as jvm
import weka.core.utils as utils
import weka.core.classes as classes
import wekatests.tests.weka_test as weka_test


class TestClasses(weka_test.WekaTest):

    def test_singleindex(self):
        """
        Tests the SingleIndex class.
        """
        index = classes.SingleIndex()
        self.assertEqual("", index.single_index)

        index = classes.SingleIndex(index="first")
        index.upper(10)
        self.assertEqual("first", index.single_index)
        self.assertEqual(0, index.index())

        index = classes.SingleIndex(index="2")
        index.upper(10)
        self.assertEqual("2", index.single_index)
        self.assertEqual(1, index.index())

    def test_range(self):
        """
        Tests the Range class.
        """
        rang = classes.Range()
        self.assertEqual("", rang.ranges)

        rang = classes.Range(ranges="first")
        rang.upper(10)
        self.assertEqual("first", rang.ranges)
        self.assertEqual([0], rang.selection())

        rang = classes.Range(ranges="2")
        rang.upper(10)
        self.assertEqual("2", rang.ranges)
        self.assertEqual([1], rang.selection())

        rang = classes.Range(ranges="2-5,7")
        rang.upper(10)
        self.assertEqual("2-5,7", rang.ranges)
        self.assertItemsEqual([1, 2, 3, 4, 6], rang.selection())

    def test_javaobject(self):
        """
        Tests the JavaObject class.
        """
        cls = "weka.classifiers.trees.J48"
        obj = classes.JavaObject.new_instance(cls)
        self.assertIsNotNone(obj, "Failed to instantiate Java object: " + cls)
        jobj = classes.JavaObject(obj)
        self.assertEqual(cls, jobj.classname, "Classname differs!")

    def test_javaarray(self):
        """
        Tests the JavaArray class.
        """
        jarray = classes.JavaArray(classes.JavaArray.new_instance("weka.core.Tag", 3))
        self.assertIsNotNone(jarray)
        self.assertEqual(3, len(jarray), msg="Array length differs!")
        self.assertIsNone(jarray[0], msg="Initial value must be none")
        count = 0
        for i in jarray:
            self.assertIsNone(i, msg="Element #" + str(count) + " is not none!")
            count += 1
        tag = classes.Tag(ident=1, ident_str="BLAH", readable="blahblah")
        jarray[0] = tag
        self.assertIsNotNone(jarray[0], msg="Should not be none")
        count = 0
        for i in jarray:
            if count == 0:
                self.assertIsNotNone(i, msg="Element #" + str(count) + " is none!")
            else:
                self.assertIsNone(i, msg="Element #" + str(count) + " is not none!")
            count += 1

    def test_enum(self):
        """
        Tests the enum class.
        """

        enum = "weka.core.Capabilities$Capability"
        member = "NOMINAL_CLAS"
        try:
            classes.Enum(enum=enum, member=member)
            self.fail("Should not have instantiated enum")
        except:
            pass

        member = "NOMINAL_CLASS"
        enum1 = classes.Enum(enum=enum, member=member)
        self.assertIsNotNone(enum1, "Failed to instantiate enum")
        self.assertEqual(member, enum1.name)

        enum2 = classes.Enum(jobject=enum1.jobject)
        self.assertIsNotNone(enum2, "Failed to instantiate enum")
        self.assertEqual(member, enum2.name)

        values = enum1.values
        self.assertIsNotNone(values, "Failed to retrieve list of members")
        self.assertGreater(len(values), 0, msg="Should have at least one member")

    def test_tag(self):
        """
        Tests the Tag class.
        """
        tag1 = classes.Tag(ident=1, ident_str="tag1", readable="blah blah")
        self.assertIsNotNone(tag1, msg="Failed to instantiate tag")
        self.assertEqual(tag1.ident, 1, msg="ID differs")
        self.assertEqual(tag1.identstr, "TAG1", msg="ID string differs")
        self.assertEqual(tag1.readable, "blah blah", msg="Readable string differs")
        tag2 = classes.Tag(ident=2, ident_str="tag2", readable="more blah", uppercase=False)
        self.assertIsNotNone(tag2, msg="Failed to instantiate tag")
        self.assertEqual(tag2.ident, 2, msg="ID differs")
        self.assertEqual(tag2.identstr, "tag2", msg="ID string differs")
        self.assertEqual(tag2.readable, "more blah", msg="Readable string differs")

    def test_tags(self):
        """
        Tests the Tags class.
        """
        tag1 = classes.Tag(ident=1, ident_str="tag1", readable="blah 1")
        tag2 = classes.Tag(ident=2, ident_str="tag2", readable="blah 2")
        tag3 = classes.Tag(ident=3, ident_str="tag3", readable="blah 3")
        tags = classes.Tags(tags=[tag1, tag2, tag3])
        self.assertEqual(3, len(tags), "Number of tags differs!")
        self.assertEqual("TAG1|TAG2|TAG3", str(tags), msg="String differs")
        smo = classes.JavaObject(classes.JavaObject.new_instance(classname="weka.classifiers.functions.SMO"))
        tags = classes.Tags(jobject=javabridge.get_static_field("Lweka/classifiers/functions/SMO;", "TAGS_FILTER", "[Lweka/core/Tag;"))
        self.assertEqual(3, len(tags), "Number of tags differs!")
        self.assertEqual("0|1|2", str(tags), msg="String differs")

    def test_selectedtag(self):
        """
        Tests the SelectedTag  class.
        """
        tags = classes.Tags(jobject=javabridge.get_static_field("Lweka/classifiers/functions/SMO;", "TAGS_FILTER", "[Lweka/core/Tag;"))
        stag = classes.SelectedTag(tag_id=1, tags=tags)
        self.assertEqual(1, stag.selected.ident, "ID differs")
        stag = classes.SelectedTag(tag_text="2", tags=tags)
        self.assertEqual(2, stag.selected.ident, "ID differs")


def suite():
    """
    Returns the test suite.
    :return: the test suite
    :rtype: unittest.TestSuite
    """
    return unittest.TestLoader().loadTestsFromTestCase(TestClasses)


if __name__ == '__main__':
    jvm.start()
    unittest.TextTestRunner().run(suite())
    jvm.stop()
