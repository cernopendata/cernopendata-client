# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client utils test."""

import click
import pytest

from cernopendata_client.utils import parse_parameters


def test_parse_parameters():
    """Test parse_parameters() method."""
    pytest.raises(click.BadParameter, parse_parameters, ("test.py"))
    pytest.raises(click.BadParameter, parse_parameters, (9))
    pytest.raises(click.BadParameter, parse_parameters, ("name test.py, name=test1.py"))
    assert parse_parameters(("name=test.py",)) == [
        {"filter": "name", "value": "test.py"}
    ]
    assert parse_parameters(("range=2-4,range=9-12",)) == [
        {"filter": "range", "value": "2-4"},
        {"filter": "range", "value": "9-12"},
    ]
