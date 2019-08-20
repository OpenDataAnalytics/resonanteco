#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requirements = [
    'girder==3.0.0a7.dev148',
    'girder-client'
]

setup(
    author_email='kitware@kitware.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    description='Server side functionality of ResonantEco',
    install_requires=requirements,
    license='Apache Software License 2.0',
    include_package_data=True,
    keywords='',
    name='resonanteco_server',
    packages=find_packages(exclude=['test', 'test.*']),
    url='',
    version='0.1.0',
    zip_safe=False,
    entry_points={
        'girder.plugin': [
            'resonanteco_server = resonanteco_server:GirderPlugin'
        ]
    }
)
