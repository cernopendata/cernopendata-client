# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2020, 2025 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client cli command get-file-locations test."""

from click.testing import CliRunner
from cernopendata_client.cli import get_file_locations
from cernopendata_client.config import SERVER_HTTPS_URI, SERVER_ROOT_URI


def test_get_file_locations_from_recid():
    """Test `get-file-locations --recid` command."""
    test_get_file_locations = CliRunner()
    test_result = test_get_file_locations.invoke(get_file_locations, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert "0d0714743f0204ed3c0144941e6ce248.configFile.py" in test_result.output


def test_get_file_locations_from_recid_without_files():
    """Test `get-file-locations --recid` command for recid without files."""
    test_get_file_locations = CliRunner()
    test_result = test_get_file_locations.invoke(get_file_locations, ["--recid", 550])
    assert test_result.exit_code == 0
    assert "" in test_result.output


def test_get_file_locations_from_recid_expand():
    """Test `get-file-locations --recid` command with expand."""
    test_get_file_locations = CliRunner()
    test_result = test_get_file_locations.invoke(get_file_locations, ["--recid", 282])
    assert test_result.exit_code == 0
    assert "2A227E10-C949-E311-B033-003048FEAF50.root" in test_result.output


def test_get_file_locations_from_recid_expand_verbose():
    """Test `get-file-locations --recid` command with expand and verbose."""
    test_get_file_locations = CliRunner()
    test_result = test_get_file_locations.invoke(
        get_file_locations, ["--recid", 282, "--verbose"]
    )
    assert test_result.exit_code == 0
    assert "2A227E10-C949-E311-B033-003048FEAF50.root" in test_result.output


def test_get_file_locations_from_recid_wrong():
    """Test `get-file-locations --recid` command for wrong values."""
    test_get_file_locations = CliRunner()
    test_result = test_get_file_locations.invoke(get_file_locations, ["--recid", 0])
    assert test_result.exit_code == 2


def test_get_file_locations_from_doi():
    """Test `get-file-locations --doi` command."""
    test_get_file_locations = CliRunner()
    test_result = test_get_file_locations.invoke(
        get_file_locations, ["--doi", "10.7483/OPENDATA.CMS.A342.9982", "--no-expand"]
    )
    assert test_result.exit_code == 0
    assert (
        "CMS_Run2010B_BTau_AOD_Apr21ReReco-v1_0001_file_index.json"
        in test_result.output
    )


def test_get_file_locations_from_doi_wrong():
    """Test `get-file-locations --doi` command for wrong values."""
    test_get_file_locations = CliRunner()
    test_result = test_get_file_locations.invoke(
        get_file_locations, ["--doi", "NONEXISTING", "--no-expand"]
    )
    assert test_result.exit_code == 2


def test_get_file_locations_with_verbose():
    """Test `get-file-locations --verbose` command."""
    test_get_file_locations = CliRunner()
    test_result = test_get_file_locations.invoke(
        get_file_locations, ["--recid", 5500, "--verbose"]
    )
    assert test_result.exit_code == 0
    assert "\t93152\tadler32:62e0c299\n" in test_result.output


def test_get_file_locations_with_https_server():
    """Test `get-file-locations --server` command for https server."""
    test_get_file_locations = CliRunner()
    test_result = test_get_file_locations.invoke(
        get_file_locations, ["--recid", 3005, "--server", SERVER_HTTPS_URI]
    )
    assert test_result.exit_code == 0
    assert "configFile.py" in test_result.output


def test_get_file_locations_with_https_server_xrootd_protocol():
    """Test `get-file-locations --server --protocol xrootd` command for https server."""
    test_get_file_locations = CliRunner()
    test_result = test_get_file_locations.invoke(
        get_file_locations,
        ["--recid", 3005, "--server", SERVER_HTTPS_URI, "--protocol", "xrootd"],
    )
    assert test_result.exit_code == 0
    assert "root://eospublic.cern.ch//eos/" in test_result.output


def test_get_file_locations_no_expand_with_xrootd_protocol():
    """Test `get-file-locations --no-expand --protocol xrootd` command."""
    test_get_file_locations = CliRunner()
    test_result = test_get_file_locations.invoke(
        get_file_locations,
        ["--recid", 1, "--no-expand", "--protocol", "xrootd"],
    )
    assert test_result.exit_code == 0
    assert SERVER_ROOT_URI in test_result.output
    assert "file_index" in test_result.output


def test_get_file_locations_no_expand_with_http_protocol():
    """Test `get-file-locations --no-expand --protocol http` command."""
    test_get_file_locations = CliRunner()
    test_result = test_get_file_locations.invoke(
        get_file_locations,
        ["--recid", 1, "--no-expand", "--protocol", "http"],
    )
    assert test_result.exit_code == 0
    assert "http://opendata.cern.ch" in test_result.output
    assert "file_index" in test_result.output


def test_get_file_locations_with_custom_https_server():
    """Test `get-file-locations --server` command for custom https server."""
    test_get_file_locations = CliRunner()
    test_result = test_get_file_locations.invoke(
        get_file_locations, ["--recid", 3005, "--server", "https://opendata-qa.cern.ch"]
    )
    assert test_result.exit_code == 0
    assert "https://opendata-qa.cern.ch" in test_result.output
    assert "https://opendata.cern.ch" not in test_result.output
    assert "configFile.py" in test_result.output
