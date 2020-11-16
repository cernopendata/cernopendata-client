# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client verify-files tests."""

import os
import pytest
from click.testing import CliRunner
from cernopendata_client.cli import download_files, verify_files
from cernopendata_client.config import SERVER_HTTPS_URI


def test_verify_files():
    """Test verify-files command."""

    # remove test file
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    if os.path.isfile(test_file):
        os.remove(test_file)

    # first download it
    test_download_files = CliRunner()
    test_result = test_download_files.invoke(download_files, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")

    # now test verifier
    test_verify_files = CliRunner()
    test_result = test_verify_files.invoke(verify_files, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert test_result.output.endswith("\n==> Success!\n")

    # remove test file
    if os.path.isfile(test_file):
        os.remove(test_file)


def test_verify_files_https_server():
    """Test verify-files command with https server."""

    # remove test file
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    if os.path.isfile(test_file):
        os.remove(test_file)

    # first download it
    test_download_files = CliRunner()
    test_result = test_download_files.invoke(
        download_files, ["--recid", 3005, "--server", SERVER_HTTPS_URI]
    )
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")

    # now test verifier
    test_verify_files = CliRunner()
    test_result = test_verify_files.invoke(
        verify_files, ["--recid", 3005, "--server", SERVER_HTTPS_URI]
    )
    assert test_result.exit_code == 0
    assert test_result.output.endswith("\n==> Success!\n")

    # remove test file
    if os.path.isfile(test_file):
        os.remove(test_file)


def test_verify_files_empty_value():
    """Test verify-files command with empty value."""
    test_verify_files_empty_value = CliRunner()
    test_result = test_verify_files_empty_value.invoke(verify_files)
    assert test_result.exit_code == 1
    assert "Please provide at least one of following arguments" in test_result.output


def test_verify_files_wrong_value():
    """Test verify-files command with wrong value."""
    test_verify_files_wrong_value = CliRunner()
    test_result = test_verify_files_wrong_value.invoke(
        verify_files,
        ["--recid", 5500, "--server", "foo"],
    )
    assert test_result.exit_code == 2
    assert "Invalid value for --server" in test_result.output


def test_verify_files_witout_download():
    """Test verify-files command."""
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    if os.path.isfile(test_file):
        os.remove(test_file)
    test_verify_files = CliRunner()
    test_result = test_verify_files.invoke(verify_files, ["--recid", 3005])
    assert test_result.exit_code == 1
    assert "No local files found for record 3005" in test_result.output
