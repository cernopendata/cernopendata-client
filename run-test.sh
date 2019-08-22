#!/bin/sh

isort -rc -c -df **/*.py && \
# check-manifest --ignore ".travis-*" && \
sphinx-build -qnNW docs docs/_build/html && \
python setup.py test
sphinx-build -qnNW -b doctest docs docs/_build/doctest
