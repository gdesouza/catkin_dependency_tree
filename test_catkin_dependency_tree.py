import unittest

from catkin_dependency_tree import Package
from catkin_dependency_tree import PackageFromXmlFile
from catkin_dependency_tree import Dependency
from catkin_dependency_tree import DependencyFromXmlNode
from catkin_dependency_tree import get_paths

class GetDependencyRelationshipTestCase(unittest.TestCase):
    def setUp(self):
        import xml.etree.ElementTree as ET

    def test_get_version_eq_should_be_successful(self):
        import xml.etree.ElementTree as ET
        expected_version = "1.0"
        dep = DependencyFromXmlNode(ET.fromstring("<build_depend version_eq='1.0'/>"))
        self.assertEqual(dep.version, f'={expected_version}')

    def test_get_version_gte_should_be_successful(self):
        import xml.etree.ElementTree as ET
        expected_version = "1.0"
        dep = DependencyFromXmlNode(ET.fromstring("<build_depend version_gte='1.0'/>"))
        self.assertEqual(dep.version, f'>={expected_version}')

    def test_get_none_version_should_return_empty(self):
        import xml.etree.ElementTree as ET
        dep = DependencyFromXmlNode(ET.fromstring("<build_depend other_attrib='1.0'/>"))
        self.assertEqual(dep.version, f'')

    def test_get_no_version_should_return_empty(self):
        import xml.etree.ElementTree as ET
        dep = DependencyFromXmlNode(ET.fromstring("<build_depend/>"))
        self.assertEqual(dep.version, f'')


class GetDependenciesTestCase(unittest.TestCase):

    def test_dependency_class(self):
        package_a = Dependency('package_A', '=1.0.0', 'run_depend')
        package_same = Dependency('package_A', '=1.0.0', 'run_depend')
        package_differ = Dependency('package_B', '=1.0.0', 'run_depend')
        self.assertTrue(package_a == package_same)
        self.assertFalse(package_a == package_differ)

    def test_init_dependency_with_xml_node(self):
        import xml.etree.ElementTree
        tree = xml.etree.ElementTree.parse('./test_package.xml')
        root = tree.getroot()
        xml_nodes = root.findall('build_depend')

        dependencies = [ DependencyFromXmlNode(xml_node) 
                         for xml_node in xml_nodes ]
        self.assertIsNotNone(dependencies)
        self.assertEqual(len(dependencies), 2)
        self.assertEqual(dependencies[0].name, 'package_B')
        self.assertEqual(dependencies[0].version, '>=2.0.0')
        self.assertEqual(dependencies[1].name, 'package_C')
        self.assertEqual(dependencies[1].version, '')

    def test_get_path(self):
        result = get_paths('test_package.xml', '.')
        self.assertEqual(result[0], './test_package.xml')

class PackageTestCase(unittest.TestCase):
    def test_package_class(self):
        package_a = Package('package_A', '=1.0.0')
        package_same = Package('package_A', '=1.0.0')
        package_diff = Package('package_B', '=1.0.0')
        self.assertTrue(package_a == package_same)
        self.assertFalse(package_a == package_diff)

    def test_get_package_from_file(self):
        package = PackageFromXmlFile('./test_package.xml')
        package.add_dependency(Dependency('package_A', '=1.0.0', 'run_depend'))
        self.assertEqual(package.name, 'package_name')
        self.assertEqual(package.version, '1.2.0')




if __name__ == '__main__':  # pragma: no cover
    unittest.main()