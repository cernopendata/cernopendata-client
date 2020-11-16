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
    validate_directory,
    validate_retry_limit,
    validate_retry_sleep,
)


def test_validate_recid():
    """Test validate_recid()."""
    pytest.raises(SystemExit, validate_recid, -1)
    pytest.raises(SystemExit, validate_recid, 0)
    pytest.raises(SystemExit, validate_recid, None)
    assert validate_recid(1) is True


def test_validate_server():
    """Test validate_server()."""
    assert validate_server("http://opendata.cern.ch") is True
    assert validate_server("http://opendata-dev.cern.ch") is True
    assert validate_server("http://0.0.0.0:5000") is True
    assert validate_server("https://opendata.cern.ch") is True
    pytest.raises(SystemExit, validate_server, "root://opendata.cern.ch")
    pytest.raises(SystemExit, validate_server, "opendata.cern.ch")


def test_validate_range():
    """Test validate_range()."""
    assert validate_range(range="3-9", count=10) is True
    assert validate_range(range="1-5", count=8) is True
    pytest.raises(SystemExit, validate_range, "0-9", 5)
    pytest.raises(SystemExit, validate_range, "0", 5)
    pytest.raises(SystemExit, validate_range, "1-9", 5)
    pytest.raises(SystemExit, validate_range, "3-2", 5)
    pytest.raises(SystemExit, validate_range, "3,2", 5)


def test_validate_directory():
    """Test validate_directory()."""
    assert validate_directory(directory="/eos/opendata/cms/validated-runs/") is True
    pytest.raises(
        SystemExit,
        validate_directory,
        "root://eospublic.cern.ch//eos/opendata/cms/validated-runs",
    )
    pytest.raises(SystemExit, validate_directory, 90)


def test_validate_retry_limit():
    """Test validate_retry_limit()."""
    pytest.raises(SystemExit, validate_retry_limit, -1)
    pytest.raises(SystemExit, validate_retry_limit, 0)
    pytest.raises(SystemExit, validate_retry_limit, None)
    assert validate_recid(1) is True


def test_validate_retry_sleep():
    """Test validate_retry_sleep()."""
    pytest.raises(SystemExit, validate_retry_sleep, -1)
    pytest.raises(SystemExit, validate_retry_sleep, 0)
    pytest.raises(SystemExit, validate_retry_sleep, None)
    assert validate_recid(1) is True
