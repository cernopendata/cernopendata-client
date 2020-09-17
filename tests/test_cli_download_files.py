# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client cli command download-files test."""

import os
import pytest
from click.testing import CliRunner
from cernopendata_client.cli import download_files


def test_download_files():
    """Test download_files() command."""
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    if os.path.isfile(test_file):
        os.remove(test_file)
    test_download_files = CliRunner()
    test_result = test_download_files.invoke(download_files, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")
    if os.path.isfile(test_file):
        os.remove(test_file)


def test_download_files_filter_name():
    """Test download_files() command with filter-name options."""
    test_file = "5500/BuildFile.xml"
    if os.path.isfile(test_file):
        os.remove(test_file)
    test_download_files_filter = CliRunner()
    test_result_name_one = test_download_files_filter.invoke(
        download_files,
        [
            "--recid",
            5500,
            "--filter-name",
            "BuildFile.xml",
        ],
    )
    assert test_result_name_one.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert test_result_name_one.output.endswith("\n==> Success!\n")
    if os.path.isfile(test_file):
        os.remove(test_file)
    test_result_name_two = test_download_files_filter.invoke(
        download_files, ["--recid", 5500, "--filter-name", "test_name.py"]
    )
    assert test_result_name_two.exit_code == 1
    assert test_result_name_two.output == "\nNo files matching the filters\n"


def test_download_files_filter_regexp():
    """Test download_files() command with filter-regexp options."""
    test_one_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    test_two_files = [
        "5500/HiggsDemoAnalyzer.cc",
        "5500/M4Lnormdatall.cc",
        "5500/M4Lnormdatall_lvl3.cc",
    ]
    if os.path.isfile(test_one_file):
        os.remove(test_one_file)
    test_download_files_filter = CliRunner()
    test_result_regexp_one = test_download_files_filter.invoke(
        download_files, ["--recid", 3005, "--filter-regexp", "py$"]
    )
    assert test_result_regexp_one.exit_code == 0
    assert test_result_regexp_one.output.endswith("\n==> Success!\n")
    if os.path.isfile(test_one_file):
        os.remove(test_one_file)
    else:
        pytest.fail("{} not downloaded".format(test_one_file))

    for file_location in test_two_files:
        if os.path.isfile(file_location):
            os.remove(file_location)
    test_result_regexp_two = test_download_files_filter.invoke(
        download_files, ["--recid", 5500, "--filter-regexp", ".cc$"]
    )
    assert test_result_regexp_two.exit_code == 0
    for file_location in test_two_files:
        if os.path.isfile(file_location):
            os.remove(file_location)
        else:
            pytest.fail("{} not downloaded".format(file_location))
    assert test_result_regexp_two.output.endswith("\n==> Success!\n")

    test_result_regexp_three = test_download_files_filter.invoke(
        download_files, ["--recid", 5500, "--filter-regexp", "wontmatchanything"]
    )
    assert test_result_regexp_three.exit_code == 1
    assert test_result_regexp_three.output == "\nNo files matching the filters\n"


def test_download_files_filter_range():
    """Test download_files() command with filter-range options."""
    test_files = [
        "5500/BuildFile.xml",
        "5500/HiggsDemoAnalyzer.cc",
        "5500/List_indexfile.txt",
        "5500/M4Lnormdatall.cc",
    ]
    for file_location in test_files:
        if os.path.isfile(file_location):
            os.remove(file_location)
    test_download_files_filter = CliRunner()
    test_result_range = test_download_files_filter.invoke(
        download_files, ["--recid", 5500, "--filter-range", "1-4"]
    )
    assert test_result_range.exit_code == 0
    for file_location in test_files:
        if os.path.isfile(file_location):
            os.remove(file_location)
        else:
            pytest.fail("{} not downloaded".format(file_location))
    assert test_result_range.output.endswith("\n==> Success!\n")
