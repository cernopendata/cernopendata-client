# -*- coding: utf-8 -*-
#!/bin/sh
# This file is part of cernopendata-client.
#
# Copyright (C) 2019 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

black --check .
check-manifest --ignore ".travis-*" && \
sphinx-build -qnNW docs docs/_build/html && \
python setup.py test
sphinx-build -qnNW -b doctest docs docs/_build/doctest
