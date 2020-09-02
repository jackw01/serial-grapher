#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='serialgrapher',
    version='0.1.0',
    description='Utility for graphing CSV data received over a serial port',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='jackw01',
    python_requires='>=3.7.0',
    url='https://github.com/jackw01/serial-grapher',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'pyserial>=3.4',
        'matplotlib>=3.2.2'
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'serialgrapher=serialgrapher:main'
        ]
    },
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
