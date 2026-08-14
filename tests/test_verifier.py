# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2020, 2021, 2025, 2026 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client file verifier tests."""

import os
import subprocess
import tempfile
import zlib

import pytest
import requests

from cernopendata_client.cli import download_files, verify_files
from cernopendata_client.verifier import (
    CHECKSUM_CHUNK_SIZE,
    get_file_size,
    get_file_checksum,
    get_file_info_local,
    verify_downloaded_file,
    verify_file_info,
)


@pytest.mark.local
def test_get_file_size():
    """Test get_file_size()."""
    afile = "./tests/test_version.py"
    assert get_file_size(afile) == 628


@pytest.mark.local
def test_get_file_checksum():
    """Test get_file_checksum()."""
    afile = "./tests/test_version.py"
    assert get_file_checksum(afile) == "adler32:41cdd471"


@pytest.mark.local
def test_get_file_checksum_reads_in_chunks(mocker):
    """Test get_file_checksum() uses bounded reads."""
    content = b"a" * (CHECKSUM_CHUNK_SIZE * 2 + 17)
    expected = "adler32:{:08x}".format(zlib.adler32(content, 1) & 0xFFFFFFFF)
    reader = mocker.mock_open(read_data=content).return_value

    mocker.patch("builtins.open", return_value=reader)

    assert get_file_checksum("large-file") == expected
    assert reader.read.call_count == 4
    assert all(
        call.args == (CHECKSUM_CHUNK_SIZE,) for call in reader.read.call_args_list
    )


@pytest.mark.local
@pytest.mark.parametrize(
    "content, expected_size, failure",
    [(b"short", 10, "incomplete"), (b"too long", 3, "oversized")],
)
def test_verify_downloaded_file_rejects_wrong_size(
    tmp_path, capsys, content, expected_size, failure
):
    """Test exact-file verification rejects truncated and oversized files."""
    destination = tmp_path / "data.bin"
    destination.write_bytes(content)

    with pytest.raises(SystemExit) as exc_info:
        verify_downloaded_file(destination, expected_size=expected_size)

    assert exc_info.value.code == 1
    output = capsys.readouterr().out
    assert "Expected size {}, found {}".format(expected_size, len(content)) in output
    assert failure in output


@pytest.mark.local
def test_verify_downloaded_file_rejects_missing_destination(tmp_path, capsys):
    """Test exact-file verification reports a missing engine output cleanly."""
    destination = tmp_path / "missing.bin"

    with pytest.raises(SystemExit) as exc_info:
        verify_downloaded_file(destination, expected_size=10)

    assert exc_info.value.code == 1
    assert "Downloaded file is missing" in capsys.readouterr().out


@pytest.mark.local
def test_verify_downloaded_file_can_skip_checksum(tmp_path, mocker):
    """Test disabling checksums retains the expected-size check."""
    destination = tmp_path / "data.bin"
    destination.write_bytes(b"data")
    checksum = mocker.patch("cernopendata_client.verifier.get_file_checksum")

    assert (
        verify_downloaded_file(
            destination,
            expected_size=4,
            expected_checksum="adler32:00000000",
            verify_checksum=False,
        )
        is True
    )
    checksum.assert_not_called()


@pytest.mark.local
def test_verify_downloaded_empty_file_without_checksum(tmp_path, mocker):
    """Test zero-sized files with absent checksums still receive a size check."""
    destination = tmp_path / "empty.bin"
    destination.touch()
    checksum = mocker.patch("cernopendata_client.verifier.get_file_checksum")

    assert (
        verify_downloaded_file(
            destination,
            expected_size=0,
            expected_checksum="",
        )
        is True
    )
    checksum.assert_not_called()


def test_get_file_checksum_zero_padding():
    """Test get_file_checksum() zero-pads checksums to 8 hex characters.

    Uses a real open data file from recid 93773 whose checksum has a leading
    zero.
    """
    file_url = "http://opendata.cern.ch/eos/opendata/delphi/simulated-data/cern/hzha03pyth6156/va0u/206.5/hzha03pyth6156_hattbb_206.5_70_90_22432.xsdst"
    file_checksum = "adler32:03d9681c"

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name
        response = requests.get(file_url)
        tmp.write(response.content)

    try:
        result = get_file_checksum(tmp_path)
        assert result == file_checksum
    finally:
        os.remove(tmp_path)


@pytest.mark.local
def test_get_file_info_local_wrong_input():
    """Test get_file_info_local() for wrong inputs."""

    assert get_file_info_local(123456) == []


