# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2020, 2025, 2026 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client verify-files tests."""

import os
import zlib

import pytest

from cernopendata_client.cli import download_files, verify_files
from cernopendata_client.config import SERVER_HTTPS_URI
from cernopendata_client.searcher import FileEntry


def _checksum(content):
    """Return the metadata checksum for test content."""
    return "adler32:{:08x}".format(zlib.adler32(content, 1) & 0xFFFFFFFF)


@pytest.mark.local
def test_verify_files_uses_exact_nested_destinations(
    cli_runner, tmp_path, monkeypatch, mocker
):
    """Test duplicate basenames are verified in their exact subdirectories."""
    monkeypatch.chdir(tmp_path)
    first_content = b"first"
    second_content = b"second"
    entries = [
        FileEntry(
            "http://example.com/data/0001/data.root",
            len(first_content),
            _checksum(first_content),
        ),
        FileEntry(
            "http://example.com/data/0002/data.root",
            len(second_content),
            _checksum(second_content),
        ),
    ]
    first = tmp_path / "42" / "0001" / "data.root"
    second = tmp_path / "42" / "0002" / "data.root"
    first.parent.mkdir(parents=True)
    second.parent.mkdir(parents=True)
    first.write_bytes(first_content)
    second.write_bytes(second_content)
    record = mocker.patch(
        "cernopendata_client.cli.get_record_as_json",
        return_value={"metadata": {"recid": "42"}},
    )
    file_entries = mocker.patch(
        "cernopendata_client.cli.get_file_entries", return_value=entries
    )

    result = cli_runner.invoke(verify_files, ["--recid", "42"])

    assert result.exit_code == 0
    assert "42/0001/data.root" in result.output
    assert "42/0002/data.root" in result.output
    assert result.output.endswith("\n==> Success!\n")
    record.assert_called_once()
    file_entries.assert_called_once()


def test_verify_files(cli_runner):
    """Test verify-files command."""
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"

    # first download it
    test_result = cli_runner.invoke(download_files, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")

    # now test verifier
    test_result = cli_runner.invoke(verify_files, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert test_result.output.endswith("\n==> Success!\n")


def test_verify_files_https_server(cli_runner):
    """Test verify-files command with https server."""
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"

    # first download it
    test_result = cli_runner.invoke(
        download_files, ["--recid", 3005, "--server", SERVER_HTTPS_URI]
    )
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")

    # now test verifier
    test_result = cli_runner.invoke(
        verify_files, ["--recid", 3005, "--server", SERVER_HTTPS_URI]
    )
    assert test_result.exit_code == 0
    assert test_result.output.endswith("\n==> Success!\n")


@pytest.mark.local
def test_verify_files_empty_value(cli_runner):
    """Test verify-files command with empty value."""
    test_result = cli_runner.invoke(verify_files)
    assert test_result.exit_code == 1
    assert "Please provide at least one of following arguments" in test_result.output


@pytest.mark.local
def test_verify_files_wrong_value(cli_runner):
    """Test verify-files command with wrong value."""
    test_result = cli_runner.invoke(
        verify_files,
        ["--recid", 5500, "--server", "foo"],
    )
    assert test_result.exit_code == 2
    assert "Invalid value for --server" in test_result.output


def test_verify_files_witout_download(cli_runner):
    """Test verify-files command."""
    test_result = cli_runner.invoke(verify_files, ["--recid", 3005])
    assert test_result.exit_code == 1
    assert "No local files found for record 3005" in test_result.output
