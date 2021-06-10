""" Module to install shorturl as a module """

import os
from setuptools import setup, find_packages

project_path = os.path.dirname(os.path.abspath(__file__))

setup(
    name='shorturl',
    version='1.0',
    packages=find_packages(where=project_path)
)
