# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client validator test."""

import click
import pytest

from cernopendata_client.validator import (
    validate_recid,
    validate_server,
    validate_range,
)


def test_validate_recid():
    """Test validate_recid()."""
    pytest.raises(click.BadParameter, validate_recid, -1)
    pytest.raises(click.BadParameter, validate_recid, 0)
    assert validate_recid(1) is True


def test_validate_server():
    """Test validate_server()."""
    assert validate_server("http://opendata.cern.ch") is True
    assert validate_server("http://opendata-dev.cern.ch") is True
    assert validate_server("http://0.0.0.0:5000") is True
    pytest.raises(click.BadParameter, validate_server, "https://opendata.cern.ch")
    pytest.raises(click.BadParameter, validate_server, "opendata.cern.ch")


def test_validate_range():
    """Test validate_range()."""
    assert validate_range(range="3-9", count=10) is True
    assert validate_range(range="1-5", count=8) is True
    pytest.raises(click.BadParameter, validate_range, "0-9", 5)
    pytest.raises(click.BadParameter, validate_range, "0", 5)
    pytest.raises(click.BadParameter, validate_range, "1-9", 5)
    pytest.raises(click.BadParameter, validate_range, "3-2", 5)
