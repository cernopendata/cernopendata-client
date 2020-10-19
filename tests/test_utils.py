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
    pytest.raises(SystemExit, parse_parameters, (9))
    assert parse_parameters(("test.py",)) == ["test.py"]
    assert parse_parameters(("2-4,9-12",)) == ["2-4", "9-12"]
