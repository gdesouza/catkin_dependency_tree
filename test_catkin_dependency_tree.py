import unittest
import catkin_dependency_tree as test_obj

class GetDependencyRelationshipTestCase(unittest.TestCase):
    def test_get_version_eq_should_be_successful(self):
        expected_version = 1
        attrib = {'version_eq': expected_version}
        result = test_obj.get_dependency_relationship(attrib)
        self.assertEqual(result, f'={expected_version}')

    def test_get_version_gte_should_be_successful(self):
        expected_version = 1
        attrib = {'version_gte': expected_version}
        result = test_obj.get_dependency_relationship(attrib)
        self.assertEqual(result, f'>={expected_version}')

    def test_get_none_version_should_return_empty(self):
        expected_version = 1
        attrib = {'other_attrib': expected_version}
        result = test_obj.get_dependency_relationship(None)
        self.assertEqual(result, f'')

    def test_get_no_version_should_return_empty(self):
        expected_version = 1
        attrib = {'other_attrib': expected_version}
        result = test_obj.get_dependency_relationship(attrib)
        self.assertEqual(result, f'')

class ExtractDependencyTestCase(unittest.TestCase):
    def test_extract_dependency_with_version_should_return_success(self):
        import xml.etree.ElementTree
        tree = xml.etree.ElementTree.parse('./test_package.xml')
        root = tree.getroot()
        root.find('buildtool_depend')
        dependency = test_obj.extract_dependency(root.find('buildtool_depend'))
        self.assertEqual(dependency.name, "package_A")
        self.assertEqual(dependency.version, "=1.0.0")
        self.assertEqual(dependency.type, "buildtool_depend")


if __name__ == '__main__':  # pragma: no cover
    unittest.main()