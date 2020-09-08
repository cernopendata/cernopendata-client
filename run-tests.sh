#!/bin/sh
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2019, 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

# Check Python code formatting
if which black; then
    black --check .
fi

# Check Python manifest completeness
check-manifest --ignore ".travis-*"

# Check Sphinx documentation
sphinx-build -qnNW docs docs/_build/html

# Run test suite
python setup.py test

# Check Sphinx documentation with doctests
sphinx-build -qnNW -b doctest docs docs/_build/doctest
