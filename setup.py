#!/usr/bin/env python3
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long', 'tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name='jsonwatch',
    version='0.0.1',
    packages=['jsonwatch'],
    url='https://github.com/MrLeeh/jsonwatch',
    license='MIT license',
    author='Stefan Lehmann',
    author_email='Stefan.St.Lehmann@gmail.com',
    description='keep track of json data',
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    platforms='any'
)
