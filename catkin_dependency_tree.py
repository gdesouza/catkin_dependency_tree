#!/usr/bin/env python3
"""
Creates the dependency tree in a catkin workspace
"""

import os
import argparse
import xml.etree.ElementTree
from glob import glob

DEPENDENCY_TYPES = [ 'run_depend', 'build_depend', 'exec_depend', 'depend',
                     'buildtool_depend', 'build_export_depend']

class Package:
    """ROS Package as defined in package.xml"""

    def __init__(self, name, version):
        self.name = name
        self.version = version
        self.dependencies = []

    def add_dependency(self, dependency):
        self.dependencies.append(dependency)

    def __str__(self):
        return ''

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


class Dependency:
    """ROS package dependency"""

    def __init__(self, name, version, dependency_type):
        self.name = name
        self.version = version
        self.type = dependency_type

    def __str__(self):
        return f'({self.type}) {self.name}: {self.version}'

    def __eq__(self, other):
        return str(self) == str(other)


def get_dependency_relationship(attrib):
    """Returns the dependency relationship"""

    if attrib is None:
        return ''

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


def extract_dependency(xml_element):
    """Return the dependency object represented by the xml node"""

    text = xml_element.text
    tag = xml_element.tag
    value = get_dependency_relationship(xml_element.attrib)
    return Dependency(text, value, tag)


def get_dependencies_from(xml_element, dependency_type):
    """Get child dependencies given of xml_element"""

    return [extract_dependency(child) for child in xml_element.findall(dependency_type)]


def get_paths(filename='package.xml', path='.'):
    """Return full paths of all files found under the given path"""

    return [ y
             for x in os.walk(path)
             for y in glob(os.path.join(x[0], filename))]


def get_dependencies_from_file(package_xml):
    """Get the dependencies from a package.xml file"""

    tree = xml.etree.ElementTree.parse(package_xml)
    root = tree.getroot()
    dependencies = []
    for dependency_type in DEPENDENCY_TYPES:
        dependencies.extend(get_dependencies_from(root, dependency_type))
    return dependencies



def main(path):  # pragma: no cover
    """Main function"""

    for package_xml in get_paths('package.xml', path):
        package = PackageFromXmlFile(package_xml)
        for dependency in get_dependencies_from_file(package_xml):
            package.add_dependency(dependency)



if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(usage='%(prog)s <command> [<options> ...]')
    parser.add_argument('path', help='Source code path')
    parser.add_argument('--filter', help='Filter packages')
    args = parser.parse_args()

    main(args.path)