def test_get_file_info_local_good_input(cli_runner):
    """Test get_file_info_local() for good inputs."""
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"

    # first download it
    test_result = cli_runner.invoke(download_files, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")

    # now test get_file_info_local()
    local_result = get_file_info_local(3005)
    assert len(local_result) == 1
    assert local_result[0]["name"] == "0d0714743f0204ed3c0144941e6ce248.configFile.py"
    assert local_result[0]["size"] == 3644
    assert local_result[0]["checksum"] == "adler32:be83a186"

    # now test verifier
    test_result = cli_runner.invoke(verify_files, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert test_result.output.endswith("\n==> Success!\n")


def test_get_file_info_local_good_input_wrong_count(cli_runner):
    """Test get_file_info_local() for good inputs simulating wrong file count."""
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"

    # first download it
    test_result = cli_runner.invoke(download_files, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")

    # simulate getting more files
    cmd = "cp {} {}.extra".format(test_file, test_file)
    subprocess.check_output(cmd, shell=True)

    # now test verifier
    test_result = cli_runner.invoke(verify_files, ["--recid", 3005])
    assert test_result.exit_code == 1


def test_get_file_info_local_good_input_wrong_checksum(cli_runner):
    """Test get_file_info_local() for good inputs simulating wrong file checksum."""
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"

    # first download it
    test_result = cli_runner.invoke(download_files, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")

    # simulate checksum change
    with open(test_file, "r") as f:
        content = f.read()
    with open(test_file, "w") as f:
        f.write(content.replace("a", "b"))

    # now test verifier
    test_result = cli_runner.invoke(verify_files, ["--recid", 3005])
    assert test_result.exit_code == 1


def test_get_file_info_local_good_input_wrong_size(cli_runner):
    """Test get_file_info_local() for good inputs simulating wrong file size."""
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"

    # first download it
    test_result = cli_runner.invoke(download_files, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")

    # simulate size change
    with open(test_file, "r") as f:
        content = f.read()
    with open(test_file, "w") as f:
        f.write(content.replace("a", "bbbbbb"))

    # now test verifier
    test_result = cli_runner.invoke(verify_files, ["--recid", 3005])
    assert test_result.exit_code == 1


@pytest.mark.local
def test_verify_file_info_good_input():
    """Test verify_file_info() for good input."""

    # Remote test files info
    test_file_info_remote = [
        {
            "checksum": "adler32:ff63668a",
            "name": "BuildFile.xml",
            "size": 305,
            "uri": "http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/BuildFile.xml",
        },
        {
            "checksum": "adler32:f205f068",
            "name": "HiggsDemoAnalyzer.cc",
            "size": 83761,
            "uri": "http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/HiggsDemoAnalyzer.cc",
        },
        {
            "checksum": "adler32:46a907fc",
            "name": "List_indexfile.txt",
            "size": 1669,
            "uri": "http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/List_indexfile.txt",
        },
        {
            "checksum": "adler32:af301992",
            "name": "M4Lnormdatall.cc",
            "size": 14943,
            "uri": "http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/M4Lnormdatall.cc",
        },
    ]

    # Local test files info
    test_file_info_local = [
        {"name": "List_indexfile.txt", "size": 1669, "checksum": "adler32:46a907fc"},
        {"name": "M4Lnormdatall.cc", "size": 14943, "checksum": "adler32:af301992"},
        {"name": "BuildFile.xml", "size": 305, "checksum": "adler32:ff63668a"},
        {"name": "HiggsDemoAnalyzer.cc", "size": 83761, "checksum": "adler32:f205f068"},
    ]

    # Simulating function call
    assert verify_file_info(test_file_info_local, test_file_info_remote) is True


@pytest.mark.local
def test_verify_file_info_wrong_input():
    """Test verify_file_info() for wrong input."""

    # Remote test files info
    test_file_info_remote = [
        {
            "checksum": "adler32:ff63668a",
            "name": "BuildFile.xml",
            "size": 305,
            "uri": "http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/BuildFile.xml",
        },
        {
            "checksum": "adler32:f205f068",
            "name": "HiggsDemoAnalyzer.cc",
            "size": 83761,
            "uri": "http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/HiggsDemoAnalyzer.cc",
        },
        {
            "checksum": "adler32:46a907fc",
            "name": "List_indexfile.txt",
            "size": 1669,
            "uri": "http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/List_indexfile.txt",
        },
        {
            "checksum": "adler32:af301992",
            "name": "M4Lnormdatall.cc",
            "size": 14943,
            "uri": "http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/M4Lnormdatall.cc",
        },
    ]

    # Local test files info
    test_file_info_local = [
        {"name": "List_indexfile.txt", "size": 1669, "checksum": "adler32:46a907fc"},
        {"name": "M4Lnormdatall.cc", "size": 14943, "checksum": "adler32:af301992"},
        {"name": "BuildFile.xml", "size": 305, "checksum": "adler32:ff63668a"},
    ]

    # Simualting function call to exit for wrong input
    pytest.raises(
        SystemExit, verify_file_info, test_file_info_local, test_file_info_remote
    )


@pytest.mark.local
def test_verify_file_info_wrong_checksum():
    """Test verify_file_info() for wrong checksum."""

    # Remote test files info
    test_file_info_remote = [
        {
            "checksum": "adler32:ff63668a",
            "name": "BuildFile.xml",
            "size": 305,
            "uri": "http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/BuildFile.xml",
        },
        {
            "checksum": "adler32:46a907fd",
            "name": "List_indexfile.txt",
            "size": 1669,
            "uri": "http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/List_indexfile.txt",
        },
        {
            "checksum": "adler32:af301992",
            "name": "M4Lnormdatall.cc",
            "size": 14943,
            "uri": "http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/M4Lnormdatall.cc",
        },
    ]

    # Local test files info
    test_file_info_local = [
        {"name": "List_indexfile.txt", "size": 1669, "checksum": "adler32:46a907fc"},
        {"name": "M4Lnormdatall.cc", "size": 14943, "checksum": "adler32:af301992"},
        {"name": "BuildFile.xml", "size": 305, "checksum": "adler32:ff63668a"},
    ]

    # Simualting function call to exit for wrong input
    pytest.raises(
        SystemExit, verify_file_info, test_file_info_local, test_file_info_remote
    )
