# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2019, 2020, 2021, 2022 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.
"""cernopendata-client."""

import os
import re

from setuptools import setup

readme = open("README.rst").read()
history = open("CHANGES.rst").read()

tests_require = [
    'black>=19.10b0 ; python_version>="3"',
    "check-manifest>=0.25",
    "coverage>=4.0",
    "mock>=3.0,<4.0",
    "pydocstyle>=1.0.0",
    "pytest-cache>=1.0",
    "pytest-cov>=1.8.0",
    "pytest>=2.8.0",
    'pytest-mock>=2.0,<3.0 ; python_version=="2.7"',
    'pytest-mock>=3.0 ; python_version>="3"',
]

extras_require = {
    "docs": [
        "Sphinx>=1.4.4,<2.0",
        "sphinx-rtd-theme>=0.1.9",
        "sphinx-click>=2.5.0",
    ],
    "tests": tests_require,
    "xrootd": [
        "xrootd>=4.12.2",
    ],
    "pycurl": ["pycurl>=7"],
}

extras_require["all"] = []
for key, reqs in extras_require.items():
    if ":" == key[0]:
        continue
    extras_require["all"].extend(reqs)

setup_requires = [
    "pytest-runner>=2.7",
]

install_requires = ["click>=7", "requests>=2"]

# Get the version string. Cannot be done with import!
with open(os.path.join("cernopendata_client", "version.py"), "rt") as f:
    version = re.search('__version__\s*=\s*"(?P<version>.*)"\n', f.read()).group(
        "version"
    )

setup(
    name="cernopendata-client",
    version=version,
    description=__doc__,
    long_description=readme + "\n\n" + history,
    author="CERN Open Data",
    author_email="opendata-team@cern.ch",
    packages=[
        "cernopendata_client",
    ],
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    entry_points={
        "console_scripts": [
            "cernopendata-client = cernopendata_client.cli:cernopendata_client"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Archiving",
    ],
)
