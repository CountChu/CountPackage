from setuptools import setup
from setuptools import find_packages
import pdb
import unittest

def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite

setup(
    name='Count',
    version='0.1',
    description='The package provides a wrapper for Count Package.',
    url='https://github.com/CountChu/CountPackage',
    author='CountChu',
    author_email='visualge@gmail.com',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    test_suite='setup.my_test_suite')
