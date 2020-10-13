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

check_script () {
    shellcheck run-tests.sh
}

check_black () {
    black --check .
}

check_pydocstyle () {
    pydocstyle cernopendata_client
}

check_flake8 () {
    flake8 .
}

check_manifest () {
    check-manifest
}

check_sphinx () {
    sphinx-build -qnNW docs docs/_build/html
    sphinx-build -qnNW -b doctest docs docs/_build/doctest
}

check_pytest () {
    python setup.py test
}

for arg in "$@"
do
    case $arg in
        --check-shellscript) check_script;;
        --check-black) check_black;;
        --check-pydocstyle) check_pydocstyle;;
        --check-flake8) check_flake8;;
        --check-manifest) check_manifest;;
        --check-sphinx) check_sphinx;;
        --check-pytest) check_pytest;;
        --check-all)
            check_script
            check_black
            check_pydocstyle
            check_flake8
            check_manifest
            check_sphinx
            check_pytest
            ;;
        *)
    esac
done
