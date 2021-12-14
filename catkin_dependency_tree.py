#!/usr/bin/env python3

import os
import argparse
import xml.etree.ElementTree
from glob import glob


class Package:
    def __init__(self):
        pass


class Dependency:
    def __init__(self, name, version, type):
        self.name = name
        self.version = version
        self.type = type


def get_dependency_relationship(attrib):
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
    text = xml_element.text
    tag = xml_element.tag
    value = get_dependency_relationship(xml_element.attrib)
    return Dependency(text, value, tag)


def get_dependencies_from(xml_element, dependency_type):
    dependencies_list = []
    for child in xml_element.findall(dependency_type):
        dependencies_list.append(extract_dependency(child))
    return dependencies_list
    # [extract_dependency(child) for child in xml_element.findall(dependency_type)]


def get_paths(filename='package.xml', path='.'):
    """Return full paths of all files found under the given path"""
    return [ y 
             for x in os.walk(path) 
             for y in glob(os.path.join(x[0], filename))]


def get_dependencies_from_file(package_xml):
    """Get the dependencies from a package.xml file"""
    dependency_types = [ 'run_depend', 'build_depend', 'exec_depend', 'depend']
    tree = xml.etree.ElementTree.parse(package_xml)
    root = tree.getroot()
    for dependency_type in dependency_types:
        dependencies = get_dependencies_from(root, dependency_type)
    return dependencies


def main(path):
    for package_xml in get_paths('package.xml', path):
        print(get_dependencies_from_file(package_xml))


if __name__ == "__main__":
   parser = argparse.ArgumentParser(usage='%(prog)s <command> [<options> ...]')
   parser.add_argument('path', help='Source code path')
   parser.add_argument('--filter', help='Filter packages')
   args = parser.parse_args()

   main(args.path)
