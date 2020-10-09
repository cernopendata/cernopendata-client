# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client cli command get-file-locations test."""

from click.testing import CliRunner
from cernopendata_client.cli import get_file_locations


def test_get_file_locations_from_recid():
    """Test `get-file-locations --recid` command."""
    test_get_file_locations = CliRunner()
    test_result = test_get_file_locations.invoke(get_file_locations, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert "0d0714743f0204ed3c0144941e6ce248.configFile.py" in test_result.output


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
