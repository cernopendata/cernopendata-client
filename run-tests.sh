#!/bin/sh
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2019, 2020, 2021 CERN.
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

check_dockerfile () {
    docker run -i --rm hadolint/hadolint < Dockerfile
}

check_docker_build () {
    docker build -t cernopendata/cernopendata-client .
}

check_docker_run () {
    docker run --rm -v "$PWD"/tests:/code/tests --entrypoint /bin/bash cernopendata/cernopendata-client -c 'pytest tests'
}

check_sphinx () {
    sphinx-build -qnNW docs docs/_build/html
    sphinx-build -qnNW -b doctest docs docs/_build/doctest
}

check_pytest () {
    python setup.py test
}

if [ $# -eq 0 ]; then
    check_script
    check_black
    check_pydocstyle
    check_flake8
    check_manifest
    check_dockerfile
    check_docker_build
    check_docker_run
    check_sphinx
    check_pytest
fi

for arg in "$@"
do
    case $arg in
        --check-shellscript) check_script;;
        --check-black) check_black;;
        --check-pydocstyle) check_pydocstyle;;
        --check-flake8) check_flake8;;
        --check-manifest) check_manifest;;
        --check-dockerfile) check_dockerfile;;
        --check-docker-build) check_docker_build;;
        --check-docker-run) check_docker_run;;
        --check-sphinx) check_sphinx;;
        --check-pytest) check_pytest;;
        *)
    esac
done
