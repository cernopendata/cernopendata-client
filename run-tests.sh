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

for arg in "$@"
do
    case $arg in
        --check-black) # Check Python code formatting
        black --check .
        ;;
        --check-pydocstyle) # Check compliance with Python docstring conventions
        pydocstyle cernopendata_client
        ;;
        --check-flake8) # Check compliance with pep8, pyflakes and circular complexity
        flake8 .
        ;;
        --check-manifest) # Check Python manifest completeness
        check-manifest
        ;;
        --check-sphinx) # Check Sphinx documentation with doctests
        sphinx-build -qnNW docs docs/_build/html
        sphinx-build -qnNW -b doctest docs docs/_build/doctest
        ;;
        --pytest) # Run test suite
        python setup.py test
        ;;
        --all) # Run all tests locally
        black --check .
        pydocstyle cernopendata_client
        flake8 .
        check-manifest
        sphinx-build -qnNW docs docs/_build/html
        sphinx-build -qnNW -b doctest docs docs/_build/doctest
        python setup.py test
        ;;
        *)
    esac
done
