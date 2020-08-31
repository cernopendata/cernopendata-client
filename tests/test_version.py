# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2019 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.
"""cernopendata-client version test."""


def test_version():
    """Test version import."""
    from cernopendata_client import __version__

    assert __version__
