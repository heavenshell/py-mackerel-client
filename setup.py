# -*- coding: utf-8 -*-
"""
    mackerel.client
    ~~~~~~~~~~~~~~~

    Mackerel client implemented by Python.


    :copyright: (c) 2015 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
from setuptools import setup, find_packages

requires = ['requests', 'simplejson', 'click']

app_name = 'mackerel.client'

rst_path = os.path.join(os.path.dirname(__file__), 'README.rst')
description = ''
with open(rst_path) as f:
    description = f.read()

setup(
    name=app_name,
    version='0.0.3',
    author='Shinya Ohyanagi',
    author_email='sohyanagi@gmail.com',
    url='http://github.com/heavenshell/py-mackerel-client',
    description='Mackerel client implemented by Python.',
    long_description=description,
    license='BSD',
    platforms='any',
    namespace_packages=['mackerel'],
    packages=find_packages(exclude=['tests']),
    package_dir={'': '.'},
    install_requires=requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
    entry_points="""
    [console_scripts]
    mkr.py = mackerel.runner:main
    """,
    tests_require=['requests', 'simplejson', 'mock'],
    test_suite='tests'
)
