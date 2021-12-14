#!/usr/bin/env python3
"""
Creates the dependency tree in a catkin workspace
"""

import os
import argparse
import xml.etree.ElementTree
from glob import glob


class Package:
    """ROS Package as defined in package.xml"""

    def __init__(self, name, version):
        self.name = name
        self.version = version
        self.dependencies = []

    def add_dependency(self, dependency):
        """Add dependency to package"""

        self.dependencies.append(dependency)

    def __str__(self):
        return f'{self.name}: {self.dependencies}'

    def __eq__(self, other):
        return str(self) == str(other)

class PackageFromXmlFile(Package):
    """ROS Package as defined in package.xml"""

    def __init__(self, xml_file):
        tree = xml.etree.ElementTree.parse(xml_file)
        root = tree.getroot()
        name = root.find('name').text
        version = root.find('version').text
        super().__init__(name, version)

        self.dependencies = [ DependencyFromXmlNode(child)
                             for dependency_type in Dependency.TYPES
                             for child in root.findall(dependency_type)]


class Dependency:
    """ROS package dependency"""

    TYPES = [ 'run_depend', 'build_depend', 'exec_depend', 'depend',
                     'buildtool_depend', 'build_export_depend']

    def __init__(self, name, version, dependency_type):
        self.name = name
        self.version = version
        self.type = dependency_type

    def __str__(self):
        return f'({self.type}) {self.name}: {self.version}'

    def __eq__(self, other):
        return str(self) == str(other)


class DependencyFromXmlNode(Dependency):
    """Instantiate ROS package dependency from XML node"""

    def __init__(self, xml_node):
        text = xml_node.text
        tag = xml_node.tag
        value = self.get_relationship(xml_node.attrib)
        super().__init__(text, value, tag)


    def get_relationship(self, attrib):
        """Returns the dependency relationship"""

        if 'version_eq' in attrib:
            rel = '='
            value = attrib['version_eq']
        elif 'version_gte' in attrib:
            rel = '>='
            value = attrib['version_gte']
        else:
            rel = ''
            value = ''
        return f'{rel}{value}'


def get_paths(filename='package.xml', path='.'):
    """Return full paths of all files found under the given path"""

    return [ y
             for x in os.walk(path)
             for y in glob(os.path.join(x[0], filename))]


def main(path):  # pragma: no cover
    """Main function"""

    packages = [ PackageFromXmlFile(package_xml)
                 for package_xml in get_paths('package.xml', path) ]
    


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(usage='%(prog)s <command> [<options> ...]')
    parser.add_argument('path', help='Source code path')
    parser.add_argument('--filter', help='Filter packages')
    args = parser.parse_args()

    main(args.path)
