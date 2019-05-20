#!/usr/bin/env python

"""Setup script for the package."""

import os
import sys

import setuptools

PACKAGE_NAME = 'notmuchtask'
MINIMUM_PYTHON_VERSION = '3.5'


def check_python_version():
    """Exit when the Python version is too low."""
    if sys.version < MINIMUM_PYTHON_VERSION:
        sys.exit("Python {0}+ is required.".format(MINIMUM_PYTHON_VERSION))


def read_package_variable(key, filename='__init__.py'):
    """Read the value of a variable from the package without importing."""
    module_path = os.path.join(PACKAGE_NAME, filename)
    with open(module_path) as module:
        for line in module:
            parts = line.strip().split(' ', 2)
            if parts[:-1] == [key, '=']:
                return parts[-1].strip("'")
    sys.exit("'{0}' not found in '{1}'".format(key, module_path))


def build_description():
    """Build a description for the project from documentation files."""
    try:
        readme = open("README.rst").read()
        changelog = open("CHANGELOG.rst").read()
    except IOError:
        return "<placeholder>"
    else:
        return readme + '\n' + changelog


check_python_version()

setuptools.setup(name=read_package_variable('__project__'),
                 version=read_package_variable('__version__'),

                 description="Sync mails in notmuch with taskwarrior",
                 url='https://github.com/neuhalje/notmuch-task',
                 author='Jens Neuhalfen', author_email='jens@neuhalfen.name',

                 packages=setuptools.find_packages(exclude=['tests']),

                 entry_points={
                     'console_scripts': [
                         'notmuchtask = %s.cli.main:cli' % (PACKAGE_NAME,), ]
                 },

                 long_description=build_description(),
                 long_description_content_type="text/x-rst",
                 license='MIT',
                 classifiers=[
                     # https://pypi.python.org/pypi?%3Aaction=list_classifiers
                     'Development Status :: 1 - Planning',
                     'Natural Language :: English',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 3',
                     'Programming Language :: Python :: 3.6', ],

                 python_requires='>=%s' % (MINIMUM_PYTHON_VERSION,),
                 install_requires=["click >=7.0, <7.1", "notmuch"],
                 )
