# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2020, 2021, 2025 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client file verifier tests."""

import os
import pytest
import requests
import subprocess
import tempfile

from click.testing import CliRunner
from cernopendata_client.cli import download_files, verify_files
from cernopendata_client.verifier import (
    get_file_size,
    get_file_checksum,
    get_file_info_local,
    verify_file_info,
)


def test_get_file_size():
    """Test get_file_size()."""
    afile = "./tests/test_version.py"
    assert get_file_size(afile) == 641


def test_get_file_checksum():
    """Test get_file_checksum()."""
    afile = "./tests/test_version.py"
    assert get_file_checksum(afile) == "adler32:fa91da1e"


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


def test_get_file_info_local_wrong_input():
    """Test get_file_info_local() for wrong inputs."""

    assert get_file_info_local(123456) == []


def test_get_file_info_local_good_input():
    """Test get_file_info_local() for good inputs."""

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

    # now test get_file_info_local()
    test_result = get_file_info_local(3005)
    assert len(test_result) == 1
    assert test_result[0]["name"] == "0d0714743f0204ed3c0144941e6ce248.configFile.py"
    assert test_result[0]["size"] == 3644
    assert test_result[0]["checksum"] == "adler32:be83a186"

    # now test verifier
    test_verifier_files = CliRunner()
    test_result = test_verifier_files.invoke(verify_files, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert test_result.output.endswith("\n==> Success!\n")

    # remove test file
    if os.path.isfile(test_file):
        os.remove(test_file)


def test_get_file_info_local_good_input_wrong_count():
    """Test get_file_info_local() for good inputs simulating wrong file count."""

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

    # simulate getting more files
    cmd = "cp {} {}.extra".format(test_file, test_file)
    subprocess.check_output(cmd, shell=True)

    # now test verifier
    test_verifier_files = CliRunner()
    test_result = test_verifier_files.invoke(verify_files, ["--recid", 3005])
    assert test_result.exit_code == 1

    # remove test files
    if os.path.isfile(test_file + ".extra"):
        os.remove(test_file + ".extra")
    if os.path.isfile(test_file):
        os.remove(test_file)


def test_get_file_info_local_good_input_wrong_checksum():
    """Test get_file_info_local() for good inputs simulating wrong file checksum."""

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

    # simulate checksum change
    with open(test_file, "r") as f:
        content = f.read()
    with open(test_file, "w") as f:
        f.write(content.replace("a", "b"))

    # now test verifier
    test_verifier_files = CliRunner()
    test_result = test_verifier_files.invoke(verify_files, ["--recid", 3005])
    assert test_result.exit_code == 1

    # remove test file
    if os.path.isfile(test_file):
        os.remove(test_file)


def test_get_file_info_local_good_input_wrong_size():
    """Test get_file_info_local() for good inputs simulating wrong file size."""

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

    # simulate size change
    with open(test_file, "r") as f:
        content = f.read()
    with open(test_file, "w") as f:
        f.write(content.replace("a", "bbbbbb"))

    # now test verifier
    test_verifier_files = CliRunner()
    test_result = test_verifier_files.invoke(verify_files, ["--recid", 3005])
    assert test_result.exit_code == 1

    # remove test file
    if os.path.isfile(test_file):
        os.remove(test_file)


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
