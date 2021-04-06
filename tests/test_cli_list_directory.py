# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2020, 2021 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client cli command list-directory test."""

import pytest

from click.testing import CliRunner
from cernopendata_client.cli import list_directory


def test_non_recursive_list_directory():
    """Test `list_directory` command."""
    xrootd = pytest.importorskip("XRootD")  # noqa: F841
    test_non_recursive = CliRunner()
    test_result = test_non_recursive.invoke(
        list_directory, ["/eos/opendata/cms/validated-runs/Commissioning10"]
    )
    assert test_result.exit_code == 0
    assert "Commissioning10-May19ReReco_7TeV" in test_result.output


def test_recursive_list_directory():
    """Test `list_directory --recursive` command."""
    xrootd = pytest.importorskip("XRootD")  # noqa: F841
    test_recursive = CliRunner()
    test_result = test_recursive.invoke(
        list_directory, ["/eos/opendata/cms/Run2010B/BTau/AOD", "--recursive"]
    )
    assert test_result.exit_code == 0


def test_recursive_list_directory_timeout():
    """Test `list_directory --recursive` command with timeout."""
    xrootd = pytest.importorskip("XRootD")  # noqa: F841
    test_recursive = CliRunner()
    test_result = test_recursive.invoke(
        list_directory, ["/eos/opendata/cms", "--recursive", "--timeout", 5]
    )
    assert test_result.exit_code == 2
    assert "Command timed out." in test_result.output


def test_non_recursive_list_directory_wrong():
    """Test `list_directory` command with wrong path"""
    xrootd = pytest.importorskip("XRootD")  # noqa: F841
    test_non_recursive = CliRunner()
    test_result = test_non_recursive.invoke(list_directory, ["/eos/opendata/foobar"])
    assert test_result.exit_code == 1
    assert "Directory /eos/opendata/foobar does not exist." in test_result.output


def test_recursive_list_directory_wrong():
    """Test `list_directory --recursive` command with wrong path."""
    xrootd = pytest.importorskip("XRootD")  # noqa: F841
    test_recursive = CliRunner()
    test_result = test_recursive.invoke(
        list_directory, ["/eos/opendata/recursiveFoobar", "--recursive"]
    )
    assert (
        "Directory /eos/opendata/recursiveFoobar does not exist." in test_result.output
    )
