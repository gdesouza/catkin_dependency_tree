import unittest

from catkin_dependency_tree import Dependency
from catkin_dependency_tree import Package
from catkin_dependency_tree import PackageFromXmlFile
from catkin_dependency_tree import get_dependency_relationship
from catkin_dependency_tree import extract_dependency
from catkin_dependency_tree import get_dependencies_from
from catkin_dependency_tree import get_dependencies_from_file
from catkin_dependency_tree import get_paths

class GetDependencyRelationshipTestCase(unittest.TestCase):
    def test_get_version_eq_should_be_successful(self):
        expected_version = 1
        attrib = {'version_eq': expected_version}
        result = get_dependency_relationship(attrib)
        self.assertEqual(result, f'={expected_version}')

    def test_get_version_gte_should_be_successful(self):
        expected_version = 1
        attrib = {'version_gte': expected_version}
        result = get_dependency_relationship(attrib)
        self.assertEqual(result, f'>={expected_version}')

    def test_get_none_version_should_return_empty(self):
        expected_version = 1
        attrib = {'other_attrib': expected_version}
        result = get_dependency_relationship(None)
        self.assertEqual(result, f'')

    def test_get_no_version_should_return_empty(self):
        expected_version = 1
        attrib = {'other_attrib': expected_version}
        result = get_dependency_relationship(attrib)
        self.assertEqual(result, f'')

class ExtractDependencyTestCase(unittest.TestCase):
    def test_extract_dependency_with_version_should_return_success(self):
        import xml.etree.ElementTree
        tree = xml.etree.ElementTree.parse('./test_package.xml')
        root = tree.getroot()
        dependency = extract_dependency(root.find('buildtool_depend'))
        self.assertEqual(dependency.name, "package_A")
        self.assertEqual(dependency.version, "=1.0.0")
        self.assertEqual(dependency.type, "buildtool_depend")

class GetDependenciesTestCase(unittest.TestCase):
    def test_dependency_class(self):
        package_a = Dependency('package_A', '=1.0.0', 'run_depend')
        package_same = Dependency('package_A', '=1.0.0', 'run_depend')
        package_differ = Dependency('package_B', '=1.0.0', 'run_depend')
        self.assertTrue(package_a == package_same)
        self.assertFalse(package_a == package_differ)

    def test_get_dependencies_should_return_list(self):
        import xml.etree.ElementTree
        tree = xml.etree.ElementTree.parse('./test_package.xml')
        root = tree.getroot()
        dependencies = get_dependencies_from(root, 'build_depend')
        self.assertIsNotNone(dependencies)
        self.assertEqual(len(dependencies), 2)
        self.assertEqual(dependencies[0].name, 'package_B')
        self.assertEqual(dependencies[0].version, '>=2.0.0')
        self.assertEqual(dependencies[1].name, 'package_C')
        self.assertEqual(dependencies[1].version, '')

    def test_get_dependencies_from_file_should_return_list(self):
        dependencies = get_dependencies_from_file('./test_package.xml')
        dependencies_str = [str(dep) for dep in dependencies]
        self.assertIsNotNone(dependencies)
        self.assertEqual(len(dependencies), 6)
        self.assertIn(str(Dependency('package_A', '=1.0.0', 'buildtool_depend')), dependencies_str)
        self.assertIn(str(Dependency('package_B', '>=2.0.0', 'build_depend')), dependencies_str)
        self.assertIn(str(Dependency('package_C', '', 'build_depend')), dependencies_str)
        self.assertIn(str(Dependency('package_D', '', 'build_export_depend')), dependencies_str)
        self.assertIn(str(Dependency('package_E', '', 'run_depend')), dependencies_str)
        self.assertIn(str(Dependency('package_F', '', 'exec_depend')), dependencies_str)

    def test_get_path(self):
        result = get_paths('test_package.xml', '.')
        self.assertEqual(result[0], './test_package.xml')

class PackageTestCase(unittest.TestCase):
    def test_package_class(self):
        package_a = Package('package_A', '=1.0.0')
        package_same = Package('package_A', '=1.0.0')
        self.assertTrue(package_a == package_same)

    def test_get_package_from_file(self):
        package = PackageFromXmlFile('./test_package.xml')
        package.add_dependency(Dependency('package_A', '=1.0.0', 'run_depend'))
        self.assertEqual(package.name, 'package_name')
        self.assertEqual(package.version, '1.2.0')




if __name__ == '__main__':  # pragma: no cover
    unittest.main()