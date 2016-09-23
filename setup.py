#!/usr/bin/env python


import sys
from setuptools import setup
import versioneer


setup(
    name='jsonwatch',
    version=versioneer.get_version(),
    packages=['jsonwatch'],
    url='https://github.com/MrLeeh/jsonwatch',
    license='MIT license',
    author='Stefan Lehmann',
    author_email='Stefan.St.Lehmann@gmail.com',
    description='keep track of json data',
    setup_requires=['pytest_runner'],
    tests_require=['pytest'],
    cmdclass=versioneer.get_cmdclass(),# {'test': PyTest},
    install_requires=['jsonpickle>=0.9.0'],
    platforms='any'
)
